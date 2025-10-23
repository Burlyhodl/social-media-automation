#!/usr/bin/env python3
"""
Social Media Automation - Main Orchestration Script
Automates the creation of blog post images from WordPress URLs
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from fetch_post_data import fetch_wordpress_post
from extract_colors import extract_colors


class BlogImageGenerator:
    """Main class for generating blog post images"""

    def __init__(self, output_dir='output', assets_dir='assets', template_dir='templates'):
        self.output_dir = output_dir
        self.assets_dir = assets_dir
        self.template_dir = template_dir

        # Create directories if they don't exist
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.assets_dir, exist_ok=True)
        os.makedirs(self.template_dir, exist_ok=True)

    def generate_from_url(self, blog_url, brand_text='YOURBRAND.COM',
                         width=1200, height=630, output_format='png',
                         custom_overlay=None):
        """
        Generate blog post image from WordPress URL

        Args:
            blog_url: URL to WordPress blog post
            brand_text: Text to display in brand strip
            width: Image width in pixels
            height: Image height in pixels
            output_format: 'png' or 'jpeg'
            custom_overlay: Custom overlay color (RGBA string) or None for auto

        Returns:
            Path to generated image or None if failed
        """
        print("="*60)
        print("BLOG POST IMAGE GENERATOR")
        print("="*60)
        print(f"\n🔗 Blog URL: {blog_url}\n")

        # Step 1: Fetch blog post data
        print("📡 Step 1: Fetching blog post data...")
        post_data = fetch_wordpress_post(blog_url)

        if not post_data:
            print("❌ Failed to fetch blog post data")
            return None

        title = post_data.get('title', 'Untitled')
        featured_image_url = post_data.get('featured_image_url')

        print(f"   ✓ Title: {title}")
        print(f"   ✓ Featured Image: {featured_image_url or 'None'}")

        if not featured_image_url:
            print("\n⚠️  Warning: No featured image found. Using default.")
            featured_image_url = "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=1200"

        # Step 2: Extract colors from featured image
        print("\n🎨 Step 2: Extracting colors from image...")
        colors = extract_colors(featured_image_url, self.assets_dir)

        if not colors:
            print("❌ Failed to extract colors")
            return None

        # Choose overlay color
        if custom_overlay:
            overlay_color = custom_overlay
            accent_color = custom_overlay
        else:
            # Use darker dominant color for overlay
            overlay_color = colors['darker']['rgba']
            # Use dominant color for accent
            accent_color = colors['dominant']['rgba']

        print(f"   ✓ Overlay Color: {overlay_color}")
        print(f"   ✓ Accent Color: {accent_color}")
        print(f"   ✓ Palette: {', '.join([c['hex'] for c in colors['palette'][:3]])}")

        # Step 3: Prepare configuration for image generation
        print("\n⚙️  Step 3: Preparing image generation config...")

        # Generate output filename
        slug = post_data.get('slug', 'blog-post')
        output_filename = f"{slug}.{output_format}"
        output_path = os.path.join(self.output_dir, output_filename)

        template_path = os.path.join(self.template_dir, 'blog-post-template.html')

        # Find the downloaded image path
        background_image_path = None
        for file in os.listdir(self.assets_dir):
            if file.startswith('downloaded_image'):
                background_image_path = os.path.join(self.assets_dir, file)
                break

        if not background_image_path:
            background_image_path = featured_image_url

        config = {
            'templatePath': template_path,
            'outputPath': output_path,
            'title': title,
            'backgroundImage': background_image_path,
            'overlayColor': overlay_color,
            'accentColor': accent_color,
            'brandText': brand_text,
            'width': width,
            'height': height,
            'format': output_format
        }

        # Save config to temporary file
        config_path = os.path.join(self.output_dir, 'temp_config.json')
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"   ✓ Config saved to: {config_path}")

        # Step 4: Generate image using Puppeteer
        print("\n🖼️  Step 4: Generating image with Puppeteer...")

        try:
            result = subprocess.run(
                ['node', 'scripts/generate_image.js', config_path],
                capture_output=True,
                text=True,
                check=True
            )

            print(result.stdout)

            if result.returncode == 0:
                print("\n" + "="*60)
                print("✅ SUCCESS! Image generated successfully")
                print("="*60)
                print(f"\n📁 Output: {output_path}")
                print(f"📐 Size: {width}x{height}")
                print(f"📊 Format: {output_format.upper()}")
                print("\nYou can now use this image for your blog post!")
                print("="*60)

                # Clean up temp config
                os.remove(config_path)

                return output_path
            else:
                print("❌ Image generation failed")
                return None

        except subprocess.CalledProcessError as e:
            print(f"❌ Error running Puppeteer script: {e}")
            print(f"STDOUT: {e.stdout}")
            print(f"STDERR: {e.stderr}")
            return None
        except FileNotFoundError:
            print("❌ Node.js not found. Please install Node.js and Puppeteer.")
            print("Run: npm install")
            return None


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate blog post images from WordPress URLs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --url https://yourblog.com/my-post/
  python main.py --url https://yourblog.com/my-post/ --brand "MY BLOG"
  python main.py --url https://yourblog.com/my-post/ --size 1200x630 --format jpeg
        """
    )

    parser.add_argument(
        '--url',
        required=True,
        help='WordPress blog post URL'
    )

    parser.add_argument(
        '--brand',
        default='YOURBRAND.COM',
        help='Brand text to display (default: YOURBRAND.COM)'
    )

    parser.add_argument(
        '--size',
        default='1200x630',
        help='Image size in format WIDTHxHEIGHT (default: 1200x630)'
    )

    parser.add_argument(
        '--format',
        choices=['png', 'jpeg'],
        default='png',
        help='Output format: png or jpeg (default: png)'
    )

    parser.add_argument(
        '--overlay',
        help='Custom overlay color in RGBA format (e.g., "rgba(204, 85, 0, 0.75)")'
    )

    parser.add_argument(
        '--output-dir',
        default='output',
        help='Output directory (default: output)'
    )

    args = parser.parse_args()

    # Parse size
    try:
        width, height = map(int, args.size.lower().split('x'))
    except ValueError:
        print("❌ Invalid size format. Use WIDTHxHEIGHT (e.g., 1200x630)")
        sys.exit(1)

    # Generate image
    generator = BlogImageGenerator(output_dir=args.output_dir)
    result = generator.generate_from_url(
        blog_url=args.url,
        brand_text=args.brand,
        width=width,
        height=height,
        output_format=args.format,
        custom_overlay=args.overlay
    )

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
