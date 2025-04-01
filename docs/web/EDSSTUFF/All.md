# The Developer's Guide to Edge Delivery Services (EDS): From Document to Website

## Introduction

Edge Delivery Services (EDS, formerly known as Franklin or Project Helix) represents a paradigm shift in content management systems. Unlike traditional CMSs that require content authors to adapt to the system's rigid structures, EDS flips this relationship—the system adapts to how authors naturally create content. This comprehensive guide examines how EDS transforms documents into high-performance websites, with a special focus on extending functionality without modifying core files.

## Core Philosophy and Requirements

### The Content-First Philosophy

At its core, EDS embraces a content-first approach that radically simplifies the authoring process. Content creators work in familiar tools like Google Docs or Microsoft Word, while the system handles the technical transformation into structured web pages. This separation of concerns allows:

- Content authors to focus on writing in familiar environments
- Developers to build functionality without disrupting content workflows
- Both teams to work simultaneously, accelerating delivery

As a developer working with EDS, understanding this philosophy is crucial—your job isn't to build a website from scratch, but to enhance how documents transform into web experiences.

### Development Requirements and Constraints

Before diving into EDS, it's important to understand its core development philosophy and constraints. These aren't limitations but deliberate design choices that promote simplicity, performance, and maintainability:

- **Modern JavaScript without TypeScript**: EDS relies on vanilla JavaScript, avoiding transpilation complexity
- **Pure CSS without preprocessors**: Direct CSS keeps things simple and performant
- **No build-heavy frameworks**: Skip React, Vue, and other frameworks that add complexity
- **Focus on simplicity and performance**: Every decision prioritizes page speed and core web vitals
- **Clear code organization**: Structured, well-documented code is essential
- **No dependencies and no build steps**: Zero build process means faster development and fewer points of failure

These requirements enable EDS to achieve perfect Core Web Vitals scores (100/100/100/100) by eliminating the overhead traditionally associated with modern web development. This approach is increasingly rare but remarkably effective—letting developers focus on solving real problems rather than managing toolchains.

## The Document Transformation Journey

Let's follow a document's complete journey from creation to final rendered webpage. This transformation process is at the heart of how EDS works, and understanding it will help you see where and how to extend functionality as a developer.

### Stage 1: Document Creation in Google Docs

The journey begins with a content author creating or editing a document in Google Docs (or Microsoft Word). In this familiar environment, authors naturally structure their content using:

- Headings and subheadings (H1-H6) to organize information hierarchically
- Paragraphs with rich text formatting (bold, italic, underline)
- Lists (ordered and unordered) for structured information
- Images embedded directly in the document
- Links to internal and external resources
- Text formatting for emphasis and organization

Authors can also use EDS-specific features:

- Section breaks (horizontal rules with ---) to divide content into logical sections
- Tables with specific headers to create specialized blocks like "Columns" or "Cards"
- Metadata tables with key-value pairs to define page properties for SEO and configuration

For example, a typical document might include a hero section with a main heading, followed by several content sections divided by horizontal rules, and special blocks created with tables.

### Stage 2: Document to Markdown Conversion (Server-Side)

When an author presses "Preview" in the Sidekick tool, the transformation begins:

**Document Retrieval**

- EDS accesses the document via Google Docs or SharePoint API
- The raw document content is extracted for processing

**Structural Analysis**

- The system analyzes the document structure
- It identifies headings, paragraphs, tables, and other elements
- Special elements like metadata tables are recognized

**Markdown Conversion**

- The document is systematically converted to Markdown format
- Document structure is preserved in Markdown syntax
- Tables are specially processed as potential block components
- Images are extracted and stored separately

**Markdown Storage**

- The generated Markdown becomes the source of truth for page content
- It's stored in the "content bus" for versioning and future access
- This separation allows content and code to evolve independently

The Markdown representation serves as an intermediate format that bridges the gap between the document-based authoring experience and web delivery.

### Stage 3: Markdown to Initial HTML Generation (Server-Side)

Once the Markdown is prepared, EDS transforms it into basic HTML:

**HTML Structure Creation**

- The server processes the Markdown to generate HTML
- A semantic document structure is created with appropriate HTML elements
- Headings become `<h1>` through `<h6>` elements
- Paragraphs become `<p>` elements
- Lists become `<ul>` or `<ol>` with nested `<li>` elements

**Metadata Application**

- Metadata from the metadata table is extracted and applied
- Title, description, and other SEO elements are added to the `<head>`
- Open Graph and other social sharing tags are generated

**Section Organization**

- Content is divided into sections based on horizontal rules
- Each section is wrapped in a `<div class="section">` element
- This creates the foundation for the page's visual structure

**Block Identification**

- Tables marked as blocks are converted to `<div>` elements with appropriate classes
- Each block is given a data-block-name attribute for later processing
- Block structure is preserved but not yet fully processed

This initial HTML is minimal and lacks styling or interactive features, but it contains all the content and structural information needed for the next steps.

### Stage 4: Initial HTML Delivery and Browser Processing

The server delivers this basic HTML to the browser, where the transformation continues:

**Initial Browser Rendering**

- The browser receives and parses the HTML
- Initial DOM construction begins
- Critical CSS (in styles.css) is loaded for basic styling
- The page appears in a simplified but structured form

**Core Script Loading**

- Key JavaScript files (aem.js and scripts.js) are loaded
- These scripts orchestrate the remaining transformation

**DOM Enhancement (Client-Side JavaScript)**

- The decorateTemplateAndTheme() function applies page-level structure
- The decorateSections() function processes each section
- The decorateBlocks() function identifies blocks for enhancement
- Text nodes are wrapped in appropriate elements with wrapTextNodes()
- Links are transformed into buttons where appropriate with decorateButtons()

**Block Loading and Processing**

- Each block is loaded with its CSS and JavaScript
- Blocks are processed in order, starting with the first visible section
- The loadBlock() function imports block-specific JS and CSS
- Each block's decorate() function transforms its DOM

During this phase, the HTML undergoes significant transformation through JavaScript. What starts as basic markup becomes rich, interactive content with proper styling and behavior.

### Stage 5: Final DOM Transformation and Rendering

The final stage involves completing the page enhancement with dramatic transformations to the DOM structure:

**Block Status Tracking and Wrapper Elements**

When examining the browser-rendered DOM, you'll see significant differences from the raw HTML output. For example, a simple block:

```html
<!-- Initial server-rendered HTML -->
<div class="hero block" data-block-name="hero">
  <div>
    <picture>...</picture>
  </div>
  <div>
    <h1>Page Title</h1>
  </div>
</div>
```

Gets transformed into:

```html
<!-- Final browser-processed DOM -->
<div class="hero-wrapper">
  <div class="hero block" data-block-name="hero" data-block-status="loaded">
    <div>
      <picture>...</picture>
    </div>
    <div>
      <h1>Page Title</h1>
    </div>
  </div>
</div>
```

Note the key changes:

- Addition of data-block-status="loaded" to indicate JavaScript processing is complete
- Creation of a parent wrapper element with -wrapper suffix
- The DOM structure becomes more complex but more capable

**Section Enhancement**

