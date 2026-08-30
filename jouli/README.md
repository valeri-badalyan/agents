# Jouli

A Python translator agent using Google Translate.

## Installation

```bash
# From source
pip install -e .

# With dev dependencies
pip install -e ".[dev]"
```

## Configuration

Copy `.env.example` to `.env` and optionally add your Google Translate API key:

```bash
cp .env.example .env
```

The free tier works without an API key.

## Usage

```bash
# Translate text (auto-detect source language)
jouli translate "Hello world" --to es

# Specify source language
jouli translate "Hola" --from es --to en

# Detect language
jouli detect "こんにちは"

# List supported languages
jouli languages

# List available providers
jouli providers
```

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--to` / `--target` | `-t` | Target language code (default: en) |
| `--from` / `--source` | `-f` | Source language code (default: auto) |
| `--provider` | `-p` | Translation provider (default: google) |

## Supported Languages

Run `jouli languages` to see all supported language codes.

## Development

```bash
# Run tests
pytest

# Lint
ruff check src tests

# Format
ruff format src tests
```

## License

MIT