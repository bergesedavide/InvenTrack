import React from 'react';

const Sidebar = ({ active, onChange }) => {
  const menu = [
    { id: 'home', label: 'Dashboard' },
    { id: 'products', label: 'Prodotti' },
    { id: 'orders', label: 'Ordini' },
    { id: 'analytics', label: 'Analytics' },
    { id: 'info', label: 'Informazioni' },
  ];

  return (
    <div className="sidebar">
      <h2 className="sidebar-logo">InvenTrack</h2>

      <ul className="sidebar-menu">
        {menu.map((item) => (
          <li
            key={item.id}
            className={active === item.id ? 'active' : ''}
            onClick={() => onChange(item.id)}
          >
            {item.label}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;