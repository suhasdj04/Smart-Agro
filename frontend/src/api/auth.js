import api from './axios';

export const register = (data) => api.post('/api/auth/register', data);
export const login = (data) => api.post('/api/auth/login', data);
export const logout = () => api.post('/api/auth/logout');
export const getMe = () => api.get('/api/auth/me');
export const changePassword = (data) => api.put('/api/auth/me/password', data);
export const updateProfile = (data) => api.put('/api/auth/me', data);
export const uploadProfileImage = (formData) =>
  api.post('/api/auth/me/avatar', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
