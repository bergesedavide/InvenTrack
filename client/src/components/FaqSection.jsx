import React, { useState } from 'react';

const faqItems = [
  {
    question: 'Come funziona esattamente il Simulatore?',
    answer:
      'Il simulatore crea un "gemello digitale" (digital twin) del tuo magazzino reale. Puoi applicare variazioni ipotetiche (es. aumento dei costi di spedizione, picco di domanda improvviso) e vedere come reagirebbe il tuo inventario nei successivi 3-6 mesi senza toccare i dati reali.',
  },
  {
    question: 'I miei dati aziendali vengono usati per addestrare l\'AI?',
    answer:
      'Assolutamente no. Utilizziamo modelli privati (Private LLM). L\'intelligenza artificiale accede ai tuoi dati solo per rispondere alle tue domande specifiche e le tue informazioni non vengono mai condivise esternamente o usate per addestrare modelli globali.',
  },
  {
    question: 'Posso integrare InvenTrack con Shopify?',
    answer:
      'Sì, offriamo un\'integrazione nativa in 1-click con Shopify, WooCommerce, Magento e Amazon Seller Central dal piano Pro in su. Le scorte si sincronizzano in tempo reale.',
  },
];

const FaqSection = () => {
  const [openIndex, setOpenIndex] = useState(null);

  return (
    <section className="faq reveal">
      <h2 className="section-title">Domande Frequenti</h2>

      {faqItems.map((item, index) => {
        const isActive = openIndex === index;

        return (
          <div key={item.question} className={`faq-item ${isActive ? 'active' : ''}`}>
            <button
              className="faq-question"
              type="button"
              onClick={() => setOpenIndex(isActive ? null : index)}
            >
              {item.question}
              <span className="faq-icon">{isActive ? '−' : '+'}</span>
            </button>
            <div className="faq-answer">
              <p>{item.answer}</p>
            </div>
          </div>
        );
      })}
    </section>
  );
};

export default FaqSection;

