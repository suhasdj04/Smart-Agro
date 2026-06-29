import React from 'react';
import { Box, Typography, Avatar } from '@mui/material';
import InboxIcon from '@mui/icons-material/Inbox';

const EmptyState = ({
  icon,
  title = 'No Data Found',
  message = 'There is nothing to display here yet.',
  action,
}) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        py: 8,
        px: 3,
        textAlign: 'center',
      }}
    >
      <Avatar
        sx={{
          width: 80,
          height: 80,
          bgcolor: 'primary.main',
          opacity: 0.15,
          mb: 3,
        }}
      >
        {icon || <InboxIcon sx={{ fontSize: 40, color: 'primary.main' }} />}
      </Avatar>
      <Box sx={{ opacity: 0.5, mb: 1 }}>
        {icon ? (
          <Box sx={{ color: 'text.secondary', mb: 2, '& svg': { fontSize: 48 } }}>
            {icon}
          </Box>
        ) : (
          <InboxIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
        )}
      </Box>
      <Typography variant="h6" fontWeight={600} color="text.secondary" gutterBottom>
        {title}
      </Typography>
      <Typography variant="body2" color="text.disabled" sx={{ maxWidth: 300 }}>
        {message}
      </Typography>
      {action && <Box sx={{ mt: 3 }}>{action}</Box>}
    </Box>
  );
};

export default EmptyState;
