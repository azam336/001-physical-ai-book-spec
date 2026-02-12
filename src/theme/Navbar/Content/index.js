import React from 'react';
import NavbarContent from '@theme-original/Navbar/Content';
import GlobeLanguageToggle from '../../../components/GlobeLanguageToggle';
import styles from './styles.module.css';

export default function NavbarContentWrapper(props) {
  return (
    <>
      <NavbarContent {...props} />
      <div className={styles.languageToggleContainer}>
        <GlobeLanguageToggle />
      </div>
    </>
  );
}
