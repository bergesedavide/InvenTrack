import React, { useState, useEffect } from 'react';

const API_BASE = 'https://wcwffjp7-5050.euw.devtunnels.ms/';

const InfoPage = () => {
  const [calendarData, setCalendarData] = useState(null);
  const [systemStatus, setSystemStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  const getToken = () => localStorage.getItem('access_token');

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Calendario
        const calRes = await fetch(`${API_BASE}/calendars/full`);
        const calData = await calRes.json();
        const parts = calData.date?.split(' ') || [];
        setCalendarData({ weekday: parts[0], date: parts[1]?.replace(/-/g, '/') });
        
        // Sistema
        const sysRes = await fetch(`${API_BASE}/system/status`);
        const sysData = await sysRes.json();
        setSystemStatus(sysData);
        
      } catch (error) {
        console.error('Errore fetch info:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const getStatusBadge = (status) => {
    const statusMap = {
      online: { label: '● Online', className: 'status-online' },
      offline: { label: '● Offline', className: 'status-offline' },
    };
    return statusMap[status] || statusMap.online;
  };

  if (loading) return <div className="info-page"><div className="loading-spinner">Caricamento...</div></div>;

  return (
    <div className="info-page">
      <h1>Informazioni di Sistema</h1>
      <p className="info-subtitle">Stato, documentazione e risorse per sviluppatori</p>

      <div className="info-grid">
        <div className="info-card"><div className="info-card-header"><span className="info-card-icon">📅</span><h3>Data Sistema</h3></div><div className="info-card-content">{calendarData ? (<div className="date-time-display"><div className="date-big"><span className="date-weekday">{calendarData.weekday}</span><span className="date-number">{calendarData.date?.split('/')[0]}</span></div><div className="date-details"><span>{calendarData.date}</span></div></div>) : <p>Caricamento...</p>}</div></div>

        <div className="info-card"><div className="info-card-header"><span className="info-card-icon">🖥️</span><h3>Stato Servizi</h3></div><div className="info-card-content"><div className="services-status"><div className="service-item"><span>Database</span><span className={getStatusBadge(systemStatus?.database).className}>{getStatusBadge(systemStatus?.database).label}</span></div><div className="service-item"><span>API Gateway</span><span className="status-online">● Online</span></div><div className="service-item"><span>Motore AI</span><span className={getStatusBadge(systemStatus?.aiEngine).className}>{getStatusBadge(systemStatus?.aiEngine).label}</span></div></div></div></div>

        <div className="info-card"><div className="info-card-header"><span className="info-card-icon">📊</span><h3>Performance</h3></div><div className="info-card-content"><div className="metrics-list"><div className="metric-item"><span className="metric-label">Uptime</span><span className="metric-value">{systemStatus?.uptime}</span></div><div className="metric-item"><span className="metric-label">Tempo di risposta medio</span><span className="metric-value">{systemStatus?.responseTime}</span></div><div className="metric-item"><span className="metric-label">Utenti attivi</span><span className="metric-value">{systemStatus?.activeUsers}</span></div><div className="metric-item"><span className="metric-label">Richieste totali</span><span className="metric-value">{systemStatus?.totalRequests?.toLocaleString()}</span></div></div></div></div>
      </div>
    </div>
  );
};

export default InfoPage;