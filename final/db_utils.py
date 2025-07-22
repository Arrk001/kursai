import pandas as pd
import os

CSV_FILE = os.path.join(os.path.dirname(__file__), 'media.csv')

# Read the CSV into a DataFrame
def read_watchlist():
    try:
        return pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=['title', 'type', 'genre', 'year', 'imdb_rating', 'poster_url', 'runtime', 'status', 'tmdb_id'])

# Add a new entry
def add_entry(title, type_, genre, year, status, imdb_rating='', poster_url='', runtime='', tmdb_id=''):
    df = read_watchlist()
    new_row = {'title': title, 'type': type_, 'genre': genre, 'year': year, 'imdb_rating': imdb_rating, 'poster_url': poster_url, 'runtime': runtime, 'status': status, 'tmdb_id': tmdb_id}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# Update an entry by title
def update_entry(title, **kwargs):
    df = read_watchlist()
    idx = df[df['title'].str.lower() == title.lower()].index
    for key, value in kwargs.items():
        if key in df.columns:
            df.loc[idx, key] = value
    df.to_csv(CSV_FILE, index=False)

# Query entries with a filter (returns DataFrame)
def query_entries(query_func):
    df = read_watchlist()
    return df[query_func(df)] 