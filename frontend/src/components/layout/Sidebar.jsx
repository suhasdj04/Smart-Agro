import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Box,
  Typography,
  Divider,
  Avatar,
  Tooltip,
  alpha,
  useTheme,
} from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

// Icons
import DashboardIcon from '@mui/icons-material/Dashboard';
import GrassIcon from '@mui/icons-material/Grass';
import PriceCheckIcon from '@mui/icons-material/PriceCheck';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import ReportProblemIcon from '@mui/icons-material/ReportProblem';
import HelpIcon from '@mui/icons-material/Help';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import WbSunnyIcon from '@mui/icons-material/WbSunny';
import PeopleIcon from '@mui/icons-material/People';
import PersonIcon from '@mui/icons-material/Person';
import AssessmentIcon from '@mui/icons-material/Assessment';
import AgricultureIcon from '@mui/icons-material/Agriculture';

const farmerMenu = [
  { label: 'Dashboard', icon: <DashboardIcon />, path: '/farmer/dashboard' },
  { label: 'My Crops', icon: <GrassIcon />, path: '/farmer/crops' },
  { label: 'Crop Prices', icon: <PriceCheckIcon />, path: '/farmer/prices' },
  { label: 'Apply for Loan', icon: <AccountBalanceIcon />, path: '/farmer/loans' },
  { label: 'Complaints', icon: <ReportProblemIcon />, path: '/farmer/complaints' },
  { label: 'Queries', icon: <HelpIcon />, path: '/farmer/queries' },
  { label: 'AI Tools', icon: <SmartToyIcon />, path: '/farmer/ai' },
  { label: 'Weather', icon: <WbSunnyIcon />, path: '/farmer/weather' },
];

const expertMenu = [
  { label: 'Dashboard', icon: <DashboardIcon />, path: '/expert/dashboard' },
  { label: 'Farmer Queries', icon: <HelpIcon />, path: '/expert/queries' },
  { label: 'Farmer Profiles', icon: <PeopleIcon />, path: '/expert/farmers' },
];

const bankMenu = [
  { label: 'Dashboard', icon: <DashboardIcon />, path: '/bank/dashboard' },
  { label: 'Loan Applications', icon: <AccountBalanceIcon />, path: '/bank/loans' },
  { label: 'Reports', icon: <AssessmentIcon />, path: '/bank/reports' },
];

const adminMenu = [
  { label: 'Dashboard', icon: <DashboardIcon />, path: '/admin/dashboard' },
  { label: 'Users', icon: <PeopleIcon />, path: '/admin/users' },
  { label: 'Crop Prices', icon: <PriceCheckIcon />, path: '/admin/prices' },
  { label: 'Complaints', icon: <ReportProblemIcon />, path: '/admin/complaints' },
  { label: 'Reports', icon: <AssessmentIcon />, path: '/admin/reports' },
];

const menuMap = {
  farmer: farmerMenu,
  expert: expertMenu,
  bank: bankMenu,
  admin: adminMenu,
};

const roleColors = {
  farmer: '#2E7D32',
  expert: '#1565C0',
  bank: '#6A1B9A',
  admin: '#BF360C',
};

const roleLabels = {
  farmer: 'Farmer',
  expert: 'Agri Expert',
  bank: 'Bank Officer',
  admin: 'Administrator',
};

