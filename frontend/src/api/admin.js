import api from './axios';

// Users
export const getUsers = (params) => api.get('/api/admin/users', { params });
export const getUser = (id) => api.get(`/api/admin/users/${id}`);
export const createUser = (data) => api.post('/api/admin/users', data);
export const updateUser = (id, data) => api.put(`/api/admin/users/${id}`, data);
export const deleteUser = (id) => api.delete(`/api/admin/users/${id}`);
export const toggleUserStatus = (id) => api.put(`/api/admin/users/${id}/toggle`);

// Crop Prices
export const getCropPrices = (params) => api.get('/api/admin/crop-prices', { params });
export const createCropPrice = (data) => api.post('/api/admin/crop-prices', data);
export const updateCropPrice = (id, data) => api.put(`/api/admin/crop-prices/${id}`, data);
export const deleteCropPrice = (id) => api.delete(`/api/admin/crop-prices/${id}`);

// Complaints
export const getAllComplaints = (params) => api.get('/api/admin/complaints', { params });
export const getComplaint = (id) => api.get(`/api/admin/complaints/${id}`);
export const replyComplaint = (id, data) => api.put(`/api/admin/complaints/${id}/reply`, data);
export const updateComplaintStatus = (id, data) =>
  api.put(`/api/admin/complaints/${id}/status`, data);

// Reports
export const getAdminReports = (params) => api.get('/api/admin/reports', { params });
export const getSystemStats = () => api.get('/api/admin/stats');

// Admin Dashboard
export const getAdminDashboard = () => api.get('/api/admin/dashboard');
