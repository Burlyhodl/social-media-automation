"""
Batch Blog Post Image Generator
Process multiple blog posts from JSON file
"""

import json
import argparse
from pathlib import Path
from image_generator import BlogImageGenerator


def process_batch(input_file: str, config_file: str = None):
    """
    Process multiple blog post images from JSON file

    Args:
        input_file: Path to JSON file with blog post data
        config_file: Optional path to config file
    """
    # Load blog posts data
    with open(input_file, 'r') as f:
        posts = json.load(f)

    # Initialize generator
    generator = BlogImageGenerator(config_file)

    print(f"Processing {len(posts)} blog post images...\n")

    # Process each post
    successful = 0
    failed = 0

    for i, post in enumerate(posts, 1):
        try:
            title = post.get("title", "")
            subtitle = post.get("subtitle", "")
            template = post.get("template", "basic")
            output = post.get("output", f"blog_post_{i}.png")

            print(f"[{i}/{len(posts)}] Processing: {title[:50]}...")

            # Generate image based on template type
            if template == "gradient":
                output_path = generator.create_gradient_template(title, subtitle, output)
            elif template == "minimal":
                output_path = generator.create_minimal_template(title, subtitle, output)
            else:
                output_path = generator.create_basic_template(title, subtitle, output)

            print(f"  ✓ Created: {output_path}")
            successful += 1

        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            failed += 1

    # Print summary
    print(f"\n{'=' * 50}")
    print(f"Batch processing complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"{'=' * 50}")


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Batch generate blog post images from JSON file"
    )
    parser.add_argument(
        "input",
        help="Path to JSON file with blog post data"
    )
    parser.add_argument(
        "-c", "--config",
        help="Path to configuration file",
        default=None
    )

    args = parser.parse_args()

    # Check if input file exists
    if not Path(args.input).exists():
        print(f"Error: Input file '{args.input}' not found")
        return

    # Process batch
    process_batch(args.input, args.config)


if __name__ == "__main__":
    main()
