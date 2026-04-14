import React from 'react';

const CtaSection = ({ onOpenAuth }) => (
  <section className="cta reveal">
    <h2>Pronto a parlare con il tuo inventario?</h2>
    <p style={{ marginBottom: 30, fontSize: 18 }}>
      Unisciti a oltre 2.000 aziende che hanno smesso di indovinare e iniziato a prevedere.
    </p>
    <button
      type="button"
      className="btn-outline"
      onClick={() => onOpenAuth?.('register')}
    >
      Crea Account Gratuito
    </button>
  </section>
);

export default CtaSection;

