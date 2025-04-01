# Edge Delivery Services (EDS) Development Reference Guide

## Introduction

This reference guide provides essential patterns, practices, and examples for Edge Delivery Services development. It serves as a companion to the main EDS Developer's Guide, offering standardized approaches to common development tasks. The examples and patterns in this guide follow EDS best practices for performance, maintainability, and clean separation of concerns.

## Configuration and Structure

### Configuration Constants Pattern

When developing blocks for EDS, it's recommended to use configuration constants at the top of your JavaScript files. This pattern improves code readability, maintainability, and prevents "magic numbers" or strings from being scattered throughout your code:

```javascript
const BLOCK_CONFIG = {
  // Visual appearance
  ANIMATION_DURATION: 300,
  COPY_BUTTON_RESET_DELAY: 2000,
  
  // Content thresholds
  MAX_ITEMS: 12,
  LONG_DOCUMENT_THRESHOLD: 40,
  SUMMARY_LENGTH: 150,
  
  // Content labels
  ERROR_MESSAGE: 'Error loading content. Please try again.',
  LOADING_MESSAGE: 'Loading content...',
  COPY_TEXT: 'Copy',
  COPIED_TEXT: 'Copied!',
  EXPAND_TEXT: 'Expand',
  COLLAPSE_TEXT: 'Collapse',
  
  // API endpoints
  API_ENDPOINT: '/query-index.json',
  CONTENT_ENDPOINT: '/content/pages.json',
  
  // Feature toggles
  ENABLE_TRACKING: true,
  SHOW_TIMESTAMPS: true
};
```

Using this pattern makes it easier for other developers to find and modify configuration values without digging through implementation details. It also centralizes configuration, making it clear what aspects of the component are customizable.

### Standard File Organization

EDS projects follow a consistent file organization pattern. Each block or component has its own directory with standardized files:

```bash
/blocks/{blockname}/
├── {blockname}.js           # Core block functionality
├── {blockname}.css          # Block styles
├── README.md                # Documentation
├── example.md               # Usage examples for content authors
├── demo.md                  # More comprehensive real-world usage examples
├── example.json             # Sample data (if needed)
└── example.csv              # CSV version of sample data (if needed)
```

This structure ensures that all blocks have complete documentation, clear examples for authors, and consistent organization that makes it easy for developers to understand how the block works.

## JavaScript Patterns

### ESLint Integration

EDS follows the Airbnb JavaScript Style Guide, which discourages console output in production code. When you need to use console logging for debugging, use the following pattern:

```javascript
// eslint-disable-next-line no-console
console.log('Debug information:', data);
```

This approach prevents ESLint errors while maintaining the ability to use console logging for debugging. Remember to:

1. Keep the comment on the line immediately before the console statement
2. Be specific about which rule you're disabling
3. Remove or comment out debug logging before committing to production

### Asynchronous Data Fetching

When fetching data from APIs or the EDS query index, follow this pattern for clean, error-handled asynchronous requests:

```javascript
export default async function decorate(block) {
  try {
    // Show loading state
    block.innerHTML = '<div class="loading">Loading content...</div>';
    
    // Fetch data with proper error handling
    const response = await fetch('/query-index.json');
    
    if (!response.ok) {
      throw new Error(`API returned status ${response.status}`);
    }
    
    const data = await response.json();
    
    // Process successful response
    block.innerHTML = ''; // Clear loading state
    
    // Create and append content elements
    const container = document.createElement('div');
    container.className = 'content-container';
    
    // Add content to container
    // ...
    
    block.appendChild(container);
    
  } catch (error) {
    // eslint-disable-next-line no-console
    console.error('Error fetching content:', error);
    
    // Show user-friendly error state
    block.innerHTML = `
      <div class="error-state">
        <p>We couldn't load this content. Please try again later.</p>
      </div>
    `;
  }
}
```

This pattern includes:

1. Clear loading states to improve user experience
2. Proper error handling with try/catch blocks
3. Response validation with specific error messages
4. User-friendly error states when things go wrong
5. Clean DOM manipulation to update the UI

### Standard Data Structure

When integrating with external data sources or the EDS query-index.json, follow this consistent pattern for JSON data structures:

```json
{
  "total": 100,          // Total items available
  "offset": 0,           // Starting position for pagination
  "limit": 10,           // Maximum items returned in this response
  "data": [              // Array of actual content items
    {
      "path": "/example-path",
      "title": "Example Title",
      "image": "/path/to/image.jpg",
      "description": "Example description",
      "lastModified": "1724942455",
      "tags": ["tag1", "tag2"],
      "author": "Author Name"
    }
  ],
  "type": "sheet"        // Content type identifier
}
```

