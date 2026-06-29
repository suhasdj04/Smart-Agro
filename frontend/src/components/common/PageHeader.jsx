import React from 'react';
import { Box, Typography, Breadcrumbs, Link, Button } from '@mui/material';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import { useNavigate } from 'react-router-dom';

const PageHeader = ({
  title,
  subtitle,
  breadcrumbs = [],
  action,
  actionIcon,
  onAction,
}) => {
  const navigate = useNavigate();

  return (
    <Box sx={{ mb: 4 }}>
      {breadcrumbs.length > 0 && (
        <Breadcrumbs
          separator={<NavigateNextIcon fontSize="small" />}
          sx={{ mb: 1 }}
        >
          {breadcrumbs.map((crumb, i) =>
            crumb.href ? (
              <Link
                key={i}
                underline="hover"
                color="inherit"
                href={crumb.href}
                onClick={(e) => {
                  e.preventDefault();
                  navigate(crumb.href);
                }}
                sx={{ fontSize: '0.8rem', cursor: 'pointer' }}
              >
                {crumb.label}
              </Link>
            ) : (
              <Typography key={i} color="text.primary" sx={{ fontSize: '0.8rem' }}>
                {crumb.label}
              </Typography>
            )
          )}
        </Breadcrumbs>
      )}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'flex-end',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: 2,
        }}
      >
        <Box>
          <Typography
            variant="h4"
            sx={{ fontWeight: 700, color: 'text.primary', mb: 0.5 }}
          >
            {title}
          </Typography>
          {subtitle && (
            <Typography variant="body2" color="text.secondary">
              {subtitle}
            </Typography>
          )}
        </Box>
        {action && (
          <Button
            variant="contained"
            color="primary"
            startIcon={actionIcon}
            onClick={onAction}
            id="page-header-action-btn"
          >
            {action}
          </Button>
        )}
      </Box>
    </Box>
  );
};

export default PageHeader;