Sections undergo similar transformations:

```html
<!-- Initial server-rendered HTML -->
<div class="section">
  <div>Content here</div>
</div>
```

Becomes:

```html
<!-- Final browser-processed DOM -->
<div class="section hero-container" data-section-status="loaded">
  <div class="default-content-wrapper">
    Content here
  </div>
</div>
```

Key transformations include:

- Addition of container-specific classes (e.g., hero-container)
- Addition of data-section-status="loaded" tracking attribute
- Wrapping of general content in a `<div class="default-content-wrapper">`

**Button Styling Enhancement**

Simple links written by authors:

```html
<!-- Initial link -->
<p><a href="https://example.com">Get in touch</a></p>
```

Are automatically enhanced into styled buttons:

```html
<!-- Enhanced button -->
<p class="button-container">
  <a href="https://example.com" class="button primary" target="_blank" title="Get in touch">Get in touch</a>
</p>
```

The system automatically:

- Adds appropriate button classes
- Adds parent container classes
- Enhances with additional attributes like title and target

**Media Optimization**

Perhaps the most dramatic transformation happens with images. A simple image in a document:

```html
<!-- Basic image reference -->
<img src="./image.png" alt="Description">
```

Is transformed into a fully optimized, responsive picture element:

```html
<!-- Optimized responsive image -->
<picture>
  <source type="image/webp" srcset="./image.png?width=2000&format=webply&optimize=medium" media="(min-width: 600px)">
  <source type="image/webp" srcset="./image.png?width=750&format=webply&optimize=medium">
  <source type="image/png" srcset="./image.png?width=2000&format=png&optimize=medium" media="(min-width: 600px)">
  <img loading="lazy" alt="Description" src="./image.png?width=750&format=png&optimize=medium" width="1600" height="400">
</picture>
```

This sophisticated transformation:

- Automatically generates multiple image sizes (750px, 2000px)
- Creates WebP versions with appropriate fallbacks
- Adds responsive breakpoints using media queries
- Implements appropriate loading strategy
- Preserves image dimensions for layout stability
- Applies medium optimization for quality/size balance

**Head Section Transformation**

The metadata table from the Google Doc:

```
metadata
title | My Page Title
description | This is a description of my page
image | /path/to/image.jpg
author | Author Name
```

Is expanded into a comprehensive set of SEO and social sharing tags:

```html
<!-- Enhanced head section -->
<title>My Page Title</title>
<meta name="description" content="This is a description of my page">
<meta property="og:title" content="My Page Title">
<meta property="og:description" content="This is a description of my page">
<meta property="og:image" content="/path/to/image.jpg">
<meta property="og:url" content="https://example.com/current-path">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="My Page Title">
<meta name="twitter:description" content="This is a description of my page">
<meta name="twitter:image" content="/path/to/image.jpg">
<link rel="canonical" href="https://example.com/current-path">
<meta name="author" content="Author Name">
```

This transformation creates all the metadata needed for proper SEO and social sharing from a simple table in the document.

**Resource Loading Optimization**

The system automatically applies sophisticated resource loading strategies:

```html
<!-- Script and style loading -->
<script src="/scripts/aem.js" type="module"></script>
<script src="/scripts/scripts.js" type="module"></script>
<link rel="stylesheet" href="/styles/styles.css">
```

And component-specific resources are loaded only when needed:

```html
<link rel="stylesheet" href="/blocks/header/header.css">
<link rel="stylesheet" href="/blocks/footer/footer.css">
```

The hero image loading is specifically optimized for performance:

```html
<!-- Before optimization -->
<img loading="lazy" alt="Hero image" src="...">

<!-- After optimization -->
<img loading="eager" alt="Hero image" src="...">
```

This change ensures the above-the-fold hero image loads as early as possible for better LCP (Largest Contentful Paint) performance.

Through these multiple transformations, what started as a simple document becomes a fully-featured, high-performance web page with sophisticated optimization techniques applied automatically.

This multi-stage process allows content authors to focus on content while the system handles the technical implementation, creating a clean separation of concerns that is central to EDS's document-based authoring philosophy.

## EDS's Three-Phase Loading Strategy

A cornerstone of EDS's performance optimization is its sophisticated three-phase loading strategy, often referred to as E-L-D (Eager-Lazy-Delayed). This strategy is key to maintaining perfect Core Web Vitals scores (100/100/100/100) by carefully managing resource loading.

### Phase E (Eager)

**Purpose**: Loads critical content needed for Largest Contentful Paint (LCP)  
**Timeline**: Begins immediately on page load  
**Components**:

- First section (typically hero)
- Main heading and hero image
- Critical CSS in styles.css
- Core scripts (aem.js and scripts.js)
- Essential functions

It's recommended to keep the aggregate payload before LCP below 100KB for optimal performance. This stringent requirement ensures pages load quickly even on slower connections.

In the code, this is implemented in scripts.js:

```javascript
async function loadEager(doc) {
  document.documentElement.lang = 'en';
  decorateTemplateAndTheme();
  const main = doc.querySelector('main');
  if (main) {
    decorateMain(main);
    document.body.classList.add('appear');
    await loadSection(main.querySelector('.section'), waitForFirstImage);
  }
  sampleRUM.enhance();
  try {
    // if desktop (proxy for fast connection) or fonts already loaded, load fonts.css
    if (window.innerWidth >= 900 || sessionStorage.getItem('fonts-loaded')) {
      loadFonts();
    }
  } catch (e) {
    // do nothing
  }
}
```

Note how it only loads the first section and waits for the first image before proceeding. This targeted approach ensures critical content appears quickly.

### Phase L (Lazy)

**Purpose**: Loads important but non-critical elements  
**Timeline**: Begins after first section is loaded  
**Components**:

- Remaining sections
- Header and footer components
- Non-critical CSS (lazy-styles.css)
- Below-the-fold images
- Additional fonts

The implementation in scripts.js shows this phased approach:

```javascript
async function loadLazy(doc) {
  const main = doc.querySelector('main');
  await loadSections(main);
  const { hash } = window.location;
  const element = hash ? doc.getElementById(hash.substring(1)) : false;
  if (hash && element) element.scrollIntoView();
  loadHeader(doc.querySelector('header'));
  loadFooter(doc.querySelector('footer'));
  loadCSS(`${window.hlx.codeBasePath}/styles/lazy-styles.css`);
  loadFonts();
}
```

This function loads all remaining sections, header, footer, and non-critical CSS only after the eager phase completes.

### Phase D (Delayed)

**Purpose**: Handles lowest-priority elements  
**Timeline**: Begins after a 3-second delay  
**Components**:

- Analytics
- Third-party scripts
- Marketing tools
- Social widgets
- Chat functionality
- Anything loaded through delayed.js

This implementation is deceptively simple:

```javascript
function loadDelayed() {
  // eslint-disable-next-line import/no-cycle
  window.setTimeout(() => import('./delayed.js'), 3000);
  // load anything that can be postponed to the latest here
}
```

The 3-second delay is crucial—it ensures the main content is fully loaded and interactive before any non-essential scripts run. As the documentation notes: "The delayed phase should be at least three seconds after the LCP event to leave enough time for the rest of the experience to get settled."

