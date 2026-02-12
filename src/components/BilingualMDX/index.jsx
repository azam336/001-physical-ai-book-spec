import React from 'react';
import { useLanguage } from '../../contexts/LanguageContext';
import MDXContent from '@theme/MDXContent';

/**
 * BilingualMDX - Wrapper component that displays content based on current language
 * @param {object} english - English MDX content
 * @param {object} urdu - Urdu MDX content
 */
export default function BilingualMDX({ english, urdu }) {
  const { lang } = useLanguage();

  // Render content based on current language
  const content = lang === 'ur' ? urdu : english;

  return <MDXContent>{content}</MDXContent>;
}

/**
 * BilingualSection - For inline bilingual content sections
 */
export function BilingualSection({ en, ur, children }) {
  const { lang } = useLanguage();

  if (children) {
    return <>{children}</>;
  }

  return <>{lang === 'ur' ? ur : en}</>;
}

/**
 * BilingualText - For simple text translation
 */
export function BilingualText({ en, ur }) {
  const { lang } = useLanguage();
  return <>{lang === 'ur' ? ur : en}</>;
}
