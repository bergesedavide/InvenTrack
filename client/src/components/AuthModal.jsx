import React, { useEffect, useState } from 'react';

const AuthModal = ({ open, initialMode = 'login', onClose }) => {
  const [mode, setMode] = useState(initialMode);
  const [step, setStep] = useState(1);

  // Login state
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);

  // Registrazione – step 1: titolare
  const [ownerLastName, setOwnerLastName] = useState('');
  const [ownerFirstName, setOwnerFirstName] = useState('');
  const [ownerEmail, setOwnerEmail] = useState('');
  const [registerPassword, setRegisterPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [birthDate, setBirthDate] = useState('');
  const [birthCountry, setBirthCountry] = useState('');

  // Registrazione – step 2: azienda
  const [companyName, setCompanyName] = useState('');
  const [companyDescription, setCompanyDescription] = useState('');
  const [plan, setPlan] = useState('starter'); // starter | pro | enterprise
  const [companyEmail, setCompanyEmail] = useState('');
  const [companyPhone, setCompanyPhone] = useState('');
  const [proAiChoice, setProAiChoice] = useState('chatbot'); // chatbot | bi
  const [proAddonChoice, setProAddonChoice] = useState('price_control'); // price_control | mobile_app
  const [logoFile, setLogoFile] = useState(null);

  // Registrazione – step 3: pagamento
  const [paymentMethod, setPaymentMethod] = useState('card'); // card | iban

  // carta
  const [cardHolder, setCardHolder] = useState('');
  const [cardNumber, setCardNumber] = useState('');
  const [cardExpiry, setCardExpiry] = useState('');
  const [cardCvv, setCardCvv] = useState('');

  // iban
  const [iban, setIban] = useState('');

  const [error, setError] = useState('');

  useEffect(() => {
    if (open) {
      setMode(initialMode);
      setStep(1);
      setError('');
    }
  }, [open, initialMode]);

  if (!open) return null;

  const isLogin = mode === 'login';

  const switchMode = (nextMode) => {
    setMode(nextMode);
    setStep(1);
    setError('');
  };

  const handleLoginSubmit = async (event) => {
    event.preventDefault();
    setError('');

    if (!loginEmail || !loginPassword) {
      setError('Inserisci email e password per accedere.');
      return;
    }

    const payload = {
      email: loginEmail,
      password: loginPassword,
    };

    try {
      const response = await fetch('http://localhost:5050/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.message || 'Errore durante il login');
        return;
      }

      // Salva il token (es. localStorage se rememberMe è attivo)
      /*
      if (rememberMe) {
        localStorage.setItem('authToken', data.token);
      } else {
        sessionStorage.setItem('authToken', data.token);
      }
        */

      console.log('Login successo:', data);
      onClose(); // chiude il modal
      
      window.location.href = '/dashboard';
    } catch (err) {
      console.error(err);
      setError('Errore di connessione al server');
    }
  };

  const validateStep1 = () => {
    if (
      !ownerLastName ||
      !ownerFirstName ||
      !ownerEmail ||
      !registerPassword ||
      !confirmPassword ||
      !birthDate ||
      !birthCountry
    ) {
      setError('Compila tutti i campi del titolare.');
      return false;
    }

    if (registerPassword !== confirmPassword) {
      setError('Le password non coincidono.');
      return false;
    }

    return true;
  };

  const validateStep2 = () => {
    if (!companyName || !companyDescription || !plan) {
      setError('Compila i campi principali dell’azienda e seleziona un piano.');
      return false;
    }

    if (plan === 'pro' && (!proAiChoice || !proAddonChoice)) {
      setError('Completa entrambe le scelte dedicate al piano Pro.');
      return false;
    }

    return true;
  };

  const handleNext = () => {
    setError('');
    if (step === 1 && !validateStep1()) return;
    if (step === 2 && !validateStep2()) return;
    setStep((prev) => Math.min(prev + 1, 3));
  };

  const handleBack = () => {
    setError('');
    setStep((prev) => Math.max(prev - 1, 1));
  };

  const handleRegisterSubmit = (event) => {
    event.preventDefault();
    setError('');

    if (!validateStep1() || !validateStep2()) return;

    if (paymentMethod === 'card') {
      if (!cardHolder || !cardNumber || !cardExpiry || !cardCvv) {
        setError('Compila tutti i dati della carta per completare la registrazione.');
        return;
      }
    } else if (paymentMethod === 'iban') {
      if (!iban) {
        setError('Inserisci un IBAN per completare la registrazione.');
        return;
      }
    } else {
      setError('Seleziona un metodo di pagamento.');
      return;
    }

    const payload = {
      mode: 'register',
      owner: {
        lastName: ownerLastName,
        firstName: ownerFirstName,
        email: ownerEmail,
        password: registerPassword,
        birthDate,
        birthCountry,
      },
      company: {
        name: companyName,
        description: companyDescription,
        plan,
        proAiChoice: plan === 'pro' ? proAiChoice : null,
        proAddonChoice: plan === 'pro' ? proAddonChoice : null,
        contactEmail: companyEmail || null,
        phone: companyPhone || null,
      },
      payment: {
        method: paymentMethod,
        card:
          paymentMethod === 'card'
            ? {
                holder: cardHolder,
                number: cardNumber,
                expiry: cardExpiry,
                cvv: cardCvv,
              }
            : null,
        iban: paymentMethod === 'iban' ? iban : null,
      },
      logoFileName: logoFile ? logoFile.name : null,
    };

    // TODO: collega queste chiamate al tuo backend; per il logo usa FormData
    console.log('Auth register submit', payload);
    onClose();
  };

  const renderSteps = () => {
    if (isLogin) return null;

    return (
      <div className="auth-steps">
        <div className={`auth-step ${step === 1 ? 'active' : ''} ${step > 1 ? 'completed' : ''}`}>
          <span className="auth-step-number">1</span>
          <span className="auth-step-label">Titolare</span>
        </div>
        <div className={`auth-step ${step === 2 ? 'active' : ''} ${step > 2 ? 'completed' : ''}`}>
          <span className="auth-step-number">2</span>
          <span className="auth-step-label">Azienda</span>
        </div>
        <div className={`auth-step ${step === 3 ? 'active' : ''}`}>
          <span className="auth-step-number">3</span>
          <span className="auth-step-label">Pagamento</span>
        </div>
      </div>
    );
  };

  const renderLoginForm = () => (
    <form className="auth-form" onSubmit={handleLoginSubmit}>
      <div className="auth-field">
        <label htmlFor="login-email">Email di lavoro</label>
        <input
          id="login-email"
          type="email"
          placeholder="nome.cognome@azienda.it"
          value={loginEmail}
          onChange={(event) => setLoginEmail(event.target.value)}
        />
      </div>

      <div className="auth-field">
        <label htmlFor="login-password">Password</label>
        <input
          id="login-password"
          type="password"
          placeholder="••••••••"
          value={loginPassword}
          onChange={(event) => setLoginPassword(event.target.value)}
        />
      </div>

      <div className="auth-extra">
        <label className="auth-remember">
          <input
            type="checkbox"
            checked={rememberMe}
            onChange={(event) => setRememberMe(event.target.checked)}
          />{' '}
          Rimani connesso
        </label>
        <button type="button" className="auth-link">
          Hai dimenticato la password?
        </button>
      </div>

      {error && <div className="auth-error">{error}</div>}

      <button type="submit" className="btn-primary auth-submit">
        Accedi
      </button>

      <p className="auth-footer">
        Non hai ancora un account?{' '}
        <button type="button" className="auth-link" onClick={() => switchMode('register')}>
          Registrati
        </button>
      </p>
    </form>
  );

  const renderRegisterStep1 = () => (
    <>
      <div className="auth-field-group">
        <div className="auth-field">
          <label htmlFor="owner-last-name">Cognome</label>
          <input
            id="owner-last-name"
            type="text"
            placeholder="Rossi"
            value={ownerLastName}
            onChange={(event) => setOwnerLastName(event.target.value)}
          />
        </div>
        <div className="auth-field">
          <label htmlFor="owner-first-name">Nome</label>
          <input
            id="owner-first-name"
            type="text"
            placeholder="Luca"
            value={ownerFirstName}
            onChange={(event) => setOwnerFirstName(event.target.value)}
          />
        </div>
      </div>

      <div className="auth-field">
        <label htmlFor="owner-email">Email personale di lavoro</label>
        <input
          id="owner-email"
          type="email"
          placeholder="luca.rossi@azienda.it"
          value={ownerEmail}
          onChange={(event) => setOwnerEmail(event.target.value)}
        />
      </div>

      <div className="auth-field-group">
        <div className="auth-field">
          <label htmlFor="register-password">Password</label>
          <input
            id="register-password"
            type="password"
            placeholder="••••••••"
            value={registerPassword}
            onChange={(event) => setRegisterPassword(event.target.value)}
          />
        </div>
        <div className="auth-field">
          <label htmlFor="confirm-password">Conferma password</label>
          <input
            id="confirm-password"
            type="password"
            placeholder="••••••••"
            value={confirmPassword}
            onChange={(event) => setConfirmPassword(event.target.value)}
          />
        </div>
      </div>

      <div className="auth-field-group">
        <div className="auth-field">
          <label htmlFor="birth-date">Data di nascita</label>
          <input
            id="birth-date"
            type="date"
            value={birthDate}
            onChange={(event) => setBirthDate(event.target.value)}
          />
        </div>
        <div className="auth-field">
          <label htmlFor="birth-country">Stato di nascita</label>
          <input
            id="birth-country"
            type="text"
            placeholder="Italia"
            value={birthCountry}
            onChange={(event) => setBirthCountry(event.target.value)}
          />
        </div>
      </div>
    </>
  );

  const renderPlanOptions = () => (
    <div className="auth-plan-grid">
      <button
        type="button"
        className={`auth-plan-card ${plan === 'starter' ? 'selected' : ''}`}
        onClick={() => setPlan('starter')}
      >
        <div className="auth-plan-header">
          <span className="auth-plan-name">Starter</span>
          <span className="auth-plan-price">€0/mese</span>
        </div>
        <p className="auth-plan-tag">Perfetto per testare la piattaforma con fino a 500 prodotti.</p>
      </button>

      <button
        type="button"
        className={`auth-plan-card ${plan === 'pro' ? 'selected' : ''}`}
        onClick={() => setPlan('pro')}
      >
        <div className="auth-plan-header">
          <span className="auth-plan-name">Pro Intelligence</span>
          <span className="auth-plan-chip">Più scelto</span>
          <span className="auth-plan-price">€49/mese</span>
        </div>
        <p className="auth-plan-tag">
          Accesso completo al simulatore, AI avanzata e integrazioni e‑commerce.
        </p>
      </button>

      <button
        type="button"
        className={`auth-plan-card ${plan === 'enterprise' ? 'selected' : ''}`}
        onClick={() => setPlan('enterprise')}
      >
        <div className="auth-plan-header">
          <span className="auth-plan-name">Enterprise</span>
          <span className="auth-plan-price">€199/mese</span>
        </div>
        <p className="auth-plan-tag">
          Per aziende strutturate che richiedono modelli dedicati e supporto avanzato.
        </p>
      </button>
    </div>
  );

  const renderProExtras = () => {
    if (plan !== 'pro') return null;

    return (
      <div className="auth-pro-extra">
        <div className="auth-field">
          <span className="auth-field-label">Per il piano Pro scegli il motore principale</span>
          <div className="auth-choice-row">
            <button
              type="button"
              className={`auth-choice-pill ${proAiChoice === 'chatbot' ? 'selected' : ''}`}
              onClick={() => setProAiChoice('chatbot')}
            >
              Chatbot
            </button>
            <button
              type="button"
              className={`auth-choice-pill ${proAiChoice === 'bi' ? 'selected' : ''}`}
              onClick={() => setProAiChoice('bi')}
            >
              Business Intelligence
            </button>
          </div>
        </div>

        <div className="auth-field">
          <span className="auth-field-label">E la funzionalità aggiuntiva</span>
          <div className="auth-choice-row">
            <button
              type="button"
              className={`auth-choice-pill ${proAddonChoice === 'price_control' ? 'selected' : ''}`}
              onClick={() => setProAddonChoice('price_control')}
            >
              Controllo prezzi
            </button>
            <button
              type="button"
              className={`auth-choice-pill ${proAddonChoice === 'mobile_app' ? 'selected' : ''}`}
              onClick={() => setProAddonChoice('mobile_app')}
            >
              App mobile
            </button>
          </div>
        </div>
      </div>
    );
  };

  const renderRegisterStep2 = () => (
    <>
      <div className="auth-field">
        <label htmlFor="company-name">Nome azienda</label>
        <input
          id="company-name"
          type="text"
          placeholder="Magazzino Rossi SRL"
          value={companyName}
          onChange={(event) => setCompanyName(event.target.value)}
        />
      </div>

      <div className="auth-field">
        <label htmlFor="company-description">Descrizione</label>
        <textarea
          id="company-description"
          rows={3}
          placeholder="Es. e-commerce moda con 3 magazzini tra Milano e Bologna…"
          value={companyDescription}
          onChange={(event) => setCompanyDescription(event.target.value)}
          className="auth-textarea"
        />
      </div>

      <div className="auth-field">
        <span className="auth-field-label">Piano scelto</span>
        {renderPlanOptions()}
      </div>

      {renderProExtras()}

      <div className="auth-field-group">
        <div className="auth-field">
          <label htmlFor="company-email">Email aziendale (opzionale)</label>
          <input
            id="company-email"
            type="email"
            placeholder="contatti@azienda.it"
            value={companyEmail}
            onChange={(event) => setCompanyEmail(event.target.value)}
          />
        </div>
        <div className="auth-field">
          <label htmlFor="company-phone">Telefono (opzionale)</label>
          <input
            id="company-phone"
            type="tel"
            placeholder="+39 333 1234567"
            value={companyPhone}
            onChange={(event) => setCompanyPhone(event.target.value)}
          />
        </div>
      </div>

      <div className="auth-field">
        <label htmlFor="company-logo">Logo aziendale (opzionale)</label>
        <div className="auth-file-input">
          <input
            id="company-logo"
            type="file"
            accept="image/*"
            onChange={(event) => {
              const file = event.target.files && event.target.files[0];
              setLogoFile(file || null);
            }}
          />
          {logoFile && <span className="auth-file-name">{logoFile.name}</span>}
        </div>
      </div>
    </>
  );

  const renderRegisterStep3 = () => (
    <>
      <div className="auth-summary">
        <h3>Riepilogo piano</h3>
        <p>
          <strong>{plan === 'starter' ? 'Starter' : plan === 'pro' ? 'Pro Intelligence' : 'Enterprise'}</strong>
          {plan === 'starter' && ' · €0/mese'}
          {plan === 'pro' && ' · €49/mese'}
          {plan === 'enterprise' && ' · €199/mese'}
        </p>
        {plan === 'pro' && (
          <>
            <p className="auth-summary-detail">
              Motore: {proAiChoice === 'chatbot' ? 'Chatbot' : 'Business Intelligence'}
            </p>
            <p className="auth-summary-detail">
              Aggiuntivo: {proAddonChoice === 'mobile_app' ? 'App mobile' : 'Controllo prezzi'}
            </p>
          </>
        )}
      </div>

      <div className="auth-field">
        <span className="auth-field-label">Metodo di pagamento</span>
        <div className="auth-payment-methods">
          <button
            type="button"
            className={`auth-payment-card ${paymentMethod === 'card' ? 'selected' : ''}`}
            onClick={() => setPaymentMethod('card')}
          >
            <span className="auth-payment-title">Carta</span>
            <span className="auth-payment-subtitle">Visa, Mastercard, ecc.</span>
          </button>
          <button
            type="button"
            className={`auth-payment-card ${paymentMethod === 'iban' ? 'selected' : ''}`}
            onClick={() => setPaymentMethod('iban')}
          >
            <span className="auth-payment-title">IBAN</span>
            <span className="auth-payment-subtitle">Addebito SEPA</span>
          </button>
        </div>
      </div>

      {paymentMethod === 'card' ? (
        <>
          <div className="auth-field">
            <label htmlFor="card-holder">Titolare</label>
            <input
              id="card-holder"
              type="text"
              placeholder="Nome Cognome"
              value={cardHolder}
              onChange={(event) => setCardHolder(event.target.value)}
            />
          </div>

          <div className="auth-field">
            <label htmlFor="card-number">Numero carta</label>
            <input
              id="card-number"
              type="text"
              inputMode="numeric"
              placeholder="1234 5678 9012 3456"
              value={cardNumber}
              onChange={(event) => setCardNumber(event.target.value)}
            />
          </div>

          <div className="auth-field-group">
            <div className="auth-field">
              <label htmlFor="card-expiry">Scadenza</label>
              <input
                id="card-expiry"
                type="text"
                inputMode="numeric"
                placeholder="MM/AA"
                value={cardExpiry}
                onChange={(event) => setCardExpiry(event.target.value)}
              />
            </div>
            <div className="auth-field">
              <label htmlFor="card-cvv">CVV</label>
              <input
                id="card-cvv"
                type="password"
                inputMode="numeric"
                placeholder="•••"
                value={cardCvv}
                onChange={(event) => setCardCvv(event.target.value)}
              />
            </div>
          </div>
        </>
      ) : (
        <div className="auth-field">
          <label htmlFor="iban">IBAN</label>
          <input
            id="iban"
            type="text"
            placeholder="IT60 X054 2811 1010 0000 0123 456"
            value={iban}
            onChange={(event) => setIban(event.target.value)}
          />
        </div>
      )}

      <p className="auth-help-text">
        Non verrà effettuato alcun addebito ora. Usiamo questo dato per attivare il piano scelto.
      </p>
    </>
  );

  const renderRegisterForm = () => (
    <form className="auth-form" onSubmit={handleRegisterSubmit}>
      {renderSteps()}

      {step === 1 && renderRegisterStep1()}
      {step === 2 && renderRegisterStep2()}
      {step === 3 && renderRegisterStep3()}

      {error && <div className="auth-error">{error}</div>}

      <div className="auth-actions">
        {step > 1 && (
          <button type="button" className="auth-secondary" onClick={handleBack}>
            Indietro
          </button>
        )}
        {step < 3 && (
          <button type="button" className="btn-primary auth-submit" onClick={handleNext}>
            Prosegui
          </button>
        )}
        {step === 3 && (
          <button type="submit" className="btn-primary auth-submit">
            Completa registrazione
          </button>
        )}
      </div>

      <p className="auth-footer">
        Hai già un account?{' '}
        <button type="button" className="auth-link" onClick={() => switchMode('login')}>
          Accedi
        </button>
      </p>
    </form>
  );

  return (
    <div className="auth-backdrop" role="dialog" aria-modal="true">
      <div className="auth-modal reveal active">
        <button type="button" className="auth-close" onClick={onClose} aria-label="Chiudi">
          ×
        </button>

        <div className="auth-tabs">
          <button
            type="button"
            className={`auth-tab ${isLogin ? 'active' : ''}`}
            onClick={() => switchMode('login')}
          >
            Accedi
          </button>
          <button
            type="button"
            className={`auth-tab ${!isLogin ? 'active' : ''}`}
            onClick={() => switchMode('register')}
          >
            Registrati
          </button>
        </div>

        <h2 className="auth-title">
          {isLogin ? 'Accedi al simulatore' : 'Crea il tuo account InvenTrack'}
        </h2>
        <p className="auth-subtitle">
          {isLogin
            ? 'Entra nel tuo ambiente di simulazione e continua da dove avevi lasciato.'
            : 'Pochi passi per configurare il tuo simulatore aziendale.'}
        </p>

        {isLogin ? renderLoginForm() : renderRegisterForm()}
      </div>
    </div>
  );
};

export default AuthModal;

