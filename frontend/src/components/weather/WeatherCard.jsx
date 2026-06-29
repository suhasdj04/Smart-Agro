import React from 'react';
import { Card, CardContent, Box, Typography, Avatar, Divider, Grid } from '@mui/material';
import WbSunnyIcon from '@mui/icons-material/WbSunny';
import CloudIcon from '@mui/icons-material/Cloud';
import ThunderstormIcon from '@mui/icons-material/Thunderstorm';
import AcUnitIcon from '@mui/icons-material/AcUnit';
import WaterDropIcon from '@mui/icons-material/WaterDrop';
import AirIcon from '@mui/icons-material/Air';
import CompressIcon from '@mui/icons-material/Compress';
import ThermostatIcon from '@mui/icons-material/Thermostat';
import VisibilityIcon from '@mui/icons-material/Visibility';

const getWeatherIcon = (condition, size = 48) => {
  const c = (condition || '').toLowerCase();
  if (c.includes('rain') || c.includes('drizzle')) return <WaterDropIcon sx={{ fontSize: size, color: '#29B6F6' }} />;
  if (c.includes('snow')) return <AcUnitIcon sx={{ fontSize: size, color: '#90CAF9' }} />;
  if (c.includes('thunder') || c.includes('storm')) return <ThunderstormIcon sx={{ fontSize: size, color: '#7E57C2' }} />;
  if (c.includes('cloud')) return <CloudIcon sx={{ fontSize: size, color: '#90A4AE' }} />;
  return <WbSunnyIcon sx={{ fontSize: size, color: '#FFA726' }} />;
};

const WeatherCard = ({ weather }) => {
  if (!weather) return null;

  const bgGradient = (() => {
    const c = (weather.description || '').toLowerCase();
    if (c.includes('rain')) return 'linear-gradient(135deg, #1565C0, #0D47A1)';
    if (c.includes('cloud')) return 'linear-gradient(135deg, #546E7A, #37474F)';
    if (c.includes('thunder')) return 'linear-gradient(135deg, #4A148C, #6A1B9A)';
    return 'linear-gradient(135deg, #1B5E20, #2E7D32)';
  })();

  return (
    <Card
      sx={{
        background: bgGradient,
        color: '#fff',
        borderRadius: 3,
        overflow: 'hidden',
        position: 'relative',
      }}
    >
      <Box
        sx={{
          position: 'absolute',
          top: -30,
          right: -30,
          width: 160,
          height: 160,
          borderRadius: '50%',
          bgcolor: 'rgba(255,255,255,0.06)',
        }}
      />
      <CardContent sx={{ p: 3, position: 'relative', zIndex: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Box>
            <Typography variant="h6" fontWeight={700} sx={{ opacity: 0.9 }}>
              {weather.city || weather.name}
            </Typography>
            <Typography variant="caption" sx={{ opacity: 0.7 }}>
              {weather.country || ''}
            </Typography>
          </Box>
          {getWeatherIcon(weather.description)}
        </Box>

        <Box sx={{ mb: 2 }}>
          <Typography variant="h2" fontWeight={800} sx={{ lineHeight: 1 }}>
            {Math.round(weather.temperature || weather.temp)}°C
          </Typography>
          <Typography variant="body1" sx={{ opacity: 0.85, textTransform: 'capitalize', mt: 0.5 }}>
            {weather.description}
          </Typography>
          <Typography variant="body2" sx={{ opacity: 0.7 }}>
            Feels like {Math.round(weather.feels_like || weather.feelsLike)}°C
          </Typography>
        </Box>

        <Divider sx={{ bgcolor: 'rgba(255,255,255,0.2)', mb: 2 }} />

        <Grid container spacing={1.5}>
          <Grid item xs={4}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <WaterDropIcon sx={{ fontSize: 16, opacity: 0.8 }} />
              <Box>
                <Typography variant="caption" sx={{ opacity: 0.7, display: 'block' }}>Humidity</Typography>
                <Typography variant="body2" fontWeight={600}>{weather.humidity}%</Typography>
              </Box>
            </Box>
          </Grid>
          <Grid item xs={4}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <AirIcon sx={{ fontSize: 16, opacity: 0.8 }} />
              <Box>
                <Typography variant="caption" sx={{ opacity: 0.7, display: 'block' }}>Wind</Typography>
                <Typography variant="body2" fontWeight={600}>{weather.wind_speed || weather.windSpeed} km/h</Typography>
              </Box>
            </Box>
          </Grid>
          <Grid item xs={4}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <CompressIcon sx={{ fontSize: 16, opacity: 0.8 }} />
              <Box>
                <Typography variant="caption" sx={{ opacity: 0.7, display: 'block' }}>Pressure</Typography>
                <Typography variant="body2" fontWeight={600}>{weather.pressure} hPa</Typography>
              </Box>
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default WeatherCard;
