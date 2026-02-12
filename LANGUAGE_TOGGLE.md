# Language Toggle Feature - English ⇄ Urdu

## ✅ Implementation Complete

The Physical AI Book now supports bilingual content switching between English and Urdu.

---

## Features

### UI/UX
- 🌐 **Globe Button** in navbar (next to Glossary)
- **Smart Label** - Shows the *other* language to switch to:
  - English active → Button shows "اردو"
  - Urdu active → Button shows "English"
- **One-Click Toggle** - Instant language switch
- **RTL Support** - Automatic right-to-left layout for Urdu
- **Session Persistence** - Language choice saved in `sessionStorage`
- **Cross-Navigation** - Language persists across all pages

### Technical
- ✅ React Context API for global state
- ✅ sessionStorage persistence (key: `book_lang`)
- ✅ RTL/LTR automatic switching
- ✅ Translation system with fallbacks
- ✅ Swizzled Navbar integration
- ✅ Responsive design (mobile + desktop)

---

## How It Works

### User Flow

1. **Default State**
   - Language: English (`en`)
   - Button shows: "اردو"
   - Layout: LTR (Left-to-Right)

2. **Click Globe Button**
   - Language switches to: Urdu (`ur`)
   - Button now shows: "English"
   - Layout: RTL (Right-to-Left)
   - Content: Displays Urdu translations

3. **Navigate to Another Page**
   - Language remains: Urdu
   - No reset on navigation

4. **Refresh Page**
   - Language persists: Urdu (from sessionStorage)
   - User doesn't need to toggle again

5. **Close Browser/Tab**
   - sessionStorage cleared
   - Next session starts with: English (default)

---

## File Structure

```
src/
├── contexts/
│   └── LanguageContext.jsx          # Global language state
├── components/
│   ├── GlobeLanguageToggle/
│   │   ├── index.jsx                # Toggle button component
│   │   └── styles.module.css        # Button styles
│   └── TranslatedText/
│       └── index.jsx                # Helper component for translations
├── hooks/
│   └── useTranslation.js            # Translation hook
├── translations/
│   └── index.js                     # Translation data (en/ur)
├── theme/
│   ├── Root.js                      # LanguageProvider wrapper
│   ├── Navbar/Content/
│   │   ├── index.js                 # Swizzled navbar with toggle
│   │   └── styles.module.css        # Navbar toggle placement
│   └── DocRoot/Layout/
│       └── index.js                 # RTL/LTR direction switcher
└── css/
    └── rtl.css                      # RTL layout styles
```

---

## Usage Guide

### For Users

**Desktop:**
1. Look for 🌐 globe button in top navbar (next to "Glossary")
2. Click to switch language
3. All content updates immediately

**Mobile:**
1. Open menu
2. Find globe button
3. Click to toggle

### For Developers

#### 1. Add Translations

Edit `src/translations/index.js`:

```javascript
const translations = {
  en: {
    mySection: {
      title: 'My Title',
      description: 'My Description',
    },
  },
  ur: {
    mySection: {
      title: 'میرا عنوان',
      description: 'میری تفصیل',
    },
  },
};
```

#### 2. Use Translations in Components

**Method 1: useTranslation Hook**
```jsx
import { useTranslation } from '../hooks/useTranslation';

function MyComponent() {
  const { t } = useTranslation();

  return (
    <div>
      <h1>{t('mySection.title')}</h1>
      <p>{t('mySection.description')}</p>
    </div>
  );
}
```

**Method 2: TranslatedText Component**
```jsx
import TranslatedText from '../components/TranslatedText';

function MyComponent() {
  return (
    <div>
      <h1>
        <TranslatedText tkey="mySection.title" />
      </h1>
      <p>
        <TranslatedText tkey="mySection.description" />
      </p>
    </div>
  );
}
```

**Method 3: Direct Language Check**
```jsx
import { useLanguage } from '../contexts/LanguageContext';

function MyComponent() {
  const { lang, isEnglish, isUrdu } = useLanguage();

  return (
    <div>
      {isEnglish && <p>English content here</p>}
      {isUrdu && <p>اردو مواد یہاں</p>}
    </div>
  );
}
```

