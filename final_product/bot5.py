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
import pandas as pd
import os

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Individualios veiklos asistentas", layout="wide")
st.title("📄 Individualios veiklos asistentas 📄")
st.markdown("Įkelkite kelis sąskaitų faktūrų failus (PDF, JPG, PNG) ir leiskite AI išgauti duomenis")

# --- Initialize session state for invoice data ---
if "processed_invoices" not in st.session_state:
    st.session_state.processed_invoices = []

DB_CSV_PATH = "invoices_db.csv"

def invoice_to_rows(invoice_details):
    """
    Flatten invoice details into a list of dicts (one per service item, or one if no items), using Lithuanian schema fields.
    """
    rows = []
    items = invoice_details.get("paslaugos", [])
    base = {
        "saskaitos_numeris": invoice_details.get("saskaitos_numeris", ""),
        "data": invoice_details.get("data", ""),
        "pardavejas": invoice_details.get("pardavejas", {}).get("name", ""),
        "pirkejas": invoice_details.get("pirkejas", {}).get("name", ""),
        "bendra_suma": invoice_details.get("bendra_suma", ""),
        "pvm": invoice_details.get("pvm", ""),
        "suma_zodziais": invoice_details.get("suma_zodziais", ""),
        "apmokejimo_budas": invoice_details.get("apmokejimo_budas", ""),
        "apmokejimo_terminas": invoice_details.get("apmokejimo_terminas", ""),
        "parasas": invoice_details.get("parasas", ""),
    }
    if items:
        for item in items:
            row = base.copy()
            row.update({
                "paslauga_aprasymas": item.get("description", ""),
                "kiekis": item.get("quantity", ""),
                "vienetas": item.get("unit", ""),
                "kaina_uz_vnt": item.get("price_per_unit", ""),
                "viso": item.get("total", ""),
            })
            rows.append(row)
    else:
        rows.append(base)
    return rows

def update_invoice_db(processed_invoices, db_path=DB_CSV_PATH):
    """
    Append new successful invoices to the CSV database. If a saskaitos_numeris already exists, add _1, _2, etc. to the new saskaitos_numeris.
    """
    import pandas as pd
    from pandas.errors import EmptyDataError
    # Load existing DB
    if os.path.exists(db_path):
        try:
            db_df = pd.read_csv(db_path, dtype=str)
        except EmptyDataError:
            db_df = pd.DataFrame()
    else:
        db_df = pd.DataFrame()
    # Collect new rows
    new_rows = []
    for inv in processed_invoices:
        if inv["status"] == "success" and "details" in inv:
            rows = invoice_to_rows(inv["details"])
            for row in rows:
                orig_number = row["saskaitos_numeris"]
                if not orig_number:
                    new_rows.append(row)
                    continue
                # Find all existing invoice numbers that match this pattern
                if not db_df.empty:
                    existing = db_df[db_df["saskaitos_numeris"].str.startswith(orig_number, na=False)]
                    # Count how many already exist (including _1, _2, ...)
                    count = 0
                    for val in existing["saskaitos_numeris"].values:
                        if val == orig_number:
                            count = max(count, 1)
                        elif val.startswith(f"{orig_number}_"):
                            try:
                                suffix = int(val.split(f"{orig_number}_")[-1])
                                count = max(count, suffix + 1)
                            except Exception:
                                pass
                    if count == 0 and orig_number in db_df["saskaitos_numeris"].values:
                        count = 1
                    if count > 0:
                        row["saskaitos_numeris"] = f"{orig_number}_{count}"
                new_rows.append(row)
    if not new_rows:
        return
    new_df = pd.DataFrame(new_rows)
    # No duplicate dropping, as we want to keep all, but with unique saskaitos_numeris
    if not db_df.empty:
        combined = pd.concat([db_df, new_df], ignore_index=True)
    else:
        combined = new_df
    combined.to_csv(db_path, index=False)

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
        "Įkelkite savo sąskaitų faktūrų failus",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
        help="Palaikomi formatai: PDF, PNG, JPG, JPEG. Galite įkelti kelis failus vienu metu!"
    )

    # --- Process Button ---
    if uploaded_files:
        st.success(f"Įkelti failai: {len(uploaded_files)} failas(-ai)")

        # Show file list
        with st.expander("📁 Įkelti failai", expanded=False):
            for i, file in enumerate(uploaded_files):
                st.write(f"{i+1}. {file.name} ({file.size} bytes)")
        
        # Process button
        if st.button("🚀 Apdoroti visas sąskaitas faktūras", type="primary"):
            with st.spinner("Apdorojama sąskaitos faktūros... Tai gali užtrukti kelias akimirkas."):
                st.session_state.processed_invoices = process_multiple_files(uploaded_files)
                # Update the CSV database automatically
                update_invoice_db(st.session_state.processed_invoices)
            st.success("Apdorojimas baigtas! Duomenų bazė atnaujinta.")

    # --- Display Results ---
    if st.session_state.processed_invoices:
        st.subheader("📋 Apdorotos sąskaitos faktūros")

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
            # Show current database
            if os.path.exists(DB_CSV_PATH):
                st.markdown("#### Current Invoice Database (CSV)")
                db_df = pd.read_csv(DB_CSV_PATH, dtype=str)
                st.dataframe(db_df)
                st.download_button(
                    label="📥 Download Full Invoice Database (CSV)",
                    data=db_df.to_csv(index=False),
                    file_name="invoices_db.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()