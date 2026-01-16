/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  bookSidebar: [
    'index',
    {
      type: 'category',
      label: 'Chapters',
      collapsed: false,
      items: [
        'chapter-01-introduction-to-embodied-ai',
        'chapter-02-sensors-and-perception',
        'chapter-03-kinematics-and-actuation',
        'chapter-04-cognitive-architectures-for-humanoids',
        'chapter-05-safety-and-ethics-in-physical-ai',
      ],
    },
    'glossary',
    {
      type: 'category',
      label: 'Resources',
      items: [
        'resources/troubleshooting',
        'resources/community',
      ],
    },
    'contributing',
  ],
};

module.exports = sidebars;
