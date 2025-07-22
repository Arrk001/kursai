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
from datetime import datetime

DB_CSV_PATH = "invoices_db.csv"

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Individualios veiklos asistentas", layout="wide")
st.title("📄 Individualios veiklos asistentas 📄")
st.markdown("Įkelkite kelis sąskaitų faktūrų failus (PDF, JPG, PNG) ir leiskite AI išgauti duomenis")

# --- Show Database Button (Sticky) ---
if "show_db" not in st.session_state:
    st.session_state.show_db = False

if st.button("Rodyti sąskaitų duomenų bazę"):
    st.session_state.show_db = True

if st.session_state.show_db:
    db_df = None
    db_path_exists = os.path.exists(DB_CSV_PATH)
    if db_path_exists:
        db_df = pd.read_csv(DB_CSV_PATH, dtype=str)
        st.info(f"Naudojama duomenų bazė: {DB_CSV_PATH}")
    else:
        st.warning("Nėra numatytos sąskaitų duomenų bazės. Galite pasirinkti CSV failą rankiniu būdu.")
        uploaded_db = st.file_uploader("Pasirinkite sąskaitų duomenų bazės CSV failą", type=["csv"], key="db_csv_upload")
        if uploaded_db is not None:
            db_df = pd.read_csv(uploaded_db, dtype=str)
            st.info(f"Rodomas įkeltas failas: {uploaded_db.name}")
    if db_df is not None:
        st.dataframe(db_df)
        st.download_button(
            label="📥 Atsisiųsti šį sąskaitų duomenų bazės CSV",
            data=db_df.to_csv(index=False),
            file_name="invoices_db.csv",
            mime="text/csv"
        )
    elif not db_path_exists:
        st.warning("Nepavyko rasti ar įkelti sąskaitų duomenų bazės failo.")

# --- Initialize session state for invoice data ---
if "processed_invoices" not in st.session_state:
    st.session_state.processed_invoices = []


def invoice_to_rows(invoice_details):
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
    import pandas as pd
    from pandas.errors import EmptyDataError
    if os.path.exists(db_path):
        try:
            db_df = pd.read_csv(db_path, dtype=str)
        except EmptyDataError:
            db_df = pd.DataFrame()
    else:
        db_df = pd.DataFrame()
    new_rows = []
    for inv in processed_invoices:
        if inv["status"] == "success" and "details" in inv:
            rows = invoice_to_rows(inv["details"])
            for row in rows:
                orig_number = row["saskaitos_numeris"]
                if not orig_number:
                    new_rows.append(row)
                    continue
                if not db_df.empty:
                    existing = db_df[db_df["saskaitos_numeris"].str.startswith(orig_number, na=False)]
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
    if not db_df.empty:
        combined = pd.concat([db_df, new_df], ignore_index=True)
    else:
        combined = new_df
    combined.to_csv(db_path, index=False)

# --- Tax Calculation Function ---
def calculate_individual_activity_taxes(
    gross_income: float,
    expense_mode: str,
    custom_expenses: float,
    gpm_rate: float
):
    if expense_mode == "30%":
        expenses = gross_income * 0.3
    else:
        expenses = custom_expenses
    tax_base = gross_income - expenses
    sodra_base = tax_base * 0.9
    vsd = sodra_base * 0.1252
    psd = sodra_base * 0.0698
    gpm = tax_base * gpm_rate
    total_tax = vsd + psd + gpm
    return {
        "tax_base": tax_base,
        "sodra_base": sodra_base,
        "vsd": vsd,
        "psd": psd,
        "gpm": gpm,
        "total_tax": total_tax
    }

