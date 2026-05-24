// file: src/pages/Dashboard.jsx
import React, { useState, useEffect } from 'react';
import Sidebar from '../components/dashboard/Sidebar';
import DashboardHome from '../components/dashboard/DashboardHome';
import ProductsTable from '../components/dashboard/ProductsTable';
import OrdersTable from '../components/dashboard/OrdersTable';
import AnalyticsPage from '../components/dashboard/AnalyticsPage';
import InfoPage from '../components/dashboard/InfoPage';

const API_BASE = 'https://wcwffjp7-5050.euw.devtunnels.ms';

const Dashboard = () => {
  const [activeSection, setActiveSection] = useState('home');
  const [products, setProducts] = useState([]);
  const [refreshKey, setRefreshKey] = useState(0);

  const fetchProducts = async () => {
    try {
      const response = await fetch(`${API_BASE}/products/`);
      const data = await response.json();
      console.log('Prodotti aggiornati:', data.length);
      setProducts(data);
    } catch (err) {
      console.error('Errore fetch prodotti:', err);
    }
  };

  // Fetch iniziale
  useEffect(() => {
    fetchProducts();
  }, []);
  
  useEffect(() => {
    const interval = setInterval(() => {
      fetchProducts();
    }, 5 * 60 * 1000);
    
    return () => clearInterval(interval);
  }, []);

  // Funzione per forzare refresh manuale
  const handleRefresh = () => {
    fetchProducts();
  };

  const renderContent = () => {
    switch (activeSection) {
      case 'home':
        return <DashboardHome products={products} onRefresh={handleRefresh} />;
      case 'products':
        return (
          <>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h1>Prodotti</h1>
            </div>
            <ProductsTable products={products} showFilters={true} onRefresh={handleRefresh} />
          </>
        );
      case 'orders':
        return (
          <>
            <h1>Ordini</h1>
            <OrdersTable />
          </>
        );
      case 'analytics':
        return <AnalyticsPage />;
      case 'info':
        return <InfoPage />;
      default:
        return <DashboardHome products={products} onRefresh={handleRefresh} />;
    }
  };

  return (
    <div className="dashboard-layout">
      <Sidebar active={activeSection} onChange={setActiveSection} />
      <div className="dashboard-content">
        {renderContent()}
      </div>
    </div>
  );
};

export default Dashboard;