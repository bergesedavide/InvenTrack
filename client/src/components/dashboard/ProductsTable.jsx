import React from 'react';

const statusMap = {
  IN_STOCK: { label: 'Disponibile', className: 'ok' },
  LOW_STOCK: { label: 'Scorte basse', className: 'warning' },
  OUT_OF_STOCK: { label: 'Esaurito', className: 'danger' },
};

const ProductsTable = ({ products }) => {
  return (
    <div className="dashboard-card">
      <h3>Gestione Prodotti</h3>

      <table className="dashboard-table">
        <thead>
          <tr>
            <th>Nome</th>
            <th>Stock</th>
            <th>Prezzo</th>
            <th>Stato</th>
          </tr>
        </thead>

        <tbody>
          {products.map((p) => {
            const status = statusMap[p.status];

            return (
              <tr key={p.id}>
                <td>{p.name}</td>
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