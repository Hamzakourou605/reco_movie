"""
MyTflix - API Flask de recommandation de films
Posters TMDB charges en arriere-plan, recommandations optimisees
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
import threading
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import requests as req

load_dotenv()

from ml_model import MovieRecommender

TMDB_API_KEY = "e5c934fe24429749beb4d1f4724bb2ee"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

app = Flask(__name__)
CORS(app)

recommender = None
poster_cache = {}        # movieId -> full poster URL
links_dict = {}          # movieId -> tmdbId
cache_ready = False

# ------------------------------------------------------------------ #
# TMDB : construction du cache en arrière-plan
# ------------------------------------------------------------------ #

def fetch_poster_path(tmdb_id):
    try:
        r = req.get(
            f"https://api.themoviedb.org/3/movie/{int(tmdb_id)}",
            params={"api_key": TMDB_API_KEY},
            timeout=5
        )
        if r.status_code == 200:
            path = r.json().get("poster_path")
            if path:
                return TMDB_IMAGE_BASE + path
    except Exception:
        pass
    return None


def build_poster_cache_thread():
    """Lance le telechargement du cache posters en fond."""
    global cache_ready
    total = len(links_dict)
    print(f"[BG] Construction du cache TMDB ({total} films)...")
    count = 0
    for movie_id, tmdb_id in links_dict.items():
        if movie_id not in poster_cache:
            url = fetch_poster_path(tmdb_id)
            if url:
                poster_cache[movie_id] = url
        count += 1
        if count % 500 == 0:
            print(f"[BG] {count}/{total} posters en cache...")
    cache_ready = True
    print(f"[BG] Cache TMDB termine: {len(poster_cache)} images")


def get_poster(movie_id):
    mid = int(movie_id)
    if mid in poster_cache:
        return poster_cache[mid]
    # Réponse rapide si pas encore en cache : on tente une fois, sinon null
    tmdb_id = links_dict.get(mid)
    if not tmdb_id:
        return None
    url = fetch_poster_path(tmdb_id)
    if url:
        poster_cache[mid] = url
    return url


def movie_to_dict(m, extra=None):
    mid = int(m['movieId'])
    d = {
        "movieId": mid,
        "title": str(m['title']),
        "genres": str(m['genres']),
        "avg_rating": round(float(m.get('avg_rating', 0) or 0), 2),
        "rating_count": int(m.get('rating_count', 0) or 0),
        "poster_url": poster_cache.get(mid)   # Cache seulement, pas de blocage
    }
    if extra:
        for f in extra:
            if f in m:
                try:
                    d[f] = round(float(m[f]), 4)
                except Exception:
                    pass
    return d

# ------------------------------------------------------------------ #
# INIT
# ------------------------------------------------------------------ #

def init_recommender():
    global recommender
    print("[*] Chargement du modele ML...")
    model_path = 'recommender_model.pkl'
    if not Path(model_path).exists():
        print("[*] Entrainement du modele...")
        recommender = MovieRecommender()
        recommender.train()
        recommender.save(model_path)
        print("[OK] Modele entraine et sauvegarde!")
    else:
        recommender = MovieRecommender.load(model_path)
        print("[OK] Modele charge!")


def load_links():
    global links_dict
    try:
        df = pd.read_csv('links.csv')[['movieId', 'tmdbId']].dropna()
        df['tmdbId'] = df['tmdbId'].astype(int)
        links_dict = dict(zip(df['movieId'].astype(int), df['tmdbId']))
        print(f"[OK] {len(links_dict)} liens TMDB charges")
    except Exception as e:
        print(f"[WARN] links.csv non charge: {e}")


with app.app_context():
    print("\n" + "="*50)
    print("DEMARRAGE DU SERVEUR MYTFLIX")
    print("="*50)
    init_recommender()
    load_links()
    
    if recommender and recommender.movies is not None:
        print(f"[OK] Backend prêt avec {len(recommender.movies)} films")
    
    # Lancer le cache TMDB en arrière-plan - ne bloque pas le serveur
    t = threading.Thread(target=build_poster_cache_thread, daemon=True)
    t.start()
    print("="*50 + "\n")

# ------------------------------------------------------------------ #
# ROUTES
# ------------------------------------------------------------------ #

@app.route("/", methods=["GET"])
def read_root():
    return jsonify({
        "message": "MyTflix API Flask",
        "status": "online" if recommender is not None else "initializing",
        "poster_cache_size": len(poster_cache),
        "poster_cache_ready": cache_ready
    })

@app.route("/health", methods=["GET"])
def health_check():
    if recommender is None:
        return jsonify({"status": "initializing"}), 503
    return jsonify({"status": "healthy", "poster_cache_size": len(poster_cache)})

@app.route("/api/top-films", methods=["GET"])
@app.route("/top-films", methods=["GET"])
def get_top_films():
    n    = request.args.get('n', default=20, type=int)
    skip = request.args.get('skip', default=0, type=int)
    if recommender is None:
        return jsonify({"error": "Modele non charge"}), 503
    try:
        top = recommender.get_top_movies(n=n + skip)
        return jsonify([movie_to_dict(m) for _, m in top.iloc[skip:skip+n].iterrows()])
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/films/genre/<string:genre>", methods=["GET"])
@app.route("/films/genre/<string:genre>", methods=["GET"])
def get_films_by_genre(genre):
    n = request.args.get('n', default=20, type=int)
    if recommender is None:
        return jsonify({"error": "Modele non charge"}), 503
    try:
        movies = recommender.get_movies_by_genre(genre, n=n)
        return jsonify([movie_to_dict(m) for _, m in movies.iterrows()])
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/recommandations", methods=["POST"])
@app.route("/recommandations", methods=["POST"])
def get_recommendations():
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({"error": "user_id requis"}), 400

    user_id = int(data['user_id'])
    n       = int(data.get('n_recommendations', 12))

    if recommender is None:
        return jsonify({"error": "Modele non charge"}), 503
    try:
        recs = recommender.get_recommendations_by_ratings(user_id, n=n)
        if recs.empty:
            return jsonify({"error": f"Aucune donnee pour l'utilisateur {user_id}. Essayez un ID entre 1 et 610."}), 404
        return jsonify([movie_to_dict(m) for _, m in recs.iterrows()])
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/genres", methods=["GET"])
@app.route("/genres", methods=["GET"])
def get_all_genres():
    if recommender is None:
        return jsonify({"error": "Modele non charge"}), 503
    try:
        genres = recommender.get_all_genres()
        return jsonify({"genres": genres, "total": len(genres)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/recommend/<string:movie_title>", methods=["GET"])
@app.route("/recommend/<string:movie_title>", methods=["GET"])
def recommend_by_title(movie_title):
    n = request.args.get('n', default=10, type=int)
    if recommender is None:
        return jsonify({"error": "Modele non charge"}), 503
    try:
        match = recommender.movies[
            recommender.movies['title'].str.contains(movie_title, case=False, na=False)
        ]
        if match.empty:
            return jsonify({"error": f"Film non trouve: {movie_title}"}), 404
        movie_id = int(match.iloc[0]['movieId'])
        recs = recommender.get_recommendations_by_genres(movie_id, n=n)
        return jsonify([movie_to_dict(m, extra=['similarity_score']) for _, m in recs.iterrows()])
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)