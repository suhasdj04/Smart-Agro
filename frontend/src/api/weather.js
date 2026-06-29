import api from './axios';

export const getCurrentWeather = (city) =>
  api.get('/api/weather/current', { params: { city } });
export const getForecast = (city) =>
  api.get('/api/weather/forecast', { params: { city } });
export const getWeatherByCoords = (lat, lon) =>
  api.get('/api/weather/current', { params: { lat, lon } });

// Public crop prices
export const getCropPricesPublic = (params) => api.get('/api/prices', { params });
