import React, { useState, useEffect, useRef, useCallback } from 'react';
import './styles.css';
import { useAuth } from '../../contexts/AuthContext';

const API_URL = 'http://localhost:8000/api/chat';

function generateSessionId() {
  return 'session_' + Math.random().toString(36).substring(2, 15) + Date.now().toString(36);
}

function getOrCreateSessionId() {
  if (typeof window === 'undefined') {
    return generateSessionId();
  }
  let sessionId = sessionStorage.getItem('chatbot_session_id');
  if (!sessionId) {
    sessionId = generateSessionId();
    sessionStorage.setItem('chatbot_session_id', sessionId);
  }
  return sessionId;
}

export default function ChatbotWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [sessionId] = useState(getOrCreateSessionId);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // Listen for text selection on the page
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection?.toString().trim();
      if (text && text.length > 0 && text.length < 2000) {
        setSelectedText(text);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, []);

  const clearSelectedText = () => {
    setSelectedText('');
  };

  const sendMessage = useCallback(async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue.trim();
    setInputValue('');
    setIsLoading(true);

    // Add user message to chat
    setMessages(prev => [...prev, {
      role: 'user',
      content: userMessage,
      selectedText: selectedText || null
    }]);

    // Add placeholder for assistant response
    setMessages(prev => [...prev, {
      role: 'assistant',
      content: '',
      isStreaming: true
    }]);

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
          session_id: sessionId,
          selected_text: selectedText || null
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let assistantMessage = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        assistantMessage += chunk;

        // Update the last message with streamed content
        setMessages(prev => {
          const newMessages = [...prev];
          const lastIndex = newMessages.length - 1;
          newMessages[lastIndex] = {
            ...newMessages[lastIndex],
            content: assistantMessage
          };
          return newMessages;
        });
      }

      // Mark streaming as complete
      setMessages(prev => {
        const newMessages = [...prev];
        const lastIndex = newMessages.length - 1;
        newMessages[lastIndex] = {
          ...newMessages[lastIndex],
          isStreaming: false
        };
        return newMessages;
      });

      // Clear selected text after sending
      setSelectedText('');

    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => {
        const newMessages = [...prev];
        const lastIndex = newMessages.length - 1;
        newMessages[lastIndex] = {
          role: 'assistant',
          content: 'Sorry, there was an error processing your request. Please try again.',
          isError: true,
          isStreaming: false
        };
        return newMessages;
      });
    } finally {
      setIsLoading(false);
    }
  }, [inputValue, isLoading, selectedText, sessionId]);

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="chatbot-widget">
      {/* Chat Window */}
      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <div className="chatbot-title">
              <span className="chatbot-icon">🤖</span>
              Physical AI Assistant
            </div>
            <button className="chatbot-close" onClick={toggleChat}>
              ×
            </button>
          </div>

          <div className="chatbot-messages">
            {messages.length === 0 && (
              <div className="chatbot-welcome">
                <p>👋 Hi! I'm your Physical AI textbook assistant.</p>
                <p>Ask me anything about the book content!</p>
                {selectedText && (
                  <p className="chatbot-tip">💡 Tip: You have text selected. Your question will reference it.</p>
                )}
              </div>
            )}

            {messages.map((msg, index) => (
              <div key={index} className={`chatbot-message ${msg.role}`}>
                {msg.role === 'user' && msg.selectedText && (
                  <div className="chatbot-selected-context">
                    <span className="context-label">📝 Selected text:</span>
                    <span className="context-text">{msg.selectedText.substring(0, 100)}...</span>
                  </div>
                )}
                <div className={`message-content ${msg.isError ? 'error' : ''}`}>
                  {msg.content}
                  {msg.isStreaming && msg.content === '' && (
                    <span className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </span>
                  )}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {selectedText && (
            <div className="chatbot-selected-text">
              <div className="selected-text-header">
                <span>📝 Selected text:</span>
                <button onClick={clearSelectedText}>×</button>
              </div>
              <div className="selected-text-content">
                {selectedText.length > 150
                  ? selectedText.substring(0, 150) + '...'
                  : selectedText}
              </div>
            </div>
          )}

          <div className="chatbot-input-area">
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about the textbook..."
              disabled={isLoading}
              rows={1}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputValue.trim()}
              className="send-button"
            >
              {isLoading ? '...' : '➤'}
            </button>
          </div>
        </div>
      )}

      {/* Floating Button */}
      <button
        className={`chatbot-fab ${isOpen ? 'open' : ''}`}
        onClick={toggleChat}
        aria-label="Toggle chat"
      >
        {isOpen ? '×' : '💬'}
      </button>
    </div>
  );
}