This is where teams often add their analytics, personalization, cookie consent, and other secondary functionality:

```javascript
// In delayed.js
// Add analytics
(function loadAnalytics() {
  // Load analytics script
  const script = document.createElement('script');
  script.src = 'https://www.googletagmanager.com/gtag/js?id=UA-XXXXXXXX-X';
  script.async = true;
  document.head.appendChild(script);
  
  // Initialize analytics
  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  gtag('js', new Date());
  gtag('config', 'UA-XXXXXXXX-X');
})();

// Add cookie consent banner
(function loadCookieConsent() {
  // Cookie consent implementation
})();
```

This E-L-D pattern ensures the most critical content loads quickly for good user experience, while deferring less important resources to maintain performance scores. It's a key reason why EDS sites can consistently achieve perfect Lighthouse scores even while incorporating sophisticated functionality.

## Core Components of Edge Delivery Services

The EDS system relies on three core JavaScript files that orchestrate the page loading and enhancement process:

### aem.js

This is the foundation of EDS functionality, providing utility functions and core behavior. Without aem.js, your EDS site would be static and unresponsive. Key components include:

- **Initial Setup**: init() function sets up the environment and initializes RUM (Real User Monitoring)
- **Core Utility Functions**: Tools like toClassName(), readBlockConfig(), loadCSS(), and getMetadata()
- **Image Handling**: createOptimizedPicture() creates responsive picture elements
- **DOM Manipulation**: Functions for decorating templates, wrapping text nodes, and processing buttons
- **Section and Block Handling**: Methods for decorating, building, and loading sections and blocks
- **Performance Monitoring**: RUM sampling and tracking for performance analysis

### scripts.js

This file orchestrates the page loading process with the three phases described above:

- **Imports and Utility Functions**: Imports useful functions from aem.js and defines additional utilities
- **Auto Blocking**: Functions that programmatically create blocks from content patterns
- **Loading Phases**:
  - loadEager(): Handles critical elements needed for initial page view
  - loadLazy(): Manages important but non-critical elements
  - loadDelayed(): Deals with the lowest-priority elements after a delay
- **Page Load Orchestration**: Coordinates the entire page loading process

### delayed.js

A simple file meant for custom code that should load after a delay:

```javascript
// add delayed functionality here
```

This file is intentionally minimal, serving as a location where developers can add non-critical functionality without modifying the core files.

## Understanding Blocks in EDS

Blocks are the fundamental building units for custom functionality in EDS. They allow documents to include specialized components and layouts while maintaining the content-first philosophy that makes EDS unique.

### Block Creation in Documents

Authors create blocks using tables in the document:

- The first cell in the first row defines the block type (e.g., "Columns")
- The remaining cells provide the block content
- For variations, authors can specify options in parentheses: "Columns (wide)"

For example, a columns block in a Google Doc might look like this:

```
| Columns              |                       |
| -------------------- | --------------------- |
| Text in first column | Text in second column |
| More content here    | More content here     |
```

When authors want a variation, they simply add it in parentheses:

```
| Columns (dark, wide) |               |
| -------------------- | ------------- |
| Left content         | Right content |
```

The document structure is transformed into HTML, with the table element removed and replaced with appropriate divs and semantic elements.

### Autoblocking in Detail

Beyond manual block creation via tables, EDS offers "autoblocking" — a system where the platform automatically applies styling and structure to content from Google Docs without requiring developers to create custom components for every scenario.

Here's how autoblocking works:

- **Pattern Recognition**: The system identifies common content patterns (like an image followed by a heading)
- **Automatic Transformation**: These patterns are automatically transformed into appropriate blocks
- **Consistent Styling**: The resulting blocks get consistent styling without author intervention

For example, when an author includes an image followed by a heading at the beginning of a document, the autoblocking system might automatically convert this into a hero block without the author needing to create a table.

This is configured in the buildAutoBlocks function in scripts.js:

```javascript
function buildAutoBlocks(main) {
  const h1 = main.querySelector('h1');
  const picture = main.querySelector('picture');
  // eslint-disable-next-line no-bitwise
  if (h1 && picture && (h1.compareDocumentPosition(picture) & Node.DOCUMENT_POSITION_PRECEDING)) {
    const section = document.createElement('div');
    section.append(buildBlock('hero', { elems: [picture, h1] }));
    main.prepend(section);
  }
}
```

Autoblocking allows EDS to provide a rich web experience while minimizing the use of tables in documents, which can interrupt the reading flow for authors.

### Block Development in Code

Each block corresponds to a specific folder and files in your project structure:

```
/blocks/{blockname}/
├── {blockname}.js           # Core block functionality
├── {blockname}.css          # Block styles
├── README.md                # Documentation
├── example.md               # Usage examples
├── demo.md                  # Demo content
├── example.json             # Sample data (if needed)
└── example.csv              # CSV version of sample data
```

This structured organization ensures consistency across blocks and makes maintenance easier. Each file serves a specific purpose:

- **JS file**: Contains the block's logic and DOM manipulation
- **CSS file**: Contains block-specific styling
- **README.md**: Documents the block's purpose and configuration options
- **example.md**: Provides simple examples for content authors
- **demo.md**: Shows more comprehensive, real-world usage

When documenting code examples in Franklin markdown files, remember to use single backticks (not triple backticks) to enclose code snippets for better compatibility with the EDS systems.

A basic block implementation looks like:

```javascript
export default function decorate(block) {
  // Transform the block DOM as needed
  // 'block' is a DOM element with the class 'blockname'
}
```

CSS for blocks should be isolated to prevent affecting other elements:

```css
.blockname {
  /* Block-specific styles */
}

/* Don't style the container directly */
.blockname-container {
  /* AVOID putting styles here */
}

/* Handle variations through class combinations */
.blockname.variation {
  /* Variation-specific styles */
}

/* Ensure responsiveness */
@media (min-width: 768px) {
  .blockname {
    /* Desktop styles */
  }
}
```

EDS passes the block's DOM element to the decorate function, allowing you to transform it as needed. This is where you can add interactivity, fetch data, or reorganize the content.

### Block Variations

A powerful feature of EDS blocks is the ability to create variations with minimal additional code. When authors add parenthetical options to a block:

```
| Columns (dark, wide) |
```

These options become additional CSS classes:

```html
<div class="columns dark wide">
```

This allows you to create styling variations through CSS without needing separate JavaScript implementations. For example:

```css
/* Base block styling */
.columns {
  display: grid;
  gap: 20px;
}

/* Width variation */
.columns.wide {
  max-width: 1200px;
}

/* Color theme variation */
.columns.dark {
  background-color: #333;
  color: white;
}

/* Combined variations create unique looks */
.columns.dark.wide {
  border: 1px solid #555;
}
```

This approach provides tremendous flexibility while keeping the codebase maintainable.

### Data Integration with Blocks

If your block requires external data, you should follow consistent patterns for data structure. Here's an example of the expected JSON structure for data integration:

