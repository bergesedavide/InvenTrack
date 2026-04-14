import React, { useState } from 'react';
import Sidebar from '../components/dashboard/Sidebar';
import SalesChart from '../components/dashboard/SalesChart';
import ProductsTable from '../components/dashboard/ProductsTable';

import { salesData, products } from '../data/mockData';

const Dashboard = () => {
  const [activeSection, setActiveSection] = useState('home');

  const renderContent = () => {
    switch (activeSection) {
      case 'home':
        return (
          <>
            <h1>Dashboard</h1>

            <div className="dashboard-grid">
              <SalesChart data={salesData} />
              <ProductsTable products={products.slice(0, 4)} />
            </div>
          </>
        );

      case 'products':
        return (
          <>
            <h1>Prodotti</h1>
            <ProductsTable products={products} />
          </>
        );

      case 'orders':
        return <h1>Ordini (in arrivo)</h1>;

      case 'analytics':
        return <h1>Analytics (in arrivo)</h1>;

      case 'settings':
        return <h1>Impostazioni (in arrivo)</h1>;

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