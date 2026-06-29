import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Cell,
} from 'recharts';

const BarChartWidget = ({
  title,
  data = [],
  dataKeys = [],
  colors = ['#4CAF50', '#2196F3', '#FF8F00'],
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
          <BarChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.06)" vertical={false} />
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
              <Bar
                key={key}
                dataKey={key}
                fill={colors[i] || '#4CAF50'}
                radius={[6, 6, 0, 0]}
                maxBarSize={50}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};

export default BarChartWidget;
