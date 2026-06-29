import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Badge,
  Avatar,
  Box,
  Menu,
  MenuItem,
  Divider,
  Tooltip,
  Popover,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Button,
  Switch,
  FormControlLabel,
  useTheme,
  Chip,
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import NotificationsIcon from '@mui/icons-material/Notifications';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import LightModeIcon from '@mui/icons-material/LightMode';
import LogoutIcon from '@mui/icons-material/Logout';
import PersonIcon from '@mui/icons-material/Person';
import SettingsIcon from '@mui/icons-material/Settings';
import AgricultureIcon from '@mui/icons-material/Agriculture';
import MarkEmailReadIcon from '@mui/icons-material/MarkEmailRead';
import NotificationsNoneIcon from '@mui/icons-material/NotificationsNone';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useNotifications } from '../../hooks/useNotifications';

const roleColors = {
  farmer: '#2E7D32',
  expert: '#1565C0',
  bank: '#6A1B9A',
  admin: '#BF360C',
};

const Navbar = ({ sidebarOpen, onToggleSidebar }) => {
  const theme = useTheme();
  const navigate = useNavigate();
  const { user, logout, darkMode, toggleDarkMode } = useAuth();
  const { notifications, unreadCount, markAsRead, markAllAsRead } = useNotifications();
  const [anchorElUser, setAnchorElUser] = useState(null);
  const [anchorElNotif, setAnchorElNotif] = useState(null);

  const roleColor = roleColors[user?.role] || '#2E7D32';

  const handleLogout = async () => {
    setAnchorElUser(null);
    await logout();
    navigate('/login');
  };

  const formatTime = (dateStr) => {
    if (!dateStr) return '';
    const d = new Date(dateStr);
    return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });
  };

  return (
    <AppBar
      position="fixed"
      elevation={0}
      sx={{
        zIndex: theme.zIndex.drawer + 1,
        bgcolor: theme.palette.mode === 'dark' ? '#132035' : '#fff',
        borderBottom: '1px solid',
        borderColor: 'divider',
        color: 'text.primary',
      }}
    >
      <Toolbar sx={{ gap: 1 }}>
        {/* Hamburger */}
        <IconButton
          id="sidebar-toggle-btn"
          edge="start"
          onClick={onToggleSidebar}
          sx={{ color: 'text.secondary' }}
        >
          <MenuIcon />
        </IconButton>

        {/* Logo */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mr: 'auto' }}>
          <AgricultureIcon sx={{ color: roleColor, fontSize: 28 }} />
          <Typography
            variant="h6"
            fontWeight={800}
            sx={{
              background: `linear-gradient(135deg, ${roleColor}, #1565C0)`,
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              display: { xs: 'none', sm: 'block' },
            }}
          >
            Smart Agro
          </Typography>
        </Box>

        {/* Dark/Light toggle */}
        <Tooltip title={darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}>
          <IconButton id="theme-toggle-btn" onClick={toggleDarkMode} sx={{ color: 'text.secondary' }}>
            {darkMode ? <LightModeIcon /> : <DarkModeIcon />}
          </IconButton>
        </Tooltip>

        {/* Notifications */}
        <Tooltip title="Notifications">
          <IconButton
            id="notifications-btn"
            onClick={(e) => setAnchorElNotif(e.currentTarget)}
            sx={{ color: 'text.secondary' }}
          >
            <Badge badgeContent={unreadCount} color="error" max={99}>
              <NotificationsIcon />
            </Badge>
          </IconButton>
        </Tooltip>

        {/* User Avatar */}
        <Tooltip title="Account">
          <IconButton
            id="user-menu-btn"
            onClick={(e) => setAnchorElUser(e.currentTarget)}
            sx={{ p: 0.5 }}
          >
            <Avatar
              sx={{
                width: 36,
                height: 36,
                bgcolor: `${roleColor}20`,
                color: roleColor,
                fontWeight: 700,
                fontSize: 14,
                border: `2px solid ${roleColor}40`,
              }}
            >
              {user?.name?.charAt(0)?.toUpperCase() || 'U'}
            </Avatar>
          </IconButton>
        </Tooltip>
      </Toolbar>

      {/* Notifications Popover */}
      <Popover
        open={Boolean(anchorElNotif)}
        anchorEl={anchorElNotif}
        onClose={() => setAnchorElNotif(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        PaperProps={{
          sx: {
            width: 360,
            maxHeight: 480,
            borderRadius: 3,
            boxShadow: '0 8px 40px rgba(0,0,0,0.15)',
            overflow: 'hidden',
          },
        }}
      >
        <Box
          sx={{
            p: 2,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            borderBottom: '1px solid',
            borderColor: 'divider',
          }}
        >
          <Typography variant="h6" fontWeight={700}>
            Notifications
          </Typography>
          {unreadCount > 0 && (
            <Button
              size="small"
              startIcon={<MarkEmailReadIcon />}
              onClick={markAllAsRead}
              sx={{ fontSize: '0.75rem' }}
            >
              Mark all read
            </Button>
          )}
        </Box>
        <Box sx={{ overflow: 'auto', maxHeight: 380 }}>
          {notifications.length === 0 ? (
            <Box sx={{ p: 4, textAlign: 'center' }}>
              <NotificationsNoneIcon sx={{ fontSize: 40, color: 'text.disabled', mb: 1 }} />
              <Typography variant="body2" color="text.secondary">
                No notifications yet
              </Typography>
            </Box>
          ) : (
            <List dense>
              {notifications.slice(0, 20).map((notif, i) => (
                <React.Fragment key={notif._id || i}>
                  <ListItem
                    alignItems="flex-start"
                    button
                    onClick={() => markAsRead(notif._id)}
                    sx={{
                      px: 2,
                      py: 1.5,
                      bgcolor: notif.read ? 'transparent' : 'primary.main' + '08',
                      '&:hover': { bgcolor: 'action.hover' },
                    }}
                  >
                    <ListItemAvatar sx={{ minWidth: 36 }}>
                      <Avatar sx={{ width: 28, height: 28, bgcolor: 'primary.light', fontSize: 12 }}>
                        {notif.title?.charAt(0) || 'N'}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', gap: 1 }}>
                          <Typography variant="body2" fontWeight={notif.read ? 400 : 600} sx={{ flex: 1 }}>
                            {notif.title || 'Notification'}
                          </Typography>
                          {!notif.read && (
                            <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: 'primary.main', mt: 0.5, flexShrink: 0 }} />
                          )}
                        </Box>
                      }
                      secondary={
                        <Box>
                          <Typography variant="caption" color="text.secondary" component="span" display="block">
                            {notif.message}
                          </Typography>
                          <Typography variant="caption" color="text.disabled" component="span">
                            {formatTime(notif.createdAt)}
                          </Typography>
                        </Box>
                      }
                    />
                  </ListItem>
                  {i < notifications.length - 1 && <Divider component="li" sx={{ mx: 2 }} />}
                </React.Fragment>
              ))}
            </List>
          )}
        </Box>
      </Popover>

      {/* User Menu */}
      <Menu
        anchorEl={anchorElUser}
        open={Boolean(anchorElUser)}
        onClose={() => setAnchorElUser(null)}
        PaperProps={{
          sx: { width: 220, borderRadius: 3, mt: 1, boxShadow: '0 8px 30px rgba(0,0,0,0.15)' },
        }}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <Box sx={{ px: 2, py: 1.5 }}>
          <Typography variant="subtitle2" fontWeight={700} noWrap>
            {user?.name}
          </Typography>
          <Typography variant="caption" color="text.secondary" noWrap display="block">
            {user?.email}
          </Typography>
          <Chip
            label={user?.role?.toUpperCase()}
            size="small"
            sx={{
              mt: 0.5,
              bgcolor: `${roleColor}18`,
              color: roleColor,
              fontWeight: 700,
              fontSize: '0.65rem',
              height: 20,
            }}
          />
        </Box>
        <Divider />
        <MenuItem
          onClick={() => { setAnchorElUser(null); navigate('/profile'); }}
          id="nav-profile-menu-item"
        >
          <PersonIcon sx={{ mr: 1.5, fontSize: 18, color: 'text.secondary' }} />
          <Typography variant="body2">Profile</Typography>
        </MenuItem>
        <MenuItem
          onClick={() => { setAnchorElUser(null); navigate('/settings'); }}
          id="nav-settings-menu-item"
        >
          <SettingsIcon sx={{ mr: 1.5, fontSize: 18, color: 'text.secondary' }} />
          <Typography variant="body2">Settings</Typography>
        </MenuItem>
        <Divider />
        <MenuItem onClick={handleLogout} id="nav-logout-menu-item" sx={{ color: 'error.main' }}>
          <LogoutIcon sx={{ mr: 1.5, fontSize: 18 }} />
          <Typography variant="body2">Logout</Typography>
        </MenuItem>
      </Menu>
    </AppBar>
  );
};

export default Navbar;
