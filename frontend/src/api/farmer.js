import api from './axios';

// Crops
export const getCrops = (params) => api.get('/api/farmer/crops', { params });
export const getCrop = (id) => api.get(`/api/farmer/crops/${id}`);
export const createCrop = (data) => api.post('/api/farmer/crops', data);
export const updateCrop = (id, data) => api.put(`/api/farmer/crops/${id}`, data);
export const deleteCrop = (id) => api.delete(`/api/farmer/crops/${id}`);
export const uploadCropImage = (id, formData) =>
  api.post(`/api/farmer/crops/${id}/image`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

// Loans
export const getMyLoans = (params) => api.get('/api/farmer/loans', { params });
export const applyLoan = (data) => api.post('/api/farmer/loans', data);
export const getLoan = (id) => api.get(`/api/farmer/loans/${id}`);

// Complaints
export const getComplaints = (params) => api.get('/api/farmer/complaints', { params });
export const createComplaint = (data) => api.post('/api/farmer/complaints', data);
export const getComplaint = (id) => api.get(`/api/farmer/complaints/${id}`);

// Queries
export const getQueries = (params) => api.get('/api/farmer/queries', { params });
export const createQuery = (data) => api.post('/api/farmer/queries', data);
export const getQuery = (id) => api.get(`/api/farmer/queries/${id}`);

// Farmer Profile
export const getFarmerProfile = () => api.get('/api/farmer/profile');
export const updateFarmerProfile = (data) => api.put('/api/farmer/profile', data);

// Dashboard Stats
export const getFarmerDashboard = () => api.get('/api/farmer/dashboard');
