import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const API_BASE = 'https://wcwffjp7-5050.euw.devtunnels.ms';

const SalesChart = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_BASE}/analytics/sales?period=year`);
        const salesData = await response.json();
        setData(salesData);
      } catch (error) {
        console.error('Errore fetch sales:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="dashboard-card"><h3>Andamento vendite</h3><div>Caricamento...</div></div>;

  return (
    <div className="dashboard-card">
      <h3>Andamento vendite</h3>
      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={data}>
          <XAxis dataKey={data[0]?.date ? 'date' : 'month'} stroke="var(--muted)" fontSize={12}/>
          <YAxis stroke="var(--muted)" fontSize={12} tickFormatter={(value) => `€${(value / 1000).toFixed(0)}k`}/>
          <Tooltip formatter={(value) => `€${value}`} contentStyle={{ backgroundColor: 'var(--surface)', borderColor: 'var(--border)' }} />
          <Line type="monotone" dataKey="sales" stroke="#4f46e5" strokeWidth={3} dot={{ fill: '#4f46e5', r: 4 }} activeDot={{ r: 6 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SalesChart;