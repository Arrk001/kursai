import streamlit as st
from invoice_tools2 import (
    process_uploaded_file,
    extract_invoice_details,
    display_invoice_summary,
    print_invoice_json,
    get_google_client,
    process_multiple_files
)
import json

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Invoice AI Assistant", layout="wide")
st.title("📄 Invoice AI Assistant")
st.markdown("Upload multiple invoice files (PDF, JPG, PNG) and let AI extract the details as JSON!")

# --- Initialize session state for invoice data ---
if "processed_invoices" not in st.session_state:
    st.session_state.processed_invoices = []

# --- Main Application Logic ---
def main():
    # Check for API key availability
    try:
        get_google_client()
    except ValueError as e:
        st.error(str(e))
        st.stop()

    # --- File Uploader ---
    uploaded_files = st.file_uploader(
        "Drag and Drop your Invoice Files Here",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
        help="Supported formats: PDF, PNG, JPG, JPEG. You can upload multiple files at once!"
    )

    # --- Process Button ---
    if uploaded_files:
        st.success(f"Files uploaded: {len(uploaded_files)} file(s)")
        
        # Show file list
        with st.expander("📁 Uploaded Files", expanded=False):
            for i, file in enumerate(uploaded_files):
                st.write(f"{i+1}. {file.name} ({file.size} bytes)")
        
        # Process button
        if st.button("🚀 Process All Invoices", type="primary"):
            with st.spinner("Processing invoices... This may take a few moments."):
                st.session_state.processed_invoices = process_multiple_files(uploaded_files)
            st.success("Processing complete!")

    # --- Display Results ---
    if st.session_state.processed_invoices:
        st.subheader("📋 Processed Invoices")
        
        # Summary statistics
        successful = sum(1 for inv in st.session_state.processed_invoices if inv["status"] == "success")
        failed = sum(1 for inv in st.session_state.processed_invoices if inv["status"] == "failed")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Files", len(st.session_state.processed_invoices))
        with col2:
            st.metric("Successful", successful, delta=f"+{successful}")
        with col3:
            st.metric("Failed", failed, delta=f"-{failed}")
        
        st.divider()
        
        # Display each invoice in a collapsible section
        for i, invoice in enumerate(st.session_state.processed_invoices):
            # Create a unique key for each expander
            expander_key = f"invoice_{i}_{invoice['filename']}"
            
            # Determine expander title and icon based on status
            if invoice["status"] == "success":
                title = f"✅ {invoice['filename']}"
                icon = "✅"
            elif invoice["status"] == "failed":
                title = f"❌ {invoice['filename']}"
                icon = "❌"
            else:
                title = f"⏳ {invoice['filename']}"
                icon = "⏳"
            
            with st.expander(title, expanded=False):
                # File metadata
                st.write(f"**File Type:** {invoice['file_type']}")
                st.write(f"**File Size:** {invoice['file_size']} bytes")
                st.write(f"**Status:** {invoice['status']}")
                
                if invoice["status"] == "success":
                    st.write(f"**Pages:** {invoice.get('page_count', 'N/A')}")
                    
                    # Display invoice details
                    if "details" in invoice:
                        # Show summary first
                        display_invoice_summary(invoice["details"])
                        
                        # Show full JSON in a collapsible section
                        with st.expander("📄 Full JSON Data", expanded=False):
                            st.json(invoice["details"])
                            
                            # Download button for JSON
                            json_str = json.dumps(invoice["details"], indent=2)
                            st.download_button(
                                label=f"📥 Download {invoice['filename']}.json",
                                data=json_str,
                                file_name=f"{invoice['filename']}.json",
                                mime="application/json"
                            )
                        
                        # Print to console for debugging
                        print_invoice_json(invoice["details"])
                        
                elif invoice["status"] == "failed":
                    st.error(f"**Error:** {invoice.get('error', 'Unknown error')}")
        
        # --- Batch Operations ---
        if successful > 0:
            st.divider()
            st.subheader("📊 Batch Operations")
            
            # Export all successful invoices as a single JSON file
            successful_invoices = [inv for inv in st.session_state.processed_invoices if inv["status"] == "success"]
            if successful_invoices:
                all_invoices_data = {
                    "processed_at": st.session_state.get("processing_time", "Unknown"),
                    "total_files": len(st.session_state.processed_invoices),
                    "successful_count": len(successful_invoices),
                    "invoices": [
                        {
                            "filename": inv["filename"],
                            "details": inv["details"]
                        } for inv in successful_invoices
                    ]
                }
                
                json_str = json.dumps(all_invoices_data, indent=2)
                st.download_button(
                    label="📥 Download All Invoices (JSON)",
                    data=json_str,
                    file_name="all_invoices.json",
                    mime="application/json"
                )

if __name__ == "__main__":
    main() 