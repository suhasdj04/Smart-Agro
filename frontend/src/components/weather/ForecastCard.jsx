import React from 'react';
import { Card, CardContent, Box, Typography } from '@mui/material';
import WbSunnyIcon from '@mui/icons-material/WbSunny';
import CloudIcon from '@mui/icons-material/Cloud';
import ThunderstormIcon from '@mui/icons-material/Thunderstorm';
import AcUnitIcon from '@mui/icons-material/AcUnit';
import WaterDropIcon from '@mui/icons-material/WaterDrop';

const getWeatherIcon = (condition, size = 28) => {
  const c = (condition || '').toLowerCase();
  if (c.includes('rain') || c.includes('drizzle')) return <WaterDropIcon sx={{ fontSize: size, color: '#29B6F6' }} />;
  if (c.includes('snow')) return <AcUnitIcon sx={{ fontSize: size, color: '#90CAF9' }} />;
  if (c.includes('thunder') || c.includes('storm')) return <ThunderstormIcon sx={{ fontSize: size, color: '#7E57C2' }} />;
  if (c.includes('cloud')) return <CloudIcon sx={{ fontSize: size, color: '#90A4AE' }} />;
  return <WbSunnyIcon sx={{ fontSize: size, color: '#FFA726' }} />;
};

const ForecastCard = ({ forecast }) => {
  if (!forecast) return null;

  const formatDay = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-IN', { weekday: 'short', day: '2-digit', month: 'short' });
  };

  return (
    <Card
      className="hover-card"
      sx={{
        textAlign: 'center',
        background: 'linear-gradient(135deg, rgba(46,125,50,0.08), rgba(21,101,192,0.06))',
        border: '1px solid',
        borderColor: 'divider',
        flex: 1,
        minWidth: 100,
      }}
    >
      <CardContent sx={{ p: 1.5 }}>
        <Typography variant="caption" fontWeight={600} color="text.secondary" display="block" gutterBottom>
          {formatDay(forecast.date || forecast.dt_txt)}
        </Typography>
        <Box sx={{ my: 1 }}>
          {getWeatherIcon(forecast.description)}
        </Box>
        <Typography variant="body2" fontWeight={700} color="text.primary">
          {Math.round(forecast.temp_max || forecast.tempMax)}°
        </Typography>
        <Typography variant="caption" color="text.secondary">
          {Math.round(forecast.temp_min || forecast.tempMin)}°
        </Typography>
        <Typography variant="caption" color="text.disabled" display="block" sx={{ mt: 0.5, fontSize: '0.65rem', textTransform: 'capitalize' }}>
          {forecast.description}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default ForecastCard;
