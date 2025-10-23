"""
Blog Post Image Generator
Automates the creation of blog post images with burnt orange branding
"""

from PIL import Image, ImageDraw, ImageFont
import os
import json
from typing import Tuple, Optional
from pathlib import Path


class BlogImageGenerator:
    """Generate branded blog post images with burnt orange theme"""

    # Burnt Orange color palette
    BURNT_ORANGE = "#CC5500"
    DARK_ORANGE = "#A64400"
    LIGHT_ORANGE = "#FF6A13"
    CREAM = "#FFF8DC"
    DARK_GRAY = "#2C2C2C"
    WHITE = "#FFFFFF"

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the image generator

        Args:
            config_path: Path to configuration file (optional)
        """
        self.config = self._load_config(config_path)
        self.width = self.config.get("width", 1200)
        self.height = self.config.get("height", 630)
        self.output_dir = Path(self.config.get("output_dir", "output"))
        self.output_dir.mkdir(exist_ok=True)

    def _load_config(self, config_path: Optional[str]) -> dict:
        """Load configuration from file or use defaults"""
        default_config = {
            "width": 1200,
            "height": 630,
            "output_dir": "output",
            "font_title_size": 72,
            "font_subtitle_size": 36,
            "primary_color": self.BURNT_ORANGE,
            "background_color": self.CREAM,
            "text_color": self.DARK_GRAY
        }

        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)

        return default_config

    def _get_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Get font with fallback options"""
        font_options = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "C:\\Windows\\Fonts\\Arial.ttf"
        ]

        for font_path in font_options:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    continue

        # Fallback to default font
        return ImageFont.load_default()

    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list:
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            width = bbox[2] - bbox[0]

            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def create_basic_template(
        self,
        title: str,
        subtitle: str = "",
        output_filename: str = "blog_image.png"
    ) -> str:
        """
        Create a basic blog post image with burnt orange theme

        Args:
            title: Main title text
            subtitle: Optional subtitle text
            output_filename: Output filename

        Returns:
            Path to generated image
        """
        # Create image with cream background
        img = Image.new('RGB', (self.width, self.height), self.config["background_color"])
        draw = ImageDraw.Draw(img)

        # Add burnt orange header bar
        header_height = self.height // 6
        draw.rectangle(
            [(0, 0), (self.width, header_height)],
            fill=self.config["primary_color"]
        )

        # Add burnt orange footer bar
        footer_height = self.height // 8
        draw.rectangle(
            [(0, self.height - footer_height), (self.width, self.height)],
            fill=self.DARK_ORANGE
        )

        # Add decorative accent
        accent_width = self.width // 20
        draw.rectangle(
            [(0, header_height), (accent_width, self.height - footer_height)],
            fill=self.LIGHT_ORANGE
        )

        # Prepare fonts
        title_font = self._get_font(self.config["font_title_size"])
        subtitle_font = self._get_font(self.config["font_subtitle_size"])

        # Wrap and draw title
        max_text_width = self.width - (accent_width + 100)
        title_lines = self._wrap_text(title, title_font, max_text_width)

        y_offset = header_height + 100
        for line in title_lines:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = accent_width + (self.width - accent_width - text_width) // 2

            # Draw text with shadow for depth
            draw.text((x + 2, y_offset + 2), line, fill=self.DARK_ORANGE, font=title_font)
            draw.text((x, y_offset), line, fill=self.config["text_color"], font=title_font)
            y_offset += bbox[3] - bbox[1] + 20

        # Draw subtitle if provided
        if subtitle:
            y_offset += 30
            subtitle_lines = self._wrap_text(subtitle, subtitle_font, max_text_width)

            for line in subtitle_lines:
                bbox = draw.textbbox((0, 0), line, font=subtitle_font)
                text_width = bbox[2] - bbox[0]
                x = accent_width + (self.width - accent_width - text_width) // 2
                draw.text((x, y_offset), line, fill=self.DARK_GRAY, font=subtitle_font)
                y_offset += bbox[3] - bbox[1] + 15

        # Save image
        output_path = self.output_dir / output_filename
        img.save(output_path, quality=95, optimize=True)

        return str(output_path)

    def create_gradient_template(
        self,
        title: str,
        subtitle: str = "",
        output_filename: str = "blog_image_gradient.png"
    ) -> str:
        """
        Create a blog post image with gradient background

        Args:
            title: Main title text
            subtitle: Optional subtitle text
            output_filename: Output filename

        Returns:
            Path to generated image
        """
        # Create image
        img = Image.new('RGB', (self.width, self.height), self.WHITE)
        draw = ImageDraw.Draw(img)

        # Create gradient background from burnt orange to cream
        for y in range(self.height):
            ratio = y / self.height
            r = int(204 * (1 - ratio) + 255 * ratio)
            g = int(85 * (1 - ratio) + 248 * ratio)
            b = int(0 * (1 - ratio) + 220 * ratio)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))

        # Add semi-transparent overlay for better text readability
        overlay = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 180))
        img.paste(overlay, (0, 0), overlay)
        img = img.convert('RGB')
        draw = ImageDraw.Draw(img)

        # Prepare fonts
        title_font = self._get_font(self.config["font_title_size"])
        subtitle_font = self._get_font(self.config["font_subtitle_size"])

        # Draw title
        max_text_width = self.width - 100
        title_lines = self._wrap_text(title, title_font, max_text_width)

        total_text_height = sum([title_font.getbbox(line)[3] for line in title_lines])
        y_offset = (self.height - total_text_height) // 2 - 50

        for line in title_lines:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (self.width - text_width) // 2

            # Draw with outline for better visibility
            for adj in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
                draw.text((x + adj[0], y_offset + adj[1]), line, fill=self.WHITE, font=title_font)
            draw.text((x, y_offset), line, fill=self.BURNT_ORANGE, font=title_font)
            y_offset += bbox[3] - bbox[1] + 20

        # Draw subtitle if provided
        if subtitle:
            y_offset += 30
            subtitle_lines = self._wrap_text(subtitle, subtitle_font, max_text_width)

            for line in subtitle_lines:
                bbox = draw.textbbox((0, 0), line, font=subtitle_font)
                text_width = bbox[2] - bbox[0]
                x = (self.width - text_width) // 2
                draw.text((x, y_offset), line, fill=self.DARK_ORANGE, font=subtitle_font)
                y_offset += bbox[3] - bbox[1] + 15

        # Save image
        output_path = self.output_dir / output_filename
        img.save(output_path, quality=95, optimize=True)

        return str(output_path)

    def create_minimal_template(
        self,
        title: str,
        subtitle: str = "",
        output_filename: str = "blog_image_minimal.png"
    ) -> str:
        """
        Create a minimal blog post image

        Args:
            title: Main title text
            subtitle: Optional subtitle text
            output_filename: Output filename

        Returns:
            Path to generated image
        """
        # Create image with white background
        img = Image.new('RGB', (self.width, self.height), self.WHITE)
        draw = ImageDraw.Draw(img)

        # Add burnt orange accent line
        line_thickness = 8
        margin = 50
        draw.rectangle(
            [(margin, margin), (self.width - margin, margin + line_thickness)],
            fill=self.BURNT_ORANGE
        )

        # Prepare fonts
        title_font = self._get_font(self.config["font_title_size"])
        subtitle_font = self._get_font(self.config["font_subtitle_size"])

        # Draw title
        max_text_width = self.width - (margin * 2)
        title_lines = self._wrap_text(title, title_font, max_text_width)

        y_offset = margin + 80
        for line in title_lines:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = margin
            draw.text((x, y_offset), line, fill=self.DARK_GRAY, font=title_font)
            y_offset += bbox[3] - bbox[1] + 20

        # Draw subtitle if provided
        if subtitle:
            y_offset += 30
            subtitle_lines = self._wrap_text(subtitle, subtitle_font, max_text_width)

            for line in subtitle_lines:
                draw.text((margin, y_offset), line, fill=self.BURNT_ORANGE, font=subtitle_font)
                bbox = draw.textbbox((0, 0), line, font=subtitle_font)
                y_offset += bbox[3] - bbox[1] + 15

        # Add bottom accent line
        draw.rectangle(
            [(margin, self.height - margin - line_thickness), (self.width - margin, self.height - margin)],
            fill=self.LIGHT_ORANGE
        )

        # Save image
        output_path = self.output_dir / output_filename
        img.save(output_path, quality=95, optimize=True)

        return str(output_path)


def main():
    """Example usage"""
    generator = BlogImageGenerator()

    # Example 1: Basic template
    print("Creating basic template...")
    output1 = generator.create_basic_template(
        title="Automate Your Blog Post Images",
        subtitle="Save time with automated image generation",
        output_filename="example_basic.png"
    )
    print(f"Created: {output1}")

    # Example 2: Gradient template
    print("Creating gradient template...")
    output2 = generator.create_gradient_template(
        title="Beautiful Blog Post Images",
        subtitle="Professional designs in seconds",
        output_filename="example_gradient.png"
    )
    print(f"Created: {output2}")

    # Example 3: Minimal template
    print("Creating minimal template...")
    output3 = generator.create_minimal_template(
        title="Clean and Simple Design",
        subtitle="Minimal yet effective",
        output_filename="example_minimal.png"
    )
    print(f"Created: {output3}")


if __name__ == "__main__":
    main()
