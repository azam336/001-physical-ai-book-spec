import React from 'react';
import { useTranslation } from '../../hooks/useTranslation';

/**
 * Component to display translated text
 * @param {string} tkey - Translation key
 * @param {object} params - Optional parameters for interpolation
 * @param {string} fallback - Fallback text if translation not found
 */
export default function TranslatedText({ tkey, params, fallback, children }) {
  const { t } = useTranslation();

  if (tkey) {
    return <>{t(tkey, params)}</>;
  }

  if (fallback) {
    return <>{fallback}</>;
  }

  return <>{children}</>;
}
