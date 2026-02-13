import React from 'react';
import { Redirect, useLocation } from '@docusaurus/router';
import useBaseUrl from '@docusaurus/useBaseUrl';
import { useAuth } from '../contexts/AuthContext';

/**
 * ProtectedRoute - Auth gate for protected content (book pages)
 * - Redirects to /login if not authenticated
 * - Preserves intended URL for post-login redirect
 * - Shows loading state while checking auth
 */
export default function ProtectedRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();
  const loginUrl = useBaseUrl('/login');

  // Loading state - show while checking authentication
  if (isLoading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '60vh',
        fontSize: '18px',
        color: '#667eea'
      }}>
        <div>Loading...</div>
      </div>
    );
  }

  // Not authenticated - redirect to login
  if (!isAuthenticated) {
    // Prevent redirect loops - don't redirect if already on login/register
    const currentPath = location.pathname;
    if (currentPath.includes('/login') || currentPath.includes('/register')) {
      return children;
    }

    // Save intended destination to sessionStorage for post-login redirect
    if (typeof window !== 'undefined') {
      sessionStorage.setItem('auth_redirect', currentPath);
    }

    // Redirect to login
    if (typeof window !== 'undefined') {
      window.location.href = loginUrl;
      return null;
    }

    return <Redirect to={loginUrl} />;
  }

  // Authenticated - render protected content
  return children;
}