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

def try_repair_json(json_string):
    """
    Attempt to repair common LLM JSON issues: trailing commas, missing braces, and random tokens.
    Returns a string that is more likely to be valid JSON.
    """
    import re
    # Remove trailing commas before closing brackets/braces
    json_string = re.sub(r',\s*([}\]])', r'\1', json_string)
    # Remove any double commas
    json_string = re.sub(r',\s*,', ',', json_string)
    # Remove any stray commas at the end of arrays/objects
    json_string = re.sub(r',\s*([}\]])', r'\1', json_string)
    # Remove random non-JSON tokens between objects in arrays (e.g., hallucinated words)
    # This will remove any word (letters only) that appears between a number/null/true/false and a closing brace
    json_string = re.sub(r'(\d+\.?\d*|null|true|false)\s+([a-zA-Z_]+)\s*([}\]])', r'\1\3', json_string)
    # Remove any word (letters only) that appears before a closing brace in an object
    json_string = re.sub(r'([}\]])\s+[a-zA-Z_]+\s*([}\]])', r'\1\2', json_string)
    return json_string

def extract_invoice_details(image_data):
    """
    Prompts the Gemini model to extract invoice details and format them as JSON using the Lithuanian schema.
    """
    client = get_google_client()
    
    prompt = """
    Analizuok pateiktą sąskaitos faktūros atvaizdą (-us). Ištrauk visą informaciją pagal šią JSON schemą. Jei laukas nerastas, naudok `null`.

    JSON struktūra:
    ```json
    {
      "saskaitos_numeris": "STRING",
      "data": "YYYY-MM-DD",
      "pardavejas": {
        "name": "STRING",
        "asmens_kodas": "STRING",
        "individualios_veiklos_pazymejimo_numeris": "STRING",
        "address": "STRING",
        "phone": "STRING",
        "email": "STRING"
      },
      "pirkejas": {
        "name": "STRING",
        "asmens_kodas": "STRING",
        "individualios_veiklos_pazymejimo_numeris": "STRING",
        "address": "STRING",
        "phone": "STRING",
        "email": "STRING"
      },
      "paslaugos": [
        {
          "description": "STRING",
          "quantity": "NUMBER",
          "unit": "STRING",
          "price_per_unit": "NUMBER",
          "total": "NUMBER"
        }
      ],
      "bendra_suma": "NUMBER",
      "pvm": "NUMBER",
      "suma_zodziais": "STRING",
      "apmokejimo_budas": "STRING",
      "apmokejimo_terminas": "STRING",
      "parasas": "STRING"
    }
    ```
    Atsakyk TIK su JSON, be papildomų paaiškinimų.
    """
    parts = []
    for img in image_data:
        img_bytes = pil_image_to_bytes(img)
        parts.append(types.Part.from_bytes(data=img_bytes, mime_type="image/png"))
    contents = parts + [prompt]

    with st.spinner("Analizuojama sąskaita... Palaukite."):
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents
        )

    if response.text:
        try:
            json_start = response.text.find("```json")
            json_end = response.text.rfind("```")
            if json_start != -1 and json_end != -1 and json_end > json_start:
                json_string = response.text[json_start + len("```json"):json_end].strip()
            else:
                json_string = response.text.strip()
            try:
                invoice_json = json.loads(json_string)
            except json.JSONDecodeError:
                repaired = try_repair_json(json_string)
                invoice_json = json.loads(repaired)
            return invoice_json
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse JSON from AI response: {e}")
            st.code(response.text, language="text")
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
    Display a formatted summary of the extracted invoice details (Lithuanian schema).
    """
    st.subheader("Sąskaitos santrauka:")
    st.write(f"**Sąskaitos numeris:** {invoice_details.get('saskaitos_numeris', 'N/A')}")
    st.write(f"**Data:** {invoice_details.get('data', 'N/A')}")
    st.write(f"**Bendra suma:** {invoice_details.get('bendra_suma', 'N/A')}")
    st.write(f"**PVM:** {invoice_details.get('pvm', 'N/A')}")
    st.write(f"**Apmokėjimo būdas:** {invoice_details.get('apmokejimo_budas', 'N/A')}")
    st.write(f"**Apmokėjimo terminas:** {invoice_details.get('apmokejimo_terminas', 'N/A')}")
    if invoice_details.get('pardavejas'):
        st.write(f"**Pardavėjas:** {invoice_details['pardavejas'].get('name', 'N/A')}")
    if invoice_details.get('pirkejas'):
        st.write(f"**Pirkėjas:** {invoice_details['pirkejas'].get('name', 'N/A')}")
    if invoice_details.get('paslaugos'):
        st.subheader("Paslaugos:")
        for item in invoice_details['paslaugos']:
            st.write(f"- {item.get('description', 'N/A')}: {item.get('quantity', 'N/A')} {item.get('unit', '')} x {item.get('price_per_unit', 'N/A')} = {item.get('total', 'N/A')}")

def print_invoice_json(invoice_details):
    """
    Print the extracted invoice JSON to console for debugging.
    """
    print("Extracted Invoice JSON:")
    print(json.dumps(invoice_details, indent=2))