This structure works well with EDS's built-in query functionality and makes it easier to create consistent data handling patterns across your site.

### Event Handling

For event handling, use this pattern to maintain clean separation and avoid memory leaks:

```javascript
export default function decorate(block) {
  // Create elements
  const button = document.createElement('button');
  button.textContent = 'Click me';
  button.className = 'action-button';
  
  // Define handler functions separately for clarity
  function handleClick(event) {
    // Handle the click event
    console.log('Button clicked', event);
    
    // Example: Toggle state
    button.classList.toggle('active');
  }
  
  // Add event listeners
  button.addEventListener('click', handleClick);
  
  // Append elements to the block
  block.appendChild(button);
  
  // Optional: Return a cleanup function for SPA environments
  return () => {
    button.removeEventListener('click', handleClick);
  };
}
```

Key benefits of this pattern:

1. Handler functions are defined separately for better readability
2. Event listeners are clearly attached in one section
3. Optional cleanup function helps prevent memory leaks in single-page applications

## CSS Best Practices

### CSS Variables for Theming

Define configuration through CSS variables to create consistent, flexible theming:

```css
:root {
  /* Color palette */
  --color-primary: #1473e6;
  --color-secondary: #2680eb;
  --color-background: #ffffff;
  --color-text: #2c2c2c;
  --color-text-light: #707070;
  --color-border: #e1e1e1;
  --color-error: #d7373f;
  --color-success: #268e6c;
  
  /* Typography */
  --font-family-heading: 'Adobe Clean', sans-serif;
  --font-family-body: 'Adobe Clean', sans-serif;
  --font-weight-normal: 400;
  --font-weight-bold: 700;
  --line-height-tight: 1.2;
  --line-height-normal: 1.5;
  --line-height-loose: 1.8;
  
  /* Spacing system */
  --spacing-xs: 4px;
  --spacing-s: 8px;
  --spacing-m: 16px;
  --spacing-l: 24px;
  --spacing-xl: 32px;
  --spacing-xxl: 48px;
  
  /* UI elements */
  --border-radius-small: 4px;
  --border-radius-medium: 8px;
  --border-radius-large: 16px;
  --shadow-small: 0 1px 3px rgba(0,0,0,0.12);
  --shadow-medium: 0 4px 6px rgba(0,0,0,0.12);
  --shadow-large: 0 10px 20px rgba(0,0,0,0.12);
  
  /* Transitions */
  --transition-fast: 0.15s ease;
  --transition-normal: 0.3s ease;
  --transition-slow: 0.5s ease;
  
  /* Layout */
  --container-width-small: 600px;
  --container-width-medium: 900px;
  --container-width-large: 1200px;
  --content-width: 72ch;
}

/* Using variables in components */
.button {
  background-color: var(--color-primary);
  color: white;
  padding: var(--spacing-s) var(--spacing-m);
  border-radius: var(--border-radius-small);
  font-family: var(--font-family-body);
  font-weight: var(--font-weight-bold);
  transition: background-color var(--transition-fast);
}

.button:hover {
  background-color: var(--color-secondary);
}

.card {
  background-color: var(--color-background);
  border-radius: var(--border-radius-medium);
  padding: var(--spacing-m);
  box-shadow: var(--shadow-medium);
  max-width: var(--container-width-small);
}
```

This comprehensive approach to CSS variables provides several benefits:

1. Consistent visual design across the site
2. Easy updates to the design system by changing variable values
3. Better organization of design tokens
4. Simplified maintenance and theme switching

### Standard Breakpoints

EDS follows a common set of breakpoints for responsive design:

```css
/* Mobile (default) - 0-599px */
.component {
  /* Mobile styles */
  padding: var(--spacing-m);
  font-size: 16px;
}

/* Tablet - 600-899px */
@media (min-width: 600px) {
  .component {
    /* Tablet styles */
    padding: var(--spacing-l);
    font-size: 18px;
  }
}

/* Desktop - 900-1199px */
@media (min-width: 900px) {
  .component {
    /* Desktop styles */
    padding: var(--spacing-xl);
    font-size: 20px;
  }
}

/* Large Desktop - 1200px+ */
@media (min-width: 1200px) {
  .component {
    /* Large desktop styles */
    padding: var(--spacing-xxl);
    max-width: var(--container-width-large);
    margin: 0 auto;
  }
}
```

Key principles for responsive design in EDS:

1. Always use `min-width` queries for consistency
2. Design mobile-first, adding complexity for larger screens
3. Use standard breakpoints (600px, 900px, 1200px) for consistency
4. Test all components at each breakpoint

### Block Variation Pattern

