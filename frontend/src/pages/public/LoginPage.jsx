import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  IconButton,
  InputAdornment,
  FormControlLabel,
  Checkbox,
  Divider,
  Alert,
  CircularProgress,
} from '@mui/material';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import AgricultureIcon from '@mui/icons-material/Agriculture';
import LockIcon from '@mui/icons-material/Lock';
import { useAuth } from '../../context/AuthContext';
import { toast } from 'react-toastify';

const LoginPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const from = location.state?.from?.pathname;

  const getRoleRedirect = (role) => {
    const map = {
      farmer: '/farmer/dashboard',
      expert: '/expert/dashboard',
      bank: '/bank/dashboard',
      admin: '/admin/dashboard',
    };
    return from || map[role] || '/farmer/dashboard';
  };

  const handleChange = (e) => {
    setError('');
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.email || !formData.password) {
      setError('Please fill in all fields.');
      return;
    }
    try {
      setLoading(true);
      setError('');
      const user = await login(formData.email, formData.password);
      toast.success(`Welcome back, ${user.name}! 🌾`);
      navigate(getRoleRedirect(user.role), { replace: true });
    } catch (err) {
      const msg = err.response?.data?.message || 'Login failed. Please check your credentials.';
      setError(msg);
      toast.error(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        bgcolor: 'background.default',
      }}
    >
      {/* Left Panel */}
      <Box
        className="hero-gradient"
        sx={{
          flex: 1,
          display: { xs: 'none', md: 'flex' },
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          p: 6,
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <Box sx={{ position: 'absolute', top: -50, left: -50, width: 250, height: 250, borderRadius: '50%', bgcolor: 'rgba(255,255,255,0.05)' }} />
        <Box sx={{ position: 'absolute', bottom: -30, right: -30, width: 200, height: 200, borderRadius: '50%', bgcolor: 'rgba(255,255,255,0.05)' }} />
        <Box className="float-animation" sx={{ textAlign: 'center', zIndex: 1 }}>
          <AgricultureIcon sx={{ fontSize: 100, color: 'rgba(255,255,255,0.7)', mb: 3 }} />
          <Typography variant="h3" fontWeight={800} color="white" gutterBottom>
            Smart Agro
          </Typography>
          <Typography variant="h6" sx={{ color: 'rgba(255,255,255,0.75)', fontWeight: 400, maxWidth: 380, lineHeight: 1.7 }}>
            AI-powered agriculture management for a smarter, more productive future.
          </Typography>
          <Box sx={{ mt: 4, display: 'flex', flexDirection: 'column', gap: 1.5, alignItems: 'flex-start', bgcolor: 'rgba(255,255,255,0.1)', p: 3, borderRadius: 3, backdropFilter: 'blur(10px)' }}>
            {['🌾 AI Crop Recommendations', '🌦️ Real-time Weather Insights', '💰 Loan Management', '👨‍🌾 Expert Guidance'].map((item) => (
              <Typography key={item} variant="body2" sx={{ color: 'rgba(255,255,255,0.9)' }}>
                {item}
              </Typography>
            ))}
          </Box>
        </Box>
      </Box>

      {/* Right Panel - Form */}
      <Box
        sx={{
          flex: { xs: 1, md: '0 0 480px' },
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          p: { xs: 2, sm: 4 },
          bgcolor: 'background.paper',
        }}
      >
        <Box sx={{ width: '100%', maxWidth: 400 }}>
          {/* Mobile Logo */}
          <Box sx={{ display: { xs: 'flex', md: 'none' }, alignItems: 'center', gap: 1, mb: 4, justifyContent: 'center' }}>
            <AgricultureIcon sx={{ color: 'primary.main', fontSize: 32 }} />
            <Typography variant="h5" fontWeight={800} color="primary.main">
              Smart Agro
            </Typography>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 1 }}>
              <Box sx={{ p: 1, borderRadius: 2, bgcolor: 'primary.main' + '18' }}>
                <LockIcon sx={{ color: 'primary.main', fontSize: 20 }} />
              </Box>
              <Typography variant="h5" fontWeight={700}>
                Welcome Back
              </Typography>
            </Box>
            <Typography variant="body2" color="text.secondary">
              Sign in to your Smart Agro account
            </Typography>
          </Box>

          {error && (
            <Alert severity="error" sx={{ mb: 2, borderRadius: 2 }}>
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit} id="login-form">
            <TextField
              fullWidth
              label="Email Address"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              margin="normal"
              required
              autoComplete="email"
              id="login-email-field"
              disabled={loading}
            />
            <TextField
              fullWidth
              label="Password"
              name="password"
              type={showPassword ? 'text' : 'password'}
              value={formData.password}
              onChange={handleChange}
              margin="normal"
              required
              autoComplete="current-password"
              id="login-password-field"
              disabled={loading}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      id="toggle-password-visibility"
                      onClick={() => setShowPassword((v) => !v)}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOffIcon /> : <VisibilityIcon />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mt: 1 }}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    size="small"
                    color="primary"
                    id="remember-me-checkbox"
                  />
                }
                label={<Typography variant="body2">Remember me</Typography>}
              />
              <Typography
                variant="body2"
                sx={{ color: 'primary.main', cursor: 'pointer', fontWeight: 600 }}
                component="span"
              >
                Forgot Password?
              </Typography>
            </Box>

            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={loading}
              id="login-submit-btn"
              sx={{ mt: 3, mb: 2, py: 1.5, fontSize: '1rem' }}
            >
              {loading ? (
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <CircularProgress size={20} color="inherit" />
                  Signing In...
                </Box>
              ) : (
                'Sign In'
              )}
            </Button>

            <Divider sx={{ my: 2 }}>
              <Typography variant="caption" color="text.secondary">
                OR
              </Typography>
            </Divider>

            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="body2" color="text.secondary">
                Don't have an account?{' '}
                <Link to="/register" style={{ color: 'inherit', fontWeight: 700 }}>
                  <Typography component="span" variant="body2" color="primary.main" fontWeight={700}>
                    Register now
                  </Typography>
                </Link>
              </Typography>
            </Box>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default LoginPage;
