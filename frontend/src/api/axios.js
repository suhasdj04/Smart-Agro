import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
});

// Request interceptor — add JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('smart_agro_token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor — handle 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('smart_agro_token');
      localStorage.removeItem('smart_agro_user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
