import React from 'react';

const HeroSection = ({ onOpenAuth }) => (
  <section className="hero reveal">
    <div className="badge">L&apos;Inventario Incontra l&apos;Intelligenza Artificiale ✨</div>
    <h1>
      La nuova generazione
      <br />
      di gestione inventario
    </h1>
    <p>
      Non solo un gestionale, ma un vero e proprio ambiente di simulazione. Prevedi il mercato, chatta
      con i tuoi dati e ottimizza le scorte prima che si esauriscano.
    </p>

    <div className="hero-buttons">
      <button
        type="button"
        className="btn-primary"
        onClick={() => onOpenAuth?.('register')}
      >
        Inizia la simulazione
        <span>→</span>
      </button>
    </div>

    <div className="dashboard-mockup reveal">
      <div className="mockup-header">
        <div className="mockup-dot" />
        <div className="mockup-dot" />
        <div className="mockup-dot" />
      </div>
      <div className="mockup-grid">
        <div className="mockup-card">
          <p>Prodotti Attivi</p>
          <h4 className="counter" data-target="12450">
            0
          </h4>
        </div>
        <div className="mockup-card">
          <p>Previsione Rottura Stock</p>
          <h4 style={{ color: '#ef4444' }}>
            <span className="counter" data-target="14">
              0
            </span>{' '}
            gg
          </h4>
        </div>
        <div className="mockup-card">
          <p>Fiducia AI sui Trend</p>
          <h4>
            <span className="counter" data-target="96">
              0
            </span>
            %
          </h4>
        </div>
      </div>
    </div>
  </section>
);

export default HeroSection;

