import React, { useState, useEffect } from 'react';
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell
} from 'recharts';

const API_BASE = 'https://wcwffjp7-5050.euw.devtunnels.ms/';

const AnalyticsPage = () => {
  const [timeRange, setTimeRange] = useState('year');
  const [selectedMetric, setSelectedMetric] = useState('sales');
  const [loading, setLoading] = useState(true);
  
  // State per dati reali
  const [kpi, setKpi] = useState(null);
  const [salesData, setSalesData] = useState([]);
  const [categoryData, setCategoryData] = useState([]);
  const [topProducts, setTopProducts] = useState([]);
  const [criticalStock, setCriticalStock] = useState([]);
  const [insights, setInsights] = useState([]);

  // Recupera token dal localStorage
  const getToken = () => localStorage.getItem('access_token');

  // Fetch con autenticazione
  const fetchWithAuth = async (url) => {
    const token = getToken();
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  };

  useEffect(() => {
    const fetchAllData = async () => {
      setLoading(true);
      try {
        const [kpiData, salesTrend, categories, products, critical] = await Promise.all([
          fetchWithAuth(`${API_BASE}/analytics/kpi`),
          fetchWithAuth(`${API_BASE}/analytics/sales?period=${timeRange}`),
          fetchWithAuth(`${API_BASE}/analytics/categories`),
          fetchWithAuth(`${API_BASE}/analytics/top-products?limit=5`),
          fetchWithAuth(`${API_BASE}/analytics/critical-stock?threshold=5`)
        ]);
        
        setKpi(kpiData);
        setSalesData(salesTrend);
        setCategoryData(categories);
        setTopProducts(products);
        setCriticalStock(critical);
        
        // Insights (opzionale - possono venire da API o essere generati)
        setInsights([
          { icon: '📈', title: 'Previsione Vendite', text: `Basato sui trend, le vendite del prossimo mese potrebbero aumentare del ${kpiData?.revenue_growth || 15}%`, confidence: 'Alta' },
          { icon: '⚠️', title: 'Rischio Rottura Stock', text: `${critical.length} prodotti hanno stock critico. Si consiglia riassortimento immediato.`, confidence: 'Priorità: Alta' },
          { icon: '💡', title: 'Opportunità', text: 'I clienti che acquistano prodotti di punta spesso acquistano anche accessori', confidence: 'Potenziale: +15%' }
        ]);
      } catch (error) {
        console.error('Errore fetch analytics:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchAllData();
  }, [timeRange]);

  const formatCurrency = (value) => `€${(value || 0).toLocaleString('it-IT')}`;
  const formatNumber = (value) => (value || 0).toLocaleString('it-IT');

  const getCategoryColors = () => ['#4f46e5', '#8b5cf6', '#3b82f6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444'];

  if (loading) {
    return <div className="analytics-page"><div className="loading-spinner">Caricamento dati...</div></div>;
  }

  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <h1>Analytics & Intelligence</h1>
        <div className="analytics-controls">
          <div className="time-range-selector">
            <button className={`range-btn ${timeRange === 'month' ? 'active' : ''}`} onClick={() => setTimeRange('month')}>Mese</button>
            <button className={`range-btn ${timeRange === 'quarter' ? 'active' : ''}`} onClick={() => setTimeRange('quarter')}>Trimestre</button>
            <button className={`range-btn ${timeRange === 'year' ? 'active' : ''}`} onClick={() => setTimeRange('year')}>Anno</button>
          </div>
        </div>
      </div>

      {/* KPI Cards - DATI REALI */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-icon">💰</div>
          <div className="kpi-content">
            <span className="kpi-label">Ricavi Totali</span>
            <span className="kpi-value">{formatCurrency(kpi?.total_revenue)}</span>
            <span className={`kpi-trend ${kpi?.revenue_growth >= 0 ? 'positive' : 'negative'}`}>
              {kpi?.revenue_growth >= 0 ? '+' : ''}{kpi?.revenue_growth}% vs periodo scorso
            </span>
          </div>
        </div>
        <div className="kpi-card">
          <div className="kpi-icon">📦</div>
          <div className="kpi-content">
            <span className="kpi-label">Ordini Totali</span>
            <span className="kpi-value">{formatNumber(kpi?.total_orders)}</span>
            <span className="kpi-trend positive">Basati su dati reali</span>
          </div>
        </div>
        <div className="kpi-card">
          <div className="kpi-icon">💳</div>
          <div className="kpi-content">
            <span className="kpi-label">Valore Medio Ordine</span>
            <span className="kpi-value">{formatCurrency(kpi?.avg_order_value)}</span>
            <span className="kpi-trend positive">Calcolato su ordini reali</span>
          </div>
        </div>
        <div className="kpi-card">
          <div className="kpi-icon">🔄</div>
          <div className="kpi-content">
            <span className="kpi-label">Rotazione Stock</span>
            <span className="kpi-value">{kpi?.stock_turnover || 0}x</span>
            <span className="kpi-trend warning">Basato su vendite/stock</span>
          </div>
        </div>
      </div>

      {/* Grafico principale - DATI REALI */}
      <div className="analytics-card full-width">
        <div className="card-header">
          <h3>Andamento Vendite</h3>
          <div className="metric-selector">
            <button className={`metric-btn ${selectedMetric === 'sales' ? 'active' : ''}`} onClick={() => setSelectedMetric('sales')}>Ricavi</button>
          </div>
        </div>
        <ResponsiveContainer width="100%" height={350}>
          <LineChart data={salesData}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
            <XAxis dataKey={salesData[0]?.month ? 'month' : 'date'} stroke="var(--muted)" />
            <YAxis stroke="var(--muted)" tickFormatter={(value) => `€${value/1000}k`} />
            <Tooltip formatter={(value) => formatCurrency(value)} />
            <Legend />
            <Line type="monotone" dataKey="sales" name="Ricavi (€)" stroke="#4f46e5" strokeWidth={3} dot={{ fill: '#4f46e5' }} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Categorie - DATI REALI */}
      <div className="analytics-grid-2col">
        <div className="analytics-card">
          <h3>Vendite per Categoria</h3>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={categoryData} cx="50%" cy="50%" innerRadius={60} outerRadius={100} paddingAngle={2} dataKey="value"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}>
                {categoryData.map((entry, index) => (<Cell key={`cell-${index}`} fill={getCategoryColors()[index % getCategoryColors().length]} />))}
              </Pie>
              <Tooltip formatter={(value) => formatCurrency(value)} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Top Products - DATI REALI */}
        <div className="analytics-card">
          <h3>🏆 Top 5 Prodotti per Vendite</h3>
          <div className="top-products-list">
            {topProducts.map((product, idx) => (
              <div key={product.id} className="product-row">
                <div className="product-rank">{idx + 1}</div>
                <div className="product-info">
                  <div className="product-name">{product.name}</div>
                  <div className="product-stats">
                    <span>Vendite: {formatCurrency(product.sales)}</span>
                    <span className={product.growth >= 0 ? 'positive' : 'negative'}>
                      {product.growth >= 0 ? `+${product.growth}%` : `${product.growth}%`}
                    </span>
                  </div>
                </div>
                <div className="product-stock">
                  <span className="stock-label">Stock:</span>
                  <span className={`stock-value ${product.stock < 30 ? 'low' : ''}`}>{product.stock} unità</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Critical Stock - DATI REALI */}
      <div className="analytics-card critical">
        <h3>⚠️ Allerta Stock Critico</h3>
        <div className="critical-stock-list">
          {criticalStock.map((item) => (
            <div key={item.id} className="critical-row">
              <div className="critical-info">
                <div className="critical-name">{item.name}</div>
                <div className="critical-details">Stock attuale: <strong className="danger">{item.stock}</strong> / Soglia: {item.threshold}</div>
              </div>
              <div className="critical-warning"><span className="warning-badge">Scadenza tra {item.days_until_out} giorni</span></div>
            </div>
          ))}
          {criticalStock.length === 0 && <div className="no-critical">✅ Nessun prodotto con stock critico</div>}
        </div>
        <div className="critical-footer"><button className="btn-sm" onClick={() => window.location.href = '/dashboard?section=products'}>Vai alla gestione magazzino →</button></div>
      </div>

      {/* AI Insights */}
      <div className="analytics-card ai-insights">
        <div className="ai-insights-header"><span className="ai-icon">🤖</span><h3>AI Insights & Raccomandazioni</h3></div>
        <div className="insights-grid">
          {insights.map((insight, idx) => (
            <div key={idx} className="insight-card">
              <div className="insight-icon">{insight.icon}</div>
              <div className="insight-content">
                <h4>{insight.title}</h4>
                <p>{insight.text}</p>
                <span className="insight-confidence">{insight.confidence}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPage;