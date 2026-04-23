import React, { useState, useEffect } from 'react';
import Sidebar from '../components/dashboard/Sidebar';
import SalesChart from '../components/dashboard/SalesChart';
import ProductsTable from '../components/dashboard/ProductsTable';
import InfoPage from '../components/dashboard/InfoPage';

import { salesData } from '../data/mockData';

const Dashboard = () => {
  const [activeSection, setActiveSection] = useState('home');
  const [products, setProducts] = useState([]);

  useEffect(() => {
    //fetch('http://127.0.0.1:5050/products/subscription')
    fetch('http://127.0.0.1:5050/products')
      .then(res => res.json())
      .then(data => {
        const normalized = (Array.isArray(data) ? data : [data]).map(p => ({
          ...p,
          //stock: p.stock ?? 0
          stock: Math.floor(Math.random() * 15) // fake
        }));

        setProducts(normalized);
      })
      .catch(err => console.error(err));
  }, []);

  const renderContent = () => {
    switch (activeSection) {
      case 'home':
        const sortedProducts = [...products]
          .sort((a, b) => a.stock - b.stock)
          .slice(0, 5); 
        return (
          <>
            <h1>Dashboard</h1>

            <div className="dashboard-grid">
              <SalesChart data={salesData} />
              <ProductsTable products={sortedProducts} showFilters={false} />
            </div>
          </>
        );

      case 'products':
        return (
          <>
            <h1>Prodotti</h1>
            <ProductsTable products={products} showFilters={true} />
          </>
        );

      case 'orders':
        return <h1>Ordini (in arrivo)</h1>;

      case 'analytics':
        return <h1>Analytics (in arrivo)</h1>;

      case 'info':
        return (
          <>
            <h1>Informazioni</h1>
            <InfoPage />
          </>
        );

      default:
        return <h1>Dashboard</h1>;
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