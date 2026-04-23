import React, { useState, useEffect } from 'react';

const InfoPage = () => {
  const [calendarData, setCalendarData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:5050/calendars/full')
      .then(res => {
        if (!res.ok) {
          throw new Error('Errore nella risposta del server');
        }
        return res.json();
      })
      .then(data => {
        const raw = data.date; // "LUNEDI 18-02-2026"

        if (!raw) throw new Error('Dato mancante');

        const parts = raw.split(' ');

        if (parts.length !== 2) {
          throw new Error('Formato data non valido');
        }

        const weekday = parts[0];
        const date = parts[1].replace(/-/g, '/');

        setCalendarData({ weekday, date });
      })
      .catch(err => {
        console.error('Errore calendario:', err);
        setError(err.message);
      });
  }, []);

  return (
    <div className="info-page">
      <div className="dashboard-card">
        <h3>Data corrente</h3>

        {error && <p style={{ color: 'red' }}>{error}</p>}

        {calendarData ? (
          <div className="date-display">
            <span className="badge ok">{calendarData.weekday}</span> <span className="date-full">{calendarData.date}</span>
          </div>
        ) : !error ? (
          <p>Caricamento...</p>
        ) : null}
      </div>
    </div>
  );
};

export default InfoPage;