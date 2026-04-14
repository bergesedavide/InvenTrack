import React from 'react';

const Header = ({ onOpenAuth }) => (
  <header>
    <div className="container">
      <nav>
        <div className="logo">
          <a href="#">InvenTrack</a>
        </div>
        <div className="nav-actions">
          <button className="theme-toggle" id="theme-btn" aria-label="Cambia tema">
            🌙
          </button>
          <a href="#pricing" className="btn-outline">
            Prezzi
          </a>
          <button
            type="button"
            className="btn-primary"
            onClick={() => onOpenAuth?.('login')}
          >
            Accedi al simulatore
          </button>
        </div>
      </nav>
    </div>
  </header>
);

export default Header;

