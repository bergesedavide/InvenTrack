import React, { useState, useEffect } from 'react';

const API_BASE = 'https://wcwffjp7-5050.euw.devtunnels.ms/';

const statusMap = {
  PENDING: { label: 'In elaborazione', className: 'warning' },
  PROCESSING: { label: 'In preparazione', className: 'info' },
  SHIPPED: { label: 'Spedito', className: 'ok' },
  DELIVERED: { label: 'Consegnato', className: 'success' },
  CANCELLED: { label: 'Annullato', className: 'danger' },
};

const OrdersTable = () => {
  const [orders, setOrders] = useState([]);
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await fetch(`${API_BASE}/orders`);
        const data = await response.json();
        setOrders(data);
      } catch (err) {
        console.error('Errore fetch ordini:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchOrders();
  }, []);

  const statuses = ["ALL", "PENDING", "PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"];

  const filteredOrders = orders.filter(order => {
    const matchesStatus = statusFilter === "ALL" || order.status === statusFilter;
    const matchesSearch = searchTerm === "" || 
      (order.codice || '').toLowerCase().includes(searchTerm.toLowerCase());
    return matchesStatus && matchesSearch;
  });

  const stats = {
    total: orders.length,
    pending: orders.filter(o => o.status === "PENDING").length,
    shipped: orders.filter(o => o.status === "SHIPPED").length,
    delivered: orders.filter(o => o.status === "DELIVERED").length,
    totalRevenue: orders.reduce((sum, o) => sum + (o.totale || 0), 0),
  };

  const formatPrice = (price) => `€${(price || 0).toLocaleString('it-IT')}`;

  if (loading) return <div className="dashboard-card orders-container"><div className="loading-spinner">Caricamento ordini...</div></div>;

  return (
    <div className="dashboard-card orders-container">
      <div className="orders-header">
        <h3>Gestione Ordini</h3>
        <div className="orders-stats">
          <div className="stat-item"><span className="stat-label">Totale ordini</span><span className="stat-value">{stats.total}</span></div>
          <div className="stat-item"><span className="stat-label">In attesa</span><span className="stat-value warning">{stats.pending}</span></div>
          <div className="stat-item"><span className="stat-label">Spediti</span><span className="stat-value info">{stats.shipped}</span></div>
          <div className="stat-item"><span className="stat-label">Ricavi totali</span><span className="stat-value">{formatPrice(stats.totalRevenue)}</span></div>
        </div>
      </div>

      <div className="orders-filters">
        <div className="search-box"><input type="text" placeholder="Cerca per ID ordine..." value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} className="search-input" /></div>
        <div className="filter-buttons">{statuses.map(status => (<button key={status} className={`filter-chip ${statusFilter === status ? 'active' : ''}`} onClick={() => setStatusFilter(status)}>{status === "ALL" ? "Tutti" : statusMap[status]?.label || status}</button>))}</div>
      </div>

      <div className="orders-table-wrapper">
        <table className="dashboard-table orders-table">
          <thead><tr><th>ID Ordine</th><th>Totale</th><th>Data</th><th>Stato</th></tr></thead>
          <tbody>
            {filteredOrders.map((order) => (<tr key={order.id}><td className="order-id">{order.codice}</td><td>{formatPrice(order.totale)}</td><td>{order.data}</td><td><span className={`badge ${statusMap[order.status]?.className || ''}`}>{statusMap[order.status]?.label || order.status}</span></td></tr>))}
          </tbody>
        </table>
        {filteredOrders.length === 0 && (<div className="no-results">Nessun ordine trovato con i filtri selezionati.</div>)}
      </div>
    </div>
  );
};

export default OrdersTable;