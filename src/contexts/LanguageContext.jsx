import React, { createContext, useState, useContext, useEffect } from 'react';

const LanguageContext = createContext(null);

const STORAGE_KEY = 'book_lang';
const DEFAULT_LANG = 'en';

export const LanguageProvider = ({ children }) => {
  const [lang, setLang] = useState(() => {
    // Hydrate from sessionStorage on mount
    if (typeof window !== 'undefined') {
      const saved = sessionStorage.getItem(STORAGE_KEY);
      return saved === 'ur' || saved === 'en' ? saved : DEFAULT_LANG;
    }
    return DEFAULT_LANG;
  });

  const toggleLang = () => {
    setLang(prevLang => {
      const newLang = prevLang === 'en' ? 'ur' : 'en';

      // Persist to sessionStorage
      if (typeof window !== 'undefined') {
        sessionStorage.setItem(STORAGE_KEY, newLang);
      }

      return newLang;
    });
  };

  const value = {
    lang,
    toggleLang,
    isEnglish: lang === 'en',
    isUrdu: lang === 'ur',
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within LanguageProvider');
  }
  return context;
};

export default LanguageContext;
