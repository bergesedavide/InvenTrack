import { useState, useEffect } from 'react';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isErrorVisible, setIsErrorVisible] = useState(false);

  useEffect(() => {
    if (error) {
      setIsErrorVisible(true);
      const fadeTimer = setTimeout(() => setIsErrorVisible(false), 2000);
      const removeTimer = setTimeout(() => setError(''), 2500);
      return () => { clearTimeout(fadeTimer); clearTimeout(removeTimer); };
    }
  }, [error]);

  const handleSubmit = async (e) => {
    if (e) e.preventDefault(); 
    
    setError('');
    
    // Validazione base locale
    if (!email || !password) {
      setError('Inserisci email e password');
      return;
    }

    setIsLoading(true);

    try {
      // Invio della richiesta POST
      const response = await fetch('http://127.0.0.1:8080/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email,
          password: password
        }),
      });

      // Ricezione dei dati dal server
      const data = await response.json();

      if (!response.ok) {
        // Se il server risponde con un errore (es. 401 Credenziali errate)
        throw new Error(data.message || 'Credenziali non valide');
      }

      // Successo! Salva il token e reindirizza l'utente
      console.log('Login effettuato con successo:', data);
      //localStorage.setItem('token', data.token); // Esempio: salvataggio JWT
      //window.location.href = '/dashboard'; // Reindirizza

    } catch (err) {
      // Gestione errori di rete o credenziali
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#FFFCFF] flex items-center justify-center p-4 sm:p-8 font-sans relative overflow-hidden">
      
      {/* ELEMENTI DECORATIVI DINAMICI */}
      <div className="absolute inset-0 z-0">
        <div className="absolute w-[40vw] h-[40vw] max-w-[500px] max-h-[500px] bg-[#CBD4C2]/30 rounded-full blur-[80px] -top-10 -left-10"></div>
        <div className="absolute w-[30vw] h-[30vw] max-w-[400px] max-h-[400px] bg-[#C3B299]/20 rounded-full blur-[100px] bottom-0 right-0"></div>
      </div>

      {/* LA CARD PRINCIPALE (ADATTABILE) */}
      <div className="relative z-10 w-full max-w-[450px] transition-all duration-300">
        <div className="bg-white/90 backdrop-blur-md rounded-[2.5rem] shadow-[0_20px_50px_rgba(80,81,79,0.1)] p-6 sm:p-10 border border-[#CBD4C2]">
          
          <div className="text-center mb-8">
            {/* Icona scalabile */}
            <div className="inline-flex items-center justify-center w-16 h-16 bg-[#247BA0] rounded-2xl mb-4 shadow-lg">
              <svg className="w-12 h-12 text-[#FFFCFF]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
            {/* Testo in REM (text-2xl/3xl) */}
            <h1 className="text-2xl sm:text-3xl font-extrabold text-[#50514F] tracking-tight">Accesso Riservato</h1>
            <p className="text-[#C3B299] text-sm sm:text-base font-medium mt-2">Gestione Infrastruttura</p>
          </div>

          <div className="space-y-5">
            {/* INPUT CON ALTEZZA RELATIVA */}
            <div>
              <label className="block text-[0.7rem] font-bold text-[#50514F] uppercase tracking-widest mb-2 ml-1">Email</label>
              <input
                type="email"
                className="w-full px-5 py-3.5 bg-[#CBD4C2]/10 border-2 border-[#CBD4C2]/30 rounded-2xl text-[#50514F] focus:ring-4 focus:ring-[#247BA0]/10 focus:border-[#247BA0] transition-all outline-none"
                placeholder="nome@azienda.it"
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <div>
              <label className="block text-[0.7rem] font-bold text-[#50514F] uppercase tracking-widest mb-2 ml-1">Password</label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  className="w-full px-5 py-3.5 bg-[#CBD4C2]/10 border-2 border-[#CBD4C2]/30 rounded-2xl text-[#50514F] focus:ring-4 focus:ring-[#247BA0]/10 focus:border-[#247BA0] transition-all outline-none"
                  placeholder="••••••••"
                  onChange={(e) => setPassword(e.target.value)}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-[#C3B299] hover:text-[#247BA0] transition-colors"
                >
                  {showPassword ? "Nascondi" : "Mostra"}
                </button>
              </div>
            </div>

            {/* LAYOUT FLEXBOX PER OPZIONI */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-sm pt-2">
              <label className="flex items-center text-[#50514F] cursor-pointer group">
                <input type="checkbox" className="w-4 h-4 rounded border-[#CBD4C2] text-[#247BA0] focus:ring-[#247BA0]" />
                <span className="ml-2 group-hover:text-[#247BA0] transition-colors">Resta connesso</span>
              </label>
              <button className="text-[#247BA0] font-bold hover:underline">Password dimenticata?</button>
            </div>

            {error && (
              <div className={`bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-r-xl text-sm transition-all duration-500 ${isErrorVisible ? 'opacity-100' : 'opacity-0'}`}>
                {error}
              </div>
            )}

            <button
              onClick={handleSubmit}
              disabled={isLoading}
              className="w-full bg-[#247BA0] text-white font-bold py-4 rounded-2xl shadow-lg hover:shadow-[#247BA0]/40 hover:-translate-y-0.5 active:scale-[0.98] transition-all disabled:opacity-50"
            >
              {isLoading ? 'Accesso in corso...' : 'Entra nel Dashboard'}
            </button>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-10 text-center">
          <p className="text-[#C3B299] text-sm">
            Supporto Tecnico: <span className="text-[#50514F] font-semibold">support@inventrack.com</span>
          </p>
        </div>
      </div>
    </div>
  );
}