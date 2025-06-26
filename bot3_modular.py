import streamlit as st
from invoice_tools import (
    process_uploaded_file,
    extract_invoice_details,
    display_invoice_summary,
    print_invoice_json,
    get_google_client
)

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Invoice AI Assistant", layout="wide")
st.title("📄 Invoice AI Assistant")
st.markdown("Upload your invoice file (PDF, JPG, PNG) and let AI extract the details as JSON!")

# --- Initialize session state for invoice data ---
if "invoice_data" not in st.session_state:
    st.session_state.invoice_data = None

# --- Main Application Logic ---
def main():
    # Check for API key availability
    try:
        get_google_client()
    except ValueError as e:
        st.error(str(e))
        st.stop()

    # --- File Uploader ---
    uploaded_file = st.file_uploader(
        "Drag and Drop your Invoice File Here",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=False,
        help="Supported formats: PDF, PNG, JPG, JPEG"
    )

    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")
        
        # Process the uploaded file
        invoice_images = process_uploaded_file(uploaded_file)
        
        if invoice_images:
            # Extract invoice details using AI
            invoice_details = extract_invoice_details(invoice_images)
            
            if invoice_details:
                # Store in session state
                st.session_state.invoice_data = invoice_details
                
                # Display results
                st.subheader("Extracted Invoice Details (JSON):")
                st.json(invoice_details)
                
                # Print JSON to console (VSCode terminal)
                print_invoice_json(invoice_details)
                
                # Display summary
                display_invoice_summary(invoice_details)

if __name__ == "__main__":
    main() 