def gemini_check_and_qa(tax_results, user_question=None):
    client = get_google_client()
    MODEL_NAME = "gemini-2.5-flash"
    prompt = (
        "Tu esi mokesčių konsultantas, kuris tikrina individualios veiklos mokesčių skaičiavimus pagal Lietuvos įstatymus. "
        "Patikrink šiuos rezultatus ir patvirtink, ar jie atrodo teisingi, ar yra kokių nors klaidų ar pastabų. "
        "Jei reikia, gali ieškoti informacijos internete. Atsakyk lietuviškai, aiškiai ir draugiškai.\n\n"
        "SVARBU: Sodros įmokų bazė = MMA × 63,2 %. 2025 metais MMA yra 1015 EUR.\n"
        "SVARBU: VSD įmokų bazė = 90% nuo apmokestinamo pelno, VSD = 12,52% nuo šios bazės.\n"
        "SVARBU: PSD (privalomasis sveikatos draudimas) tarifas yra 6,98% nuo MMA.\n"
        "SVARBU: Apmokestinamas pelnas = Pajamos × 70 %.\n\n"
        f"Skaičiavimo rezultatai:\n{json.dumps(tax_results, indent=2, ensure_ascii=False)}\n"
    )
    if user_question:
        prompt += f"\nPapildomas vartotojo klausimas: {user_question}\nAtsakyk į šį klausimą."
    with st.spinner("Google Gemini tikrina rezultatus..."):
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt]
        )
    return response.text if hasattr(response, 'text') else str(response)

