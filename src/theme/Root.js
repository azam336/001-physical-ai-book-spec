
import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';
import { LanguageProvider } from '../contexts/LanguageContext';
import ChatbotWidget from '../components/ChatbotWidget';

export default function Root({children}) {
  return (
    <AuthProvider>
      <LanguageProvider>
        {children}
        <ChatbotWidget />
      </LanguageProvider>
    </AuthProvider>
  );
}