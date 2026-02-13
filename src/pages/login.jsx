import React, { useState } from 'react';
import { useHistory } from '@docusaurus/router';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { useAuth } from '../contexts/AuthContext';
import '../css/auth.css';

export default function Login() {
  const history = useHistory();
  const { login, isAuthenticated } = useAuth();
  
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState('');

  // Redirect if already authenticated
  React.useEffect(() => {
    if (isAuthenticated) {
      // Check if there's a saved redirect URL from ProtectedRoute
      const redirectTo = typeof window !== 'undefined'
        ? sessionStorage.getItem('auth_redirect')
        : null;

      if (redirectTo) {
        // Clear the redirect URL
        sessionStorage.removeItem('auth_redirect');
        history.push(redirectTo);
      } else {
        // Default redirect to home or first book page
        history.push('/');
      }
    }
  }, [isAuthenticated, history]);

  const validateForm = () => {
    const newErrors = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError('');

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    const result = await login(formData.email, formData.password);

    setIsLoading(false);

    if (result.success) {
      // Check for saved redirect URL (from ProtectedRoute)
      const savedRedirect = typeof window !== 'undefined'
        ? sessionStorage.getItem('auth_redirect')
        : null;

      if (savedRedirect) {
        sessionStorage.removeItem('auth_redirect');
        history.push(savedRedirect);
      } else {
        // Fallback to query param or home
        const params = new URLSearchParams(window.location.search);
        const redirectTo = params.get('redirect') || '/';
        history.push(redirectTo);
      }
    } else {
      setApiError(result.error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  return (
    <Layout title="Login" description="Login to your account">
      <div className="auth-container">
        <div className="auth-card">
          <div className="auth-header">
            <h1>Welcome Back</h1>
            <p>Login to access Physical AI Book</p>
          </div>

          {apiError && (
            <div className="auth-error-banner">
              {apiError}
            </div>
          )}

          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className={errors.email ? 'error' : ''}
                placeholder="john@example.com"
                disabled={isLoading}
                autoFocus
              />
              {errors.email && (
                <span className="error-message">{errors.email}</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className={errors.password ? 'error' : ''}
                placeholder="Enter your password"
                disabled={isLoading}
              />
              {errors.password && (
                <span className="error-message">{errors.password}</span>
              )}
              <div style={{ textAlign: 'right', marginTop: '8px' }}>
                <Link to="/forgot-password" className="auth-link">
                  Forgot Password?
                </Link>
              </div>
            </div>

            <button
              type="submit"
              className="auth-submit-btn"
              disabled={isLoading}
            >
              {isLoading ? 'Logging in...' : 'Login'}
            </button>
          </form>

          <div className="auth-footer">
            Don't have an account?{' '}
            <Link to="/register">Register here</Link>
          </div>
        </div>
      </div>
    </Layout>
  );
}
