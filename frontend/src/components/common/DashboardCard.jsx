import React from 'react';
import {
  Card,
  CardContent,
  Box,
  Typography,
  Avatar,
  Chip,
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import TrendingFlatIcon from '@mui/icons-material/TrendingFlat';

const DashboardCard = ({
  title,
  value,
  icon,
  color = '#2E7D32',
  trend,
  trendValue,
  subtitle,
  gradient,
}) => {
  const getTrendIcon = () => {
    if (trend === 'up') return <TrendingUpIcon sx={{ fontSize: 14 }} />;
    if (trend === 'down') return <TrendingDownIcon sx={{ fontSize: 14 }} />;
    return <TrendingFlatIcon sx={{ fontSize: 14 }} />;
  };

  const getTrendColor = () => {
    if (trend === 'up') return '#4CAF50';
    if (trend === 'down') return '#f44336';
    return '#9E9E9E';
  };

  const bgGradient =
    gradient ||
    `linear-gradient(135deg, ${color}15 0%, ${color}08 100%)`;

  return (
    <Card
      className="hover-card"
      sx={{
        height: '100%',
        background: bgGradient,
        border: `1px solid ${color}25`,
        position: 'relative',
        overflow: 'hidden',
        '&::before': {
          content: '""',
          position: 'absolute',
          top: -20,
          right: -20,
          width: 100,
          height: 100,
          borderRadius: '50%',
          background: `${color}12`,
        },
        '&::after': {
          content: '""',
          position: 'absolute',
          bottom: -30,
          right: 20,
          width: 60,
          height: 60,
          borderRadius: '50%',
          background: `${color}08`,
        },
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
          <Box>
            <Typography
              variant="body2"
              sx={{ color: 'text.secondary', fontWeight: 500, mb: 1, fontSize: '0.8rem' }}
            >
              {title}
            </Typography>
            <Typography
              variant="h4"
              sx={{ fontWeight: 800, color: 'text.primary', lineHeight: 1.2 }}
            >
              {value}
            </Typography>
            {subtitle && (
              <Typography variant="caption" sx={{ color: 'text.secondary', mt: 0.5, display: 'block' }}>
                {subtitle}
              </Typography>
            )}
            {trendValue && (
              <Box
                sx={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 0.5,
                  mt: 1,
                  px: 1,
                  py: 0.3,
                  borderRadius: 2,
                  bgcolor: `${getTrendColor()}18`,
                  color: getTrendColor(),
                }}
              >
                {getTrendIcon()}
                <Typography variant="caption" sx={{ fontWeight: 700, fontSize: '0.7rem' }}>
                  {trendValue}
                </Typography>
              </Box>
            )}
          </Box>
          <Avatar
            sx={{
              bgcolor: `${color}20`,
              width: 52,
              height: 52,
              color: color,
              boxShadow: `0 4px 12px ${color}30`,
            }}
          >
            {icon}
          </Avatar>
        </Box>
      </CardContent>
    </Card>
  );
};

export default DashboardCard;
