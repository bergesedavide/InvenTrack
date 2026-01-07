import { useState } from 'react';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    setError('');
    setIsLoading(true);

    setTimeout(() => {
      if (email && password) {
        console.log('Login:', { email, password });
        alert('Login effettuato con successo!');
      } else {
        setError('Inserisci email e password');
      }
      setIsLoading(false);
    }, 1000);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  };

  return (
    // Sfondo principale con i colori DBF4AD e A9E190
    <div className="min-h-screen bg-gradient-to-br from-[#DBF4AD] via-[#A9E190] to-[#DBF4AD] flex items-center justify-center p-4 font-sans">
      
      {/* Sfondo animato con blur */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute w-96 h-96 bg-[#CDC776]/30 rounded-full blur-3xl -top-48 -left-48 animate-pulse"></div>
        <div className="absolute w-96 h-96 bg-[#A5AA52]/20 rounded-full blur-3xl -bottom-48 -right-48 animate-pulse"></div>
      </div>

      <div className="relative w-full max-w-md">
        {/* Card Login - Background CDC776 con opacità */}
        <div className="bg-[#CDC776]/80 backdrop-blur-xl rounded-2xl shadow-2xl p-8 border border-[#A5AA52]/40">
          
          {/* Logo/Titolo - Colore 767522 per il testo scuro */}
          <div className="text-center mb-8">
            <div className="inline-block p-3 bg-gradient-to-br from-[#A5AA52] to-[#767522] rounded-2xl mb-4 shadow-lg">
              <svg className="w-12 h-12 text-[#DBF4AD]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-[#767522] mb-2">Bentornato</h1>
            <p className="text-[#767522]/80">Accedi al sistema gestionale</p>
          </div>

          <div className="space-y-6">
            {/* Email */}
            <div>
              <label htmlFor="email" className="block text-sm font-bold text-[#767522] mb-2">
                Email
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="w-5 h-5 text-[#767522]/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                </div>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="w-full pl-10 pr-4 py-3 bg-[#DBF4AD]/40 border border-[#A5AA52]/50 rounded-xl text-[#767522] placeholder-[#767522]/50 focus:outline-none focus:ring-2 focus:ring-[#767522] focus:border-transparent transition"
                  placeholder="nome@esempio.com"
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label htmlFor="password" className="block text-sm font-bold text-[#767522] mb-2">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="w-5 h-5 text-[#767522]/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="w-full pl-10 pr-12 py-3 bg-[#DBF4AD]/40 border border-[#A5AA52]/50 rounded-xl text-[#767522] placeholder-[#767522]/50 focus:outline-none focus:ring-2 focus:ring-[#767522] focus:border-transparent transition"
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-[#767522]/60 hover:text-[#767522] transition"
                >
                  {showPassword ? (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                    </svg>
                  ) : (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  )}
                </button>
              </div>
            </div>

            {/* Ricordami / Password dimenticata */}
            <div className="flex items-center justify-between text-sm">
              <label className="flex items-center text-[#767522] cursor-pointer font-medium">
                <input type="checkbox" className="w-4 h-4 rounded border-[#A5AA52] bg-[#DBF4AD]/50 text-[#767522] focus:ring-[#767522] focus:ring-offset-0" />
                <span className="ml-2">Ricordami</span>
              </label>
              <button className="text-[#767522] hover:underline transition font-medium">
                Password dimenticata?
              </button>
            </div>

            {/* Errore */}
            {error && (
              <div className="bg-red-500/10 border border-red-500/50 text-red-700 px-4 py-3 rounded-xl text-sm font-medium">
                {error}
              </div>
            )}

            {/* Pulsante Login - Gradient A5AA52 to 767522 */}
            <button
              onClick={handleSubmit}
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-[#A5AA52] to-[#767522] text-[#DBF4AD] font-bold py-3 rounded-xl hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-[#767522] focus:ring-offset-2 focus:ring-offset-[#DBF4AD] transition-all transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              {isLoading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-[#DBF4AD]" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Accesso in corso...
                </span>
              ) : (
                'Accedi'
              )}
            </button>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-[#767522] text-sm mt-6 font-medium">
          © 2024 Sistema Gestionale. Tutti i diritti riservati.
        </p>
      </div>
    </div>
  );
}