import api from './axios';

// Crop Recommendation
export const getCropRecommendation = (data) => api.post('/api/ai/crop-recommendation', data);

// Disease Detection — uses FormData (file upload)
export const detectDisease = (formData) =>
  api.post('/api/ai/disease-detection', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

// Yield Prediction
export const predictYield = (data) => api.post('/api/ai/yield-prediction', data);

// Fertilizer Recommendation
export const getFertilizerRecommendation = (data) =>
  api.post('/api/ai/fertilizer-recommendation', data);
