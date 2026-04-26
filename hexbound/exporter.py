"""Export color palettes to various formats.

Supports exporting palettes as plain text, JSON, CSS variables,
and a simple terminal preview.
"""

import json
from pathlib import Path
from typing import List


def export_as_text(palette: List[str], output_path: str | None = None) -> str:
    """Export palette as a plain newline-separated list of hex codes.

    Args:
        palette: List of hex color strings (e.g. ['#ff0000', '#00ff00']).
        output_path: Optional file path to write the output to.

    Returns:
        The formatted string content.
    """
    content = "\n".join(palette) + "\n"
    if output_path:
        Path(output_path).write_text(content)
    return content


def export_as_json(palette: List[str], output_path: str | None = None) -> str:
    """Export palette as a JSON array of hex strings.

    Args:
        palette: List of hex color strings.
        output_path: Optional file path to write the output to.

    Returns:
        The JSON string.
    """
    content = json.dumps({"palette": palette}, indent=2) + "\n"
    if output_path:
        Path(output_path).write_text(content)
    return content


def export_as_css(palette: List[str], output_path: str | None = None) -> str:
    """Export palette as CSS custom properties on the :root selector.

    Variables are named --color-0, --color-1, etc.

    Args:
        palette: List of hex color strings.
        output_path: Optional file path to write the output to.

    Returns:
        The CSS string.
    """
    lines = [":root {"]  
    for i, hex_color in enumerate(palette):
        lines.append(f"  --color-{i}: {hex_color};")
    lines.append("}\n")
    content = "\n".join(lines)
    if output_path:
        Path(output_path).write_text(content)
    return content


def _ansi_block(hex_color: str) -> str:
    """Return an ANSI-colored block character for terminal preview.

    Args:
        hex_color: A hex string like '#a1b2c3'.

    Returns:
        ANSI escape sequence string that prints a colored square.
    """
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    # Use truecolor ANSI background escape with two spaces as the block
    return f"\x1b[48;2;{r};{g};{b}m  \x1b[0m"


def preview_palette(palette: List[str]) -> None:
    """Print a simple color swatch preview to the terminal.

    Each color is shown as a colored block followed by its hex code.

    Args:
        palette: List of hex color strings.
    """
    print("Palette preview:")
    for hex_color in palette:
        block = _ansi_block(hex_color)
        print(f"  {block}  {hex_color}")


EXPORT_FORMATS = {
    "text": export_as_text,
    "json": export_as_json,
    "css": export_as_css,
}


def export_palette(
    palette: List[str],
    fmt: str = "text",
    output_path: str | None = None,
) -> str:
    """Dispatch palette export to the appropriate format handler.

    Args:
        palette: List of hex color strings.
        fmt: One of 'text', 'json', or 'css'.
        output_path: Optional file path to write the output to.

    Returns:
        The exported content as a string.

    Raises:
        ValueError: If an unsupported format is requested.
    """
    if fmt not in EXPORT_FORMATS:
        supported = ", ".join(EXPORT_FORMATS.keys())
        raise ValueError(f"Unsupported format '{fmt}'. Choose from: {supported}")
    return EXPORT_FORMATS[fmt](palette, output_path)
