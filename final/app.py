import streamlit as st
import db_utils
import ai_utils
import metadata_api

st.set_page_config(page_title="StreamRecs: AI-Powered Watchlist Manager")
st.title("🎬 StreamRecs: AI-Powered Watchlist Manager 🎬")

# Initialize df here, will be reloaded after updates
df = db_utils.read_watchlist()

# --- Add New Entry ---
st.header("Add to Your Watchlist")

# Reset fields if needed before rendering widgets
if st.session_state.get('reset_fields'):
    st.session_state['user_title_form'] = '' # Ensure these keys match your form's keys
    st.session_state['user_year_form'] = ''  # Ensure these keys match your form's keys
    st.session_state['status_form'] = 'Seen' # Ensure these keys match your form's keys
    del st.session_state['reset_fields']
    st.rerun() # Rerun to clear the input fields after successful save

# Use st.form to group input widgets and handle submission
with st.form(key='add_movie_form'):
    user_title = st.text_input("Enter a show or movie name:", key='user_title_form')
    user_year = st.text_input("Enter the year (optional):", key='user_year_form')
    status = st.selectbox("Have you seen this?", ["Seen", "Want to See", "Not Interested"], key='status_form')

    submit_button = st.form_submit_button(label='Add Movie to Watchlist')

    if submit_button:
        if not user_title.strip():
            st.session_state['save_movie_message'] = ('error', "Please enter a movie title.")
        else:
            title_to_use = st.session_state.get('clarified_title', user_title).strip()
            year_to_use = user_year.strip() if user_year.strip() else None

            meta = metadata_api.fetch_metadata(title_to_use, year_to_use)
            if meta:
                if 'tmdb_id' in df.columns and meta.get('tmdb_id') and str(meta['tmdb_id']) in df['tmdb_id'].astype(str).values:
                    st.session_state['save_movie_message'] = ('warning', f"This movie is already in your watchlist.")
                else:
                    db_utils.add_entry(meta['title'], meta['type'], meta['genre'], meta['year'], status, meta.get('imdb_rating', ''), meta.get('poster_url', ''), meta.get('runtime', ''), meta.get('tmdb_id', ''))
                    st.session_state['save_movie_message'] = ('success', f"Saved: {meta['title']} ({meta['year']}) [{meta['genre']}] as {status}")
                    st.session_state['reset_fields'] = True # Mark for reset on next run
                    # --- IMPORTANT CHANGE HERE ---
                    st.session_state['refresh_watchlist'] = True # Flag to refresh the display
            else:
                db_utils.add_entry(title_to_use, '', '', year_to_use or '', status, '', '', '', '')
                st.session_state['save_movie_message'] = ('warning', f"Saved with minimal info: {title_to_use}")
                st.session_state['reset_fields'] = True # Mark for reset on next run
                # --- IMPORTANT CHANGE HERE ---
                st.session_state['refresh_watchlist'] = True # Flag to refresh the display

# Show save message if present
if 'save_movie_message' in st.session_state:
    msg_type, msg = st.session_state['save_movie_message']
    if msg_type == 'success':
        st.success(msg)
    elif msg_type == 'warning':
        st.warning(msg)
    elif msg_type == 'error':
        st.error(msg)
    del st.session_state['save_movie_message']

# AI Suggestion button (kept outside the form as it's a separate action)
if st.button("Check Title (AI Suggestion)") and st.session_state['user_title_form']:
    clarified = ai_utils.clarify_title(st.session_state['user_title_form'])
    st.session_state['clarified_title'] = clarified
    st.success(f"AI Suggests: {clarified}")

# --- IMPORTANT CHANGE HERE ---
# Reload DataFrame if a refresh is triggered (after adding/updating)
if st.session_state.get('refresh_watchlist'):
    df = db_utils.read_watchlist()
    del st.session_state['refresh_watchlist']
    st.rerun() # Rerun to display the updated DataFrame immediately

