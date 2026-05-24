import React, { useState, useEffect } from 'react';
import SalesChart from './SalesChart';
import ProductsTable from './ProductsTable';

const API_BASE = 'https://wcwffjp7-5050.euw.devtunnels.ms/';

const DashboardHome = ({ products, onRefresh }) => {
  const [calendarData, setCalendarData] = useState(null);
  const [kpi, setKpi] = useState(null);
  const [recentActivities, setRecentActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchKPI = async () => {
      try {
        const kpiData = await fetch(`${API_BASE}/analytics/kpi`)
                              .then(data => data.json());
        setKpi(kpiData);
        
        const orders = await fetch(`${API_BASE}/orders?limit=5`)
                              .then(data => data.json());
        const activities = orders.map(o => ({ 
          id: o.id, 
          type: 'order', 
          message: `Nuovo ordine #${o.codice} - €${o.totale}`, 
          time: o.data 
        }));
        setRecentActivities(activities.slice(0, 5));

        const calData = await fetch(`${API_BASE}/calendars/full`)
                              .then(data => data.json());
        setCalendarData(calData);
      } catch (error) {
        console.error('Errore fetch dashboard:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchKPI();
  }, []);

  const formatCurrency = (value) => `€${(value || 0).toLocaleString('it-IT')}`;
  const formatNumber = (value) => (value || 0).toLocaleString('it-IT');

  const criticalStockProducts = (products || []).filter(p => p.stock <= 5).slice(0, 4);
  const topStockProducts = (products || []).sort((a, b) => b.stock - a.stock).slice(0, 5);
  const lowStockProducts = (products || []).sort((a, b) => a.stock - b.stock).slice(0, 5);
  const totalStockValue = (products || []).reduce((sum, p) => sum + (p.price * p.stock), 0);

  const getSimulatedDate = () => {
    if (!calendarData?.date) return 'Caricamento...';
    
    const parts = calendarData.date.split(' ');
    if (parts.length === 2) {
      return `${parts[0]} ${parts[1]}`;
    }
    return calendarData.date;
  };

  if (loading) return <div className="dashboard-home"><div className="loading-spinner">Caricamento dashboard...</div></div>;

  return (
    <div className="dashboard-home">
      <div className="dashboard-header">
        <div className="welcome-section">
          <h1>Dashboard</h1>
          <p>Panoramica generale del tuo business</p>
        </div>
        <div style={{ textAlign: 'right' }}>
            <div className="current-date" style={{ fontSize: '14px', fontWeight: '500' }}>
              📅 {getSimulatedDate()}
            </div>
          </div>
      </div>

      {/* KPI Cards */}
      <div className="kpi-dashboard-grid">
        <div className="kpi-dashboard-card">
          <div className="kpi-icon-wrapper revenue"><span className="kpi-icon">💰</span></div>
          <div className="kpi-info">
            <span className="kpi-label">Fatturato Totale</span>
            <span className="kpi-value">{formatCurrency(kpi?.total_revenue)}</span>
            <span className="kpi-trend positive">↑ Dati reali</span>
          </div>
        </div>
        <div className="kpi-dashboard-card">
          <div className="kpi-icon-wrapper orders"><span className="kpi-icon">📦</span></div>
          <div className="kpi-info">
            <span className="kpi-label">Ordini Totali</span>
            <span className="kpi-value">{formatNumber(kpi?.total_orders)}</span>
            <span className="kpi-trend positive">↑ Dati reali</span>
          </div>
        </div>
        <div className="kpi-dashboard-card">
          <div className="kpi-icon-wrapper customers"><span className="kpi-icon">💳</span></div>
          <div className="kpi-info">
            <span className="kpi-label">Valore Medio Ordine</span>
            <span className="kpi-value">{formatCurrency(kpi?.avg_order_value)}</span>
            <span className="kpi-trend positive">↑ Calcolato</span>
          </div>
        </div>
        <div className="kpi-dashboard-card">
          <div className="kpi-icon-wrapper stock"><span className="kpi-icon">🏪</span></div>
          <div className="kpi-info">
            <span className="kpi-label">Valore Magazzino</span>
            <span className="kpi-value">{formatCurrency(totalStockValue)}</span>
            <span className="kpi-trend neutral">Stock totale</span>
          </div>
        </div>
      </div>

      {/* Grafici */}
      <div className="dashboard-grid">
        <SalesChart />
        <ProductsTable products={lowStockProducts} showFilters={false} onRefresh={onRefresh} />
      </div>

      {/* Stock Critico */}
      {criticalStockProducts.length > 0 && (
        <div className="stock-alert-card">
          <div className="alert-header">
            <span className="alert-icon">⚠️</span>
            <h3>Allerta Stock Critico</h3>
            <span className="alert-count">{criticalStockProducts.length} prodotti a rischio</span>
          </div>
          <div className="critical-stock-list">
            {criticalStockProducts.map((product) => (
              <div key={product.id} className="critical-stock-item">
                <div className="critical-info">
                  <span className="critical-name">{product.name}</span>
                  <span className="critical-code">ID: {product.id}</span>
                </div>
                <div className="critical-stock-value">
                  <span className={`stock-number ${product.stock === 0 ? 'danger' : 'warning'}`}>
                    {product.stock === 0 ? 'ESAURITO' : `${product.stock} rimasti`}
                  </span>
                  <span className="stock-threshold">Soglia minima: 5</span>
                </div>
                <button className="reorder-btn" onClick={onRefresh}>🔄 Aggiorna</button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Top Stock e Attività */}
      <div className="dashboard-grid-2col">
        <div className="dashboard-analytics-card">
          <div className="card-header"><h3>📦 Prodotti con più stock</h3></div>
          <div className="top-products-list">
            {topStockProducts.map((product, idx) => (
              <div key={product.id} className="top-product-item">
                <div className="product-rank">{idx + 1}</div>
                <div className="product-details">
                  <div className="product-name">{product.name}</div>
                  <div className="product-stats">
                    <span>{product.category}</span>
                    <span>{formatCurrency(product.price)}</span>
                  </div>
                </div>
                <div className="product-stock-info">
                  <span className="stock-label">Stock:</span>
                  <span className="stock-value">{product.stock} unità</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="dashboard-analytics-card">
          <div className="card-header">
            <h3>🔄 Attività recenti</h3>
            <button className="view-all-btn" onClick={() => window.location.href = '/dashboard?section=orders'}>Vedi tutti →</button>
          </div>
          <div className="activities-list">
            {recentActivities.map((activity) => (
              <div key={activity.id} className={`activity-item ${activity.type}`}>
                <div className="activity-icon">{activity.type === 'order' ? '🛒' : '⚠️'}</div>
                <div className="activity-content">
                  <p className="activity-message">{activity.message}</p>
                  <span className="activity-time">{activity.time}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* AI Assistant */}
      <div className="dashboard-analytics-card ai-assistant">
        <div className="ai-assistant-header">
          <span className="ai-avatar">🤖</span>
          <div>
            <h3>AI Assistant</h3>
            <p>Domande frequenti sui tuoi dati</p>
          </div>
        </div>
        <div className="ai-suggestions">
          <div className="ai-suggestion">
            <span className="suggestion-icon">📊</span>
            <div className="suggestion-text">
              <strong>Previsione stock</strong>
              <p>Prodotti con stock basso: {criticalStockProducts.length}</p>
            </div>
          </div>
          <div className="ai-suggestion">
            <span className="suggestion-icon">💡</span>
            <div className="suggestion-text">
              <strong>Suggerimento</strong>
              <p>Qual è il prodotto meno venduto? Chiedimi in chat!</p>
            </div>
          </div>
        </div>
        <div className="ai-chat-input">
          <input type="text" placeholder="Es: Quali prodotti hanno stock basso?" />
          <button>Invia</button>
        </div>
      </div>
    </div>
  );
};

export default DashboardHome;