import requests
import os
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
OMDB_API_KEY = os.getenv('OMDB_API_KEY')
TMDB_URL = 'https://api.themoviedb.org/3'
OMDB_URL = 'http://www.omdbapi.com/'

# TMDb genre ID to name mapping
TMDB_GENRE_MAP = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western"
}

# Helper: Search for a movie and get its TMDb ID
def search_movie(title, year=None):
    params = {
        'api_key': TMDB_API_KEY,
        'query': title,
        'language': 'en-US',
    }
    if year:
        params['year'] = year
    response = requests.get(f'{TMDB_URL}/search/movie', params=params)
    data = response.json()
    results = data.get('results', [])
    if results:
        return results[0]  # Return the first match
    return None

# Helper: Get IMDb ID from TMDb movie ID
def get_imdb_id(tmdb_id):
    params = {
        'api_key': TMDB_API_KEY,
    }
    response = requests.get(f'{TMDB_URL}/movie/{tmdb_id}/external_ids', params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('imdb_id')
    return None

# Helper: Get IMDb rating from OMDb
def get_imdb_rating(imdb_id):
    params = {
        'apikey': OMDB_API_KEY,
        'i': imdb_id
    }
    response = requests.get(OMDB_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        rating = data.get('imdbRating')
        if rating and rating != 'N/A':
            return rating
    return None

def fetch_metadata(title, year=None):
    movie = search_movie(title, year)
    if not movie:
        return None
    imdb_rating = ''
    tmdb_vote = movie.get('vote_average', '')
    tmdb_id = movie.get('id')
    imdb_id = get_imdb_id(tmdb_id) if tmdb_id else None
    if imdb_id and OMDB_API_KEY:
        imdb_rating = get_imdb_rating(imdb_id)
    if not imdb_rating:
        imdb_rating = tmdb_vote
    # Map genre IDs to names
    genre_names = ', '.join([TMDB_GENRE_MAP.get(g, str(g)) for g in movie.get('genre_ids', [])])
    # Build poster URL
    poster_path = movie.get('poster_path')
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""
    # Fetch runtime from TMDb movie details endpoint
    runtime = ''
    if tmdb_id:
        params = {'api_key': TMDB_API_KEY, 'language': 'en-US'}
        details_resp = requests.get(f'{TMDB_URL}/movie/{tmdb_id}', params=params)
        if details_resp.status_code == 200:
            details = details_resp.json()
            runtime = details.get('runtime', '')
    return {
        'title': movie.get('title', title),
        'type': 'Movie',
        'genre': genre_names,
        'year': movie.get('release_date', '')[:4],
        'imdb_rating': imdb_rating,
        'poster_url': poster_url,
        'runtime': runtime,
        'tmdb_id': tmdb_id
    }

def fetch_recommendations_movies(title, n=5):
    movie = search_movie(title)
    if not movie:
        return []
    movie_id = movie['id']
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US',
        'page': 1
    }
    response = requests.get(f'{TMDB_URL}/movie/{movie_id}/recommendations', params=params)
    data = response.json()
    results = data.get('results', [])
    results = sorted(results, key=lambda m: (m.get('popularity', 0), m.get('vote_average', 0)), reverse=True)
    return [m['title'] for m in results[:n]]

def fetch_similar_movies(title, n=5):
    # Try recommendations endpoint first
    recs = fetch_recommendations_movies(title, n)
    if recs:
        return recs
    # Fallback to similar endpoint
    movie = search_movie(title)
    if not movie:
        return []
    movie_id = movie['id']
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US',
        'page': 1
    }
    response = requests.get(f'{TMDB_URL}/movie/{movie_id}/similar', params=params)
    data = response.json()
    results = data.get('results', [])
    results = sorted(results, key=lambda m: (m.get('popularity', 0), m.get('vote_average', 0)), reverse=True)
    return [m['title'] for m in results[:n]] 