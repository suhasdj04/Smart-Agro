import api from './axios';

// Queries
export const getAllQueries = (params) => api.get('/api/expert/queries', { params });
export const getQuery = (id) => api.get(`/api/expert/queries/${id}`);
export const answerQuery = (id, data) => api.post(`/api/expert/queries/${id}/answer`, data);
export const closeQuery = (id) => api.put(`/api/expert/queries/${id}/close`);

// Farmer Profiles
export const getFarmers = (params) => api.get('/api/expert/farmers', { params });
export const getFarmerDetail = (id) => api.get(`/api/expert/farmers/${id}`);
export const getFarmerCrops = (id) => api.get(`/api/expert/farmers/${id}/crops`);

// Expert Dashboard
export const getExpertDashboard = () => api.get('/api/expert/dashboard');
export const getExpertStats = () => api.get('/api/expert/stats');
