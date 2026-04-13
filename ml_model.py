"""
Module de Machine Learning pour les recommandations de films
Utilise la similarit collaborative et base sur le contenu
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
from pathlib import Path

class MovieRecommender:
    def __init__(self, data_dir='./'):
        self.data_dir = data_dir
        self.movies = None
        self.ratings = None
        self.tags = None
        self.movie_similarity = None
        self.user_item_matrix = None
        self.genre_similarity = None
        self.user_similarity = None  # Cache de similarite utilisateur
        
    def load_data(self):
        """Charge les donnes CSV"""
        print(" Chargement des donnes...")
        self.movies = pd.read_csv(os.path.join(self.data_dir, 'movies.csv'))
        self.ratings = pd.read_csv(os.path.join(self.data_dir, 'ratings.csv'))
        self.tags = pd.read_csv(os.path.join(self.data_dir, 'tags.csv'))
        print(f" {len(self.movies)} films chargs")
        print(f" {len(self.ratings)} valuations charges")
        print(f" {len(self.tags)} tags chargs")
        return self
    
    def build_user_item_matrix(self):
        """Cre la matrice utilisateur-film"""
        print(" Construction de la matrice utilisateur-film...")
        self.user_item_matrix = self.ratings.pivot_table(
            index='userId',
            columns='movieId',
            values='rating',
            fill_value=0
        )
        print(f" Matrice cre: {self.user_item_matrix.shape}")
        return self
    
    def build_genre_similarity(self):
        """Construit une matrice de similarit base sur les genres"""
        print(" Construction de la similarit des genres...")
        
        # Vectorise les genres
        vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 2))
        genre_vectors = vectorizer.fit_transform(self.movies['genres'].fillna(''))
        
        # Calcule la similarit cosinus
        self.genre_similarity = cosine_similarity(genre_vectors)
        print(f" Similarit des genres calcule")
        return self
    
    def calculate_user_similarity(self):
        """Calcule la similarite entre utilisateurs avec cosine_similarity (rapide)"""
        if self.user_similarity is not None:
            return self.user_similarity
        print("Calcul de la similarite utilisateur (cosine, rapide)...")
        # Normaliser la matrice utilisateur
        matrix = self.user_item_matrix.values  # numpy array
        # cosine_similarity retourne shape (n_users, n_users)
        sim_matrix = cosine_similarity(matrix)
        self.user_similarity = pd.DataFrame(
            sim_matrix,
            index=self.user_item_matrix.index,
            columns=self.user_item_matrix.index
        )
        print("[OK] Similarite utilisateur calculee et mise en cache")
        return self.user_similarity
    
    def get_recommendations_by_genres(self, movie_id, n=10):
        """Obtient les films recommands bass sur les genres similaires"""
        if movie_id not in self.movies['movieId'].values:
            return pd.DataFrame()
        
        movie_idx = self.movies[self.movies['movieId'] == movie_id].index[0]
        similarities = self.genre_similarity[movie_idx]
        similar_movies_idx = np.argsort(similarities)[::-1][1:n+1]
        
        recommended_movies = self.movies.iloc[similar_movies_idx][['movieId', 'title', 'genres']].copy()
        recommended_movies['similarity_score'] = similarities[similar_movies_idx]
        return recommended_movies
    
    def get_recommendations_by_ratings(self, user_id, n=10):
        """Obtient les films recommands bass sur les valuations des utilisateurs similaires"""
        if user_id not in self.user_item_matrix.index:
            return pd.DataFrame()
        
        # Calcule la similarit avec d'autres utilisateurs
        user_similarity = self.calculate_user_similarity()
        similar_users = user_similarity[user_id].sort_values(ascending=False)[1:11]
        
        # Films apprcis par des utilisateurs similaires
        recommendations = {}
        for similar_user_id, similarity_score in similar_users.items():
            # Films nots par l'utilisateur similaire
            rated_movies = self.ratings[self.ratings['userId'] == similar_user_id]
            high_rated = rated_movies[rated_movies['rating'] >= 4.0]
            
            for _, row in high_rated.iterrows():
                movie_id = row['movieId']
                # Ignorer les films dj nots par l'utilisateur
                if movie_id not in self.user_item_matrix.loc[user_id][self.user_item_matrix.loc[user_id] > 0].index:
                    if movie_id not in recommendations:
                        recommendations[movie_id] = 0
                    recommendations[movie_id] += similarity_score * row['rating']
        
        # Trier et retourner les top n
        top_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:n]
        movie_ids = [m[0] for m in top_recs]
        scores = [m[1] for m in top_recs]
        
        rec_movies = self.movies[self.movies['movieId'].isin(movie_ids)].copy()
        rec_movies['score'] = rec_movies['movieId'].map(dict(zip(movie_ids, scores)))
        return rec_movies.sort_values('score', ascending=False)
    
    def get_top_movies(self, n=20):
        """Obtient les films les mieux nots"""
        avg_ratings = self.ratings.groupby('movieId')['rating'].agg(['mean', 'count'])
        avg_ratings = avg_ratings[avg_ratings['count'] >= 5]  # Au moins 5 votes
        top_movies = avg_ratings.sort_values('mean', ascending=False).head(n).index.tolist()
        
        result = self.movies[self.movies['movieId'].isin(top_movies)].copy()
        result['avg_rating'] = result['movieId'].map(dict(zip(avg_ratings.index, avg_ratings['mean'])))
        result['rating_count'] = result['movieId'].map(dict(zip(avg_ratings.index, avg_ratings['count'])))
        return result.sort_values('avg_rating', ascending=False)
    
    def get_movies_by_genre(self, genre, n=20):
        """Obtient les films d'un genre donn"""
        genre_movies = self.movies[self.movies['genres'].str.contains(genre, case=False, na=False)]
        
        # Ajoute les notes moyennes
        avg_ratings = self.ratings.groupby('movieId')['rating'].agg(['mean', 'count'])
        avg_ratings = avg_ratings[avg_ratings['count'] >= 2]
        
        genre_movies = genre_movies[genre_movies['movieId'].isin(avg_ratings.index)].copy()
        genre_movies['avg_rating'] = genre_movies['movieId'].map(dict(zip(avg_ratings.index, avg_ratings['mean'])))
        genre_movies['rating_count'] = genre_movies['movieId'].map(dict(zip(avg_ratings.index, avg_ratings['count'])))
        
        return genre_movies.sort_values('avg_rating', ascending=False).head(n)
    
    def get_user_ratings(self, user_id, n=20):
        """Obtient les films valus par un utilisateur"""
        user_ratings = self.ratings[self.ratings['userId'] == user_id].sort_values('rating', ascending=False)
        user_movies = user_ratings.merge(self.movies, on='movieId')
        return user_movies[['movieId', 'title', 'genres', 'rating']].head(n)
    
    def get_all_genres(self):
        """Retourne la liste de tous les genres uniques"""
        all_genres = set()
        for genres_str in self.movies['genres'].dropna():
            if genres_str != '(no genres listed)':
                all_genres.update(genres_str.split('|'))
        return sorted(list(all_genres))
    
    def recommend_by_multiple_genres(self, genres, n=20):
        """
        Recommande des films bass sur une ou plusieurs genres
        
        Args:
            genres: list - Liste des genres (ex: ['Action', 'Adventure'])
            n: int - Nombre de films  recommander
            
        Returns:
            DataFrame avec les films recommands
        """
        if not genres or len(genres) == 0:
            return pd.DataFrame()
        
        # Filtrer les films qui contiennent au moins un des genres slectionns
        genre_filter = '|'.join(genres)
        matching_movies = self.movies[
            self.movies['genres'].str.contains(genre_filter, case=False, na=False)
        ].copy()
        
        if matching_movies.empty:
            return pd.DataFrame()
        
        # Ajouter les scores de popularit et de rating
        avg_ratings = self.ratings.groupby('movieId').agg({
            'rating': ['mean', 'count']
        }).reset_index()
        avg_ratings.columns = ['movieId', 'avg_rating', 'rating_count']
        
        # Merger avec les donnes de ratings
        result = matching_movies.merge(avg_ratings, on='movieId', how='left')
        result['avg_rating'] = result['avg_rating'].fillna(0)
        result['rating_count'] = result['rating_count'].fillna(0)
        
        # Filtrer les films avec au moins 1 valuation
        result = result[result['rating_count'] >= 1]
        
        # Calculer un score composite (70% rating, 30% popularit)
        max_count = result['rating_count'].max()
        result['popularity_score'] = (result['rating_count'] / max_count) if max_count > 0 else 0
        result['composite_score'] = (0.7 * result['avg_rating'] / 5.0) + (0.3 * result['popularity_score'])
        
        # Trier et retourner les top n
        return result.sort_values('composite_score', ascending=False).head(n)[
            ['movieId', 'title', 'genres', 'avg_rating', 'rating_count', 'composite_score']
        ]
    
    def get_genre_stats(self, genre):
        """
        Retourne les statistiques pour un genre donn
        
        Args:
            genre: str - Le genre
            
        Returns:
            dict avec les statistiques
        """
        genre_movies = self.movies[
            self.movies['genres'].str.contains(genre, case=False, na=False)
        ]
        
        if genre_movies.empty:
            return None
        
        # Obtenir les ratings pour ces films
        genre_ratings = self.ratings[
            self.ratings['movieId'].isin(genre_movies['movieId'])
        ]
        
        stats = {
            'genre': genre,
            'total_movies': len(genre_movies),
            'total_ratings': len(genre_ratings),
            'avg_rating': genre_ratings['rating'].mean() if len(genre_ratings) > 0 else 0,
            'median_rating': genre_ratings['rating'].median() if len(genre_ratings) > 0 else 0,
            'std_rating': genre_ratings['rating'].std() if len(genre_ratings) > 0 else 0,
        }
        return stats
    
    def train(self):
        """Entraine tous les modeles"""
        print("\n" + "="*60)
        print("ENTRAINEMENT DU MODELE DE RECOMMANDATION")
        print("="*60)
        
        self.load_data()
        self.build_user_item_matrix()
        self.build_genre_similarity()
        # Pre-calculer la similarite utilisateur au moment de l'entrainement
        self.calculate_user_similarity()
        
        print("\n[OK] Modele entraine avec succes!")
        print("="*60 + "\n")
        return self
    
    def save(self, path='model.pkl'):
        """Sauvegarde le modle"""
        with open(path, 'wb') as f:
            pickle.dump(self, f)
        print(f" Modle sauvegard: {path}")
    
    @staticmethod
    def load(path='model.pkl'):
        """Charge un modle sauvegard"""
        with open(path, 'rb') as f:
            return pickle.load(f)


if __name__ == '__main__':
    # Entrane et sauvegarde le modle
    recommender = MovieRecommender()
    recommender.train()
    recommender.save('recommender_model.pkl')
