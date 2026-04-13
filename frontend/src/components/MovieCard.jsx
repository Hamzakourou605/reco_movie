import React, { useState } from 'react';
import { Star, Film } from 'lucide-react';

const MovieCard = ({ movie }) => {
  const [imgError, setImgError] = useState(false);

  const formatRating = (rating) =>
    rating ? parseFloat(rating).toFixed(1) : 'N/A';

  const genres = movie.genres ? movie.genres.split('|').slice(0, 3) : [];

  return (
    <div className="movie-card glass animate-fade-in">
      {/* Poster */}
      <div style={{ width: '100%', height: '380px', overflow: 'hidden', borderRadius: '16px 16px 0 0', background: '#1e222b' }}>
        {movie.poster_url && !imgError ? (
          <img
            src={movie.poster_url}
            alt={movie.title}
            onError={() => setImgError(true)}
            style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
          />
        ) : (
          <div className="placeholder-poster" style={{ height: '100%' }}>
            <Film size={56} color="rgba(255,255,255,0.15)" />
            <span style={{ color: 'rgba(255,255,255,0.3)', fontSize: '0.85rem', padding: '0 1rem', textAlign: 'center' }}>
              {movie.title}
            </span>
          </div>
        )}
      </div>

      {/* Infos */}
      <div className="movie-card-content">
        <h3 className="movie-card-title">{movie.title}</h3>

        <div className="movie-card-genres">
          {genres.map(g => (
            <span key={g} className="genre-tag">{g}</span>
          ))}
        </div>

        <div className="movie-card-footer">
          <div className="rating-badge">
            <Star size={16} fill="#fbbf24" color="#fbbf24" />
            <span>{formatRating(movie.avg_rating)}</span>
          </div>
          {movie.rating_count > 0 ? (
            <span className="rating-count">({movie.rating_count} avis)</span>
          ) : movie.similarity_score ? (
            <span className="rating-count">Similaire à {(movie.similarity_score * 100).toFixed(0)}%</span>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default MovieCard;
