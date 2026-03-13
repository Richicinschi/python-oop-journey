/** @type {import('next').NextConfig} */
const nextConfig = {
  // Production output configuration
  output: 'standalone',
  
  // Experimental features for optimization
  experimental: {
    externalDir: true,
    optimizePackageImports: [
      'lucide-react',
      '@radix-ui/react-dialog',
      '@radix-ui/react-dropdown-menu',
      '@radix-ui/react-tabs',
      '@radix-ui/react-select',
      '@radix-ui/react-tooltip',
      '@radix-ui/react-progress',
      '@radix-ui/react-scroll-area',
      '@radix-ui/react-collapsible',
      '@radix-ui/react-context-menu',
      'date-fns',
    ],
    // Optimize CSS
    optimizeCss: true,
    // Turbo mode for faster builds
    turbo: {
      rules: {
        '*.svg': {
          loaders: ['@svgr/webpack'],
          as: '*.js',
        },
      },
    },
  },
  
  // Transpile packages
  transpilePackages: ['@oop-journey/ui', '@oop-journey/shared', '@repo/types'],
  
  // Image optimization
  images: {
    formats: ['image/webp', 'image/avif'],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.jsdelivr.net',
      },
      {
        protocol: 'https',
        hostname: '**.githubusercontent.com',
      },
    ],
    // Enable image optimization in production
    unoptimized: process.env.NODE_ENV === 'development',
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
  
  // Compression
  compress: true,
  
  // Headers for caching and security
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on',
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=63072000; includeSubDomains; preload',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
      {
        source: '/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/_next/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/api/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'no-store, no-cache, must-revalidate, proxy-revalidate',
          },
        ],
      },
    ];
  },
  
  // Redirects
  async redirects() {
    return [];
  },
  
  // Rewrites
  async rewrites() {
    return [];
  },
  
  // Webpack configuration
  webpack: (config, { dev, isServer }) => {
    // Optimize Monaco Editor chunks
    if (!dev && !isServer) {
      config.optimization = {
        ...config.optimization,
        splitChunks: {
          chunks: 'all',
          cacheGroups: {
            // Vendor chunk for node_modules
            vendor: {
              name: 'vendors',
              test: /[\\/]node_modules[\\/]/,
              priority: 10,
              reuseExistingChunk: true,
            },
            // Monaco Editor chunk
            monaco: {
              name: 'monaco-editor',
              test: /[\\/]node_modules[\\/]monaco-editor[\\/]/,
              priority: 20,
              reuseExistingChunk: true,
            },
            // UI components chunk
            ui: {
              name: 'ui-components',
              test: /[\\/]packages[\\/]ui[\\/]/,
              priority: 15,
              reuseExistingChunk: true,
            },
            // Common chunk
            common: {
              name: 'common',
              minChunks: 2,
              priority: 5,
              reuseExistingChunk: true,
            },
          },
        },
      };
    }
    
    return config;
  },
  
  // Performance budgets
  performance: {
    // Warn if bundles exceed these sizes
    maxInitialJsResourceSize: 500 * 1024, // 500KB
    maxInitialCssResourceSize: 100 * 1024, // 100KB
  },
  
  // Logging
  logging: {
    fetches: {
      fullUrl: process.env.NODE_ENV === 'development',
    },
  },
  
  // Disable x-powered-by header
  poweredByHeader: false,
  
  // Generate ETags for caching
  generateEtags: true,
  
  // Trailing slash handling
  trailingSlash: false,
};

module.exports = nextConfig;
