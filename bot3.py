import streamlit as st
from dotenv import load_dotenv
import os
import io
from PIL import Image
import fitz  # PyMuPDF
from google import genai
from google.genai import types
import json

# --- Configuration ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_TOKEN")
if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_TOKEN environment variable not found. Please set it.")
    st.stop()

client = genai.Client(api_key=GOOGLE_API_KEY)
MODEL_NAME = "gemini-2.5-flash"  # Using gemini-2.5-flash for multimodal capabilities

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Invoice AI Assistant", layout="wide")
st.title("📄 Invoice AI Assistant")
st.markdown("Upload your invoice file (PDF, JPG, PNG) and let AI extract the details as JSON!")

# --- Initialize session state for invoice data ---
if "invoice_data" not in st.session_state:
    st.session_state.invoice_data = None

# --- Helper Functions ---
def convert_pdf_to_images(file_path):
    """
    Converts each page of a PDF file into a PIL Image object.
    Requires PyMuPDF (fitz)
    """
    document = fitz.open(stream=file_path.read(), filetype="pdf")
    images = []
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        pix = page.get_pixmap()
        img_bytes = pix.tobytes("png")  # Convert to PNG bytes
        image = Image.open(io.BytesIO(img_bytes))
        images.append(image)
    return images

def pil_image_to_bytes(image, format="PNG"):
    """Converts a PIL Image to bytes."""
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    return buffered.getvalue()

def extract_invoice_details(image_data):
    """
    Prompts the Gemini model to extract invoice details and format them as JSON.
    """
    prompt = """
    Analyze the provided invoice image(s). Extract the following details and provide them in a JSON object.
    Be precise with numerical values and dates. If a field is not found, use `null`.

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
          "quantity": "NUMBER",
          "unit_price": "NUMBER",
          "line_total": "NUMBER"
        }
      ],
      "subtotal": "NUMBER",
      "tax_amount": "NUMBER",
      "total_amount": "NUMBER",
      "currency": "STRING",
      "payment_terms": "STRING",
      "notes": "STRING"
    }
    ```
    Ensure the output is valid JSON, enclosed only within the ```json ... ``` block.
    """
    parts = []
    for img in image_data:
        img_bytes = pil_image_to_bytes(img)
        parts.append(types.Part.from_bytes(data=img_bytes, mime_type="image/png"))
    contents = parts + [prompt]

    with st.spinner("Analyzing invoice... This may take a moment."):
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents
        )

    if response.text:
        try:
            # Extract JSON string from the response (it might be wrapped in ```json tags)
            json_start = response.text.find("```json")
            json_end = response.text.rfind("```")
            if json_start != -1 and json_end != -1 and json_end > json_start:
                json_string = response.text[json_start + len("```json"):json_end].strip()
            else:
                json_string = response.text.strip()  # Assume it's just JSON if no tags

            invoice_json = json.loads(json_string)
            return invoice_json
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse JSON from AI response: {e}")
            st.code(response.text, language="text")  # Show raw response for debugging
            return None
    return None

# --- File Uploader ---
uploaded_file = st.file_uploader(
    "Drag and Drop your Invoice File Here",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=False,
    help="Supported formats: PDF, PNG, JPG, JPEG"
)

if uploaded_file is not None:
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
            # Print JSON to console (VSCode terminal)
            print("Extracted Invoice JSON:")
            print(json.dumps(invoice_details, indent=2))

            # Display a summary for readability
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