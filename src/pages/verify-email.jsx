import React, { useEffect, useState } from 'react';
import { useLocation, useHistory } from '@docusaurus/router';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import '../css/auth.css';

export default function VerifyEmail() {
  const [status, setStatus] = useState('verifying'); // 'verifying', 'success', 'error'
  const [message, setMessage] = useState('');
  const location = useLocation();
  const history = useHistory();

  useEffect(() => {
    const verifyEmail = async () => {
      // Extract token from URL query params
      const params = new URLSearchParams(location.search);
      const token = params.get('token');

      if (!token) {
        setStatus('error');
        setMessage('Invalid verification link. No token provided.');
        return;
      }

      try {
        const response = await fetch('http://localhost:8000/api/auth/verify-email', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ token }),
        });

        const data = await response.json();

        if (response.ok) {
          setStatus('success');
          setMessage('Email verified successfully! Redirecting to login...');

          // Redirect to login after 3 seconds
          setTimeout(() => {
            history.push('/login');
          }, 3000);
        } else {
          setStatus('error');
          setMessage(data.detail || 'Email verification failed. The link may be expired or invalid.');
        }
      } catch (error) {
        setStatus('error');
        setMessage('An error occurred while verifying your email. Please try again.');
        console.error('Verification error:', error);
      }
    };

    verifyEmail();
  }, [location, history]);

  return (
    <Layout title="Verify Email" description="Email verification page">
      <div className="auth-container">
        <div className="auth-card">
          <h1>Email Verification</h1>

          {status === 'verifying' && (
            <div className="auth-message info">
              <p>Verifying your email address...</p>
            </div>
          )}

          {status === 'success' && (
            <div className="auth-message success">
              <h2>✓ Success!</h2>
              <p>{message}</p>
            </div>
          )}

          {status === 'error' && (
            <div className="auth-message error">
              <h2>✗ Verification Failed</h2>
              <p>{message}</p>
              <div style={{ marginTop: '20px' }}>
                <Link to="/login" className="auth-link">
                  Return to Login
                </Link>
                {' | '}
                <Link to="/register" className="auth-link">
                  Register Again
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
