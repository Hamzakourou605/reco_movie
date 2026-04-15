import React, { useState } from 'react';
import { getRecommendations, getRecommendationsByTitle } from '../api';
import MovieCard from '../components/MovieCard';
import AdminDashboard from '../components/AdminDashboard';
import { Search, AlertCircle, LayoutDashboard } from 'lucide-react';

const Recommend = () => {
  const [userId, setUserId] = useState('');
  const [movieTitle, setMovieTitle] = useState('');
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [mode, setMode] = useState('user');
  const [isAdmin, setIsAdmin] = useState(false);
  const [currentId, setCurrentId] = useState('');

  const handleRecommendUser = async (e) => {
    e.preventDefault();
    if (!userId) return;
    setLoading(true);
    setError('');
    setMovies([]);
    
    // Check if it's Admin (ID 0 or "admin" string)
    const isUserAdmin = userId.toString().toLowerCase() === 'admin' || userId === '0';
    const finalUserId = isUserAdmin ? '0' : userId;
    
    setIsAdmin(isUserAdmin);
    setCurrentId(finalUserId);
    
    try {
      // Si c'est l'admin, on ne récupère pas de recommandations de films
      if (isUserAdmin) {
        setMovies([]);
      } else {
        const data = await getRecommendations(finalUserId, 12);
        if (!Array.isArray(data) || data.length === 0) {
          setError("Aucune recommandation trouvée. Essayez un ID entre 1 et 610.");
        } else {
          setMovies(data);
        }
      }
    } catch (err) {
      const msg = err?.response?.data?.error || "Erreur serveur. Verifiez que l'ID est entre 1 et 610.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleRecommendTitle = async (e) => {
    e.preventDefault();
    if (!movieTitle) return;
    setLoading(true);
    setError('');
    setMovies([]);
    setIsAdmin(false);
    setCurrentId('');
    try {
      const data = await getRecommendationsByTitle(movieTitle);
      if (!Array.isArray(data) || data.length === 0) {
        setError("Aucun film similaire trouvé.");
      } else {
        setMovies(data);
      }
    } catch (err) {
      const msg = err?.response?.data?.error || "Film non trouvé. Essayez: 'Toy Story', 'Matrix', 'Titanic'...";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <h1 className="page-title">
        {isAdmin ? "Espace Administration" : "Recommandations Pour Vous"}
      </h1>

      {/* Mode Switch */}
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
        <button
          className="btn"
          style={{ background: mode === 'user' ? 'var(--primary)' : 'rgba(255,255,255,0.1)' }}
          onClick={() => { setMode('user'); setError(''); setMovies([]); setIsAdmin(false); }}
        >
          Par ID Utilisateur
        </button>
        <button
          className="btn"
          style={{ background: mode === 'title' ? 'var(--primary)' : 'rgba(255,255,255,0.1)' }}
          onClick={() => { setMode('title'); setError(''); setMovies([]); setIsAdmin(false); }}
        >
          Par Film Similaire
        </button>
      </div>

      {/* Form */}
      <div className="glass" style={{ padding: '2rem', maxWidth: '600px', marginBottom: '3rem' }}>
        {mode === 'user' ? (
          <form onSubmit={handleRecommendUser}>
            <div className="form-group">
              <label className="form-label">Votre ID Utilisateur (1-610) ou 'admin' pour le dashboard</label>
              <input
                type="text"
                className="form-input"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                placeholder="Ex: 1, 42, admin (ID 0)..."
                required
              />
            </div>
            <button type="submit" className="btn" disabled={loading}>
              <Search size={18} />
              {loading ? 'Connexion...' : (userId.toLowerCase() === 'admin' || userId === '0' ? 'Accéder au Dashboard' : 'Trouver des films')}
            </button>
          </form>
        ) : (
          <form onSubmit={handleRecommendTitle}>
            <div className="form-group">
              <label className="form-label">Titre d'un film que vous aimez</label>
              <input
                type="text"
                className="form-input"
                value={movieTitle}
                onChange={(e) => setMovieTitle(e.target.value)}
                placeholder="Ex: Toy Story, Matrix, Inception..."
                required
              />
            </div>
            <button type="submit" className="btn" disabled={loading}>
              <Search size={18} />
              {loading ? 'Recherche...' : 'Films similaires'}
            </button>
          </form>
        )}
      </div>

      {/* Error */}
      {error && (
        <div style={{
          display: 'flex', alignItems: 'center', gap: '0.75rem',
          background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239,68,68,0.3)',
          borderRadius: '12px', padding: '1rem 1.5rem', marginBottom: '2rem', color: '#f87171'
        }}>
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {/* Results */}
      {loading ? (
        <div style={{ textAlign: 'center', paddingTop: '4rem' }}>
          <div className="spinner"></div>
          <p style={{ color: 'var(--text-muted)', marginTop: '1rem' }}>
            {isAdmin ? "Chargement du Dashboard..." : "Calcul des recommandations..."}
          </p>
        </div>
      ) : (
        <>
          {isAdmin ? (
            <AdminDashboard />
          ) : (
            <div className="movie-grid">
              {movies.map(m => (
                <MovieCard key={m.movieId} movie={m} />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Recommend;
