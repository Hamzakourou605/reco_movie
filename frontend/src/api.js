import axios from 'axios';

const getApiUrl = () => {
  let url = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000/api';
  
  // Si on est sur Render et que l'URL ne contient pas de protocole, on ajoute https://
  if (url && !url.startsWith('http')) {
    url = `https://${url}`;
  }
  
  // S'assure que l'URL se termine par /api pour correspondre aux routes Flask
  if (url && !url.endsWith('/api') && !url.includes('/api/')) {
    url = `${url.replace(/\/$/, '')}/api`;
  }
  
  // Supprime le slash final s'il existe (pour éviter // dans axios)
  url = url.replace(/\/$/, '');
  
  console.log('📡 Base API URL:', url);
  return url;
};

const api = axios.create({
  baseURL: getApiUrl(),
});

export const getTopFilms = async (n = 20) => {
  const response = await api.get(`/top-films?n=${n}`);
  return response.data;
};

export const getGenres = async () => {
  const response = await api.get('/genres');
  return response.data;
};

export const getFilmsByGenre = async (genre, n = 20) => {
  const response = await api.get(`/films/genre/${genre}?n=${n}`);
  return response.data;
};

export const getRecommendations = async (userId, n_recommendations = 10) => {
  const response = await api.post('/recommandations', { user_id: parseInt(userId), n_recommendations });
  return response.data;
};

export const getRecommendationsByTitle = async (title) => {
  const response = await api.get(`/recommend/${title}`);
  return response.data;
};

export const getAdminStats = async () => {
  const response = await api.get('/admin/stats');
  return response.data;
};

export default api;
