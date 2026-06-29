import React from 'react';
import {
  Box,
  Typography,
  Button,
  Container,
  Grid,
  Card,
  CardContent,
  Avatar,
  Chip,
  useTheme,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import AgricultureIcon from '@mui/icons-material/Agriculture';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import WbSunnyIcon from '@mui/icons-material/WbSunny';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import GrassIcon from '@mui/icons-material/Grass';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import VerifiedIcon from '@mui/icons-material/Verified';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';

const features = [
  {
    icon: <GrassIcon sx={{ fontSize: 32 }} />,
    title: 'Crop Management',
    description: 'Track and manage all your crops with real-time updates on growth, health, and harvest schedules.',
    color: '#2E7D32',
  },
  {
    icon: <SmartToyIcon sx={{ fontSize: 32 }} />,
    title: 'AI Prediction',
    description: 'Get intelligent crop recommendations, disease detection, yield predictions, and fertilizer advice powered by AI.',
    color: '#1565C0',
  },
  {
    icon: <WbSunnyIcon sx={{ fontSize: 32 }} />,
    title: 'Weather Insights',
    description: 'Real-time weather data and 5-day forecasts with farming advice tailored to current conditions.',
    color: '#FF8F00',
  },
  {
    icon: <AccountBalanceIcon sx={{ fontSize: 32 }} />,
    title: 'Loan Management',
    description: 'Apply for agricultural loans, track applications, and connect directly with bank officers.',
    color: '#6A1B9A',
  },
];

const steps = [
  { step: '01', title: 'Register', desc: 'Create your account as a Farmer, Expert, or Bank Officer.' },
  { step: '02', title: 'Set Up Profile', desc: 'Add your farm details, crops, and preferences to personalize your experience.' },
  { step: '03', title: 'Use AI Tools', desc: 'Get crop recommendations, detect plant diseases, and predict yields instantly.' },
  { step: '04', title: 'Grow & Prosper', desc: 'Access expert advice, weather insights, and financial support to maximize your harvest.' },
];

const stats = [
  { value: '10,000+', label: 'Farmers Registered' },
  { value: '95%', label: 'AI Accuracy Rate' },
  { value: '₹50Cr+', label: 'Loans Facilitated' },
  { value: '500+', label: 'Expert Advisors' },
];

const LandingPage = () => {
  const navigate = useNavigate();
  const theme = useTheme();

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default', overflow: 'hidden' }}>
      {/* Navbar */}
      <Box
        sx={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          zIndex: 100,
          backdropFilter: 'blur(20px)',
          bgcolor: 'rgba(255,255,255,0.85)',
          borderBottom: '1px solid rgba(0,0,0,0.08)',
          px: { xs: 2, md: 6 },
          py: 1.5,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <AgricultureIcon sx={{ color: '#2E7D32', fontSize: 30 }} />
          <Typography variant="h6" fontWeight={800} sx={{ color: '#2E7D32' }}>
            Smart Agro
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button variant="outlined" color="primary" onClick={() => navigate('/login')} id="landing-login-btn">
            Login
          </Button>
          <Button variant="contained" color="primary" onClick={() => navigate('/register')} id="landing-register-btn">
            Get Started
          </Button>
        </Box>
      </Box>

      {/* Hero Section */}
      <Box
        className="hero-gradient"
        sx={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        {/* Decorative circles */}
        <Box sx={{ position: 'absolute', top: '10%', right: '5%', width: 300, height: 300, borderRadius: '50%', bgcolor: 'rgba(255,255,255,0.04)' }} />
        <Box sx={{ position: 'absolute', bottom: '15%', left: '-5%', width: 200, height: 200, borderRadius: '50%', bgcolor: 'rgba(255,255,255,0.04)' }} />
        <Box sx={{ position: 'absolute', top: '50%', right: '20%', width: 100, height: 100, borderRadius: '50%', bgcolor: 'rgba(255,255,255,0.06)' }} />

        <Container maxWidth="lg" sx={{ pt: 12, pb: 8 }}>
          <Grid container spacing={6} alignItems="center">
            <Grid item xs={12} md={6}>
              <Box className="slide-in-left">
                <Chip
                  label="🌾 AI-Powered Agriculture Platform"
                  sx={{
                    mb: 3,
                    bgcolor: 'rgba(255,255,255,0.15)',
                    color: '#fff',
                    fontWeight: 600,
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255,255,255,0.2)',
                  }}
                />
                <Typography
                  variant="h1"
                  sx={{
                    fontSize: { xs: '2.5rem', md: '3.5rem', lg: '4rem' },
                    fontWeight: 800,
                    color: '#fff',
                    lineHeight: 1.1,
                    mb: 2.5,
                  }}
                >
                  Smart Agriculture
                  <br />
                  for a{' '}
                  <Box component="span" sx={{ color: '#A5D6A7', display: 'inline' }}>
                    Smarter
                  </Box>
                  <br />
                  Future
                </Typography>
                <Typography
                  variant="h6"
                  sx={{
                    color: 'rgba(255,255,255,0.8)',
                    fontWeight: 400,
                    mb: 4,
                    lineHeight: 1.6,
                    maxWidth: 480,
                  }}
                >
                  Empower your farming with AI-driven insights, real-time weather data, expert guidance, and seamless loan management — all in one platform.
                </Typography>
                <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                  <Button
                    variant="contained"
                    size="large"
                    onClick={() => navigate('/register')}
                    id="hero-register-btn"
                    endIcon={<ArrowForwardIcon />}
                    sx={{
                      bgcolor: '#fff',
                      color: '#2E7D32',
                      fontWeight: 700,
                      px: 4,
                      py: 1.5,
                      fontSize: '1rem',
                      boxShadow: '0 8px 24px rgba(0,0,0,0.2)',
                      '&:hover': {
                        bgcolor: '#f5f5f5',
                        transform: 'translateY(-2px)',
                        boxShadow: '0 12px 32px rgba(0,0,0,0.25)',
                      },
                      '& .MuiButton-root': { background: 'none !important' },
                      background: '#fff !important',
                    }}
                  >
                    Get Started Free
                  </Button>
                  <Button
                    variant="outlined"
                    size="large"
                    onClick={() => navigate('/login')}
                    id="hero-login-btn"
                    sx={{
                      borderColor: 'rgba(255,255,255,0.5)',
                      color: '#fff',
                      fontWeight: 600,
                      px: 4,
                      py: 1.5,
                      fontSize: '1rem',
                      '&:hover': {
                        borderColor: '#fff',
                        bgcolor: 'rgba(255,255,255,0.1)',
                      },
                    }}
                  >
                    Sign In
                  </Button>
                </Box>
              </Box>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box
                className="float-animation slide-in-right"
                sx={{ display: 'flex', justifyContent: 'center', position: 'relative' }}
              >
                {/* Illustration placeholder */}
                <Box
                  sx={{
                    width: { xs: 280, md: 420 },
                    height: { xs: 280, md: 420 },
                    borderRadius: '50%',
                    background: 'rgba(255,255,255,0.08)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    backdropFilter: 'blur(10px)',
                    border: '2px solid rgba(255,255,255,0.15)',
                    boxShadow: '0 20px 60px rgba(0,0,0,0.2)',
                    position: 'relative',
                  }}
                >
                  <AgricultureIcon sx={{ fontSize: { xs: 120, md: 180 }, color: 'rgba(255,255,255,0.6)' }} />
                  {/* Floating badges */}
                  {[
                    { icon: <SmartToyIcon />, label: 'AI Powered', top: '10%', right: '-5%', color: '#1565C0' },
                    { icon: <WbSunnyIcon />, label: 'Weather', bottom: '15%', right: '-8%', color: '#FF8F00' },
                    { icon: <VerifiedIcon />, label: 'Certified', top: '20%', left: '-10%', color: '#2E7D32' },
                  ].map((badge, i) => (
                    <Box
                      key={i}
                      sx={{
                        position: 'absolute',
                        ...badge,
                        bgcolor: '#fff',
                        borderRadius: 2.5,
                        px: 1.5,
                        py: 0.8,
                        display: 'flex',
                        alignItems: 'center',
                        gap: 0.5,
                        boxShadow: '0 4px 16px rgba(0,0,0,0.15)',
                        animation: `float ${4 + i}s ease-in-out infinite`,
                        animationDelay: `${i * 0.5}s`,
                      }}
                    >
                      <Box sx={{ color: badge.color, display: 'flex' }}>{badge.icon}</Box>
                      <Typography variant="caption" fontWeight={700} color="text.primary" noWrap>
                        {badge.label}
                      </Typography>
                    </Box>
                  ))}
                </Box>
              </Box>
            </Grid>
          </Grid>

          {/* Stats row */}
          <Grid container spacing={3} sx={{ mt: 6 }}>
            {stats.map((stat, i) => (
              <Grid item xs={6} md={3} key={i}>
                <Box
                  sx={{
                    textAlign: 'center',
                    p: 2,
                    borderRadius: 2,
                    bgcolor: 'rgba(255,255,255,0.08)',
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255,255,255,0.12)',
                  }}
                >
                  <Typography variant="h4" fontWeight={800} sx={{ color: '#A5D6A7', mb: 0.5 }}>
                    {stat.value}
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                    {stat.label}
                  </Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* Features Section */}
      <Box sx={{ py: 10, bgcolor: 'background.default' }}>
        <Container maxWidth="lg">
          <Box sx={{ textAlign: 'center', mb: 6 }}>
            <Chip label="Features" color="primary" variant="outlined" sx={{ mb: 2 }} />
            <Typography variant="h3" fontWeight={700} gutterBottom>
              Everything You Need to
              <Box component="span" sx={{ color: 'primary.main' }}> Grow Better</Box>
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ maxWidth: 600, mx: 'auto' }}>
              A comprehensive platform designed for modern farmers, agricultural experts, and financial institutions.
            </Typography>
          </Box>
          <Grid container spacing={3}>
            {features.map((feature, i) => (
              <Grid item xs={12} sm={6} md={3} key={i}>
                <Card
                  className="hover-card"
                  sx={{
                    height: '100%',
                    textAlign: 'center',
                    p: 1,
                    border: `1px solid ${feature.color}20`,
                  }}
                >
                  <CardContent sx={{ p: 3 }}>
                    <Avatar
                      sx={{
                        bgcolor: `${feature.color}15`,
                        color: feature.color,
                        width: 64,
                        height: 64,
                        mx: 'auto',
                        mb: 2,
                        boxShadow: `0 8px 24px ${feature.color}25`,
                      }}
                    >
                      {feature.icon}
                    </Avatar>
                    <Typography variant="h6" fontWeight={700} gutterBottom>
                      {feature.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" lineHeight={1.7}>
                      {feature.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* How It Works */}
      <Box sx={{ py: 10, bgcolor: 'background.paper' }}>
        <Container maxWidth="lg">
          <Box sx={{ textAlign: 'center', mb: 6 }}>
            <Chip label="Process" color="secondary" variant="outlined" sx={{ mb: 2 }} />
            <Typography variant="h3" fontWeight={700} gutterBottom>
              How It Works
            </Typography>
          </Box>
          <Grid container spacing={4}>
            {steps.map((step, i) => (
              <Grid item xs={12} sm={6} md={3} key={i}>
                <Box sx={{ textAlign: 'center', position: 'relative' }}>
                  <Box
                    sx={{
                      width: 64,
                      height: 64,
                      borderRadius: '50%',
                      background: 'linear-gradient(135deg, #2E7D32, #4CAF50)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      mx: 'auto',
                      mb: 2,
                      boxShadow: '0 8px 24px rgba(46,125,50,0.3)',
                    }}
                  >
                    <Typography variant="h6" fontWeight={800} color="white">
                      {step.step}
                    </Typography>
                  </Box>
                  <Typography variant="h6" fontWeight={700} gutterBottom>
                    {step.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" lineHeight={1.7}>
                    {step.desc}
                  </Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* CTA Section */}
      <Box
        className="hero-gradient"
        sx={{ py: 10, textAlign: 'center' }}
      >
        <Container maxWidth="md">
          <Typography variant="h3" fontWeight={800} color="white" gutterBottom>
            Ready to Transform Your Farm?
          </Typography>
          <Typography variant="h6" sx={{ color: 'rgba(255,255,255,0.8)', mb: 4, fontWeight: 400 }}>
            Join thousands of farmers already using Smart Agro to maximize their yields.
          </Typography>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/register')}
            id="cta-register-btn"
            sx={{
              bgcolor: '#fff',
              color: '#2E7D32',
              fontWeight: 700,
              px: 5,
              py: 1.5,
              fontSize: '1rem',
              background: '#fff !important',
              '&:hover': { bgcolor: '#f5f5f5', transform: 'translateY(-2px)' },
            }}
          >
            Get Started for Free
          </Button>
        </Container>
      </Box>

      {/* Footer */}
      <Box sx={{ py: 4, bgcolor: '#0D1F35', textAlign: 'center' }}>
        <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.5)' }}>
          © 2025 Smart Agro. All rights reserved. | AI-Powered Agriculture Management System
        </Typography>
      </Box>
    </Box>
  );
};

export default LandingPage;
