// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Introduction to Physical AI',
  tagline: 'Learn to build intelligent systems that interact with the physical world',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: process.env.VERCEL
    ? 'https://001-physical-ai-book-spec.vercel.app'
    : 'https://azam336.github.io',
  baseUrl: process.env.VERCEL ? '/' : '/001-physical-ai-book-spec/',
  organizationName: 'azam336',
  projectName: '001-physical-ai-book-spec',
  deploymentBranch: 'gh-pages',
  trailingSlash: false,



  onBrokenLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  themes: ['@docusaurus/theme-mermaid'],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          path: 'docs',
          routeBasePath: '/',
          editUrl: 'https://github.com/azam336/001-physical-ai-book-spec/tree/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/physical-ai-social-card.jpg',
      colorMode: {
        defaultMode: 'light',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'Physical AI Book',
        logo: {
          alt: 'Physical AI Book Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'bookSidebar',
            position: 'left',
            label: 'Book',
          },
          {
            to: '/glossary',
            label: 'Glossary',
            position: 'left',
          },
          {
            href: 'https://github.com/azam336/001-physical-ai-book-spec',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Learn',
            items: [
              {
                label: 'Introduction',
                to: '/',
              },
              {
                label: 'Chapter 1: Embodied AI',
                to: '/chapter-01-introduction-to-embodied-ai',
              },
              {
                label: 'Glossary',
                to: '/glossary',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub Discussions',
                href: 'https://github.com/azam336/001-physical-ai-book-spec/discussions',
              },
              {
                label: 'Contributing',
                to: '/contributing',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'Troubleshooting',
                to: '/resources/troubleshooting',
              },
              {
                label: 'Community Projects',
                to: '/resources/community',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI Book Contributors. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['python', 'bash', 'json'],
      },
    }),
};

export default config;
