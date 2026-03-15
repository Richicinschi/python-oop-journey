// Type declarations for JSON imports

declare module '*.json' {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const value: unknown;
  export default value;
}
