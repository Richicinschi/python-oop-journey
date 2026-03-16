# Language Support on Render

Source: https://render.com/docs/language-support

## Native Runtimes

Render natively supports:
- **Node.js** / **Bun**
- **Python**
- **Ruby**
- **Go**
- **Rust**
- **Elixir**

You can also use virtually _any_ programming language with Docker.

## Default Language Versions

By default, Render uses a recent, actively supported version of each natively supported language.

**We recommend setting a language version for your service.**

### Setting Your Language Version

| Language | How to Set Version |
|----------|-------------------|
| **Node.js** | Set `NODE_VERSION` environment variable (e.g., `18.17.0`) |
| **Python** | Set `PYTHON_VERSION` environment variable (e.g., `3.11.0`) |
| **Ruby** | Include ruby version in `Gemfile` (e.g., `ruby "3.2.2"`) |
| **Go** | Set `GO_VERSION` environment variable (e.g., `1.21.0`) |
| **Rust** | Include `rust-toolchain` file in repo root |
| **Elixir** | Include elixir version in `mix.exs` |

## Minimum Supported Versions

| Language | Minimum Version |
|----------|-----------------|
| Node.js | 14.x |
| Python | 3.7 |
| Ruby | 2.7 |
| Go | 1.19 |
| Rust | 1.70 |
| Elixir | 1.12 |

## Python-Specific Information

### Specifying Python Version

Set the `PYTHON_VERSION` environment variable:

```
PYTHON_VERSION=3.11.0
```

### Requirements File

Render looks for one of these files:
- `requirements.txt`
- `Pipfile`
- `poetry.lock`

## Node.js-Specific Information

### Specifying Node Version

Set the `NODE_VERSION` environment variable, or include an `engines` field in `package.json`:

```json
{
  "engines": {
    "node": ">=18.0.0"
  }
}
```
