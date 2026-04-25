# hexbound

A terminal-based color palette manager that extracts and exports hex themes from images or URLs.

---

## Installation

```bash
pip install hexbound
```

Or install from source:

```bash
git clone https://github.com/yourusername/hexbound.git && cd hexbound && pip install .
```

---

## Usage

Extract a palette from a local image:

```bash
hexbound extract ./wallpaper.png
```

Extract from a URL and export as a theme file:

```bash
hexbound extract https://example.com/image.jpg --export theme.json
```

List saved palettes:

```bash
hexbound list
```

Apply a saved palette:

```bash
hexbound apply my-palette
```

---

## Features

- Extract dominant colors from images or remote URLs
- Export palettes as JSON, CSS variables, or plain hex lists
- Save and manage named themes locally
- Clean, minimal terminal interface

---

## Requirements

- Python 3.8+
- `Pillow`, `requests`, `rich`

---

## License

This project is licensed under the [MIT License](LICENSE).