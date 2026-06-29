import api from './axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export default api;
export { default as api } from './axios';
