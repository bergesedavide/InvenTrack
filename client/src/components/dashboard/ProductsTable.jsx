import React, { useState } from 'react';

const API_BASE = 'https://wcwffjp7-5050.euw.devtunnels.ms/';

const statusMap = {
  IN_STOCK: { label: 'Disponibile', className: 'ok' },
  LOW_STOCK: { label: 'Scorte basse', className: 'warning' },
  OUT_OF_STOCK: { label: 'Esaurito', className: 'danger' },
};

const ProductsTable = ({ products = [], showFilters = true, onRefresh }) => {
  const [selectedCategory, setSelectedCategory] = useState("ALL");
  const [searchTerm, setSearchTerm] = useState("");
  const [sortBy, setSortBy] = useState("name");
  const [sortOrder, setSortOrder] = useState("asc");
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);
  const [selectedProducts, setSelectedProducts] = useState([]);
  const [editingProduct, setEditingProduct] = useState(null);
  const [updating, setUpdating] = useState(false);

  // Categorie uniche (solo se products esiste)
  const categories = products.length > 0 ? ["ALL", ...new Set(products.map(p => p.category))] : ["ALL"];

  // Filtra prodotti
  let filteredProducts = [...products];
  
  if (selectedCategory !== "ALL") {
    filteredProducts = filteredProducts.filter(p => p.category === selectedCategory);
  }
  
  if (searchTerm) {
    filteredProducts = filteredProducts.filter(p => 
      p.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.id?.toString().toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.category?.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }

  // Ordina prodotti
  filteredProducts.sort((a, b) => {
    let aVal = a[sortBy];
    let bVal = b[sortBy];
    
    if (sortBy === "price" || sortBy === "stock") {
      aVal = Number(aVal);
      bVal = Number(bVal);
    } else {
      aVal = String(aVal || "").toLowerCase();
      bVal = String(bVal || "").toLowerCase();
    }
    
    if (aVal < bVal) return sortOrder === "asc" ? -1 : 1;
    if (aVal > bVal) return sortOrder === "asc" ? 1 : -1;
    return 0;
  });

  // Statistiche
  const stats = {
    total: products.length,
    lowStock: products.filter(p => p.stock <= 5 && p.stock > 0).length,
    outOfStock: products.filter(p => p.stock === 0).length,
    totalValue: products.reduce((sum, p) => sum + (p.price * p.stock), 0),
  };

  // Paginazione
  const totalPages = Math.ceil(filteredProducts.length / itemsPerPage);
  const paginatedProducts = filteredProducts.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  // Gestione selezione multipla
  const toggleSelectProduct = (productId) => {
    setSelectedProducts(prev => 
      prev.includes(productId) 
        ? prev.filter(id => id !== productId)
        : [...prev, productId]
    );
  };

  const toggleSelectAll = () => {
    if (selectedProducts.length === paginatedProducts.length) {
      setSelectedProducts([]);
    } else {
      setSelectedProducts(paginatedProducts.map(p => p.id));
    }
  };

  // Gestione ordinamento
  const handleSort = (column) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortBy(column);
      setSortOrder("asc");
    }
  };

  // Reset pagina quando cambiano filtri
  const handleFilterChange = (newCategory) => {
    setSelectedCategory(newCategory);
    setCurrentPage(1);
  };

  // Aggiornamento stock veloce via API
  const handleQuickStockUpdate = async (productId, newStock) => {
    if (newStock < 0) return;
    
    setUpdating(true);
    try {
      const token = getToken();
      const response = await fetch(`${API_BASE}/products/${productId}/stock`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ stock: newStock })
      });
      
      if (response.ok) {
        // Chiama onRefresh per ricaricare i dati dal parent
        if (onRefresh) {
          await onRefresh();
        }
        // Piccolo delay per dare tempo al refresh
        setTimeout(() => {
          setEditingProduct(null);
        }, 500);
      } else {
        const error = await response.json();
        console.error('Errore aggiornamento stock:', error);
        alert('Errore durante l\'aggiornamento dello stock');
        setEditingProduct(null);
      }
    } catch (err) {
      console.error('Errore di rete:', err);
      alert('Errore di connessione al server');
      setEditingProduct(null);
    } finally {
      setUpdating(false);
    }
  };

  // Export CSV
  const exportToCSV = () => {
    const headers = ["ID", "Nome", "Categoria", "Stock", "Prezzo", "Valore Totale"];
    const rows = filteredProducts.map(p => [
      p.id,
      p.name,
      p.category,
      p.stock,
      p.price,
      p.price * p.stock
    ]);
    
    const csvContent = [headers, ...rows].map(row => row.join(",")).join("\n");
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `prodotti_${new Date().toISOString().split("T")[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const getSortIcon = (column) => {
    if (sortBy !== column) return "↕️";
    return sortOrder === "asc" ? "↑" : "↓";
  };

  return (
    <div className="dashboard-card products-container">
      <div className="products-header">
        <h3>📦 Gestione Prodotti</h3>
        
        {/* Statistiche rapide */}
        <div className="products-stats-mini">
          <div className="stat-mini">
            <span className="stat-mini-label">Totale</span>
            <span className="stat-mini-value">{stats.total}</span>
          </div>
          <div className="stat-mini warning">
            <span className="stat-mini-label">Stock basso</span>
            <span className="stat-mini-value">{stats.lowStock}</span>
          </div>
          <div className="stat-mini danger">
            <span className="stat-mini-label">Esauriti</span>
            <span className="stat-mini-value">{stats.outOfStock}</span>
          </div>
          <div className="stat-mini">
            <span className="stat-mini-label">Valore</span>
            <span className="stat-mini-value">€{stats.totalValue.toLocaleString()}</span>
          </div>
        </div>
        
        <button onClick={onRefresh} className="action-btn" style={{ marginLeft: 'auto' }}>
          🔄 Aggiorna
        </button>
      </div>

      {/* Barra filtri e azioni */}
      <div className="products-filters-bar">
        <div className="products-search">
          <input
            type="text"
            placeholder="🔍 Cerca per nome, ID o categoria..."
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              setCurrentPage(1);
            }}
            className="search-input"
          />
        </div>
        
        <div className="products-filters">
          {showFilters && (
            <select
              value={selectedCategory}
              onChange={(e) => handleFilterChange(e.target.value)}
              className="category-filter"
            >
              {categories.map((cat, index) => (
                <option key={index} value={cat}>
                  {cat === "ALL" ? "📁 Tutte le categorie" : cat}
                </option>
              ))}
            </select>
          )}
          
          <button className="action-btn" onClick={exportToCSV}>
            📎 Esporta CSV
          </button>
          
          {selectedProducts.length > 0 && (
            <button className="action-btn danger">
              🗑️ Elimina ({selectedProducts.length})
            </button>
          )}
        </div>
      </div>

      {/* Tabella prodotti */}
      <div className="products-table-wrapper">
        {products.length === 0 ? (
          <div className="no-results-products">
            <span>📦</span>
            <p>Nessun prodotto disponibile.</p>
            <button onClick={onRefresh} className="clear-filters-btn">
              🔄 Aggiorna
            </button>
          </div>
        ) : (
          <table className="dashboard-table products-table">
            <thead>
              <tr>
                {showFilters && (
                  <th className="checkbox-col">
                    <input
                      type="checkbox"
                      checked={selectedProducts.length === paginatedProducts.length && paginatedProducts.length > 0}
                      onChange={toggleSelectAll}
                    />
                  </th>
                )}
                <th onClick={() => handleSort("name")} className="sortable">
                  Nome {getSortIcon("name")}
                </th>
                <th onClick={() => handleSort("category")} className="sortable">
                  Categoria {getSortIcon("category")}
                </th>
                <th onClick={() => handleSort("stock")} className="sortable stock-col">
                  Stock {getSortIcon("stock")}
                </th>
                <th onClick={() => handleSort("price")} className="sortable">
                  Prezzo {getSortIcon("price")}
                </th>
                <th>Valore Stock</th>
                <th>Stato</th>
              </tr>
            </thead>
            <tbody>
              {paginatedProducts.map((p) => {
                let status;
                if (p.stock === 0) {
                  status = statusMap["OUT_OF_STOCK"];
                } else if (p.stock <= 5) {
                  status = statusMap["LOW_STOCK"];
                } else {
                  status = statusMap["IN_STOCK"];
                }

                const stockValue = p.price * p.stock;

                return (
                  <tr key={p.id} className={selectedProducts.includes(p.id) ? "selected" : ""}>
                    {showFilters && (
                      <td className="checkbox-col">
                        <input
                          type="checkbox"
                          checked={selectedProducts.includes(p.id)}
                          onChange={() => toggleSelectProduct(p.id)}
                        />
                      </td>
                    )}
                    <td className="product-name-cell">
                      <div className="product-name-wrapper">
                        <span className="product-name">{p.name}</span>
                        <span className="product-id">#{p.id}</span>
                      </div>
                    </td>
                    <td>
                      <span className="category-badge">{p.category}</span>
                    </td>
                    <td className={`stock-cell ${p.stock <= 5 ? 'low-stock' : ''}`}>
                      {editingProduct === p.id ? (
                        <input
                          type="number"
                          defaultValue={p.stock}
                          onBlur={(e) => handleQuickStockUpdate(p.id, parseInt(e.target.value))}
                          onKeyPress={(e) => {
                            if (e.key === 'Enter') {
                              handleQuickStockUpdate(p.id, parseInt(e.target.value));
                            }
                          }}
                          autoFocus
                          disabled={updating}
                          className="stock-edit-input"
                        />
                      ) : (
                        <div className="stock-display">
                          <span className="stock-number">{p.stock}</span>
                          {p.stock <= 10 && p.stock > 0 && (
                            <span className="stock-warning-icon" style={{ marginLeft: '5px' }}>⚠️</span>
                          )}
                        </div>
                      )}
                    </td>
                    <td className="price-cell">€{p.price.toLocaleString()}</td>
                    <td className="value-cell">€{stockValue.toLocaleString()}</td>
                    <td>
                      <span className={`badge ${status.className}`}>
                        {status.label}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
        
        {paginatedProducts.length === 0 && products.length > 0 && (
          <div className="no-results-products">
            <span>🔍</span>
            <p>Nessun prodotto trovato con i filtri selezionati.</p>
            <button 
              className="clear-filters-btn"
              onClick={() => {
                setSearchTerm("");
                setSelectedCategory("ALL");
              }}
            >
              Cancella filtri
            </button>
          </div>
        )}
      </div>

      {/* Paginazione */}
      {totalPages > 1 && (
        <div className="products-pagination">
          <button
            onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
            disabled={currentPage === 1}
            className="pagination-btn"
          >
            ← Precedente
          </button>
          <div className="pagination-info">
            Pagina {currentPage} di {totalPages}
            <span className="total-items">
              ({filteredProducts.length} prodotti)
            </span>
          </div>
          <button
            onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
            disabled={currentPage === totalPages}
            className="pagination-btn"
          >
            Successiva →
          </button>
        </div>
      )}

      {/* Barra azioni rapide */}
      <div className="products-quick-actions">
        <button className="quick-action-btn" onClick={onRefresh}>
          🔄 Aggiorna dati
        </button>
        <button className="quick-action-btn">
          📦 Ordine automatico
        </button>
        <button className="quick-action-btn" onClick={exportToCSV}>
          📊 Report prodotti
        </button>
      </div>
    </div>
  );
};

export default ProductsTable;