import React from 'react';

const PricingSection = () => (
  <section id="pricing" className="pricing reveal">
    <h2 className="section-title">Inizia a simulare il tuo successo</h2>
    <p className="section-subtitle">Scegli il piano adatto al volume del tuo business.</p>

    <div className="pricing-grid">
      <div className="pricing-card">
        <h3>Starter</h3>
        <div className="price">
          €0<span>/mese</span>
        </div>
        <p style={{ color: 'var(--muted)' }}>Perfetto per testare la piattaforma.</p>
        <ul className="pricing-features">
          <li>✔️ Fino a 500 prodotti</li>
          <li>✔️ Gestione inventario base</li>
          <li>✔️ Dashboard standard</li>
          <li>❌ Chatbot AI e Simulatore</li>
        </ul>
        <a href="#" className="btn-outline">
          Inizia Gratis
        </a>
      </div>

      <div className="pricing-card popular">
        <div className="badge" style={{ margin: '0 auto 15px' }}>
          Più Scelto
        </div>
        <h3>Pro Intelligence</h3>
        <div className="price">
          €49<span>/mese</span>
        </div>
        <p style={{ color: 'var(--muted)' }}>Per aziende che vogliono scalare.</p>
        <ul className="pricing-features">
          <li>✔️ Prodotti illimitati</li>
          <li>
            ✔️ <b>Accesso completo al Simulatore</b>
          </li>
          <li>
            ✔️ <b>1.000 prompt mensili per AI Chatbot</b>
          </li>
          <li>✔️ Integrazioni API e-commerce</li>
        </ul>
        <a href="#" className="btn-primary" style={{ width: '100%', justifyContent: 'center' }}>
          Prova Pro
        </a>
      </div>

      <div className="pricing-card">
        <h3>Enterprise</h3>
        <div className="price">
          €199<span>/mese</span>
        </div>
        <p style={{ color: 'var(--muted)' }}>Simulazioni avanzate e AI illimitata.</p>
        <ul className="pricing-features">
          <li>✔️ Tutto il piano Pro</li>
          <li>✔️ Modelli AI addestrati sui tuoi dati</li>
          <li>✔️ Analisi predittiva del mercato</li>
          <li>✔️ Account manager dedicato</li>
        </ul>
        <a href="#" className="btn-outline">
          Contatta Vendite
        </a>
      </div>
    </div>
  </section>
);

export default PricingSection;

