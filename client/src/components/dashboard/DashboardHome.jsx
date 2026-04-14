import React from 'react';

const DashboardHome = () => {
  return (
    <div>
      <h1>Dashboard</h1>

      <div className="dashboard-cards">
        <div className="dashboard-card">
          <p>Prodotti</p>
          <h2>1,245</h2>
        </div>

        <div className="dashboard-card">
          <p>Ordini oggi</p>
          <h2>87</h2>
        </div>

        <div className="dashboard-card">
          <p>Fatturato</p>
          <h2>€12,340</h2>
        </div>

        <div className="dashboard-card">
          <p>Stock critico</p>
          <h2 style={{ color: 'red' }}>12</h2>
        </div>
      </div>
    </div>
  );
};

export default DashboardHome;