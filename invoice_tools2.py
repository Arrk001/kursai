import streamlit as st
from dotenv import load_dotenv
import os
import io
from PIL import Image
import fitz  # PyMuPDF
from google import genai
from google.genai import types
import json
from rich import print


# --- Configuration ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_TOKEN")
MODEL_NAME = "gemini-2.5-flash"  # Using gemini-2.5-flash for multimodal capabilities

# Initialize Google AI client
def get_google_client():
    """Initialize and return Google AI client."""
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_TOKEN environment variable not found. Please set it.")
    return genai.Client(api_key=GOOGLE_API_KEY)

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
    client = get_google_client()
    
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
          "discount": "NUMBER",  // Discount per item (amount or percentage if specified),
          "line_total": "NUMBER"
        }
      ],
      "subtotal": "NUMBER",
      "tax_amount": "NUMBER",
      "total_amount": "NUMBER",
      "total_discount": "NUMBER",  // Discount total (amount or percentage if specified),
      "currency": "STRING",
      "payment_terms": "STRING",
      "payment_method": "STRING",
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

def process_uploaded_file(uploaded_file):
    """
    Process uploaded file and return list of images.
    Handles both PDF and image files.
    """
    if uploaded_file is None:
        return None
        
    file_extension = uploaded_file.name.split(".")[-1].lower()
    invoice_images = []
    
    if file_extension == "pdf":
        try:
            invoice_images = convert_pdf_to_images(uploaded_file)
            st.info(f"PDF processed. {len(invoice_images)} page(s) extracted as images.")
        except Exception as e:
            st.error(f"Error processing PDF: {e}")
            return None
    elif file_extension in ["png", "jpg", "jpeg"]:
        invoice_images.append(Image.open(uploaded_file))
        st.info("Image file loaded.")
    else:
        st.warning("Unsupported file type.")
        return None
        
    return invoice_images

def process_multiple_files(uploaded_files):
    """
    Process multiple uploaded files and return a list of processed invoices.
    Each invoice contains metadata and extracted details.
    """
    if not uploaded_files:
        return []
    
    processed_invoices = []
    
    for uploaded_file in uploaded_files:
        if uploaded_file is None:
            continue
            
        # Create invoice metadata
        invoice_metadata = {
            "filename": uploaded_file.name,
            "file_size": uploaded_file.size,
            "file_type": uploaded_file.type,
            "status": "processing"
        }
        
        try:
            # Process the file
            invoice_images = process_uploaded_file(uploaded_file)
            
            if invoice_images:
                # Extract invoice details
                invoice_details = extract_invoice_details(invoice_images)
                
                if invoice_details:
                    invoice_metadata.update({
                        "status": "success",
                        "details": invoice_details,
                        "page_count": len(invoice_images)
                    })
                else:
                    invoice_metadata.update({
                        "status": "failed",
                        "error": "Failed to extract invoice details"
                    })
            else:
                invoice_metadata.update({
                    "status": "failed",
                    "error": "Failed to process file"
                })
                
        except Exception as e:
            invoice_metadata.update({
                "status": "failed",
                "error": str(e)
            })
        
        processed_invoices.append(invoice_metadata)
    
    return processed_invoices

def display_invoice_summary(invoice_details):
    """
    Display a formatted summary of the extracted invoice details.
    """
    st.subheader("Invoice Summary:")
    st.write(f"**Invoice Number:** {invoice_details.get('invoice_number', 'N/A')}")
    st.write(f"**Invoice Date:** {invoice_details.get('invoice_date', 'N/A')}")
    st.write(f"**Total Amount:** {invoice_details.get('currency', '')} {invoice_details.get('total_amount', 'N/A')}")
    st.write(f"**Payment Method:** {invoice_details.get('payment_method', 'N/A')}")
    
    if invoice_details.get('vendor_info'):
        st.write(f"**Vendor:** {invoice_details['vendor_info'].get('name', 'N/A')}")
    if invoice_details.get('customer_info'):
        st.write(f"**Customer:** {invoice_details['customer_info'].get('name', 'N/A')}")

    if invoice_details.get('items'):
        st.subheader("Line Items:")
        for item in invoice_details['items']:
            st.write(f"- {item.get('description', 'N/A')}: Qty {item.get('quantity', 'N/A')} @ {item.get('unit_price', 'N/A')} = {item.get('line_total', 'N/A')}")

def print_invoice_json(invoice_details):
    """
    Print the extracted invoice JSON to console for debugging.
    """
    print("Extracted Invoice JSON:")
    print(json.dumps(invoice_details, indent=2)) 