```json
{
  "total": 1,
  "offset": 0,
  "limit": 1,
  "data": [
    {
      "path": "/example-path",
      "title": "Example Title",
      "image": "/path/to/image.jpg",
      "description": "Example description",
      "lastModified": "1724942455"
    }
  ],
  "type": "sheet"
}
```

To access Franklin pages dynamically, you can use the query-index.json file available in every folder. This powerful feature enables you to create dynamic components that pull content from across your EDS site.

## Extending Functionality Without Modifying Core Files

A key challenge in EDS development is how to extend functionality without modifying the core files. Many teams face common requirements that tempt them to directly edit aem.js or scripts.js:

- Analytics tracking: Adding Google Analytics, Adobe Analytics, or other measurement tools
- Personalization: Implementing user-specific content or A/B testing
- Cookie acceptance prompts: Meeting regulatory requirements for user consent
- GDPR/privacy law compliance: Adding privacy controls and notices
- Dynamic content: Pulling content from third-party APIs or from EDS's query-index.json

As the documentation explains: "All of these code elements must be seamlessly integrated into the browser output while maintaining Edge Delivery Services' perfect Core Web Vitals score (100/100/100/100)."

However, modifying core files directly has significant downsides:

- Upgrade difficulties: When a new version of aem.js is released, your modifications must be carefully reapplied
- Maintenance challenges: Custom modifications become harder to track and maintain
- Knowledge transfer: New team members struggle to understand custom core changes
- Stability risks: Core file modifications may interact unexpectedly with other features

### The Expander Block Pattern

Instead of modifying core files, the recommended approach is to create an "expander block"—a normal block that doesn't modify containing content but includes JavaScript that enhances specific elements after the page is rendered.

For example, here's an implementation of a "code-expander" block that enhances `<pre><code>` elements on the page:

```javascript
/**
 * Minimal Code Expander Block
 * This component enhances pre/code elements on the page with:
 * Copy to clipboard functionality - One-click copy with visual feedback
 * Expand/collapse for long code blocks - Toggles visibility for better readability
 * The component works by finding all pre/code elements, wrapping them in a custom
 * container with controls, and adding event listeners for the interactive features.
 * No syntax highlighting is applied - all code is displayed as plain text.
 */
export default async function decorate(block) { 
  // Configuration values for the component 
  // These control appearance, behavior thresholds, and text labels 
  const THRESHOLD = 40;        // Line count that defines a "long" code block 
  const COPY_TEXT = 'Copy';    // Default button text for copy operation 
  const COPIED_TEXT = 'Copied!'; // Text shown briefly after successful copy 
  const EXPAND_TEXT = 'Expand';  // Text for expanding collapsed code 
  const COLLAPSE_TEXT = 'Collapse'; // Text for collapsing expanded code
  
  // Locate all code blocks on the page 
  // We're targeting standard elements which is the common HTML pattern for code blocks
  const codeElements = document.querySelectorAll('pre code');
  
  // Exit early if no code elements found - nothing to enhance 
  if (codeElements.length === 0) return;
  
  // Process each code element one by one 
  Array.from(codeElements).forEach((codeElement, index) => { 
    // Skip already processed elements to prevent double-enhancement 
    // This is important for pages where the decorator might run multiple times 
    if (codeElement.closest('.code-expander-wrapper')) return;
    
    // Extract the code content and determine if it's a long document
    const code = codeElement.textContent;
    const isLongDocument = code.split('\n').length > THRESHOLD;
    
    // Create the main wrapper element that will contain the enhanced code block
    // This gives us a container to style and to attach the enhanced functionality
    const wrapper = document.createElement('div');
    wrapper.className = 'code-expander-wrapper';
    wrapper.dataset.codeIndex = index; // Store index for potential future reference
    
    // Create the header bar that will contain control buttons
    const header = document.createElement('div');
    header.className = 'code-expander-header';
    
    // Create button container for organizing controls
    const buttonGroup = document.createElement('div');
    buttonGroup.className = 'code-expander-buttons';
    
    // Conditionally add expand/collapse button for long documents only
    // There's no need to add collapse functionality to short snippets
    let expandButton = null;
    if (isLongDocument) {
      expandButton = document.createElement('button');
      expandButton.className = 'code-expander-expand-collapse';
      expandButton.textContent = EXPAND_TEXT;
     
      // Define toggle behavior - switches between expanded and collapsed states
      // Updates button text to match current state for clarity
      expandButton.onclick = () => {
        // Toggle the CSS class that controls expansion state
        newPreElement.classList.toggle('expanded');
       
        // Update button text to reflect the current state
        expandButton.textContent = newPreElement.classList.contains('expanded') 
          ? COLLAPSE_TEXT : EXPAND_TEXT;
      };
      buttonGroup.appendChild(expandButton);
    }
    
    // Add copy button - allows one-click copying of code content
    const copyButton = document.createElement('button');
    copyButton.className = 'code-expander-copy';
    copyButton.textContent = COPY_TEXT;
    
    // Set up the copy functionality using the clipboard API
    // Provides visual feedback when copy succeeds
    copyButton.addEventListener('click', async () => {
      try {
        // Attempt to copy the code to clipboard
        await navigator.clipboard.writeText(code);
        
        // Provide visual feedback that copy succeeded
        copyButton.textContent = COPIED_TEXT;
        
        // Reset button text after a delay
        setTimeout(() => {
          copyButton.textContent = COPY_TEXT;
        }, 2000); // 2-second feedback duration
      } catch (err) {
        // Log error if clipboard operation fails
        // This can happen due to permissions or if executed in insecure context
        console.error('Error copying content:', err);
      }
    });
    buttonGroup.appendChild(copyButton);
    
    // Assemble the header structure
    header.appendChild(buttonGroup);
    wrapper.appendChild(header);
    
    // Create the new code display element
    // This replaces the original pre/code elements but preserves their content
    const newPreElement = document.createElement('pre');
   
    // Apply collapsible class for long documents
    if (isLongDocument) newPreElement.classList.add('collapsible');
    
    // Create and populate the code element
    const newCodeElement = document.createElement('code');
    newCodeElement.textContent = code; // Preserve the original code as plain text
    
    // Assemble the code display structure
    newPreElement.appendChild(newCodeElement);
    wrapper.appendChild(newPreElement);
    
    // Replace the original pre/code element with the enhanced version
    // This is a two-step process to maintain proper DOM structure
    const preElement = codeElement.parentNode; // The parent <pre> of the original <code>
    const container = document.createElement('div'); // Create container for replacement
   
    // Perform the swap - remove original and insert enhanced version
    preElement.parentNode.replaceChild(container, preElement);
    container.appendChild(wrapper);
  });
}
```

Note the key aspects of this implementation:

- Non-invasive approach: It enhances existing elements without modifying core files
- Configuration at the top: All configurable values are defined as constants at the top
- Thorough documentation: Clear comments explain the purpose and function
- Robust error handling: Try/catch blocks prevent failures from breaking the page
- Clean modularity: Each function has a single responsibility
- Performance consciousness: Uses modern APIs and efficient DOM operations

This pattern allows you to extend functionality without the risks associated with modifying core files.

When developing with EDS, you should follow specific coding standards to ensure your code is maintainable and compatible with future updates:

