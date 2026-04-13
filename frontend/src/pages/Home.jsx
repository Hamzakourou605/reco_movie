import React, { useEffect, useState } from 'react';
import { getTopFilms, getGenres, getFilmsByGenre } from '../api';
import MovieCard from '../components/MovieCard';

const Home = () => {
  const [movies, setMovies] = useState([]);
  const [genres, setGenres] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeGenre, setActiveGenre] = useState('');

  useEffect(() => {
    fetchGenres();
    fetchTopMovies();
  }, []);

  const fetchGenres = async () => {
    try {
      const data = await getGenres();
      setGenres(data.genres || []);
    } catch (e) {
      console.error(e);
    }
  };

  const fetchTopMovies = async () => {
    setLoading(true);
    try {
      const data = await getTopFilms(24);
      setMovies(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleGenreSelect = async (genre) => {
    setActiveGenre(genre);
    setLoading(true);
    try {
      if (genre) {
        const data = await getFilmsByGenre(genre, 24);
        setMovies(data);
      } else {
        fetchTopMovies();
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <h1 className="page-title">Films Populaires</h1>
      
      <div style={{ marginBottom: '2rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
        <button 
          className={`genre-tag ${!activeGenre ? 'active' : ''}`}
          style={{ background: !activeGenre ? 'var(--primary)' : 'rgba(255,255,255,0.05)', cursor: 'pointer', border: 'none', color: '#fff' }}
          onClick={() => handleGenreSelect('')}
        >
          Tous
        </button>
        {genres.slice(0, 15).map(g => (
          <button 
            key={g} 
            className={`genre-tag ${activeGenre === g ? 'active' : ''}`}
            style={{ background: activeGenre === g ? 'var(--primary)' : 'rgba(255,255,255,0.05)', cursor: 'pointer', border: 'none', color: '#fff' }}
            onClick={() => handleGenreSelect(g)}
          >
            {g}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="spinner"></div>
      ) : (
        <div className="movie-grid">
          {movies.map(m => (
            <MovieCard key={m.movieId} movie={m} />
          ))}
        </div>
      )}
    </div>
  );
};

export default Home;
