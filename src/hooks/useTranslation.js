import { useLanguage } from '../contexts/LanguageContext';
import translations from '../translations';

/**
 * Hook to get translated text based on current language
 * @returns {Function} t - Translation function that takes a key and returns translated text
 */
export function useTranslation() {
  const { lang } = useLanguage();

  /**
   * Get translation for a key
   * @param {string} key - Translation key (e.g., 'navbar.book', 'chapter1.title')
   * @param {object} params - Optional parameters for interpolation
   * @returns {string} Translated text
   */
  const t = (key, params = {}) => {
    const keys = key.split('.');
    let value = translations[lang];

    for (const k of keys) {
      if (value && typeof value === 'object') {
        value = value[k];
      } else {
        // Fallback to English if translation not found
        value = translations.en;
        for (const fallbackKey of keys) {
          value = value?.[fallbackKey];
        }
        break;
      }
    }

    // If still not found, return the key itself
    if (value === undefined || value === null) {
      return key;
    }

    // Handle string interpolation if params provided
    if (typeof value === 'string' && Object.keys(params).length > 0) {
      return value.replace(/\{(\w+)\}/g, (match, paramKey) => {
        return params[paramKey] !== undefined ? params[paramKey] : match;
      });
    }

    return value;
  };

  return { t, lang };
}

export default useTranslation;
