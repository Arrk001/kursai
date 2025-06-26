import streamlit as st
from dotenv import load_dotenv
import os
import io
from PIL import Image
import fitz  # PyMuPDF
import google.generativeai as genai
import json
import base64
from pydantic import BaseModel, ValidationError
from typing import List, Optional

# --- Configuration ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_TOKEN")
if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_TOKEN environment variable not found. Please set it.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
MODEL_NAME = "gemini-2.5-flash"

# --- Pydantic Models ---
class VendorInfo(BaseModel):
    name: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    website: Optional[str]

class CustomerInfo(BaseModel):
    name: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    email: Optional[str]

class Item(BaseModel):
    description: Optional[str]
    quantity: Optional[float]
    unit_price: Optional[float]
    line_total: Optional[float]

class InvoiceData(BaseModel):
    invoice_number: Optional[str]
    invoice_date: Optional[str]
    due_date: Optional[str]
    vendor_info: Optional[VendorInfo]
    customer_info: Optional[CustomerInfo]
    items: Optional[List[Item]]
    subtotal: Optional[float]
    tax_amount: Optional[float]
    total_amount: Optional[float]
    currency: Optional[str]
    payment_terms: Optional[str]
    notes: Optional[str]

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Invoice AI Assistant", layout="wide")
st.title("📄 Invoice AI Assistant")
st.markdown("Upload your invoice file (PDF, JPG, PNG) and let AI extract the details as JSON!")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "invoice_data" not in st.session_state:
    st.session_state.invoice_data = None
if "uploaded_file_hash" not in st.session_state:
    st.session_state.uploaded_file_hash = None # To track if the same file is re-uploaded

def convert_pdf_to_images(file_path):
    document = fitz.open(stream=file_path.read(), filetype="pdf")
    images = []
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        pix = page.get_pixmap()
        img_bytes = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_bytes))
        images.append(image)
    return images

def pil_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def get_gemini_response(prompt_parts, image_parts=None):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        contents = prompt_parts
        if image_parts: # Only include image parts if they are provided
            contents = image_parts + [{"text": prompt_parts[0]}]

        response = model.generate_content(contents,
                                          request_options={"timeout": 600})
        return response.text
    except Exception as e:
        st.error(f"Error calling Gemini API: {e}")
        return None

def extract_invoice_details(image_data):
    prompt = """
    You are an expert data extractor. Analyze the invoice image(s) and extract the data in valid JSON format.

    🔸 Respond with **only** raw JSON — no extra text, no markdown, no code fences.
    🔸 All JSON keys and string values **must use double quotes**.
    🔸 Use `null` for missing fields.
    🔸 Follow this structure exactly:

    JSON Structure:
    ```json
    {
      "invoice_number": "STRING",
      "invoice_date": "YYYY-MM-DD",
      "due_date": "YYYY-MM-DD",
      "vendor_info": {
        "name": "STRING",
        "address": "STRING",
        "phone": "STRING",
        "email": "STRING",
        "website": "STRING"
      },
      "customer_info": {
        "name": "STRING",
        "address": "STRING",
        "phone": "STRING",
        "email": "STRING"
      },
      "items": [
        {
          "description": "STRING",
          "quantity": NUMBER,
          "unit_price": NUMBER,
          "line_total": NUMBER
        }
      ],
      "subtotal": NUMBER,
      "tax_amount": NUMBER,
      "total_amount": NUMBER,
      "currency": "STRING",
      "payment_terms": "STRING",
      "notes": "STRING"
    }
    ```
    Ensure the output is valid JSON, enclosed only within the ```json ... ``` block.
    """
    image_parts = []
    for img in image_data:
        image_parts.append({
            "mime_type": "image/png",
            "data": pil_image_to_base64(img)
        })

    with st.spinner("Analyzing invoice... This may take a moment."):
        response_text = get_gemini_response([prompt], image_parts=image_parts)

    if response_text:
        try:
            json_start = response_text.find("```json")
            json_end = response_text.rfind("```")
            if json_start != -1 and json_end != -1 and json_end > json_start:
                json_string = response_text[json_start + len("```json"):json_end].strip()
            else:
                json_string = response_text.strip()

            invoice_json = json.loads(json_string)
            validated = InvoiceData(**invoice_json)
            return validated.dict()
        except (json.JSONDecodeError, ValidationError) as e:
            st.error(f"Failed to parse JSON from AI response: {e}")
            st.code(response_text, language="text")
            return None
    return None

uploaded_file = st.file_uploader(
    "Drag and Drop your Invoice File Here",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=False,
    help="Supported formats: PDF, PNG, JPG, JPEG",
    key="invoice_uploader" # Add a key to the uploader
)

