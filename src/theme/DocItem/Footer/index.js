import React, { useMemo } from 'react';
import Footer from '@theme-original/DocItem/Footer';
import { useDoc } from '@docusaurus/plugin-content-docs/client';

const SHAPE_CLASSES = ['chapter-box', 'chapter-circle', 'chapter-oval'];

function ChapterTitleDisplay() {
  const { metadata } = useDoc();

  // Randomly select a shape class (stable per page load)
  const shapeClass = useMemo(() => {
    const index = Math.floor(Math.random() * SHAPE_CLASSES.length);
    return SHAPE_CLASSES[index];
  }, []);

  // Only show for chapter pages
  const isChapter = metadata.title?.toLowerCase().includes('chapter');

  if (!isChapter) {
    return null;
  }

  return (
    <div className="chapter-title-footer">
      <div className={`chapter-title-display ${shapeClass}`}>
        {metadata.title}
      </div>
    </div>
  );
}

export default function FooterWrapper(props) {
  return (
    <>
      <ChapterTitleDisplay />
      <Footer {...props} />
    </>
  );
}
