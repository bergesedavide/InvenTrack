import React, { useState } from 'react';

const statusMap = {
  IN_STOCK: { label: 'Disponibile', className: 'ok' },
  LOW_STOCK: { label: 'Scorte basse', className: 'warning' },
  OUT_OF_STOCK: { label: 'Esaurito', className: 'danger' },
};

const ProductsTable = ({ products, showFilters }) => {
  const [selectedCategory, setSelectedCategory] = useState("ALL");

  // 🔥 prendo categorie uniche
  const categories = ["ALL", ...new Set(products.map(p => p.category))];

  // 🔥 filtro prodotti
  const filteredProducts =
    selectedCategory === "ALL"
      ? products
      : products.filter(p => p.category === selectedCategory);

  return (
    <div className="dashboard-card">
      <h3>Gestione Prodotti</h3>

      {categories.length > 2 && showFilters && (
        <div style={{ marginBottom: "10px" }}>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
          >
            {categories.map((cat, index) => (
              <option key={index} value={cat}>
                {cat === "ALL" ? "Tutte le categorie" : cat}
              </option>
            ))}
          </select>
        </div>
      )}

      <table className="dashboard-table">
        <thead>
          <tr>
            <th>Nome</th>
            <th>Categoria</th>
            <th>Stock</th>
            <th>Prezzo</th>
            <th>Stato</th>
          </tr>
        </thead>

        <tbody>
          {filteredProducts.map((p) => {
            let status;

            if (p.stock === 0) {
              status = statusMap["OUT_OF_STOCK"];
            } else if (p.stock <= 5) {
              status = statusMap["LOW_STOCK"];
            } else {
              status = statusMap["IN_STOCK"];
            }

            return (
              <tr key={p.id}>
                <td>{p.name}</td>
                <td>{p.category}</td>
                <td>{p.stock}</td>
                <td>€{p.price}</td>
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
    </div>
  );
};

export default ProductsTable;