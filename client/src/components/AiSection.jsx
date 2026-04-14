import React from 'react';

const AiSection = () => (
  <section className="ai-section reveal">
    <h2 className="section-title">Più intelligente di un foglio di calcolo</h2>
    <p className="section-subtitle">
      Scopri il motore neurale che trasforma dati grezzi in decisioni strategiche per il tuo e-commerce o
      negozio fisico.
    </p>

    <div className="ai-grid">
      <div className="ai-card">
        <h3>🕹️ Simulatore di Scenari</h3>
        <p>
          Cosa succede se aumenti i prezzi del 10% sotto Natale? Crea un ambiente <b>sandbox senza rischi</b>{' '}
          e lascia che InvenTrack simuli l&apos;impatto su vendite e giacenze in pochi secondi.
        </p>
      </div>
      <div className="ai-card" style={{ transitionDelay: '0.1s' }}>
        <h3>💬 AI Chatbot Integrato</h3>
        <p>
          Smetti di cercare nei menu. Chiedi semplicemente all&apos;AI:{' '}
          <i>&quot;Qual è il prodotto meno venduto nel Q3?&quot;</i> o{' '}
          <i>&quot;Mostrami i clienti che comprano scarpe rosse&quot;</i> e ottieni risposte in linguaggio
          naturale.
        </p>
      </div>
      <div className="ai-card" style={{ transitionDelay: '0.2s' }}>
        <h3>📈 Analisi Predittiva</h3>
        <p>
          L&apos;algoritmo analizza lo storico aziendale, la stagionalità e i trend di mercato esterni per
          dirti esattamente <b>quando e quanto riassortire</b>, minimizzando i costi di magazzino.
        </p>
      </div>
    </div>
  </section>
);

export default AiSection;