#### 3. String Interpolation

```javascript
// In translations file:
const translations = {
  en: {
    greeting: 'Hello, {name}!',
  },
  ur: {
    greeting: '{name}، السلام علیکم',
  },
};

// In component:
const { t } = useTranslation();
<p>{t('greeting', { name: 'Ahmed' })}</p>
// Renders: "Hello, Ahmed!" (en) or "Ahmed، السلام علیکم" (ur)
```

---

## API Reference

### LanguageContext

```jsx
import { useLanguage } from '../contexts/LanguageContext';

const {
  lang,        // Current language: 'en' | 'ur'
  toggleLang,  // Function to switch language
  isEnglish,   // Boolean: true if lang === 'en'
  isUrdu,      // Boolean: true if lang === 'ur'
} = useLanguage();
```

### useTranslation Hook

```jsx
import { useTranslation } from '../hooks/useTranslation';

const {
  t,     // Translation function: t(key, params)
  lang,  // Current language: 'en' | 'ur'
} = useTranslation();

// Usage:
t('navbar.book')                    // Simple key
t('greeting', { name: 'Ali' })      // With params
t('nested.deep.key')                // Nested keys
```

### TranslatedText Component

```jsx
import TranslatedText from '../components/TranslatedText';

// Basic usage
<TranslatedText tkey="navbar.book" />

// With params
<TranslatedText tkey="greeting" params={{ name: 'Ali' }} />

// With fallback
<TranslatedText tkey="missing.key" fallback="Default Text" />
```

---

## RTL Layout

### Automatic Behavior

When Urdu is selected:
- ✅ `<html dir="rtl" lang="ur">` applied
- ✅ Text alignment: right
- ✅ Margins/paddings: flipped
- ✅ Sidebar: moves to right side
- ✅ Breadcrumbs: arrows reversed
- ✅ Pagination: flipped

**Exception:** Code blocks remain LTR (left-to-right) for readability

### Custom RTL Styling

Add to `src/css/rtl.css`:

```css
html[dir='rtl'] .my-component {
  /* Your RTL-specific styles */
  text-align: right;
  margin-right: 20px;
  margin-left: 0;
}
```

---

## sessionStorage

### Key

```javascript
const STORAGE_KEY = 'book_lang';
```

### Values

- `'en'` - English
- `'ur'` - Urdu

### Behavior

- **Set on toggle** - Language choice saved
- **Cleared on browser close** - Resets to default
- **Persists during session** - Survives page refreshes and navigation

### Manual Access

```javascript
// Get current language
const lang = sessionStorage.getItem('book_lang');

// Set language
sessionStorage.setItem('book_lang', 'ur');

// Clear (reset to default)
sessionStorage.removeItem('book_lang');
```

---

## Styling

### Globe Button

Styled to match Docusaurus navbar:
- Variable-based colors (light/dark theme support)
- Hover effects
- Responsive sizing
- Smooth transitions

### Customization

Edit `src/components/GlobeLanguageToggle/styles.module.css`:

```css
.globeButton {
  /* Modify button appearance */
  padding: 8px 16px;
  border-radius: 8px;
  background: custom-color;
}

.langText {
  /* Modify text styling */
  font-size: 16px;
  font-weight: 600;
}
```

---

## Adding More Languages

### 1. Update LanguageContext

```javascript
// src/contexts/LanguageContext.jsx
const DEFAULT_LANG = 'en';
const SUPPORTED_LANGS = ['en', 'ur', 'ar']; // Add 'ar' for Arabic
```

### 2. Update Toggle Logic

```javascript
const toggleLang = () => {
  setLang(prevLang => {
    // Cycle through languages
    const currentIndex = SUPPORTED_LANGS.indexOf(prevLang);
    const nextIndex = (currentIndex + 1) % SUPPORTED_LANGS.length;
    return SUPPORTED_LANGS[nextIndex];
  });
};
```

### 3. Add Translations

