import api from './axios';

// Loan Applications
export const getLoanApplications = (params) => api.get('/api/bank/loans', { params });
export const getLoanApplication = (id) => api.get(`/api/bank/loans/${id}`);
export const approveLoan = (id, data) => api.put(`/api/bank/loans/${id}/approve`, data);
export const rejectLoan = (id, data) => api.put(`/api/bank/loans/${id}/reject`, data);
export const disburseLoan = (id, data) => api.put(`/api/bank/loans/${id}/disburse`, data);

// Reports
export const getLoanReports = (params) => api.get('/api/bank/reports', { params });
export const getLoanStats = () => api.get('/api/bank/stats');

// Bank Dashboard
export const getBankDashboard = () => api.get('/api/bank/dashboard');