# --- Display Watchlist ---
st.header("Your Watchlist")
# Arrange columns as Poster, Title, Type, Genre, Year, Runtime, IMDb Rating, Status (exclude tmdb_id)
cols = ['poster_url', 'title', 'type', 'genre', 'year', 'runtime', 'imdb_rating', 'status']
df = df[[c for c in cols if c in df.columns]]

def format_runtime(runtime):
    try:
        mins = int(runtime)
        hours = mins // 60
        minutes = mins % 60
        return f"{hours}h{minutes}m"
    except (ValueError, TypeError):
        return "-"

# Display as a custom HTML table with poster on the left
html = """
<table>
    <thead>
        <tr>
            <th>Poster</th>
            <th>Title</th>
            <th>Type</th>
            <th>Genre</th>
            <th>Year</th>
            <th>Runtime</th>
            <th>IMDb Rating</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
"""
for _, row in df.iterrows():
    poster_html = f'<img src="{row["poster_url"]}" width="60">' if row['poster_url'] else ''
    html += f"<tr>"
    html += f"<td>{poster_html}</td>"
    html += f"<td>{row['title']}</td>"
    html += f"<td>{row['type']}</td>"
    html += f"<td>{row['genre']}</td>"
    html += f"<td>{row['year']}</td>"
    html += f"<td>{format_runtime(row.get('runtime', ''))}</td>"
    html += f"<td>{row['imdb_rating']}</td>"
    html += f"<td>{row['status']}</td>"
    html += f"</tr>"
html += "</tbody></table>"
st.markdown(html, unsafe_allow_html=True)

# After the table, before the update section
seen_runtimes = df[df['status'] == 'Seen']['runtime'].dropna().astype(str)
total_minutes = 0
for r in seen_runtimes:
    try:
        total_minutes += int(float(r))
    except ValueError:
        pass
weeks = total_minutes // (7 * 24 * 60)
remainder = total_minutes % (7 * 24 * 60)
days = remainder // (24 * 60)
remainder = remainder % (24 * 60)
hours = remainder // 60
minutes = remainder % 60
if weeks > 0:
    st.markdown(f"**Total Watchtime:** {weeks} Weeks, {days} Days, {hours} Hours, {minutes} Minutes")
elif days > 0:
    st.markdown(f"**Total Watchtime:** {days} Days, {hours} Hours, {minutes} Minutes")
else:
    st.markdown(f"**Total Watchtime:** {hours} Hours and {minutes} Minutes")

# --- Interactive Status Update ---
st.header("Update Movie Status")
updated = False
remove_indices = []

# Only show movies with status 'Want to See'
df_want_to_see = df[df['status'] == 'Want to See']

for idx, row in df_want_to_see.iterrows():
    col1, col2 = st.columns([3, 2])
    with col1:
        st.write(f"{row['title']} ({row['year']}) [{row['genre']}]")
        if 'poster_url' in row and row['poster_url']:
            st.image(row['poster_url'], width=100)
    with col2:
        new_status = st.selectbox(
            f"Status for {row['title']}",
            ["Seen", "Want to See", "Not Interested"],
            index=["Seen", "Want to See", "Not Interested"].index(row['status']),
            key=f"status_{row['title']}_{row['year']}"
        )
        if new_status != row['status']:
            if new_status == "Not Interested":
                remove_indices.append(row.name)
            else:
                df.at[row.name, 'status'] = new_status
            updated = True

if updated:
    # Remove movies marked as Not Interested
    if remove_indices:
        df = df.drop(remove_indices)
    df.to_csv(db_utils.CSV_FILE, index=False)
    st.success("Watchlist updated!")
    st.session_state['refresh_watchlist'] = True # Flag to refresh after status update
    st.rerun() # Trigger rerun to apply changes and refresh df

# --- AI Chat about Watchlist ---
st.header("Ask About Your Watchlist (AI Chat)")

def ask_ai():
    answer = ai_utils.chat_about_watchlist(st.session_state['user_query'], df)
    st.session_state['ai_answer'] = answer

user_query = st.text_input("Ask a question (e.g., What sci-fi movies have I seen?)", key='user_query', on_change=ask_ai)
if 'ai_answer' in st.session_state:
    st.info(st.session_state['ai_answer'])