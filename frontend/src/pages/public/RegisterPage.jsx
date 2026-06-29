import React, { useState } from 'react';
import {
  Box,
  Button,
  TextField,
  Typography,
  Stepper,
  Step,
  StepLabel,
  Card,
  CardContent,
  Grid,
  MenuItem,
  InputAdornment,
  IconButton,
  Alert,
  CircularProgress,
  Avatar,
  Divider,
} from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import AgricultureIcon from '@mui/icons-material/Agriculture';
import PersonIcon from '@mui/icons-material/Person';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import ScienceIcon from '@mui/icons-material/Science';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import { register } from '../../api/auth';
import { toast } from 'react-toastify';

const roles = [
  {
    value: 'farmer',
    label: 'Farmer',
    description: 'Manage your farm, crops, and access AI tools',
    icon: <AgricultureIcon sx={{ fontSize: 36 }} />,
    color: '#2E7D32',
  },
  {
    value: 'expert',
    label: 'Agri Expert',
    description: 'Answer farmer queries and provide agricultural guidance',
    icon: <ScienceIcon sx={{ fontSize: 36 }} />,
    color: '#1565C0',
  },
  {
    value: 'bank',
    label: 'Bank Officer',
    description: 'Review and manage agricultural loan applications',
    icon: <AccountBalanceIcon sx={{ fontSize: 36 }} />,
    color: '#6A1B9A',
  },
];

const soilTypes = ['Sandy', 'Clay', 'Loamy', 'Silty', 'Peaty', 'Chalky', 'Black', 'Red Laterite'];
const steps = ['Select Role', 'Basic Info', 'Profile Details'];

