import React from 'react';
import { useLanguage } from '../../contexts/LanguageContext';
import styles from './styles.module.css';

export default function GlobeLanguageToggle() {
  const { lang, toggleLang } = useLanguage();

  // Show the OTHER language (the one we'll switch TO)
  const displayText = lang === 'en' ? 'اردو' : 'English';

  return (
    <button
      className={styles.globeButton}
      onClick={toggleLang}
      aria-label={`Switch to ${lang === 'en' ? 'Urdu' : 'English'}`}
      title={`Switch to ${lang === 'en' ? 'Urdu' : 'English'}`}
    >
      <span className={styles.globeIcon}>🌐</span>
      <span className={styles.langText}>{displayText}</span>
    </button>
  );
}
