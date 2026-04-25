"""Tests for the hexbound color extractor module."""

import pytest
from PIL import Image
import numpy as np

from hexbound.extractor import rgb_to_hex, quantize_colors, load_image, extract_palette


def make_test_image(colors: list[tuple[int, int, int]], size: int = 100) -> Image.Image:
    """Create a simple test image with blocks of given colors."""
    block_width = size // len(colors)
    data = np.zeros((size, size, 3), dtype=np.uint8)
    for i, color in enumerate(colors):
        data[:, i * block_width:(i + 1) * block_width] = color
    return Image.fromarray(data, mode="RGB")


class TestRgbToHex:
    def test_black(self):
        assert rgb_to_hex(0, 0, 0) == "#000000"

    def test_white(self):
        assert rgb_to_hex(255, 255, 255) == "#ffffff"

    def test_red(self):
        assert rgb_to_hex(255, 0, 0) == "#ff0000"

    def test_mixed(self):
        assert rgb_to_hex(18, 52, 86) == "#123456"

    def test_returns_lowercase(self):
        result = rgb_to_hex(171, 205, 239)
        assert result == result.lower()


class TestQuantizeColors:
    def test_returns_correct_count(self):
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        image = make_test_image(colors)
        result = quantize_colors(image, num_colors=4)
        assert len(result) == 4

    def test_returns_hex_strings(self):
        image = make_test_image([(100, 150, 200)])
        result = quantize_colors(image, num_colors=2)
        for color in result:
            assert color.startswith("#")
            assert len(color) == 7

    def test_single_color_image(self):
        image = make_test_image([(42, 42, 42)])
        result = quantize_colors(image, num_colors=1)
        assert len(result) == 1


class TestLoadImage:
    def test_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_image(str(tmp_path / "nonexistent.png"))

    def test_loads_valid_image(self, tmp_path):
        img_path = tmp_path / "test.png"
        img = make_test_image([(255, 0, 0)])
        img.save(img_path)
        loaded = load_image(str(img_path))
        assert loaded.mode == "RGB"


class TestExtractPalette:
    def test_extract_from_file(self, tmp_path):
        img_path = tmp_path / "palette_test.png"
        img = make_test_image([(255, 0, 0), (0, 0, 255)])
        img.save(img_path)
        result = extract_palette(str(img_path), num_colors=4)
        assert isinstance(result, list)
        assert all(h.startswith("#") for h in result)
