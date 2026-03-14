module.exports = {
  ci: {
    collect: {
      // Use static build
      staticDistDir: './apps/web/dist',
      // Or use startServerCommand for dynamic
      // startServerCommand: 'cd apps/web && npm run start',
      // startServerReadyPattern: 'Ready on',
      // startServerReadyTimeout: 60000,
      
      // URLs to test
      url: [
        'http://localhost:3000/',
        'http://localhost:3000/weeks',
        'http://localhost:3000/problems/problem-01-calculate-sum',
        'http://localhost:3000/dashboard',
      ],
      
      // Number of runs for median score
      numberOfRuns: 3,
      
      // Settings
      settings: {
        preset: 'desktop',
        chromeFlags: '--no-sandbox --headless',
        // Emulated form factor
        emulatedFormFactor: 'desktop',
        // Throttling
        throttling: {
          // Simulate fast 4G
          rttMs: 40,
          throughputKbps: 10240,
          cpuSlowdownMultiplier: 1,
        },
      },
    },
    
    assert: {
      // Performance assertions
      assertions: {
        // Core Web Vitals
        'categories:performance': ['warn', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.95 }],
        'categories:best-practices': ['warn', { minScore: 0.9 }],
        'categories:seo': ['warn', { minScore: 0.9 }],
        
        // Metric thresholds
        'first-contentful-paint': ['warn', { maxNumericValue: 1800 }],
        'largest-contentful-paint': ['warn', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['warn', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['warn', { maxNumericValue: 200 }],
        'interactive': ['warn', { maxNumericValue: 3800 }],
        
        // Resource budgets
        'resource-summary:document:size': ['warn', { maxNumericValue: 50000 }], // 50KB
        'resource-summary:script:size': ['warn', { maxNumericValue: 500000 }], // 500KB
        'resource-summary:image:size': ['warn', { maxNumericValue: 2000000 }], // 2MB
        'resource-summary:font:size': ['warn', { maxNumericValue: 100000 }], // 100KB
        'resource-summary:stylesheet:size': ['warn', { maxNumericValue: 100000 }], // 100KB
        'resource-summary:total:size': ['warn', { maxNumericValue: 3000000 }], // 3MB
        
        // Request counts
        'resource-summary:script:count': ['warn', { maxNumericValue: 15 }],
        'resource-summary:total:count': ['warn', { maxNumericValue: 50 }],
      },
    },
    
    upload: {
      // Upload target
      target: 'temporary-public-storage',
      
      // GitHub status check
      githubAppToken: process.env.LHCI_GITHUB_APP_TOKEN,
      
      // Comment on PR
      githubToken: process.env.GITHUB_TOKEN,
    },
    
    server: {
      // Storage for historical data
      storage: {
        storageMethod: 'sql',
        sqlDialect: 'sqlite',
        sqlDatabasePath: '/tmp/lhci.db',
      },
    },
  },
};