```javascript
// src/translations/index.js
const translations = {
  en: { /* ... */ },
  ur: { /* ... */ },
  ar: { /* ... */ }, // New language
};
```

### 4. Update Button Label

```javascript
// src/components/GlobeLanguageToggle/index.jsx
const labelMap = {
  en: 'اردو',      // Show Urdu when English active
  ur: 'English',   // Show English when Urdu active
  ar: 'English',   // Show English when Arabic active
};
```

---

## Testing

### Manual Testing

1. **Toggle Functionality**
   - Click globe button
   - Verify language switches
   - Verify button label changes

2. **Persistence**
   - Switch to Urdu
   - Navigate to different page
   - Verify language still Urdu
   - Refresh page
   - Verify language still Urdu

3. **RTL Layout**
   - Switch to Urdu
   - Verify text aligns right
   - Verify sidebar on right
   - Verify code blocks still LTR

4. **Session Reset**
   - Switch to Urdu
   - Close browser
   - Reopen
   - Verify language reset to English

### Console Testing

```javascript
// Check current language
window.sessionStorage.getItem('book_lang');

// Force language change
window.sessionStorage.setItem('book_lang', 'ur');
window.location.reload();

// Clear language
window.sessionStorage.removeItem('book_lang');
window.location.reload();
```

---

## Troubleshooting

### Issue: Toggle doesn't work

**Solution:** Check console for errors. Verify LanguageProvider wraps app in `Root.js`.

### Issue: Language resets on navigation

**Solution:** Verify sessionStorage is working. Check browser privacy settings.

### Issue: RTL not applying

**Solution:** Check DocRoot/Layout wrapper is installed. Verify rtl.css is imported.

### Issue: Translations not showing

**Solution:**
1. Check translation key exists in `translations/index.js`
2. Verify key spelling matches exactly
3. Check nested object structure

### Issue: Button not visible

**Solution:** Check Navbar/Content swizzle is in place. Clear browser cache.

---

## Current Translations

### Included

- ✅ Navbar items
- ✅ Common UI elements
- ✅ Auth pages
- ✅ Book metadata
- ✅ Chapter titles
- ✅ Footer

### To Add

- ⚠️ Full chapter content (requires manual translation)
- ⚠️ Glossary terms
- ⚠️ Error messages
- ⚠️ Form validation text

---

## Best Practices

### 1. Translation Keys

Use clear, hierarchical keys:
```javascript
// Good
'chapter01.section02.paragraph03'
'auth.login.errorMessages.invalidCredentials'

// Bad
'c1s2p3'
'loginError1'
```

### 2. Fallbacks

Always provide English fallback:
```javascript
t('key.that.might.not.exist', 'Default English text')
```

### 3. RTL-Safe Components

Avoid hardcoded `left`/`right` in CSS:
```css
/* Bad */
.element {
  margin-left: 20px;
}

/* Good */
.element {
  margin-inline-start: 20px; /* Auto-flips in RTL */
}
```

### 4. Testing Both Languages

Always test new features in both English and Urdu to ensure:
- ✅ Text fits in UI
- ✅ RTL layout works
- ✅ No hardcoded directions

---

## Future Enhancements

### Potential Additions

1. **localStorage Option** - Remember language across sessions
2. **Auto-detect** - Use browser language preference
3. **More Languages** - Add Arabic, Persian, etc.
4. **Content Translation** - Translate all book chapters
5. **Language Selector** - Dropdown for 3+ languages
6. **URL-based** - `/en/chapter1`, `/ur/chapter1`
7. **Search** - Multilingual search support

---

## Summary

✅ **Implemented:**
- Language toggle button in navbar
- English ⇄ Urdu switching
- RTL/LTR automatic layout
- Session persistence
- Translation system
- Usage examples

✅ **Ready to use!**

The language toggle is fully functional and ready for content translation.

---

**Next Steps:**
1. Add more translations to `src/translations/index.js`
2. Use `useTranslation()` hook in your components
3. Test both languages thoroughly
4. Translate book content gradually

Happy translating! 🌐📖
