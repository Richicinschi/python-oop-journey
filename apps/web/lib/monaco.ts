"use client";

import { loader } from "@monaco-editor/react";
import type { Monaco } from "@monaco-editor/react";

// Configure Monaco loader for dynamic import
export const configureMonacoLoader = () => {
  loader.config({
    paths: {
      vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs",
    },
  });
};

// Initialize Monaco with Python language support
export const initializeMonaco = (monaco: Monaco) => {
  // Configure Python language features
  monaco.languages.register({ id: "python" });

  // Set up Python syntax highlighting using built-in Monarch tokenizer
  monaco.languages.setMonarchTokensProvider("python", {
    defaultToken: "",
    tokenPostfix: ".python",

    keywords: [
      "and",
      "as",
      "assert",
      "break",
      "class",
      "continue",
      "def",
      "del",
      "elif",
      "else",
      "except",
      "exec",
      "finally",
      "for",
      "from",
      "global",
      "if",
      "import",
      "in",
      "is",
      "lambda",
      "nonlocal",
      "not",
      "or",
      "pass",
      "print",
      "raise",
      "return",
      "try",
      "while",
      "with",
      "yield",
      "True",
      "False",
      "None",
    ],

    operators: [
      "+",
      "-",
      "*",
      "/",
      "//",
      "%",
      "**",
      "@",
      "<<",
      ">>",
      "&",
      "|",
      "^",
      "~",
      "<",
      ">",
      "<=",
      ">=",
      "==",
      "!=",
    ],

    brackets: [
      { open: "{", close: "}", token: "delimiter.curly" },
      { open: "[", close: "]", token: "delimiter.square" },
      { open: "(", close: ")", token: "delimiter.parenthesis" },
    ],

    // Common regular expressions
    symbols: /[=><!~&|+\-*\/\^%]+/,
    escapes: /\\(?:[abfnrtv\\"']|x[0-9A-Fa-f]{1,4}|u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8})/,

    // The main tokenizer for Python
    tokenizer: {
      root: [
        { include: "@whitespace" },
        { include: "@numbers" },
        { include: "@strings" },
        { include: "@docstrings" },

        // Keywords
        [
          /[a-zA-Z_]\w*/,
          {
            cases: {
              "@keywords": "keyword",
              "@default": "identifier",
            },
          },
        ],

        // Operators
        [/@symbols/, { cases: { "@operators": "operator", "@default": "" } }],

        // Delimiters and brackets
        [/[{}()\[\]]/, "@brackets"],
        [/[;,.]/, "delimiter"],

        // Comments
        [/#.*$/, "comment"],
      ],

      whitespace: [
        [/[ \t\r\n]+/, "white"],
      ],

      numbers: [
        [/\d+\.\d*([eE][+-]?\d+)?/, "number.float"],
        [/\d+[eE][+-]?\d+/, "number.float"],
        [/0[xX][0-9a-fA-F]+/, "number.hex"],
        [/0[oO]?[0-7]+/, "number.octal"],
        [/0[bB][01]+/, "number.binary"],
        [/\d+/, "number"],
      ],

      strings: [
        [/'/, "string", "@singleQuotedString"],
        [/"/, "string", "@doubleQuotedString"],
      ],

      singleQuotedString: [
        [/[^\\']+/, "string"],
        [/@escapes/, "string.escape"],
        [/'/, "string", "@pop"],
      ],

      doubleQuotedString: [
        [/[^\\"]+/, "string"],
        [/@escapes/, "string.escape"],
        [/"/, "string", "@pop"],
      ],

      docstrings: [
        [/"""/, "string.docstring", "@docstringDouble"],
        [/'''/, "string.docstring", "@docstringSingle"],
      ],

      docstringDouble: [
        [/[^"]+/, "string.docstring"],
        [/"""/, "string.docstring", "@pop"],
      ],

      docstringSingle: [
        [/[^']+/, "string.docstring"],
        [/'''/, "string.docstring", "@pop"],
      ],
    },
  });

  // Configure Python language configuration (indentation, etc.)
  monaco.languages.setLanguageConfiguration("python", {
    comments: {
      lineComment: "#",
    },
    brackets: [
      ["{", "}"],
      ["[", "]"],
      ["(", ")"],
    ],
    autoClosingPairs: [
      { open: "{", close: "}" },
      { open: "[", close: "]" },
      { open: "(", close: ")" },
      { open: '"', close: '"' },
      { open: "'", close: "'" },
      { open: '"""', close: '"""' },
      { open: "'''", close: "'''" },
    ],
    surroundingPairs: [
      { open: "{", close: "}" },
      { open: "[", close: "]" },
      { open: "(", close: ")" },
      { open: '"', close: '"' },
      { open: "'", close: "'" },
    ],
    indentationRules: {
      increaseIndentPattern: /^\s*(class|def|elif|else|except|finally|for|if|try|while|with)\b.*:\s*$/,
      decreaseIndentPattern: /^\s*(elif|else|except|finally)\b.*:\s*$/,
    },
    folding: {
      offSide: true,
      markers: {
        start: /^\s*#\s*region\b/,
        end: /^\s*#\s*endregion\b/,
      },
    },
  });

  // Define custom themes that match shadcn/ui
  monaco.editor.defineTheme("vs-code-dark", {
    base: "vs-dark",
    inherit: true,
    rules: [
      { token: "keyword", foreground: "#c586c0" },
      { token: "identifier", foreground: "#9cdcfe" },
      { token: "string", foreground: "#ce9178" },
      { token: "string.docstring", foreground: "#6a9955" },
      { token: "string.escape", foreground: "#d7ba7d" },
      { token: "number", foreground: "#b5cea8" },
      { token: "number.float", foreground: "#b5cea8" },
      { token: "comment", foreground: "#6a9955" },
      { token: "operator", foreground: "#d4d4d4" },
      { token: "delimiter", foreground: "#d4d4d4" },
      { token: "delimiter.curly", foreground: "#ffd700" },
      { token: "delimiter.square", foreground: "#ffd700" },
      { token: "delimiter.parenthesis", foreground: "#ffd700" },
    ],
    colors: {
      "editor.background": "#1e1e1e",
      "editor.foreground": "#d4d4d4",
      "editorLineNumber.foreground": "#858585",
      "editorLineNumber.activeForeground": "#c6c6c6",
      "editor.selectionBackground": "#264f78",
      "editor.inactiveSelectionBackground": "#3a3d41",
      "editorCursor.foreground": "#aeafad",
      "editor.lineHighlightBackground": "#2d2d2d",
    },
  });

  monaco.editor.defineTheme("vs-code-light", {
    base: "vs",
    inherit: true,
    rules: [
      { token: "keyword", foreground: "#0000ff" },
      { token: "identifier", foreground: "#001080" },
      { token: "string", foreground: "#a31515" },
      { token: "string.docstring", foreground: "#008000" },
      { token: "string.escape", foreground: "#ff0000" },
      { token: "number", foreground: "#098658" },
      { token: "number.float", foreground: "#098658" },
      { token: "comment", foreground: "#008000" },
      { token: "operator", foreground: "#000000" },
      { token: "delimiter", foreground: "#000000" },
      { token: "delimiter.curly", foreground: "#0431fa" },
      { token: "delimiter.square", foreground: "#0431fa" },
      { token: "delimiter.parenthesis", foreground: "#0431fa" },
    ],
    colors: {
      "editor.background": "#ffffff",
      "editor.foreground": "#000000",
      "editorLineNumber.foreground": "#237893",
      "editorLineNumber.activeForeground": "#0b216f",
      "editor.selectionBackground": "#add6ff",
      "editor.inactiveSelectionBackground": "#e5ebf1",
      "editorCursor.foreground": "#000000",
      "editor.lineHighlightBackground": "#f0f0f0",
    },
  });

  console.log("Monaco initialized with Python support");
};

// Default editor options
export const getDefaultEditorOptions = (
  isDark: boolean,
  readOnly: boolean = false
): monaco.editor.IStandaloneEditorConstructionOptions => ({
  language: "python",
  theme: isDark ? "vs-code-dark" : "vs-code-light",
  automaticLayout: true,
  readOnly,
  minimap: {
    enabled: true,
    scale: 1,
    showSlider: "mouseover",
    renderSide: "right",
  },
  fontSize: 14,
  fontFamily: "'JetBrains Mono', 'Fira Code', 'Consolas', monospace",
  fontLigatures: true,
  lineNumbers: "on",
  lineHeight: 22,
  scrollBeyondLastLine: false,
  wordWrap: "on",
  wrappingIndent: "indent",
  tabSize: 4,
  insertSpaces: true,
  detectIndentation: true,
  bracketPairColorization: {
    enabled: true,
  },
  guides: {
    bracketPairs: true,
    indentation: true,
  },
  folding: true,
  foldingHighlight: true,
  showFoldingControls: "mouseover",
  renderWhitespace: "selection",
  renderLineHighlight: "line",
  cursorBlinking: "blink",
  cursorSmoothCaretAnimation: "on",
  smoothScrolling: true,
  contextmenu: true,
  quickSuggestions: true,
  suggestOnTriggerCharacters: true,
  acceptSuggestionOnEnter: "on",
  snippetSuggestions: "inline",
  formatOnType: true,
  formatOnPaste: true,
  autoIndent: "full",
  matchBrackets: "always",
  autoClosingBrackets: "always",
  autoClosingQuotes: "always",
  multiCursorModifier: "altCmd",
  find: {
    addExtraSpaceOnTop: false,
    autoFindInSelection: "never",
    seedSearchStringFromSelection: "always",
  },
});

// Sample starter code for Python
export const DEFAULT_STARTER_CODE = `# Welcome to Python OOP Journey!
# Write your Python code here.

def greet(name):
    """A simple greeting function."""
    return f"Hello, {name}!"

# Example usage
if __name__ == "__main__":
    message = greet("World")
    print(message)
`;
