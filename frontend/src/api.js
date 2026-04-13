import axios from 'axios';

const getApiUrl = () => {
  let url = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000/api';
  // Supprime le slash final s'il existe
  url = url.replace(/\/$/, '');
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

export default api;