```javascript
// Use configuration constants at the top of your code
const BLOCKNAME_CONFIG = {
  BOOK_TITLE: 'Code',
  ERROR_MESSAGE: 'Error loading content. Please try again.',
  COPY_BUTTON_RESET_DELAY: 2000,
  LONG_DOCUMENT_THRESHOLD: 40,
  // Add other configuration options here
};
```

When writing code that uses console output, remember to precede it with:

```javascript
// eslint-disable-next-line no-console
console.log('Debug information');
```

This prevents ESLint errors while maintaining the ability to use console logging for debugging purposes.

## Common Implementation Challenges and Solutions

Teams developing with EDS often encounter similar challenges. Here are practical solutions to common problems:

### Challenge: Analytics Implementation

**Problem**: Adding analytics without modifying core files.

**Solution**: Use the delayed.js file for analytics scripts:

```javascript
// In delayed.js
(function() {
  // Create script element
  const script = document.createElement('script');
  script.async = true;
  script.src = 'https://www.googletagmanager.com/gtag/js?id=UA-XXXXXXXX-X';
  document.head.appendChild(script);
  
  // Initialize analytics
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  gtag('js', new Date());
  gtag('config', 'UA-XXXXXXXX-X');
  
  // Add custom event tracking
  document.addEventListener('click', e => {
    const target = e.target.closest('a, button');
    if (!target) return;
    
    const trackingData = {
      event_category: target.tagName.toLowerCase(),
      event_label: target.innerText || target.textContent,
    };
    
    if (target.href) {
      trackingData.outbound = !target.href.includes(window.location.hostname);
    }
    
    gtag('event', 'click', trackingData);
  });
})();
```

### Challenge: Dynamic Content from External APIs

**Problem**: Incorporating content from external services.

When integrating with external data sources or the EDS query-index.json, you should follow a consistent pattern for data structures. Here's an example of the expected JSON structure for data integration:

```json
{
  "total": 1,
  "offset": 0,
  "limit": 1,
  "data": [
    {
      "path": "/example-path",
      "title": "Example Title",
      "image": "/path/to/image.jpg",
      "description": "Example description",
      "lastModified": "1724942455"
    }
  ],
  "type": "sheet"
}
```

**Solution**: Create a specialized block that fetches and formats the content:

```javascript
export default async function decorate(block) {
  const config = readBlockConfig(block);
  const apiUrl = config.apiUrl || 'https://api.example.com/data';
  
  try {
    // Clear initial content
    block.textContent = '';
    
    // Show loading state
    const loading = document.createElement('div');
    loading.className = 'loading-indicator';
    loading.textContent = 'Loading content...';
    block.appendChild(loading);
    
    // Fetch data
    const response = await fetch(apiUrl);
    if (!response.ok) throw new Error(`API returned ${response.status}`);
    const data = await response.json();
    
    // Remove loading state
    loading.remove();
    
    // Render content
    const container = document.createElement('div');
    container.className = 'dynamic-content';
    
    data.items.forEach(item => {
      const itemEl = document.createElement('div');
      itemEl.className = 'dynamic-item';
      
      const title = document.createElement('h3');
      title.textContent = item.title;
      itemEl.appendChild(title);
      
      const desc = document.createElement('p');
      desc.textContent = item.description;
      itemEl.appendChild(desc);
      
      container.appendChild(itemEl);
    });
    
    block.appendChild(container);
  } catch (error) {
    console.error('Error loading dynamic content:', error);
    
    // Show error state
    block.textContent = '';
    const errorEl = document.createElement('div');
    errorEl.className = 'error-state';
    errorEl.textContent = 'Unable to load content. Please try again later.';
    block.appendChild(errorEl);
  }
}
```

### Challenge: Cookie Consent Implementation

**Problem**: Implementing cookie consent without modifying core files.

**Solution**: Create a cookie-consent block that's included in the template:

```javascript
export default function decorate(block) {
  // Hide the original block
  block.style.display = 'none';
  
  // Check if consent already given
  if (localStorage.getItem('cookie-consent') === 'accepted') {
    // Consent already given, enable cookies/tracking
    enableTracking();
    return;
  }
  
  // Create consent banner
  const banner = document.createElement('div');
  banner.className = 'cookie-consent-banner';
  banner.innerHTML = `
    <div class="cookie-content">
      <p>This website uses cookies to ensure you get the best experience. 
      <a href="/privacy-policy">Learn more</a></p>
      <div class="cookie-buttons">
        <button class="accept-button">Accept</button>
        <button class="decline-button">Decline</button>
      </div>
    </div>
  `;
  
  // Add event listeners
  banner.querySelector('.accept-button').addEventListener('click', () => {
    localStorage.setItem('cookie-consent', 'accepted');
    banner.remove();
    enableTracking();
  });
  
  banner.querySelector('.decline-button').addEventListener('click', () => {
    localStorage.setItem('cookie-consent', 'declined');
    banner.remove();
  });
  
  // Add to page
  document.body.appendChild(banner);
}

function enableTracking() {
  // Load analytics and other tracking scripts
  const script = document.createElement('script');
  script.src = '/scripts/tracking.js';
  document.head.appendChild(script);
}
```

### Challenge: Personalization

**Problem**: Implementing personalization without complex frameworks.

**Solution**: Use local storage for simple personalization:

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
}

function determineInterests(pageVisits) {
  // Simple interest determination based on URL patterns
  const interests = {};
  
  pageVisits.forEach(visit => {
    if (visit.path.includes('/products/')) {
      interests.products = true;
    } else if (visit.path.includes('/services/')) {
      interests.services = true;
    } else if (visit.path.includes('/blog/')) {
      interests.blog = true;
    }
  });
  
  return interests;
}

function personalizeContent(block, userProfile) {
  // Clear block contents
  block.textContent = '';
  
  // Generate personalized content based on interests
  const heading = document.createElement('h2');
  heading.textContent = userProfile.interests.products 
    ? 'Products You Might Like' 
    : 'Our Popular Products';
  
  block.appendChild(heading);
  
  // ... additional personalized content ...
}
```

These practical solutions demonstrate how to implement common requirements within EDS's architectural constraints, without modifying core files or compromising performance.

Based on the examined code and documentation, here are key best practices for EDS development:

### CSS Best Practices

- **Block Isolation**: Every CSS selector in a block's CSS should only apply to that block
- **Structure with Flexbox/Grid**: Modern CSS layout techniques create responsive designs
- **Mobile-First Approach**: Base styles for mobile, then add media queries for larger screens
- **Consistent Class Naming**: Follow patterns like .blockname-element-state
- **Use CSS Variables**: Leverage custom properties for consistent theming
- **Never Style Container**: Don't apply styles directly to .blockname-container
- **Support Variations**: Handle block variations through class combinations
- **Ensure Responsiveness**: Include responsive design for different screen sizes

```css
/* Block-specific styles should be isolated */
.myblock {
  /* Only apply to elements within .myblock */
  padding: 20px;
}

/* Don't let selectors become too complex */
.myblock > div > div > p {
  /* AVOID: Too specific and fragile */
}

