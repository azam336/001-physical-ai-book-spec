import React from 'react';
import Layout from '@theme-original/DocItem/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import ProtectedRoute from '../../../components/ProtectedRoute';
import { useLanguage } from '../../../contexts/LanguageContext';
import urduContent from '../../../content/urdu/chapters';
import MDXContent from '@theme/MDXContent';
import clsx from 'clsx';

export default function DocItemLayout(props) {
  const { lang } = useLanguage();
  const { siteConfig } = useDocusaurusContext();
  const currentPath = typeof window !== 'undefined' ? window.location.pathname : '';

  // Extract route path (remove base URL dynamically)
  const basePath = siteConfig.baseUrl.replace(/\/$/, '');
  const routePath = currentPath.replace(basePath, '') || '/';

  // Check if Urdu content exists for this route
  const hasUrduContent = lang === 'ur' && urduContent[routePath];

  if (hasUrduContent) {
    // Render Urdu content
    return (
      <ProtectedRoute>
        <div className={clsx('theme-doc-markdown', 'markdown')}>
          <MDXContent>
            <div dangerouslySetInnerHTML={{ __html: markdownToHTML(urduContent[routePath]) }} />
          </MDXContent>
        </div>
      </ProtectedRoute>
    );
  }

  // Render original English content
  return (
    <ProtectedRoute>
      <Layout {...props} />
    </ProtectedRoute>
  );
}

// Simple markdown to HTML converter (basic support)
function markdownToHTML(markdown) {
  if (!markdown) return '';

  let html = markdown;

  // Headers
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

  // Bold
  html = html.replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>');

  // Lists
  html = html.replace(/^\- (.*$)/gim, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

  // Links
  html = html.replace(/\[(.*?)\]\((.*?)\)/gim, '<a href="$2">$1</a>');

  // Paragraphs
  html = html.split('\n\n').map(p => {
    if (!p.startsWith('<') && p.trim()) {
      return `<p>${p}</p>`;
    }
    return p;
  }).join('\n');

  // Tables
  html = html.replace(/\|(.+)\|/g, (match) => {
    const cells = match.split('|').filter(c => c.trim());
    return '<tr>' + cells.map(c => `<td>${c.trim()}</td>`).join('') + '</tr>';
  });

  // Code blocks
  html = html.replace(/```(.*?)\n(.*?)```/gs, '<pre><code class="language-$1">$2</code></pre>');

  return html;
}