const RegisterPage = () => {
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [selectedRole, setSelectedRole] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    name: '', email: '', password: '', confirmPassword: '',
    // Farmer fields
    farm_name: '', location: '', farm_size: '', soil_type: '', phone: '',
    // Expert fields
    specialization: '', qualification: '', experience_years: '',
    // Bank fields
    bank_name: '', branch_name: '', ifsc_code: '',
  });

  const handleChange = (e) => {
    setError('');
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const validateStep = () => {
    if (activeStep === 0 && !selectedRole) {
      setError('Please select your role to continue.');
      return false;
    }
    if (activeStep === 1) {
      if (!formData.name || !formData.email || !formData.password || !formData.confirmPassword) {
        setError('Please fill in all required fields.');
        return false;
      }
      if (formData.password.length < 6) {
        setError('Password must be at least 6 characters long.');
        return false;
      }
      if (formData.password !== formData.confirmPassword) {
        setError('Passwords do not match.');
        return false;
      }
    }
    return true;
  };

  const handleNext = () => {
    if (!validateStep()) return;
    setError('');
    setActiveStep((prev) => prev + 1);
  };

  const handleBack = () => {
    setError('');
    setActiveStep((prev) => prev - 1);
  };

  const buildPayload = () => {
    const base = {
      name: formData.name,
      email: formData.email,
      password: formData.password,
      role: selectedRole,
    };
    if (selectedRole === 'farmer') {
      return {
        ...base,
        farmerProfile: {
          farm_name: formData.farm_name,
          location: formData.location,
          farm_size: parseFloat(formData.farm_size) || 0,
          soil_type: formData.soil_type,
          phone: formData.phone,
        },
      };
    }
    if (selectedRole === 'expert') {
      return {
        ...base,
        expertProfile: {
          specialization: formData.specialization,
          qualification: formData.qualification,
          experience_years: parseInt(formData.experience_years) || 0,
        },
      };
    }
    if (selectedRole === 'bank') {
      return {
        ...base,
        bankProfile: {
          bank_name: formData.bank_name,
          branch_name: formData.branch_name,
          ifsc_code: formData.ifsc_code,
        },
      };
    }
    return base;
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setError('');
      await register(buildPayload());
      toast.success('Registration successful! Please log in.');
      navigate('/login');
    } catch (err) {
      const msg = err.response?.data?.message || 'Registration failed. Please try again.';
      setError(msg);
      toast.error(msg);
    } finally {
      setLoading(false);
    }
  };

  const roleInfo = roles.find((r) => r.value === selectedRole);

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        bgcolor: 'background.default',
        py: 4,
        px: 2,
      }}
    >
      <Box sx={{ width: '100%', maxWidth: 680 }}>
        {/* Logo */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 4, justifyContent: 'center' }}>
          <AgricultureIcon sx={{ color: 'primary.main', fontSize: 36 }} />
          <Typography variant="h5" fontWeight={800} color="primary.main">
            Smart Agro
          </Typography>
        </Box>

        <Card sx={{ borderRadius: 4, overflow: 'visible' }}>
          <CardContent sx={{ p: { xs: 3, sm: 4 } }}>
            <Typography variant="h5" fontWeight={700} gutterBottom>
              Create Account
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Join Smart Agro and transform your agricultural journey
            </Typography>

            {/* Stepper */}
            <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
              {steps.map((label) => (
                <Step key={label}>
                  <StepLabel>{label}</StepLabel>
                </Step>
              ))}
            </Stepper>

            {error && (
              <Alert severity="error" sx={{ mb: 2, borderRadius: 2 }}>
                {error}
              </Alert>
            )}

            {/* Step 0 — Role Selection */}
            {activeStep === 0 && (
              <Grid container spacing={2}>
                {roles.map((role) => (
                  <Grid item xs={12} sm={4} key={role.value}>
                    <Card
                      onClick={() => { setSelectedRole(role.value); setError(''); }}
                      id={`role-card-${role.value}`}
                      sx={{
                        cursor: 'pointer',
                        border: `2px solid`,
                        borderColor: selectedRole === role.value ? role.color : 'divider',
                        textAlign: 'center',
                        p: 1,
                        position: 'relative',
                        transition: 'all 0.2s ease',
                        '&:hover': {
                          borderColor: role.color,
                          transform: 'translateY(-2px)',
                          boxShadow: `0 8px 24px ${role.color}20`,
                        },
                        background: selectedRole === role.value ? `${role.color}08` : 'transparent',
                      }}
                    >
                      {selectedRole === role.value && (
                        <CheckCircleIcon
                          sx={{
                            position: 'absolute',
                            top: 8,
                            right: 8,
                            fontSize: 20,
                            color: role.color,
                          }}
                        />
                      )}
                      <CardContent>
                        <Avatar
                          sx={{
                            bgcolor: `${role.color}18`,
                            color: role.color,
                            width: 60,
                            height: 60,
                            mx: 'auto',
                            mb: 1.5,
                          }}
                        >
                          {role.icon}
                        </Avatar>
                        <Typography variant="subtitle1" fontWeight={700} gutterBottom>
                          {role.label}
                        </Typography>
                        <Typography variant="caption" color="text.secondary" lineHeight={1.5}>
                          {role.description}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            )}

            {/* Step 1 — Basic Info */}
            {activeStep === 1 && (
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField fullWidth label="Full Name" name="name" value={formData.name} onChange={handleChange} required id="register-name-field" />
                </Grid>
                <Grid item xs={12}>
                  <TextField fullWidth label="Email Address" name="email" type="email" value={formData.email} onChange={handleChange} required id="register-email-field" />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth label="Password" name="password"
                    type={showPassword ? 'text' : 'password'}
                    value={formData.password} onChange={handleChange} required
                    id="register-password-field"
                    InputProps={{
                      endAdornment: (
                        <InputAdornment position="end">
                          <IconButton onClick={() => setShowPassword((v) => !v)} id="register-toggle-password">
                            {showPassword ? <VisibilityOffIcon /> : <VisibilityIcon />}
                          </IconButton>
                        </InputAdornment>
                      ),
                    }}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth label="Confirm Password" name="confirmPassword"
                    type={showPassword ? 'text' : 'password'}
                    value={formData.confirmPassword} onChange={handleChange} required
                    id="register-confirm-password-field"
                    error={formData.confirmPassword && formData.password !== formData.confirmPassword}
                    helperText={formData.confirmPassword && formData.password !== formData.confirmPassword ? "Passwords don't match" : ''}
                  />
                </Grid>
              </Grid>
            )}

            {/* Step 2 — Role-specific Info */}
            {activeStep === 2 && (
              <Box>
                {roleInfo && (
                  <Box
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 1.5,
                      mb: 3,
                      p: 2,
                      borderRadius: 2,
                      bgcolor: `${roleInfo.color}10`,
                      border: `1px solid ${roleInfo.color}25`,
                    }}
                  >
                    <Avatar sx={{ bgcolor: `${roleInfo.color}20`, color: roleInfo.color, width: 36, height: 36 }}>
                      {roleInfo.icon}
                    </Avatar>
                    <Box>
                      <Typography variant="body2" fontWeight={700} color="text.primary">
                        {roleInfo.label} Details
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Please provide your {roleInfo.label.toLowerCase()} information
                      </Typography>
                    </Box>
                  </Box>
                )}

                {selectedRole === 'farmer' && (
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={6}>
                      <TextField fullWidth label="Farm Name" name="farm_name" value={formData.farm_name} onChange={handleChange} id="farmer-farm-name" />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField fullWidth label="Location / Village" name="location" value={formData.location} onChange={handleChange} id="farmer-location" />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField fullWidth label="Farm Size (acres)" name="farm_size" type="number" value={formData.farm_size} onChange={handleChange} id="farmer-farm-size" />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField select fullWidth label="Soil Type" name="soil_type" value={formData.soil_type} onChange={handleChange} id="farmer-soil-type">
                        {soilTypes.map((s) => <MenuItem key={s} value={s}>{s}</MenuItem>)}
                      </TextField>
                    </Grid>
                    <Grid item xs={12}>
                      <TextField fullWidth label="Phone Number" name="phone" value={formData.phone} onChange={handleChange} id="farmer-phone" />
                    </Grid>
                  </Grid>
                )}

                {selectedRole === 'expert' && (
                  <Grid container spacing={2}>
                    <Grid item xs={12}>
                      <TextField fullWidth label="Specialization" name="specialization" value={formData.specialization} onChange={handleChange} placeholder="e.g. Crop Disease, Soil Science" id="expert-specialization" />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField fullWidth label="Qualification" name="qualification" value={formData.qualification} onChange={handleChange} placeholder="e.g. M.Sc Agriculture" id="expert-qualification" />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField fullWidth label="Experience (years)" name="experience_years" type="number" value={formData.experience_years} onChange={handleChange} id="expert-experience" />
                    </Grid>
                  </Grid>
                )}

                {selectedRole === 'bank' && (
                  <Grid container spacing={2}>
                    <Grid item xs={12}>
                      <TextField fullWidth label="Bank Name" name="bank_name" value={formData.bank_name} onChange={handleChange} id="bank-name" />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField fullWidth label="Branch Name" name="branch_name" value={formData.branch_name} onChange={handleChange} id="bank-branch" />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField fullWidth label="IFSC Code" name="ifsc_code" value={formData.ifsc_code} onChange={handleChange} id="bank-ifsc" inputProps={{ style: { textTransform: 'uppercase' } }} />
                    </Grid>
                  </Grid>
                )}
              </Box>
            )}

            {/* Navigation Buttons */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4, gap: 2 }}>
              <Button
                variant="outlined"
                onClick={activeStep === 0 ? () => navigate('/login') : handleBack}
                id="register-back-btn"
                disabled={loading}
              >
                {activeStep === 0 ? 'Back to Login' : 'Back'}
              </Button>
              {activeStep < steps.length - 1 ? (
                <Button
                  variant="contained"
                  onClick={handleNext}
                  id="register-next-btn"
                >
                  Next
                </Button>
              ) : (
                <Button
                  variant="contained"
                  onClick={handleSubmit}
                  disabled={loading}
                  id="register-submit-btn"
                >
                  {loading ? (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <CircularProgress size={18} color="inherit" />
                      Creating Account...
                    </Box>
                  ) : (
                    'Create Account'
                  )}
                </Button>
              )}
            </Box>

            <Divider sx={{ my: 2 }} />
            <Typography variant="body2" textAlign="center" color="text.secondary">
              Already have an account?{' '}
              <Link to="/login" style={{ color: 'inherit', textDecoration: 'none' }}>
                <Typography component="span" variant="body2" color="primary.main" fontWeight={700}>
                  Sign In
                </Typography>
              </Link>
            </Typography>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
};

export default RegisterPage;