/* Mobile-first approach without initial media queries */
.columns {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

/* Standard breakpoints at 600px, 900px, 1200px */
@media (min-width: 600px) {
  .columns {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 900px) {
  .columns {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Use CSS variables for theming and configuration */
:root {
  --primary-color: #1473e6;
  --heading-font: 'Adobe Clean', sans-serif;
  --body-font: 'Adobe Clean', sans-serif;
  --spacing-m: 16px;
}

.button {
  background-color: var(--primary-color);
  font-family: var(--body-font);
  padding: var(--spacing-m);
}
```

Key principles to follow:

- **Block Isolation**: "Every CSS selector in the .css of a block only applies to the block"
- **Simplicity**: "Don't let your CSS Selectors become complex and unreadable"
- **Mobile First**: "Your CSS without media query should render a mobile site"
- **Standard Breakpoints**: "Generally use 600px, 900px and 1200px as your breakpoints, all min-width"
- **Variable-Based Configuration**: Use CSS variables for theme colors, spacing, and other configurable values

### JavaScript Best Practices

The JavaScript approach in EDS emphasizes simplicity and performance. It's recommended to adhere to Airbnb's JavaScript Style Guide to ensure clean, maintainable code. This widely-adopted style guide provides consistent conventions for variable naming, function declarations, object creation, conditional statements, error handling, and comments.

```javascript
// Configuration variables at the top
const CONFIG = {
  ANIMATION_DURATION: 300,
  MAX_ITEMS: 12,
  API_ENDPOINT: '/query-index.json',
};

// Use async/await for cleaner asynchronous code
export default async function decorate(block) {
  try {
    // Fetch data asynchronously
    const response = await fetch(CONFIG.API_ENDPOINT);
    const data = await response.json();
    
    // Process data
    const filteredItems = data.data
      .filter(item => item.type === 'blog')
      .slice(0, CONFIG.MAX_ITEMS);
    
    // Update UI
    renderItems(block, filteredItems);
  } catch (error) {
    // Handle errors gracefully
    // eslint-disable-next-line no-console
    console.error('Error loading content:', error);
    renderErrorState(block);
  }
}

// Break logic into focused functions
function renderItems(block, items) {
  // Clear existing content
  block.textContent = '';
  
  // Create container
  const container = document.createElement('div');
  container.className = 'items-container';
  
  // Add items
  items.forEach(item => {
    container.appendChild(createItemElement(item));
  });
  
  // Add to DOM
  block.appendChild(container);
}

function createItemElement(item) {
  // Create element for single item
  // ...
}

function renderErrorState(block) {
  // Show user-friendly error state
  // ...
}
```

Key principles:

- **Keep It Simple**: "Frameworks often introduce web performance issues... while trying to address trivial problems"
- **Modern Features**: "Make sure the features you are using are well supported by evergreen browsers"
- **Configuration at Top**: Place all configurable values in a config object at the top
- **Function Separation**: Each function should have a single responsibility
- **Error Handling**: Always include robust error handling
- **Asynchronous Best Practices**: Use async/await for cleaner asynchronous code

### Content Structure Best Practices

How content is structured in documents significantly impacts both authoring experience and website performance:

- **Minimize Blocks**: "Blocks are not great for authoring... It is definitely an anti-pattern to have things that are represented natively as default content and put them into a block." Use blocks only when necessary for specialized components.

- **No Nested Blocks**: "Nested blocks are definitely a lot worse" for authoring experience. Keep block structure flat for easier authoring.

- **Use Full URLs**: "Authors (and most humans) often think of a URL as an opaque token... It is always advisable to just let authors work with fully qualified URLs." Don't try to normalize or transform URLs unnecessarily.

- **Reuse Standards**: "The EDS Block Collection is a great source for well designed content models." Don't reinvent the wheel—use existing patterns when possible.

- **Progressive Enhancement**: Start with the simplest possible implementation and enhance as needed, rather than building complex solutions from the start.

### Documentation Best Practices

Comprehensive documentation is crucial for block maintainability:

```
/blocks/myblock/
├── myblock.js
├── myblock.css
├── README.md           # Comprehensive documentation
├── example.md          # Simple copy-paste example for authors
└── demo.md             # More complex real-world usage examples
```

README.md should include:

- Purpose and functionality
- Configuration options
- Usage instructions for authors
- Accessibility considerations
- Performance impact
- Variations and examples

This comprehensive documentation approach ensures both developers and content authors can effectively work with your blocks.

## Advanced Techniques

### Dynamic Content with Query Index

EDS provides a powerful indexing system for creating dynamic content:

```javascript
// Access indexed content
fetch('/query-index.json')
  .then(response => response.json())
  .then(data => {
    // Filter for specific content
    const filteredItems = data.data.filter(item => 
      item.path.includes('/blogs/')
    );
    
    // Sort as needed
    const sortedItems = filteredItems.sort((a, b) => 
      new Date(b.lastModified) - new Date(a.lastModified)
    );
    
    // Generate HTML
    const html = sortedItems.map(item => `
      <article>
        <h3><a href="${item.path}">${item.title}</a></h3>
        <p>${item.description}</p>
      </article>
    `).join('');
    
    // Update the DOM
    container.innerHTML = html;
  });
```

This technique is used in the BlogList block to create dynamic content listings without requiring authors to manually update links.

### Auto Blocking

Auto blocking programmatically creates blocks based on content patterns:

```javascript
function buildHeroBlock(main) {
  const h1 = main.querySelector('h1');
  const picture = main.querySelector('picture');
  // If h1 follows picture in the DOM
  if (h1 && picture && (h1.compareDocumentPosition(picture) & Node.DOCUMENT_POSITION_PRECEDING)) {
    const section = document.createElement('div');
    section.append(buildBlock('hero', { elems: [picture, h1] }));
    main.prepend(section);
  }
}
```

This allows you to automatically enhance document patterns without requiring authors to create block tables.

### Custom Block Libraries

Create a block library to help authors discover and use available blocks:

```html
<!-- /tools/sidekick/library.html -->
<!DOCTYPE html>
<html>
<head>
  <title>Block Library</title>
  <script src="https://www.aem.live/tools/sidekick/library/library.js"></script>
</head>
<body>
  <sidekick-library config='{"base": "/blocks", "blocks": [{"name": "Hero"}, {"name": "Cards"}]}'>
  </sidekick-library>
</body>
</html>
```

This enhances the authoring experience by providing a visual reference for available blocks.

## Block Library Examples

To help you get started with EDS development, here are some additional block implementations showcasing different patterns and techniques.

### Fortune Cookie Block

A simple block that fetches and displays random quotes:

```javascript
export default async function decorate(block) {
    const fortuneCookieElement = document.querySelector('.fortunecookie');
    const url = '/data/cookies.json';
    try {
        const response = await fetch(url);
        const data = await response.json();
        
        const dataArray = data.data;
        const randomIndex = Math.floor(Math.random() * dataArray.length);
        const randomItem = dataArray[randomIndex];
        const content = `<p><strong>${randomItem.key}:</strong> ${randomItem.value}</p>`;
        fortuneCookieElement.innerHTML = content;
    } catch (error) {
        // eslint-disable-next-line no-console
        console.error('Error fetching the JSON data:', error);
    }
}
```

This block demonstrates fetching JSON data and using it to update content dynamically.

### Index Block

A block that builds a table of contents for the page:

```javascript
export default function decorate(block) {
  const headers = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
  const indexBlock = document.querySelector('.index');
  
  // Create the index header
  const indexHeader = document.createElement('div');
  indexHeader.className = 'index-header';
  indexHeader.innerHTML = `
    <span>Index</span>
    <i class='arrow down'></i>
  `;
  
  // Create the index content container
  const indexContent = document.createElement('div');
  indexContent.className = 'index-content';
  
  // Append the index header and content container to the index block
  indexBlock.appendChild(indexHeader);
  indexBlock.appendChild(indexContent);
  let isIndexBuilt = false; // Flag to track if the index has been built
  indexHeader.addEventListener('click', () => {
    if (!isIndexBuilt) {
      buildIndex();
      isIndexBuilt = true; // Set the flag to true after building the index
      indexContent.style.display = 'none';
    }
    if (indexContent.style.display === 'none') {
      indexContent.style.display = 'block';
      indexHeader.querySelector('.arrow').style.transform = 'rotate(-135deg)';
    } else {
      indexContent.style.display = 'none';
      indexHeader.querySelector('.arrow').style.transform = 'rotate(45deg)';
    }
  });
  function buildIndex() {
    const indexContent2 = document.querySelector('.index-content');
    const ul = document.createElement('ul');
    headers.forEach((header, index) => {
      const id = `header-${index}`;
      header.id = id;
      const li = document.createElement('li');
      li.style.marginLeft = `${(parseInt(header.tagName[1], 10) - 1) * 20}px`;
      const a = document.createElement('a');
      a.href = `#${id}`;
      a.textContent = header.textContent;
      li.appendChild(a);
      ul.appendChild(li);
    });
    indexContent2.innerHTML = '';
    indexContent2.appendChild(ul);
  }
}
```

The CSS for this block creates a collapsible interface:

```css
.index {
    background-color: #f5f5f5;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 10px;
    cursor: pointer;
}
.index-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.arrow {
    border: solid black;
    border-width: 0 2px 2px 0;
    display: inline-block;
    padding: 3px;
    transition: transform 0.3s;
}
.down {
    -webkit-transform: rotate(45deg);
    transform: rotate(45deg);
}
.index-content {
    display: none;
    margin-top: 10px;
}
.index-content ul {
    list-style-type: none;
    padding: 0;
}
.index-content ul li {
    margin-bottom: 5px;
}
.index-content ul li a {
    text-decoration: none;
    color: #333;
}
```

This block demonstrates:

- Lazy initialization (only building the index when needed)
- Dynamic DOM manipulation
- Interactive UI elements
- Content discovery enhancement

### Return To Top Block

A utility block that provides a "scroll to top" button:

```javascript
export default async function decorate(block) {
  const returnToTopButton = document.querySelector('.returntotop');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
      returnToTopButton.style.display = 'block';
    } else {
      returnToTopButton.style.display = 'none';
    }
  });
  // Scroll to top when the button is clicked
  returnToTopButton.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  });
}
```

With accompanying CSS:

```css
.returntotop {
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 10px 20px;
    background-color: #007BFF;
    color: white;
    cursor: pointer;
    text-align: center;
    border-radius: 5px;
    text-decoration: none;
    font-size: 14px;
    display: none;
}
.returntotop:hover {
    background-color: #0056b3;
}
```

This simple utility block demonstrates:

- Event handling
- Fixed positioning
- User experience enhancement
- Conditional display based on scroll position

These examples showcase the variety of functionality that can be implemented as blocks in Edge Delivery Services, from content enhancement to user interface improvements, all without modifying core files.

## Conclusion

### Document-First Content Management

EDS fundamentally reverses the traditional CMS paradigm—instead of forcing authors to adapt to technical constraints, it adapts technical implementation to how authors naturally work. This philosophical shift has profound implications:

- **Natural Authoring Flow**: Authors use familiar tools (Google Docs, Word) without needing to understand web technologies
- **Separation of Concerns**: Content creation and technical implementation remain cleanly separated
- **Focus on Content**: The emphasis stays on the content itself, not on the technical container

As the documentation states: "In an ideal situation the majority of content is authored outside of blocks, as introducing tables into a document makes it harder to read and edit." This content-first approach challenges the component-first mentality that dominates most CMS platforms.

### Simplicity Over Complexity

Throughout EDS's implementation, there's a relentless focus on simplicity:

- **No Build Process**: Direct JavaScript and CSS without transpilation or processing
- **No Dependencies**: No external libraries or frameworks to manage
- **Clear Structure**: Well-defined roles for each part of the codebase
- **Minimal Core**: Small, focused JavaScript files that do specific jobs well

This simplicity-first approach delivers tremendous benefits in terms of maintainability, performance, and developer onboarding. Rather than relying on complex toolchains and frameworks, EDS pushes developers to solve problems directly with fundamental web technologies.

### Performance by Design

EDS doesn't treat performance as an afterthought or something to be optimized later—it's built into the core architecture:

- **Three-Phase Loading**: The E-L-D pattern ensures critical content loads first
- **Resource Optimization**: Automatic image optimization, responsive images, and format selection
- **Minimal JavaScript**: No heavy frameworks or unnecessary code
- **Progressive Enhancement**: Core content works even before enhancement scripts run
- **Smart Prioritization**: Resources load based on visibility and importance

This architecture consistently delivers perfect Lighthouse scores (100/100/100/100), something many development teams struggle to achieve even with significant optimization efforts.

### Empowering Both Authors and Developers

The EDS approach creates a system where:

- Authors can focus on creating great content in familiar tools
- Developers can build powerful functionality without disrupting content workflows
- Both teams can work simultaneously without blocking each other

This balance is rare in content management systems, which tend to prioritize either developer experience or author experience at the expense of the other.

### The Expander Pattern for Extension

Perhaps most importantly, EDS promotes the "expander" pattern for extending functionality without modifying core files. This pattern:

- **Preserves Upgradeability**: Core files remain untouched, allowing easy upgrades
- **Maintains Separation**: Custom functionality stays isolated and self-contained
- **Encourages Modularity**: Extensions are organized into distinct, focused blocks
- **Supports Selective Loading**: Extensions can be conditionally applied based on page type

By embracing this pattern, development teams can add sophisticated functionality—analytics, personalization, third-party integrations—without the risk and maintenance burden of modifying core files.

### Final Thoughts

Edge Delivery Services represents a refreshing perspective in web development—one that challenges many contemporary assumptions about how websites should be built and managed. By embracing document-based authoring, prioritizing performance by design, and promoting clean separation between content and code, EDS delivers a compelling alternative to traditional CMS platforms.

For developers accustomed to component-based systems and complex build processes, EDS might initially feel constraining. However, these constraints often foster creativity and focus attention on solving real problems rather than managing tooling complexity. The result is websites that are faster, more maintainable, and more author-friendly.

As you implement your own EDS projects, remember these key principles:

- **Respect the Document**: Prioritize the natural flow of document-based authoring
- **Embrace Constraints**: Let EDS's limitations guide you toward simpler, more effective solutions
- **Performance First**: Consider performance implications in every decision
- **Don't Modify Core Files**: Use the expander pattern for extensions
- **Document Everything**: Create comprehensive documentation for blocks and systems

By following these principles, you'll create websites that achieve the rare combination of excellent performance, maintainable code, and superior authoring experience that Edge Delivery Services makes possible.

# Appendix: Edge Delivery Services Development Reference Guide

## Configuration Constants Example

When developing blocks for EDS, use configuration constants at the top of your JavaScript files to make your code more maintainable:

const BLOCKNAME\_CONFIG \= {

  BOOK\_TITLE: 'Code',

  ERROR\_MESSAGE: 'Error loading content. Please try again.',

  COPY\_BUTTON\_RESET\_DELAY: 2000,

  LONG\_DOCUMENT\_THRESHOLD: 40,

  // Add other configuration options here

};

This pattern makes it easier to find and modify configuration values, improves code readability, and prevents magic numbers or strings from being scattered throughout your code.

## ESLint Integration

When writing code that uses console output, remember to precede it with:

// eslint-disable-next-line no-console

console.log('Debug information');

This prevents ESLint errors while maintaining the ability to use console logging for debugging purposes. This is important because EDS follows the Airbnb JavaScript Style Guide, which discourages console output in production code.

## Standard Data Structure

When integrating with external data sources or the EDS query-index.json, follow this consistent pattern for JSON data structures:

{

  "total": 1,

  "offset": 0,

  "limit": 1,

  "data": \[

    {

      "path": "/example-path",

      "title": "Example Title",

      "image": "/path/to/image.jpg",

      "description": "Example description",

      "lastModified": "1724942455"

    }

  \],

  "type": "sheet"

}

This structure works well with EDS's built-in query functionality and makes it easier to create consistent data handling patterns across your site.

## CSS Variables for Theming

Define configuration through CSS variables to create consistent, flexible theming:

:root {

  \--primary-color: \#1473e6;

  \--secondary-color: \#2680eb;

  \--text-color: \#2c2c2c;

  \--background-light: \#f5f5f5;

  \--background-dark: \#333333;

  \--heading-font: 'Adobe Clean', sans-serif;

  \--body-font: 'Adobe Clean', sans-serif;

  \--spacing-xs: 4px;

  \--spacing-s: 8px;

  \--spacing-m: 16px;

  \--spacing-l: 24px;

  \--spacing-xl: 32px;

  \--border-radius: 4px;

  \--shadow-small: 0 1px 3px rgba(0,0,0,0.12);

  \--shadow-medium: 0 4px 6px rgba(0,0,0,0.12);

  \--shadow-large: 0 10px 20px rgba(0,0,0,0.12);

}

/\* Using variables in components \*/

.button {

  background-color: var(--primary-color);

  color: white;

  padding: var(--spacing-s) var(--spacing-m);

  border-radius: var(--border-radius);

  font-family: var(--body-font);

  box-shadow: var(--shadow-small);

}

.card {

  background-color: white;

  border-radius: var(--border-radius);

  padding: var(--spacing-m);

  box-shadow: var(--shadow-medium);

}

This approach makes it much easier to maintain a consistent visual identity across your site and simplifies theme changes.

## Standard Breakpoints

EDS follows a common set of breakpoints for responsive design:

/\* Mobile (default) \*/

.component {

  /\* Mobile styles \*/

}

/\* Tablet \*/

@media (min-width: 600px) {

  .component {

    /\* Tablet styles \*/

  }

}

/\* Desktop \*/

@media (min-width: 900px) {

  .component {

    /\* Desktop styles \*/

  }

}

/\* Large Desktop \*/

@media (min-width: 1200px) {

  .component {

    /\* Large desktop styles \*/

  }

}

Always use `min-width` queries and design mobile-first, adding complexity for larger screens rather than trying to simplify for smaller screens.

## Block Variation Pattern

For blocks that support variations, follow this pattern:

/\* Base block styling \*/

.blockname {

  /\* Default styles \*/

}

/\* Size variations \*/

.blockname.small {

  /\* Small variation \*/

}

.blockname.large {

  /\* Large variation \*/

}

/\* Color theme variations \*/

.blockname.dark {

  /\* Dark theme \*/

}

.blockname.light {

  /\* Light theme \*/

}

/\* Layout variations \*/

.blockname.centered {

  /\* Centered layout \*/

}

.blockname.split {

  /\* Split layout \*/

}

/\* Combined variations \*/

.blockname.dark.centered {

  /\* Special styles for dark+centered combination \*/

}

This approach allows authors to specify variations in the document (e.g., `Blockname (dark, centered)`) without requiring additional JavaScript logic.

## Documentation Template

When documenting a block, include the following sections in your README.md:

\# Block Name

\#\# Overview

Brief description of what the block does and its primary use cases.

\#\# Content Structure

Explain how authors should structure content in Google Docs to use this block.

\#\#\# Example Table Structure

| BlockName |                 |

|-----------|-----------------|

| Content A | Content B       |

| More here | More here       |

\#\# Variations

List all supported variations with examples:

\- \*\*dark\*\*: Applies a dark color scheme

\- \*\*wide\*\*: Expands the block to use more horizontal space

\- \*\*centered\*\*: Centers the content within the block

\#\#\# Variation Examples

| BlockName (dark) |                 |

|------------------|-----------------|

| Content          | Content         |

\#\# Configuration Options

Any custom configuration options available for developers.

\#\# Accessibility Considerations

Notes on accessibility features and considerations.

\#\# Performance Impact

Any notable performance considerations or optimizations.

\#\# Dependencies

List any dependencies or requirements.

\#\# Known Limitations

Document any known issues or limitations.

This comprehensive documentation structure ensures that both developers and content authors can effectively use your blocks.

## Resource Loading Patterns

Follow these patterns for optimal resource loading:

### CSS Loading

// Load CSS asynchronously

function loadCSS(href) {

  const link \= document.createElement('link');

  link.rel \= 'stylesheet';

  link.href \= href;

  document.head.appendChild(link);

  return link;

}

// Usage

loadCSS('/blocks/myblock/myblock.css');

### Lazy JavaScript Loading

// Load script only when needed

async function loadScript(src) {

  return new Promise((resolve, reject) \=\> {

    const script \= document.createElement('script');

    script.src \= src;

    script.onload \= resolve;

    script.onerror \= reject;

    document.head.appendChild(script);

  });

}

// Usage with async/await

try {

  await loadScript('/scripts/feature.js');

  // Script is now loaded and can be used

} catch (error) {

  console.error('Failed to load script:', error);

}

### Delayed Functionality

// Delay non-critical functionality

function delayFunction(func, delay \= 3000\) {

  setTimeout(func, delay);

}

// Usage

delayFunction(() \=\> {

  // Initialize non-critical features

  loadChatWidget();

  setupAnalytics();

});

These patterns help ensure optimal performance by loading resources in the right order and at the right time.  
