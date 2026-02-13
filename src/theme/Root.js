import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import { AuthProvider } from '../contexts/AuthContext';
import { LanguageProvider } from '../contexts/LanguageContext';

export default function Root({children}) {
  return (
    <AuthProvider>
      <LanguageProvider>
        {children}
        <BrowserOnly fallback={null}>
          {() => {
            const ChatbotWidget = require('../components/ChatbotWidget').default;
            return <ChatbotWidget />;
          }}
        </BrowserOnly>
      </LanguageProvider>
    </AuthProvider>
  );
}