if uploaded_file is not None:
    # Check if a new file has been uploaded or if it's the same file
    current_file_hash = hash(uploaded_file.read())
    uploaded_file.seek(0) # Reset file pointer after reading for hash

    if current_file_hash != st.session_state.uploaded_file_hash:
        st.session_state.uploaded_file_hash = current_file_hash
        st.success(f"File uploaded: {uploaded_file.name}")
        file_extension = uploaded_file.name.split(".")[-1].lower()

        invoice_images = []
        if file_extension == "pdf":
            try:
                invoice_images = convert_pdf_to_images(uploaded_file)
                st.info(f"PDF processed. {len(invoice_images)} page(s) extracted as images.")
            except Exception as e:
                st.error(f"Error processing PDF: {e}")
                st.stop()
        elif file_extension in ["png", "jpg", "jpeg"]:
            invoice_images.append(Image.open(uploaded_file))
            st.info("Image file loaded.")
        else:
            st.warning("Unsupported file type.")
            st.stop()

        if invoice_images:
            invoice_details = extract_invoice_details(invoice_images)
            if invoice_details:
                st.session_state.invoice_data = invoice_details
                st.subheader("Extracted Invoice Details (JSON):")
                st.json(invoice_details)
                # ✅ Print to VS Code console
                print("Extracted Invoice Data:\n", json.dumps(invoice_details, indent=2))

                st.subheader("Invoice Summary:")
                st.write(f"**Invoice Number:** {invoice_details.get('invoice_number', 'N/A')}")
                st.write(f"**Invoice Date:** {invoice_details.get('invoice_date', 'N/A')}")
                st.write(f"**Total Amount:** {invoice_details.get('currency', '')} {invoice_details.get('total_amount', 'N/A')}")
                if invoice_details.get('vendor_info'):
                    st.write(f"**Vendor:** {invoice_details['vendor_info'].get('name', 'N/A')}")
                if invoice_details.get('customer_info'):
                    st.write(f"**Customer:** {invoice_details['customer_info'].get('name', 'N/A')}")

                if invoice_details.get('items'):
                    st.subheader("Line Items:")
                    for item in invoice_details['items']:
                        st.write(f"- {item.get('description', 'N/A')}: Qty {item.get('quantity', 'N/A')} @ {item.get('unit_price', 'N/A')} = {item.get('line_total', 'N/A')}")
            else:
                # If extraction failed, ensure invoice_data is cleared or remains None
                st.session_state.invoice_data = None
    else:
        # If the same file is re-uploaded, do nothing or show a message
        st.info("Same file re-uploaded. Using previously extracted data.")
        # Display the previously extracted data if available
        if st.session_state.invoice_data:
            st.subheader("Previously Extracted Invoice Details (JSON):")
            st.json(st.session_state.invoice_data)

            st.subheader("Invoice Summary:")
            st.write(f"**Invoice Number:** {st.session_state.invoice_data.get('invoice_number', 'N/A')}")
            st.write(f"**Invoice Date:** {st.session_state.invoice_data.get('invoice_date', 'N/A')}")
            st.write(f"**Total Amount:** {st.session_state.invoice_data.get('currency', '')} {st.session_state.invoice_data.get('total_amount', 'N/A')}")
            if st.session_state.invoice_data.get('vendor_info'):
                st.write(f"**Vendor:** {st.session_state.invoice_data['vendor_info'].get('name', 'N/A')}")
            if st.session_state.invoice_data.get('customer_info'):
                st.write(f"**Customer:** {st.session_state.invoice_data['customer_info'].get('name', 'N/A')}")

            if st.session_state.invoice_data.get('items'):
                st.subheader("Line Items:")
                for item in st.session_state.invoice_data['items']:
                    st.write(f"- {item.get('description', 'N/A')}: Qty {item.get('quantity', 'N/A')} @ {item.get('unit_price', 'N/A')} = {item.get('line_total', 'N/A')}")
        else:
            st.warning("No invoice data available for the re-uploaded file.")


st.divider()
st.subheader("Ask me anything about the invoice (or generally)! 👇")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    ai_prompt_parts = [prompt]
    # Crucial change: Only add image_parts if there's no extracted invoice data yet.
    # Otherwise, rely on the stored JSON.
    image_parts_for_gemini = None
    if st.session_state.invoice_data:
        invoice_json_string = json.dumps(st.session_state.invoice_data, indent=2)
        ai_prompt_parts.insert(0, f"""
            You have previously extracted the following invoice data. Use this data to answer the user's questions.
            Only refer to information from this JSON if relevant. If the question is general, answer generally.

            Invoice Data:
            ```json
            {invoice_json_string}
            ```
            """)
        st.info("Using previously extracted invoice data. Not re-analyzing the image.")
    elif uploaded_file is not None and st.session_state.uploaded_file_hash is not None:
        # This part should ideally not be reached if invoice_data is already populated on upload
        # but as a fallback, if for some reason invoice_data is missing but a file was uploaded,
        # you could try to re-process. However, the goal is to avoid this.
        # For this specific issue, the fix is primarily in the file uploader logic.
        pass


    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            full_response = get_gemini_response(ai_prompt_parts, image_parts=image_parts_for_gemini)
            if full_response:
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.warning("Could not get a response from the AI.")