import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext(null);

// Docusaurus doesn't expose process.env to client-side code
// Use window.location to determine API URL, or fallback to localhost
const getApiUrl = () => {
  if (typeof window !== 'undefined') {
    // In production, API would be at same domain or configured domain
    // For development, use localhost:8000
    return 'http://localhost:8000';
  }
  return 'http://localhost:8000';
};

const API_URL = getApiUrl();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [token, setToken] = useState(() => {
    // Use sessionStorage for session-based auth (cleared when browser/tab closes)
    if (typeof window !== 'undefined') {
      return sessionStorage.getItem('auth_token');
    }
    return null;
  });

  // Check authentication on mount
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    // Use sessionStorage for session-based auth
    const savedToken = typeof window !== 'undefined'
      ? sessionStorage.getItem('auth_token')
      : null;

    if (!savedToken) {
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_URL}/api/auth/me`, {
        headers: {
          'Authorization': `Bearer ${savedToken}`
        }
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
        setIsAuthenticated(true);
        setToken(savedToken);
      } else {
        // Token invalid, clear it
        if (typeof window !== 'undefined') {
          sessionStorage.removeItem('auth_token');
        }
        setUser(null);
        setIsAuthenticated(false);
        setToken(null);
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      if (typeof window !== 'undefined') {
        sessionStorage.removeItem('auth_token');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (fullName, email, password) => {
    try {
      const response = await fetch(`${API_URL}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          full_name: fullName,
          email,
          password
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Registration failed');
      }

      // Save token and user (sessionStorage for session-based auth)
      if (typeof window !== 'undefined') {
        sessionStorage.setItem('auth_token', data.token);
      }
      setToken(data.token);
      setUser(data.user);
      setIsAuthenticated(true);

      return { success: true };
    } catch (error) {
      // Provide helpful error messages
      let errorMessage = error.message;

      if (error.message === 'Failed to fetch') {
        errorMessage = 'Cannot connect to server. Please ensure the backend is running on http://localhost:8000';
      } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
        errorMessage = 'Network error. Check if backend server is running.';
      }

      console.error('Registration error:', error);
      return { success: false, error: errorMessage };
    }
  };

  const login = async (email, password) => {
    try {
      const response = await fetch(`${API_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Login failed');
      }

      // Save token and user (sessionStorage for session-based auth)
      if (typeof window !== 'undefined') {
        sessionStorage.setItem('auth_token', data.token);
      }
      setToken(data.token);
      setUser(data.user);
      setIsAuthenticated(true);

      return { success: true };
    } catch (error) {
      // Provide helpful error messages
      let errorMessage = error.message;

      if (error.message === 'Failed to fetch') {
        errorMessage = 'Cannot connect to server. Please ensure the backend is running on http://localhost:8000';
      } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
        errorMessage = 'Network error. Check if backend server is running.';
      }

      console.error('Login error:', error);
      return { success: false, error: errorMessage };
    }
  };

  const logout = async () => {
    try {
      if (token) {
        await fetch(`${API_URL}/api/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear session state regardless of API call result
      if (typeof window !== 'undefined') {
        sessionStorage.removeItem('auth_token');
        sessionStorage.removeItem('auth_redirect'); // Clear redirect too
      }
      setToken(null);
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  const value = {
    user,
    isAuthenticated,
    isLoading,
    token,
    register,
    login,
    logout,
    checkAuth
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export default AuthContext;