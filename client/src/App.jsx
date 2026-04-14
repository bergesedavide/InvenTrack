import React, { useEffect, useState } from 'react';

import HeroSection from './components/HeroSection.jsx';
import AiSection from './components/AiSection.jsx';
import FeaturesSection from './components/FeaturesSection.jsx';
import PricingSection from './components/PricingSection.jsx';
import FaqSection from './components/FaqSection.jsx';
import CtaSection from './components/CtaSection.jsx';
import Header from './components/Header.jsx';
import Footer from './components/Footer.jsx';
import AuthModal from './components/AuthModal.jsx';

const App = () => {
  const [authOpen, setAuthOpen] = useState(false);
  const [authInitialMode, setAuthInitialMode] = useState('login');

  useEffect(() => {
    const themeBtn = document.getElementById('theme-btn');
    const htmlEl = document.documentElement;

    const savedTheme =
      localStorage.getItem('theme') ||
      (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

    htmlEl.setAttribute('data-theme', savedTheme);

    if (themeBtn) {
      themeBtn.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
      const handleThemeClick = () => {
        const currentTheme = htmlEl.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';

        htmlEl.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        themeBtn.textContent = newTheme === 'dark' ? '☀️' : '🌙';
      };

      themeBtn.addEventListener('click', handleThemeClick);

      return () => {
        themeBtn.removeEventListener('click', handleThemeClick);
      };
    }
  }, []);

  useEffect(() => {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px',
    };

    const startCounters = () => {
      const counters = document.querySelectorAll('.counter');
      const speed = 200;

      counters.forEach((counter) => {
        const updateCount = () => {
          const target = Number(counter.getAttribute('data-target'));
          const count = Number(counter.innerText);
          const inc = target / speed;

          if (count < target) {
            counter.innerText = String(Math.ceil(count + inc));
            setTimeout(updateCount, 15);
          } else {
            counter.innerText = Number(target).toLocaleString('it-IT');
          }
        };

        updateCount();
      });
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');

          if (entry.target.classList.contains('dashboard-mockup')) {
            startCounters();
          }

          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    document.querySelectorAll('.reveal').forEach((el) => {
      observer.observe(el);
    });

    return () => observer.disconnect();
  }, []);

  const openAuth = (mode = 'login') => {
    setAuthInitialMode(mode);
    setAuthOpen(true);
  };

  const closeAuth = () => {
    setAuthOpen(false);
  };

  return (
    <>
      <div className="background-glow" />
      <Header onOpenAuth={openAuth} />
      <main className="container">
        <HeroSection onOpenAuth={openAuth} />
        <AiSection />
        <FeaturesSection />
        <PricingSection />
        <FaqSection />
        <CtaSection onOpenAuth={openAuth} />
      </main>
      <AuthModal open={authOpen} initialMode={authInitialMode} onClose={closeAuth} />
      <Footer />
    </>
  );
};

export default App;

