import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';
import useBaseUrl from '@docusaurus/useBaseUrl';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className={styles.heroContent}>
        <div className={styles.bookCover}>
          <div className={styles.bookSpine}></div>
          <div className={styles.bookFront}>
            <div className={styles.bookTitle}>
              <Heading as="h1" className={styles.heroTitle}>
                {siteConfig.title}
              </Heading>
              <p className={styles.heroSubtitle}>{siteConfig.tagline}</p>
            </div>
          </div>
        </div>
        <div className={styles.heroText}>
          <h2 className={styles.heroWelcome}>Welcome to Your Digital Library</h2>
          <p className={styles.heroDescription}>
            Immerse yourself in a beautifully crafted reading experience. 
            Discover knowledge presented with elegance and clarity.
          </p>
          <div className={styles.buttons}>
   
          
          <Link
  className={clsx('button button--primary button--lg', styles.primaryButton)}
  to={useBaseUrl('/chapter-01-introduction-to-embodied-ai')}>
  Start Reading
</Link>
  {/*}      
<Link
  className={clsx('button button--secondary button--lg', styles.secondaryButton)}
  to={useBaseUrl('/')}>
  Explore Topics
</Link>
  */} 
<Link
  className={clsx('button button--secondary button--lg', styles.secondaryButton)}
  to={useBaseUrl('/topics')}>
  Explore Topics
</Link>





          </div>
        </div>
      </div>
      <div className={styles.heroBackground}>
        <div className={styles.floatingBook}></div>
        <div className={styles.floatingBook2}></div>
        <div className={styles.floatingBook3}></div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="A beautiful digital book experience">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <section className={styles.featuredContent}>
          <div className="container">
            <Heading as="h2" className={styles.sectionTitle}>
              Featured Content
            </Heading>
            <div className={styles.contentGrid}>
              <div className={styles.contentCard}>
                <div className={styles.cardIcon}>📚</div>
                <h3>Rich Content</h3>
                <p>Comprehensive guides and documentation crafted with care</p>
              </div>
              <div className={styles.contentCard}>
                <div className={styles.cardIcon}>✨</div>
                <h3>Beautiful Design</h3>
                <p>An elegant reading experience that keeps you engaged</p>
              </div>
              <div className={styles.contentCard}>
                <div className={styles.cardIcon}>🚀</div>
                <h3>Fast & Responsive</h3>
                <p>Optimized for all devices and screen sizes</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
