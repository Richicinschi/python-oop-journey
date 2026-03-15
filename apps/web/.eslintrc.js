/** @type {import('eslint').Linter.Config} */
module.exports = {
  extends: ['next/core-web-vitals', 'next/typescript'],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    project: './tsconfig.json',
  },
  rules: {
    // Next.js specific
    '@next/next/no-html-link-for-pages': 'error',
    '@next/next/no-img-element': 'warn',
    
    // TypeScript
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    
    // React
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',
    'react/prop-types': 'off',
    'react/react-in-jsx-scope': 'off',
    
    // General
    'no-console': ['warn', { allow: ['error', 'warn'] }],
    'prefer-const': 'error',
    'no-var': 'error',
  },
  ignorePatterns: [
    '.next/',
    'node_modules/',
    '*.config.js',
    '*.config.ts',
  ],
};
