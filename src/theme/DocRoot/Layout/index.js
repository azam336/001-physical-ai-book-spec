import React, { useEffect } from 'react';
import Layout from '@theme-original/DocRoot/Layout';
import { useLanguage } from '../../../contexts/LanguageContext';

export default function DocRootLayoutWrapper(props) {
  const { lang } = useLanguage();

  // Apply RTL direction for Urdu
  useEffect(() => {
    if (typeof document !== 'undefined') {
      const htmlElement = document.documentElement;

      if (lang === 'ur') {
        htmlElement.setAttribute('dir', 'rtl');
        htmlElement.setAttribute('lang', 'ur');
      } else {
        htmlElement.setAttribute('dir', 'ltr');
        htmlElement.setAttribute('lang', 'en');
      }
    }
  }, [lang]);

  return <Layout {...props} />;
}
