#!/usr/bin/env python3
"""
CLI tool for blog post image generation
"""

import argparse
from image_generator import BlogImageGenerator


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Generate blog post images with burnt orange branding",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a basic template image
  python cli.py "My Blog Post Title" -s "A great subtitle" -o my_image.png

  # Use gradient template
  python cli.py "My Blog Post Title" -t gradient

  # Use custom config
  python cli.py "My Blog Post Title" -c config.json

  # For batch processing, use batch_generator.py
  python batch_generator.py examples/blog_posts.json
        """
    )

    parser.add_argument(
        "title",
        help="Blog post title"
    )
    parser.add_argument(
        "-s", "--subtitle",
        help="Blog post subtitle (optional)",
        default=""
    )
    parser.add_argument(
        "-t", "--template",
        choices=["basic", "gradient", "minimal"],
        default="basic",
        help="Template style (default: basic)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output filename (default: blog_image.png)",
        default="blog_image.png"
    )
    parser.add_argument(
        "-c", "--config",
        help="Path to configuration file",
        default=None
    )

    args = parser.parse_args()

    # Initialize generator
    generator = BlogImageGenerator(args.config)

    # Generate image based on template
    print(f"Generating {args.template} template image...")

    try:
        if args.template == "gradient":
            output_path = generator.create_gradient_template(
                args.title,
                args.subtitle,
                args.output
            )
        elif args.template == "minimal":
            output_path = generator.create_minimal_template(
                args.title,
                args.subtitle,
                args.output
            )
        else:
            output_path = generator.create_basic_template(
                args.title,
                args.subtitle,
                args.output
            )

        print(f"✓ Image created successfully: {output_path}")

    except Exception as e:
        print(f"✗ Error creating image: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
