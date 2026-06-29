import { createTheme } from '@mui/material/styles';

export const lightTheme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#2E7D32',
      light: '#4CAF50',
      dark: '#1B5E20',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#FF8F00',
      light: '#FFB300',
      dark: '#E65100',
      contrastText: '#ffffff',
    },
    background: {
      default: '#F1F8E9',
      paper: '#FFFFFF',
    },
    success: { main: '#388E3C', light: '#66BB6A', dark: '#2E7D32' },
    info: { main: '#0288D1', light: '#29B6F6', dark: '#01579B' },
    warning: { main: '#FF8F00', light: '#FFB300', dark: '#E65100' },
    error: { main: '#D32F2F', light: '#EF5350', dark: '#B71C1C' },
    text: {
      primary: '#1A2027',
      secondary: '#546E7A',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: { fontWeight: 800, letterSpacing: '-0.02em' },
    h2: { fontWeight: 700, letterSpacing: '-0.01em' },
    h3: { fontWeight: 700 },
    h4: { fontWeight: 600 },
    h5: { fontWeight: 600 },
    h6: { fontWeight: 600 },
    subtitle1: { fontWeight: 500 },
    button: { fontWeight: 600, textTransform: 'none' },
  },
  shape: { borderRadius: 12 },
  shadows: [
    'none',
    '0 1px 3px rgba(0,0,0,0.08)',
    '0 2px 6px rgba(0,0,0,0.08)',
    '0 4px 12px rgba(0,0,0,0.08)',
    '0 4px 20px rgba(0,0,0,0.1)',
    '0 8px 24px rgba(0,0,0,0.1)',
    '0 8px 32px rgba(0,0,0,0.12)',
    '0 12px 40px rgba(0,0,0,0.12)',
    '0 12px 48px rgba(0,0,0,0.14)',
    '0 16px 56px rgba(0,0,0,0.14)',
    '0 16px 64px rgba(0,0,0,0.16)',
    '0 20px 72px rgba(0,0,0,0.16)',
    '0 20px 80px rgba(0,0,0,0.18)',
    '0 24px 88px rgba(0,0,0,0.18)',
    '0 24px 96px rgba(0,0,0,0.20)',
    '0 28px 104px rgba(0,0,0,0.20)',
    '0 28px 112px rgba(0,0,0,0.22)',
    '0 32px 120px rgba(0,0,0,0.22)',
    '0 32px 128px rgba(0,0,0,0.24)',
    '0 36px 136px rgba(0,0,0,0.24)',
    '0 36px 144px rgba(0,0,0,0.26)',
    '0 40px 152px rgba(0,0,0,0.26)',
    '0 40px 160px rgba(0,0,0,0.28)',
    '0 44px 168px rgba(0,0,0,0.28)',
    '0 44px 176px rgba(0,0,0,0.30)',
  ],
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
          borderRadius: 8,
          padding: '8px 20px',
        },
        containedPrimary: {
          background: 'linear-gradient(135deg, #2E7D32, #388E3C)',
          boxShadow: '0 4px 14px rgba(46, 125, 50, 0.4)',
          '&:hover': {
            background: 'linear-gradient(135deg, #1B5E20, #2E7D32)',
            boxShadow: '0 6px 20px rgba(46, 125, 50, 0.5)',
            transform: 'translateY(-1px)',
          },
        },
        containedSecondary: {
          background: 'linear-gradient(135deg, #FF8F00, #FFA000)',
          boxShadow: '0 4px 14px rgba(255, 143, 0, 0.4)',
          '&:hover': {
            background: 'linear-gradient(135deg, #E65100, #FF8F00)',
            boxShadow: '0 6px 20px rgba(255, 143, 0, 0.5)',
            transform: 'translateY(-1px)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
          border: '1px solid rgba(0,0,0,0.04)',
          transition: 'transform 0.2s ease, box-shadow 0.2s ease',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          fontWeight: 600,
          borderRadius: 8,
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 10,
          },
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        head: {
          fontWeight: 700,
          backgroundColor: '#F1F8E9',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          borderRight: '1px solid rgba(0,0,0,0.06)',
        },
      },
    },
  },
});

export const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#4CAF50',
      light: '#81C784',
      dark: '#2E7D32',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#FFB300',
      light: '#FFD54F',
      dark: '#FF8F00',
      contrastText: '#000000',
    },
    background: {
      default: '#0A1628',
      paper: '#132035',
    },
    success: { main: '#4CAF50', light: '#81C784', dark: '#2E7D32' },
    info: { main: '#29B6F6', light: '#4FC3F7', dark: '#0288D1' },
    warning: { main: '#FFB300', light: '#FFD54F', dark: '#FF8F00' },
    error: { main: '#EF5350', light: '#EF9A9A', dark: '#D32F2F' },
    text: {
      primary: '#E8F5E9',
      secondary: '#90A4AE',
    },
    divider: 'rgba(255,255,255,0.08)',
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: { fontWeight: 800, letterSpacing: '-0.02em' },
    h2: { fontWeight: 700, letterSpacing: '-0.01em' },
    h3: { fontWeight: 700 },
    h4: { fontWeight: 600 },
    h5: { fontWeight: 600 },
    h6: { fontWeight: 600 },
    subtitle1: { fontWeight: 500 },
    button: { fontWeight: 600, textTransform: 'none' },
  },
  shape: { borderRadius: 12 },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
          borderRadius: 8,
          padding: '8px 20px',
        },
        containedPrimary: {
          background: 'linear-gradient(135deg, #2E7D32, #4CAF50)',
          boxShadow: '0 4px 14px rgba(76, 175, 80, 0.3)',
          '&:hover': {
            background: 'linear-gradient(135deg, #1B5E20, #2E7D32)',
            boxShadow: '0 6px 20px rgba(76, 175, 80, 0.4)',
            transform: 'translateY(-1px)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0 4px 24px rgba(0,0,0,0.3)',
          border: '1px solid rgba(255,255,255,0.06)',
          backgroundImage: 'none',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          fontWeight: 600,
          borderRadius: 8,
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 10,
          },
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        head: {
          fontWeight: 700,
          backgroundColor: '#0D1F35',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          borderRight: '1px solid rgba(255,255,255,0.06)',
          background: '#0D1F35',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          background: '#132035',
          boxShadow: '0 1px 0 rgba(255,255,255,0.06)',
        },
      },
    },
  },
});