For blocks that support variations, follow this pattern:

```css
/* Base block styling */
.blockname {
  /* Default styles */
  padding: var(--spacing-m);
  background: var(--color-background);
  color: var(--color-text);
}

/* Size variations */
.blockname.small {
  /* Small variation */
  padding: var(--spacing-s);
  font-size: 0.9em;
}

.blockname.large {
  /* Large variation */
  padding: var(--spacing-xl);
  font-size: 1.2em;
}

/* Color theme variations */
.blockname.dark {
  /* Dark theme */
  background: #333333;
  color: #ffffff;
}

.blockname.light {
  /* Light theme */
  background: #f5f5f5;
  color: #333333;
}

/* Layout variations */
.blockname.centered {
  /* Centered layout */
  text-align: center;
  margin-left: auto;
  margin-right: auto;
}

.blockname.split {
  /* Split layout */
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-m);
}

/* Combined variations */
.blockname.dark.centered {
  /* Special styles for dark+centered combination */
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

This approach allows authors to specify variations in the document (e.g., `Blockname (dark, centered)`) without requiring additional JavaScript logic. Content authors can easily mix and match variations to achieve their desired appearance.

## Documentation Standards

### Block Documentation Template

When documenting a block, include the following sections in your README.md:

```markdown
# Block Name

## Overview

Brief description of what the block does and its primary use cases.

## Content Structure

Explain how authors should structure content in Google Docs to use this block.

### Example Table Structure

| BlockName |           |
| --------- | --------- |
| Content A | Content B |
| More here | More here |

## Variations

List all supported variations with examples:

- **dark**: Applies a dark color scheme
- **wide**: Expands the block to use more horizontal space
- **centered**: Centers the content within the block

### Variation Examples

| BlockName (dark) |         |
| ---------------- | ------- |
| Content          | Content |

## Configuration Options

Any custom configuration options available for developers.

## Accessibility Considerations

Notes on accessibility features and considerations.

## Performance Impact

Any notable performance considerations or optimizations.

## Dependencies

List any dependencies or requirements.

## Known Limitations

Document any known issues or limitations.
```

This comprehensive documentation structure ensures that both developers and content authors can effectively use your blocks. Always include:

1. Clear examples that content authors can copy and paste
2. Visual examples of variations when possible
3. Accessibility information to ensure inclusive design
4. Performance considerations to maintain site speed

### Code Comments

For complex JavaScript functions, use JSDoc-style comments:

```javascript
/**
 * Processes a collection of content items and generates HTML elements
 * 
 * This function takes raw data from the query index, filters based on 
 * the provided criteria, and creates DOM elements for each item.
 * 
 * @param {Array} items - Collection of content items from query index
 * @param {Object} options - Configuration options
 * @param {number} options.limit - Maximum number of items to display
 * @param {string} options.layout - Layout style ('grid', 'list', etc.)
 * @param {boolean} options.showDate - Whether to display dates
 * @returns {DocumentFragment} Fragment containing generated elements
 */
function processItems(items, options = {}) {
  // Implementation details...
}
```

For CSS, include section comments to organize your stylesheet:

```css
/* ---------------------------------------------------------------------
 * CARD COMPONENT
 * 
 * Core styles for card components including base layout, variations,
 * and responsive behaviors.
 * --------------------------------------------------------------------*/

.card {
  /* Card base styles */
}

/* Card media section */
.card-media {
  /* Media styles */
}

/* Card content section */
.card-content {
  /* Content styles */
}

/* Card variations */
.card.featured {
  /* Featured card styles */
}
```

## Resource Loading Patterns

### CSS Loading

```javascript
/**
 * Loads a CSS file asynchronously
 * @param {string} href - Path to the CSS file
 * @return {HTMLLinkElement} - The created link element
 */
function loadCSS(href) {
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = href;
  document.head.appendChild(link);
  return link;
}

// Usage
loadCSS('/blocks/myblock/myblock.css');
```

### Lazy JavaScript Loading

```javascript
/**
 * Loads a JavaScript file asynchronously
 * @param {string} src - Path to the JavaScript file
 * @return {Promise} - Resolves when the script is loaded
 */
async function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = src;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

// Usage with async/await
try {
  await loadScript('/scripts/feature.js');
  // Script is now loaded and can be used
  initFeature();
} catch (error) {
  // eslint-disable-next-line no-console
  console.error('Failed to load script:', error);
  showErrorState();
}
```

### Delayed Functionality

```javascript
/**
 * Delays execution of non-critical functionality
 * @param {Function} func - Function to execute after delay
 * @param {number} delay - Delay in milliseconds (default: 3000)
 */
