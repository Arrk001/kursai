import streamlit as st
import db_utils
import ai_utils
import metadata_api

st.set_page_config(page_title="StreamRecs: AI-Powered Watchlist Manager")
st.title("🎬 StreamRecs: AI-Powered Watchlist Manager")

# --- Add New Entry ---
st.header("Add to Your Watchlist")
user_title = st.text_input("Enter a show or movie name:")

if st.button("Check Title (AI Suggestion)") and user_title:
    clarified = ai_utils.clarify_title(user_title)
    st.session_state['clarified_title'] = clarified
    st.success(f"AI Suggests: {clarified}")

clarified_title = st.session_state.get('clarified_title', user_title)

status = st.selectbox("Have you seen this?", ["Seen", "Want to See", "Not Interested"])

if st.button("Fetch Metadata & Save") and clarified_title:
    meta = metadata_api.fetch_metadata(clarified_title)
    if meta:
        db_utils.add_entry(meta['title'], meta['type'], meta['genre'], meta['year'], status)
        st.success(f"Saved: {meta['title']} ({meta['year']}) [{meta['genre']}] as {status}")
    else:
        db_utils.add_entry(clarified_title, '', '', '', status)
        st.warning(f"Saved with minimal info: {clarified_title}")

# --- Display Watchlist ---
st.header("Your Watchlist")
df = db_utils.read_watchlist()
st.dataframe(df)

# --- AI Chat about Watchlist ---
st.header("Ask About Your Watchlist (AI Chat)")
user_query = st.text_input("Ask a question (e.g., What sci-fi movies have I seen?)")
if st.button("Ask AI") and user_query:
    answer = ai_utils.chat_about_watchlist(user_query, df)
    st.info(answer) 