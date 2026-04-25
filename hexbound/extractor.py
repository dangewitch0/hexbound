"""Color extraction module for hexbound.

Extracts dominant colors from images and returns them as hex codes.
"""

from pathlib import Path
from PIL import Image
import numpy as np
from collections import Counter


DEFAULT_NUM_COLORS = 8
DEFAULT_RESIZE = (150, 150)


def load_image(source: str) -> Image.Image:
    """Load an image from a file path."""
    path = Path(source)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {source}")
    return Image.open(path).convert("RGB")


def quantize_colors(image: Image.Image, num_colors: int = DEFAULT_NUM_COLORS) -> list[str]:
    """Extract dominant colors from an image using quantization.

    Args:
        image: PIL Image object.
        num_colors: Number of dominant colors to extract.

    Returns:
        List of hex color strings (e.g. ['#1a2b3c', ...]).
    """
    resized = image.resize(DEFAULT_RESIZE, Image.LANCZOS)
    pixels = np.array(resized).reshape(-1, 3)

    quantized = resized.quantize(colors=num_colors, method=Image.Quantize.MEDIANCUT)
    quantized_rgb = quantized.convert("RGB")
    quantized_pixels = np.array(quantized_rgb).reshape(-1, 3)

    counter = Counter(map(tuple, quantized_pixels.tolist()))
    dominant = [color for color, _ in counter.most_common(num_colors)]

    return [rgb_to_hex(r, g, b) for r, g, b in dominant]


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB values to a hex color string."""
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def extract_palette(source: str, num_colors: int = DEFAULT_NUM_COLORS) -> list[str]:
    """High-level function to extract a color palette from an image path.

    Args:
        source: File path to the image.
        num_colors: Number of colors to extract.

    Returns:
        List of hex color strings.
    """
    image = load_image(source)
    return quantize_colors(image, num_colors)
