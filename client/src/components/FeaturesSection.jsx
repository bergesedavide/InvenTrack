import React from 'react';

const FeaturesSection = () => (
  <section className="features reveal">
    <h2 className="section-title">Le basi, eseguite alla perfezione</h2>

    <div className="feature-grid">
      <div className="feature-card">
        <div className="feature-icon">📦</div>
        <h3>Gestione Multimagazzino</h3>
        <p>Sincronizza scorte fisiche e digitali su più sedi contemporaneamente.</p>
      </div>
      <div className="feature-card">
        <div className="feature-icon">👥</div>
        <h3>CRM Integrato</h3>
        <p>Associa ogni movimento di inventario al cliente per uno storico completo.</p>
      </div>
      <div className="feature-card">
        <div className="feature-icon">⚡</div>
        <h3>Integrazione API</h3>
        <p>Collega Shopify, WooCommerce, Amazon e la tua fatturazione in 1 click.</p>
      </div>
      <div className="feature-card">
        <div className="feature-icon">🔒</div>
        <h3>Sicurezza Dati</h3>
        <p>Attraverso dei backup orari i tuoi dati strategici sono al sicuro.</p>
      </div>
    </div>
  </section>
);

export default FeaturesSection;

