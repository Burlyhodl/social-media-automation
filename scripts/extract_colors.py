#!/usr/bin/env python3
"""
Color Extraction Utility
Extracts dominant colors from images for overlay generation
"""

import requests
from io import BytesIO
from colorthief import ColorThief
from PIL import Image
import os
from typing import Dict, Tuple, List


class ColorExtractor:
    """Extract dominant colors from images"""

    def __init__(self, image_source: str):
        """
        Initialize color extractor

        Args:
            image_source: URL or local file path to image
        """
        self.image_source = image_source
        self.image_path = None
        self.is_url = image_source.startswith('http://') or image_source.startswith('https://')

    def download_image(self, output_path: str) -> bool:
        """
        Download image from URL or copy local file

        Args:
            output_path: Where to save the image

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.is_url:
                print(f"Downloading image from: {self.image_source}")
                response = requests.get(self.image_source, timeout=30)
                response.raise_for_status()

                # Save image
                with open(output_path, 'wb') as f:
                    f.write(response.content)

                print(f"Image downloaded to: {output_path}")
            else:
                # Copy local file
                import shutil
                shutil.copy(self.image_source, output_path)
                print(f"Image copied to: {output_path}")

            self.image_path = output_path
            return True

        except Exception as e:
            print(f"Error downloading/copying image: {e}")
            return False

    def get_dominant_color(self, quality: int = 10) -> Tuple[int, int, int]:
        """
        Get the dominant color from the image

        Args:
            quality: Quality setting (1-10, lower is better but slower)

        Returns:
            RGB tuple (r, g, b)
        """
        if not self.image_path:
            raise ValueError("Image not downloaded. Call download_image() first.")

        color_thief = ColorThief(self.image_path)
        dominant_color = color_thief.get_color(quality=quality)
        return dominant_color

    def get_color_palette(self, color_count: int = 5, quality: int = 10) -> List[Tuple[int, int, int]]:
        """
        Get a color palette from the image

        Args:
            color_count: Number of colors to extract
            quality: Quality setting (1-10, lower is better but slower)

        Returns:
            List of RGB tuples
        """
        if not self.image_path:
            raise ValueError("Image not downloaded. Call download_image() first.")

        color_thief = ColorThief(self.image_path)
        palette = color_thief.get_palette(color_count=color_count, quality=quality)
        return palette

    def get_average_color(self) -> Tuple[int, int, int]:
        """
        Get the average color of the image

        Returns:
            RGB tuple (r, g, b)
        """
        if not self.image_path:
            raise ValueError("Image not downloaded. Call download_image() first.")

        img = Image.open(self.image_path)
        img = img.convert('RGB')

        # Resize for faster processing
        img.thumbnail((100, 100))

        # Calculate average
        pixels = list(img.getdata())
        avg_r = sum([p[0] for p in pixels]) // len(pixels)
        avg_g = sum([p[1] for p in pixels]) // len(pixels)
        avg_b = sum([p[2] for p in pixels]) // len(pixels)

        return (avg_r, avg_g, avg_b)

    @staticmethod
    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex color string"""
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

    @staticmethod
    def adjust_brightness(rgb: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
        """
        Adjust brightness of a color

        Args:
            rgb: RGB tuple
            factor: Brightness factor (0.0 = black, 1.0 = original, >1.0 = brighter)

        Returns:
            Adjusted RGB tuple
        """
        r = max(0, min(255, int(rgb[0] * factor)))
        g = max(0, min(255, int(rgb[1] * factor)))
        b = max(0, min(255, int(rgb[2] * factor)))
        return (r, g, b)

    @staticmethod
    def create_overlay_color(base_color: Tuple[int, int, int], opacity: float = 0.7) -> str:
        """
        Create an RGBA color string suitable for CSS overlays

        Args:
            base_color: RGB tuple
            opacity: Opacity value (0.0 to 1.0)

        Returns:
            RGBA color string
        """
        return f'rgba({base_color[0]}, {base_color[1]}, {base_color[2]}, {opacity})'

    def extract_all_colors(self) -> Dict:
        """
        Extract comprehensive color information from the image

        Returns:
            Dictionary with various color representations
        """
        if not self.image_path:
            raise ValueError("Image not downloaded. Call download_image() first.")

        dominant = self.get_dominant_color()
        palette = self.get_color_palette(color_count=5)
        average = self.get_average_color()

        # Create darker and lighter versions for overlays
        darker = self.adjust_brightness(dominant, 0.7)
        lighter = self.adjust_brightness(dominant, 1.3)

        return {
            'dominant': {
                'rgb': dominant,
                'hex': self.rgb_to_hex(dominant),
                'rgba': self.create_overlay_color(dominant, 0.7)
            },
            'average': {
                'rgb': average,
                'hex': self.rgb_to_hex(average),
                'rgba': self.create_overlay_color(average, 0.7)
            },
            'palette': [
                {
                    'rgb': color,
                    'hex': self.rgb_to_hex(color),
                    'rgba': self.create_overlay_color(color, 0.7)
                }
                for color in palette
            ],
            'darker': {
                'rgb': darker,
                'hex': self.rgb_to_hex(darker),
                'rgba': self.create_overlay_color(darker, 0.8)
            },
            'lighter': {
                'rgb': lighter,
                'hex': self.rgb_to_hex(lighter),
                'rgba': self.create_overlay_color(lighter, 0.6)
            }
        }


def extract_colors(image_source: str, output_dir: str = 'assets') -> Dict:
    """
    Convenience function to extract colors from an image

    Args:
        image_source: URL or file path to image
        output_dir: Directory to save downloaded image

    Returns:
        Dictionary with color information
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate output filename
    if image_source.startswith('http'):
        filename = 'downloaded_image.jpg'
    else:
        filename = os.path.basename(image_source)

    output_path = os.path.join(output_dir, filename)

    # Extract colors
    extractor = ColorExtractor(image_source)

    if not extractor.download_image(output_path):
        return None

    colors = extractor.extract_all_colors()
    return colors


if __name__ == '__main__':
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python extract_colors.py <image_url_or_path>")
        sys.exit(1)

    image_source = sys.argv[1]
    colors = extract_colors(image_source)

    if colors:
        print("\n" + "="*50)
        print("EXTRACTED COLORS")
        print("="*50)
        print(json.dumps(colors, indent=2))
    else:
        print("Failed to extract colors")
        sys.exit(1)
