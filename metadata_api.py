import requests

OMDB_API_KEY = 'f10432b'  # Replace with your OMDb API key
OMDB_URL = 'http://www.omdbapi.com/'

def fetch_metadata(title):
    params = {
        't': title,
        'apikey': OMDB_API_KEY
    }
    response = requests.get(OMDB_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('Response') == 'True':
            return {
                'title': data.get('Title', title),
                'type': 'Movie' if data.get('Type') == 'movie' else 'TV Show',
                'genre': data.get('Genre', ''),
                'year': data.get('Year', ''),
                'description': data.get('Plot', ''),
                'cast': data.get('Actors', ''),
                'runtime': data.get('Runtime', ''),
                'imdb_rating': data.get('imdbRating', '')
            }
    return None 