const Sidebar = ({ open, onClose, isMobile, drawerWidth }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useAuth();
  const theme = useTheme();

  const menu = menuMap[user?.role] || [];
  const roleColor = roleColors[user?.role] || '#2E7D32';
  const roleLabel = roleLabels[user?.role] || user?.role;

  const handleNavigate = (path) => {
    navigate(path);
    if (isMobile) onClose();
  };

  const drawerContent = (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        overflow: 'hidden',
      }}
    >
      {/* Logo */}
      <Box
        sx={{
          p: 2.5,
          display: 'flex',
          alignItems: 'center',
          gap: 1.5,
          borderBottom: '1px solid',
          borderColor: 'divider',
          background: `linear-gradient(135deg, ${roleColor}18, ${roleColor}08)`,
        }}
      >
        <Avatar
          sx={{
            bgcolor: roleColor,
            width: 40,
            height: 40,
            boxShadow: `0 4px 12px ${roleColor}40`,
          }}
        >
          <AgricultureIcon sx={{ fontSize: 22 }} />
        </Avatar>
        <Box>
          <Typography
            variant="h6"
            fontWeight={800}
            sx={{ lineHeight: 1.2, color: 'text.primary' }}
          >
            Smart Agro
          </Typography>
          <Typography
            variant="caption"
            sx={{ color: roleColor, fontWeight: 600, fontSize: '0.7rem' }}
          >
            {roleLabel}
          </Typography>
        </Box>
      </Box>

      {/* User info */}
      {user && (
        <Box
          sx={{
            px: 2,
            py: 2,
            display: 'flex',
            alignItems: 'center',
            gap: 1.5,
          }}
        >
          <Avatar
            sx={{
              width: 36,
              height: 36,
              bgcolor: `${roleColor}20`,
              color: roleColor,
              fontWeight: 700,
              fontSize: 14,
            }}
          >
            {user.name?.charAt(0)?.toUpperCase() || 'U'}
          </Avatar>
          <Box sx={{ overflow: 'hidden' }}>
            <Typography
              variant="body2"
              fontWeight={600}
              noWrap
              sx={{ color: 'text.primary' }}
            >
              {user.name || 'User'}
            </Typography>
            <Typography variant="caption" noWrap sx={{ color: 'text.secondary' }}>
              {user.email}
            </Typography>
          </Box>
        </Box>
      )}

      <Divider />

      {/* Menu Items */}
      <List sx={{ flexGrow: 1, overflow: 'auto', py: 1, px: 1 }}>
        {menu.map((item) => {
          const isActive =
            location.pathname === item.path ||
            (item.path !== '/' && location.pathname.startsWith(item.path));

          return (
            <ListItem key={item.path} disablePadding sx={{ mb: 0.5 }}>
              <ListItemButton
                onClick={() => handleNavigate(item.path)}
                selected={isActive}
                sx={{
                  borderRadius: 2,
                  px: 2,
                  py: 1,
                  '&.Mui-selected': {
                    bgcolor: `${roleColor}18`,
                    color: roleColor,
                    '&:hover': { bgcolor: `${roleColor}24` },
                    '& .MuiListItemIcon-root': { color: roleColor },
                    '& .MuiListItemText-primary': { fontWeight: 700 },
                  },
                  '&:hover': {
                    bgcolor: `${roleColor}10`,
                  },
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 38,
                    color: isActive ? roleColor : 'text.secondary',
                    '& svg': { fontSize: 20 },
                  }}
                >
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.label}
                  primaryTypographyProps={{
                    fontSize: '0.875rem',
                    fontWeight: isActive ? 700 : 500,
                  }}
                />
                {isActive && (
                  <Box
                    sx={{
                      width: 4,
                      height: 20,
                      borderRadius: 2,
                      bgcolor: roleColor,
                      position: 'absolute',
                      right: 8,
                    }}
                  />
                )}
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>

      {/* Bottom - Profile & Settings */}
      <Divider />
      <List sx={{ py: 1, px: 1 }}>
        <ListItem disablePadding sx={{ mb: 0.5 }}>
          <ListItemButton
            onClick={() => handleNavigate('/profile')}
            selected={location.pathname === '/profile'}
            sx={{
              borderRadius: 2,
              px: 2,
              py: 1,
              '&.Mui-selected': {
                bgcolor: `${roleColor}18`,
                color: roleColor,
                '& .MuiListItemIcon-root': { color: roleColor },
              },
            }}
          >
            <ListItemIcon sx={{ minWidth: 38, color: 'text.secondary', '& svg': { fontSize: 20 } }}>
              <PersonIcon />
            </ListItemIcon>
            <ListItemText
              primary="Profile"
              primaryTypographyProps={{ fontSize: '0.875rem', fontWeight: 500 }}
            />
          </ListItemButton>
        </ListItem>
      </List>
    </Box>
  );

  return (
    <>
      {/* Mobile Drawer */}
      {isMobile ? (
        <Drawer
          variant="temporary"
          open={open}
          onClose={onClose}
          ModalProps={{ keepMounted: true }}
          sx={{
            '& .MuiDrawer-paper': {
              width: drawerWidth,
              boxSizing: 'border-box',
            },
          }}
        >
          {drawerContent}
        </Drawer>
      ) : (
        /* Desktop Persistent Drawer */
        <Drawer
          variant="persistent"
          open={open}
          sx={{
            width: open ? drawerWidth : 0,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: drawerWidth,
              boxSizing: 'border-box',
              transition: 'width 0.2s ease',
            },
          }}
        >
          {drawerContent}
        </Drawer>
      )}
    </>
  );
};

export default Sidebar;