# --- Main Application Logic ---
def main():
    try:
        get_google_client()
    except ValueError as e:
        st.error(str(e))
        st.stop()

    uploaded_files = st.file_uploader(
        "Įkelkite savo sąskaitų faktūrų failus",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
        help="Palaikomi formatai: PDF, PNG, JPG, JPEG. Galite įkelti kelis failus vienu metu!"
    )

    if uploaded_files:
        st.success(f"Įkelti failai: {len(uploaded_files)} failas(-ai)")
        with st.expander("📁 Įkelti failai", expanded=False):
            for i, file in enumerate(uploaded_files):
                st.write(f"{i+1}. {file.name} ({file.size} bytes)")
        if st.button("🚀 Apdoroti visas sąskaitas faktūras", type="primary"):
            with st.spinner("Apdorojama sąskaitos faktūros... Tai gali užtrukti kelias akimirkas."):
                st.session_state.processed_invoices = process_multiple_files(uploaded_files)
                update_invoice_db(st.session_state.processed_invoices)
            st.success("Apdorojimas baigtas! Duomenų bazė atnaujinta.")

    if st.session_state.processed_invoices:
        st.subheader("📋 Apdorotos sąskaitos faktūros")
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
        for i, invoice in enumerate(st.session_state.processed_invoices):
            expander_key = f"invoice_{i}_{invoice['filename']}"
            if invoice["status"] == "success":
                title = f"✅ {invoice['filename']}"
            elif invoice["status"] == "failed":
                title = f"❌ {invoice['filename']}"
            else:
                title = f"⏳ {invoice['filename']}"
            with st.expander(title, expanded=False):
                st.write(f"**File Type:** {invoice['file_type']}")
                st.write(f"**File Size:** {invoice['file_size']} bytes")
                st.write(f"**Status:** {invoice['status']}")
                if invoice["status"] == "success":
                    st.write(f"**Pages:** {invoice.get('page_count', 'N/A')}")
                    if "details" in invoice:
                        display_invoice_summary(invoice["details"])
                        with st.expander("📄 Full JSON Data", expanded=False):
                            st.json(invoice["details"])
                            json_str = json.dumps(invoice["details"], indent=2)
                            st.download_button(
                                label=f"📥 Download {invoice['filename']}.json",
                                data=json_str,
                                file_name=f"{invoice['filename']}.json",
                                mime="application/json"
                            )
                        print_invoice_json(invoice["details"])
                elif invoice["status"] == "failed":
                    st.error(f"**Error:** {invoice.get('error', 'Unknown error')}")
        if successful > 0:
            st.divider()
            st.subheader("📊 Batch Operations")
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

    # --- Tax Calculator (Remake: HTML/JS logic, Streamlit UI) ---
    st.divider()
    st.subheader("💸 Individualios Veiklos Mokesčių Skaičiuoklė (2025)")
    today = pd.Timestamp.today().date()
    start_date = st.date_input("Nuo datos", value=pd.to_datetime("2025-01-01").date(), key="tax_start")
    end_date = st.date_input("Iki datos", value=today, min_value=start_date, key="tax_end")
    # MMA for 2025 is 1015 EUR
    mma_2025 = 1015.0
    mma = st.number_input("Minimali mėnesinė alga (MMA, €)", min_value=0.0, value=mma_2025, step=1.0, key="mma")

    # Load and filter invoices
    if os.path.exists(DB_CSV_PATH):
        db_df = pd.read_csv(DB_CSV_PATH, dtype=str)
        db_df["data"] = pd.to_datetime(db_df["data"], errors="coerce")
        db_df["bendra_suma"] = pd.to_numeric(db_df["bendra_suma"], errors="coerce")
        filtered = db_df[(db_df["data"] >= pd.to_datetime(start_date)) & (db_df["data"] <= pd.to_datetime(end_date))]
        gross_income = filtered["bendra_suma"].sum()
        st.info(f"Pajamų suma iš sąskaitų: **{gross_income:.2f} €** ({len(filtered)} sąskaitos)")
    else:
        gross_income = 0.0
        st.warning("Nėra sąskaitų duomenų bazės.")

    # --- Store and display results using session_state ---
    if "tax_results" not in st.session_state:
        st.session_state.tax_results = None
    if "tax_user_question" not in st.session_state:
        st.session_state.tax_user_question = ""

    if st.button("Skaičiuoti mokesčius"):
        income = gross_income
        MMA = mma
        SODRA_BAZE_RATE = 0.632
        PSD_RATE = 0.0698
        VSD_RATE = 0.1252
        GPM_TAXABLE_RATE = 0.70
        GPM_RATE = 0.05

        sodra_baze = MMA * SODRA_BAZE_RATE
        sodra_baze_annual = sodra_baze * 12
        psd = MMA * PSD_RATE
        psd_annual = psd * 12
        gpm_taxable_profit = income * GPM_TAXABLE_RATE
        gpm_taxable_profit_annual = gpm_taxable_profit  # annual is just 12x monthly income, but income is sum from invoices
        vsd_base = gpm_taxable_profit * 0.9
        vsd_base_annual = vsd_base * 12
        vsd = vsd_base * VSD_RATE
        vsd_annual = vsd * 12
        gpm = gpm_taxable_profit * GPM_RATE
        gpm_annual = gpm * 12
        total_tax = vsd + psd + gpm
        total_tax_annual = vsd_annual + psd_annual + gpm_annual

        st.session_state.tax_results = {
            "Pajamų suma": income,
            "Sodros įmokų bazė": sodra_baze,
            "Sodros įmokų bazė (metinė)": sodra_baze_annual,
            "Apmokestinamas pelnas GPM (70% nuo pajamų)": gpm_taxable_profit,
            "Apmokestinamas pelnas GPM (metinis)": gpm_taxable_profit_annual,
            "VSD įmokų bazė (90% nuo apmokestinamo pelno)": vsd_base,
            "VSD įmokų bazė (metinė)": vsd_base_annual,
            "VSD (12,52% nuo VSD įmokų bazės)": vsd,
            "VSD (metinė)": vsd_annual,
            "PSD (6,98% nuo MMA)": psd,
            "PSD (metinė)": psd_annual,
            "GPM (5%)": gpm,
            "GPM (metinė)": gpm_annual,
            "Viso mokesčių": total_tax,
            "Viso mokesčių (metinė)": total_tax_annual
        }
        st.session_state.tax_user_question = ""
        st.session_state.gemini_checked = False
        st.session_state.gemini_response = None
        st.session_state.gemini_chat_history = []

    # Always display results if they exist
    if st.session_state.tax_results is not None:
        tr = st.session_state.tax_results
        # Defensive keys for results
        pajamos = tr.get("Pajamų suma", 0.0)
        sodra_baze = tr.get("Sodros įmokų bazė", 0.0)
        sodra_baze_annual = tr.get("Sodros įmokų bazė (metinė)", 0.0)
        gpm_taxable_profit = tr.get("Apmokestinamas pelnas GPM (70% nuo pajamų)", 0.0)
        gpm_taxable_profit_annual = tr.get("Apmokestinamas pelnas GPM (metinis)", 0.0)
        vsd_base = tr.get("VSD įmokų bazė (90% nuo apmokestinamo pelno)", 0.0)
        vsd_base_annual = tr.get("VSD įmokų bazė (metinė)", 0.0)
        vsd = tr.get("VSD (12,52% nuo VSD įmokų bazės)", 0.0)
        vsd_annual = tr.get("VSD (metinė)", 0.0)
        psd = tr.get("PSD (6,98% nuo MMA)", 0.0)
        psd_annual = tr.get("PSD (metinė)", 0.0)
        gpm = tr.get("GPM (5%)", 0.0)
        gpm_annual = tr.get("GPM (metinė)", 0.0)
        total_tax = tr.get("Viso mokesčių", 0.0)
        total_tax_annual = tr.get("Viso mokesčių (metinė)", 0.0)
        # Warn if any key is missing
        missing_keys = [k for k, v in zip([
            "Pajamų suma",
            "Sodros įmokų bazė",
            "Sodros įmokų bazė (metinė)",
            "Apmokestinamas pelnas GPM (70% nuo pajamų)",
            "Apmokestinamas pelnas GPM (metinis)",
            "VSD įmokų bazė (90% nuo apmokestinamo pelno)",
            "VSD įmokų bazė (metinė)",
            "VSD (12,52% nuo VSD įmokų bazės)",
            "VSD (metinė)",
            "PSD (6,98% nuo MMA)",
            "PSD (metinė)",
            "GPM (5%)",
            "GPM (metinė)",
            "Viso mokesčių",
            "Viso mokesčių (metinė)"
        ], [pajamos, sodra_baze, sodra_baze_annual, gpm_taxable_profit, gpm_taxable_profit_annual, vsd_base, vsd_base_annual, vsd, vsd_annual, psd, psd_annual, gpm, gpm_annual, total_tax, total_tax_annual]) if v == 0.0 and k not in tr]
        if missing_keys:
            st.warning(f"Trūksta duomenų šioms reikšmėms: {', '.join(missing_keys)}. Gali būti, kad pasikeitė skaičiavimo logika arba reikia atstatyti skaičiuoklę.")
        st.markdown(f"""
        ### Apskaičiuoti rezultatai
        **(per mėnesį / per metus)**
        | Rodiklis | Mėnesio suma | Metinė suma |
        |---|---|---|
        | Pajamų suma | **{pajamos:.2f} €** | **{pajamos*12:.2f} €** |
        | Sodros įmokų bazė | **{sodra_baze:.2f} €** | **{sodra_baze_annual:.2f} €** |
        | Apmokestinamas pelnas GPM (70% nuo pajamų) | **{gpm_taxable_profit:.2f} €** | **{gpm_taxable_profit_annual:.2f} €** |
        | VSD įmokų bazė (90% nuo apmokestinamo pelno) | **{vsd_base:.2f} €** | **{vsd_base_annual:.2f} €** |
        | VSD (12,52% nuo VSD įmokų bazės) | **{vsd:.2f} €** | **{vsd_annual:.2f} €** |
        | PSD (6,98% nuo MMA) | **{psd:.2f} €** | **{psd_annual:.2f} €** |
        | GPM (5% nuo apmokestinamo pelno) | **{gpm:.2f} €** | **{gpm_annual:.2f} €** |
        | **Viso mokesčių** | **{total_tax:.2f} €** | **{total_tax_annual:.2f} €** |
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='background: #fffbeb; border-left: 4px solid #f59e0b; padding: 1rem; border-radius: 0.5rem; color: #92400e; font-size: 0.95rem; margin-top: 1.5rem;'>
            <b>Pastaba apie Sodros įmokų bazę:</b> 2025 m. MMA yra 1015 €, Sodros įmokų bazė = MMA × 63,2 % = 641,08 € per mėnesį. <br>
            <b>Pastaba apie VSD:</b> VSD įmokų bazė = 90% nuo apmokestinamo pelno, VSD = 12,52% nuo šios bazės. <br>
            <b>Pastaba apie PSD skaičiavimą:</b> PSD įmoka yra skaičiuojama kaip 6,98% nuo MMA. <br>
            <b>Pastaba apie GPM:</b> Apmokestinamas pelnas = Pajamos × 70 %.<br>
            <b>Viso mokesčių:</b> VSD + PSD + GPM.
        </div>
        """, unsafe_allow_html=True)

        # AI check button and response
        if "gemini_checked" not in st.session_state:
            st.session_state.gemini_checked = False
        if "gemini_response" not in st.session_state:
            st.session_state.gemini_response = None
        if "gemini_chat_history" not in st.session_state:
            st.session_state.gemini_chat_history = []

        if not st.session_state.gemini_checked:
            if st.button("Patikrinti su Google Gemini"):
                gemini_response = gemini_check_and_qa(st.session_state.tax_results, None)
                st.session_state.gemini_response = gemini_response
                st.session_state.gemini_checked = True
                st.markdown("#### Google Gemini atsakymas:")
                st.write(gemini_response)
        else:
            st.markdown("#### Google Gemini atsakymas:")
            st.write(st.session_state.gemini_response)
            # Now show the chat/question input and history
            if st.session_state.gemini_chat_history:
                st.markdown("---")
                st.markdown("##### Pokalbio istorija su Gemini:")
                for i, (user_msg, ai_msg) in enumerate(st.session_state.gemini_chat_history):
                    st.markdown(f"**Jūs:** {user_msg}")
                    st.markdown(f"**Gemini:** {ai_msg}")
            user_question = st.text_input("Turite klausimą apie mokesčius ar šiuos rezultatus? Užduokite jį čia:", key="tax_qa_followup")
            if st.button("Klausti Gemini apie rezultatus") and user_question.strip():
                # Compose full chat history as context
                chat_context = ""
                for user_msg, ai_msg in st.session_state.gemini_chat_history:
                    chat_context += f"Vartotojas: {user_msg}\nGemini: {ai_msg}\n"
                chat_context += f"Vartotojas: {user_question}\nGemini:"
                # Send full context to Gemini
                full_prompt = (
                    "Tu esi mokesčių konsultantas, kuris tikrina individualios veiklos mokesčių skaičiavimus pagal Lietuvos įstatymus. "
                    "Atsakyk lietuviškai, aiškiai ir draugiškai.\n\n"
                    "SVARBU: Sodros įmokų bazė = MMA × 63,2 %. 2025 metais MMA yra 1015 EUR.\n"
                    "SVARBU: VSD įmokų bazė = 90% nuo apmokestinamo pelno, VSD = 12,52% nuo šios bazės.\n"
                    "SVARBU: PSD (privalomasis sveikatos draudimas) tarifas yra 6,98% nuo MMA.\n"
                    "SVARBU: Apmokestinamas pelnas = Pajamos × 70 %.\n\n"
                    f"Skaičiavimo rezultatai:\n{json.dumps(st.session_state.tax_results, indent=2, ensure_ascii=False)}\n\n"
                    f"Pokalbio istorija:\n{chat_context}"
                )
                client = get_google_client()
                MODEL_NAME = "gemini-2.5-flash"
                with st.spinner("Google Gemini atsako..."):
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=[full_prompt]
                    )
                ai_answer = response.text if hasattr(response, 'text') else str(response)
                st.session_state.gemini_chat_history.append((user_question, ai_answer))
                st.experimental_rerun()
            if st.session_state.get('followup_gemini_response'):
                st.markdown("#### Google Gemini atsakymas į jūsų klausimą:")
                st.write(st.session_state.followup_gemini_response)

        # Reset button
        if st.button("Atstatyti skaičiuoklę"):
            st.session_state.tax_results = None
            st.session_state.gemini_checked = False
            st.session_state.gemini_response = None
            st.session_state.gemini_chat_history = []
            st.session_state.followup_gemini_response = None

if __name__ == "__main__":
    main() 