import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';

const AreaChartWidget = ({
  title,
  data = [],
  dataKeys = [],
  colors = ['#4CAF50', '#2196F3'],
  height = 280,
  subtitle,
}) => {
  return (
    <Card sx={{ height: '100%' }}>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h6" fontWeight={600} gutterBottom>
          {title}
        </Typography>
        {subtitle && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {subtitle}
          </Typography>
        )}
        <ResponsiveContainer width="100%" height={height}>
          <AreaChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
            <defs>
              {dataKeys.map((key, i) => (
                <linearGradient key={key} id={`gradient-${key}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={colors[i] || '#4CAF50'} stopOpacity={0.3} />
                  <stop offset="95%" stopColor={colors[i] || '#4CAF50'} stopOpacity={0} />
                </linearGradient>
              ))}
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.06)" />
            <XAxis
              dataKey="name"
              tick={{ fontSize: 12, fill: '#9E9E9E' }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              tick={{ fontSize: 12, fill: '#9E9E9E' }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip
              contentStyle={{
                borderRadius: 10,
                border: 'none',
                boxShadow: '0 4px 20px rgba(0,0,0,0.15)',
                fontSize: 13,
              }}
            />
            {dataKeys.length > 1 && <Legend />}
            {dataKeys.map((key, i) => (
              <Area
                key={key}
                type="monotone"
                dataKey={key}
                stroke={colors[i] || '#4CAF50'}
                strokeWidth={2.5}
                fill={`url(#gradient-${key})`}
                dot={{ r: 4, fill: colors[i] || '#4CAF50', strokeWidth: 2, stroke: '#fff' }}
                activeDot={{ r: 6 }}
              />
            ))}
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};

export default AreaChartWidget;