function delayFunction(func, delay = 3000) {
  setTimeout(func, delay);
}

// Usage
delayFunction(() => {
  // Initialize non-critical features
  loadChatWidget();
  setupAnalytics();
  initFeedbackForm();
});
```

## Common Implementation Patterns

### Analytics Implementation

A clean pattern for implementing analytics without modifying core files:

```javascript
// In delayed.js
(function loadAnalytics() {
  // Skip in development environments
  if (window.location.hostname === 'localhost') {
    return;
  }
  
  // Create script element with async loading
  const script = document.createElement('script');
  script.async = true;
  script.src = 'https://www.googletagmanager.com/gtag/js?id=UA-XXXXXXXX-X';
  document.head.appendChild(script);
  
  // Initialize analytics
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  gtag('js', new Date());
  gtag('config', 'UA-XXXXXXXX-X', {
    'anonymize_ip': true,
    'page_title': document.title,
    'page_path': window.location.pathname
  });
  
  // Add custom event tracking with event delegation
  document.addEventListener('click', e => {
    const target = e.target.closest('a, button');
    if (!target) return;
    
    // Gather tracking data
    const trackingData = {
      event_category: target.tagName.toLowerCase(),
      event_label: target.innerText || target.textContent,
    };
    
    // Check for outbound links
    if (target.href) {
      const url = new URL(target.href);
      trackingData.outbound = url.hostname !== window.location.hostname;
      
      // Track downloads
      const fileExtension = url.pathname.split('.').pop();
      if (['pdf', 'docx', 'xlsx', 'zip'].includes(fileExtension)) {
        trackingData.event_category = 'download';
        trackingData.file_extension = fileExtension;
        trackingData.file_name = url.pathname.split('/').pop();
      }
    }
    
    // Send event to analytics
    gtag('event', 'click', trackingData);
  });
})();
```

### Cookie Consent Block

A reusable block for implementing cookie consent:

```javascript
export default function decorate(block) {
  // Configuration - can be customized via block configuration
  const config = {
    cookieName: 'cookie-consent',
    cookieExpiry: 365, // days
    showOnce: true,
    position: 'bottom', // 'bottom', 'top', 'modal'
    text: 'This website uses cookies to ensure you get the best experience.',
    learnMoreText: 'Learn more',
    learnMoreUrl: '/privacy-policy',
    acceptText: 'Accept',
    declineText: 'Decline'
  };
  
  // Only show if consent not yet given
  if (getCookie(config.cookieName)) {
    return;
  }
  
  // Create consent banner
  const banner = document.createElement('div');
  banner.className = `cookie-consent-banner ${config.position}`;
  banner.innerHTML = `
    <div class="cookie-content">
      <p>${config.text} 
      <a href="${config.learnMoreUrl}">${config.learnMoreText}</a></p>
      <div class="cookie-buttons">
        <button class="accept-button">${config.acceptText}</button>
        <button class="decline-button">${config.declineText}</button>
      </div>
    </div>
  `;
  
  // Add event listeners
  banner.querySelector('.accept-button').addEventListener('click', () => {
    setCookie(config.cookieName, 'accepted', config.cookieExpiry);
    banner.remove();
    enableTracking();
  });
  
  banner.querySelector('.decline-button').addEventListener('click', () => {
    setCookie(config.cookieName, 'declined', config.cookieExpiry);
    banner.remove();
  });
  
  // Add to page
  document.body.appendChild(banner);
  
  // Helper functions
  function setCookie(name, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = `; expires=${date.toUTCString()}`;
    document.cookie = `${name}=${value}${expires}; path=/; SameSite=Lax`;
  }
  
  function getCookie(name) {
    const nameEQ = `${name}=`;
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) === ' ') c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
  }
  
  function enableTracking() {
    // Load analytics and other tracking scripts
    delayFunction(() => {
      const script = document.createElement('script');
      script.src = '/scripts/tracking.js';
      document.head.appendChild(script);
    });
  }
}
```

### Personalization Block

A reusable block for implementing simple personalization:

```javascript
export default function decorate(block) {
  // Get or create user profile
  let userProfile = JSON.parse(localStorage.getItem('user-profile')) || {};
  
  // Track page visits
  userProfile.pageVisits = userProfile.pageVisits || [];
  userProfile.pageVisits.push({
    path: window.location.pathname,
    timestamp: Date.now(),
  });
  
  // Limit history length
  if (userProfile.pageVisits.length > 20) {
    userProfile.pageVisits = userProfile.pageVisits.slice(-20);
  }
  
  // Determine interests based on page visits
  const interests = determineInterests(userProfile.pageVisits);
  userProfile.interests = interests;
  
  // Save updated profile
  localStorage.setItem('user-profile', JSON.stringify(userProfile));
  
  // Personalize content
  personalizeContent(block, userProfile);
  
  /**
   * Analyzes user behavior to determine interests
   * @param {Array} pageVisits - Collection of page visit records
   * @return {Object} - Map of interest categories and strength
   */
  function determineInterests(pageVisits) {
    const interests = {};
    const categories = {
      products: ['/products/', '/shop/', '/store/'],
      services: ['/services/', '/solutions/'],
      blog: ['/blog/', '/articles/', '/news/'],
      support: ['/support/', '/help/', '/faq/']
    };
    
    // Count visits in each category
    pageVisits.forEach(visit => {
      Object.entries(categories).forEach(([category, paths]) => {
        if (paths.some(path => visit.path.includes(path))) {
          interests[category] = (interests[category] || 0) + 1;
        }
      });
    });
    
    // Convert counts to relative strength (0-1)
    const total = pageVisits.length || 1;
    Object.keys(interests).forEach(category => {
      interests[category] = Math.min(interests[category] / total, 1);
    });
    
    return interests;
  }
  
  /**
   * Creates personalized content based on user profile
   * @param {HTMLElement} container - Element to populate
   * @param {Object} profile - User profile data
   */
  function personalizeContent(container, profile) {
    // Clear container
    container.textContent = '';
    
    // Create personalized content heading
    const heading = document.createElement('h2');
    
    // Determine strongest interest
    let strongestInterest = '';
    let maxStrength = 0;
    
    Object.entries(profile.interests || {}).forEach(([interest, strength]) => {
      if (strength > maxStrength) {
        maxStrength = strength;
        strongestInterest = interest;
      }
    });
    
    // Set heading based on interests
    if (strongestInterest === 'products') {
      heading.textContent = 'Products You Might Like';
    } else if (strongestInterest === 'services') {
      heading.textContent = 'Services For Your Needs';
    } else if (strongestInterest === 'blog') {
      heading.textContent = 'Articles You Might Enjoy';
    } else if (strongestInterest === 'support') {
      heading.textContent = 'Support Resources';
    } else {
      heading.textContent = 'Recommended For You';
    }
    
    container.appendChild(heading);
    
    // Create content container for recommendations
    const content = document.createElement('div');
    content.className = 'personalized-content';
    
    // Fetch recommended content based on interest
    fetchRecommendations(strongestInterest)
      .then(items => {
        items.forEach(item => {
          const card = createContentCard(item);
          content.appendChild(card);
        });
      })
      .catch(error => {
        // eslint-disable-next-line no-console
        console.error('Error fetching recommendations:', error);
        content.innerHTML = '<p>Unable to load recommendations at this time.</p>';
      });
    
    container.appendChild(content);
  }
  
  /**
   * Fetches content recommendations based on interest
   * @param {string} interest - Interest category
   * @return {Promise<Array>} - Promise resolving to content items
   */
  async function fetchRecommendations(interest) {
    try {
      const response = await fetch('/query-index.json');
      if (!response.ok) throw new Error('Failed to fetch recommendations');
      
      const data = await response.json();
      
      // Filter by interest category
      let filtered = data.data;
      
      if (interest === 'products') {
        filtered = filtered.filter(item => item.path.includes('/products/'));
      } else if (interest === 'services') {
        filtered = filtered.filter(item => item.path.includes('/services/'));
      } else if (interest === 'blog') {
        filtered = filtered.filter(item => item.path.includes('/blog/'));
      } else if (interest === 'support') {
        filtered = filtered.filter(item => item.path.includes('/support/'));
      }
      
      // Limit to 3 items
      return filtered.slice(0, 3);
    } catch (error) {
      // eslint-disable-next-line no-console
      console.error('Error in fetchRecommendations:', error);
      return [];
    }
  }
  
  /**
   * Creates a content card element
   * @param {Object} item - Content item data
   * @return {HTMLElement} - Card element
   */
  function createContentCard(item) {
    const card = document.createElement('div');
    card.className = 'content-card';
    
    // Add image if available
    if (item.image) {
      const img = document.createElement('img');
      img.src = item.image;
      img.alt = item.title || '';
      card.appendChild(img);
    }
    
    // Add title
    const title = document.createElement('h3');
    const link = document.createElement('a');
    link.href = item.path;
    link.textContent = item.title;
    title.appendChild(link);
    card.appendChild(title);
    
    // Add description if available
    if (item.description) {
      const desc = document.createElement('p');
      desc.textContent = item.description;
      card.appendChild(desc);
    }
    
    return card;
  }
}
```
