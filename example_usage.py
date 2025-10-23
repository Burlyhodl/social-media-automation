#!/usr/bin/env python3
"""
Example usage of the Blog Image Generator
Shows how to use the library programmatically
"""

from main import BlogImageGenerator

# Example 1: Basic usage
def example_basic():
    """Generate a single image from a blog post URL"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Usage")
    print("="*60 + "\n")

    generator = BlogImageGenerator()
    result = generator.generate_from_url(
        blog_url="https://wordpress.org/news/2024/01/example-post/",
        brand_text="MY AWESOME BLOG"
    )

    if result:
        print(f"\nSuccess! Image saved to: {result}")
    else:
        print("\nFailed to generate image")


# Example 2: Batch processing multiple posts
def example_batch():
    """Process multiple blog posts at once"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Batch Processing")
    print("="*60 + "\n")

    blog_urls = [
        "https://yourblog.com/post-1/",
        "https://yourblog.com/post-2/",
        "https://yourblog.com/post-3/"
    ]

    generator = BlogImageGenerator()

    for url in blog_urls:
        print(f"\nProcessing: {url}")
        result = generator.generate_from_url(
            blog_url=url,
            brand_text="TECH BLOG"
        )
        print(f"Result: {result}")


# Example 3: Custom settings
def example_custom():
    """Generate image with custom settings"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Custom Settings")
    print("="*60 + "\n")

    generator = BlogImageGenerator(output_dir="custom_output")

    result = generator.generate_from_url(
        blog_url="https://wordpress.org/news/2024/01/example-post/",
        brand_text="CUSTOM BRAND",
        width=1920,
        height=1080,
        output_format="jpeg",
        custom_overlay="rgba(150, 50, 200, 0.7)"  # Purple overlay
    )

    if result:
        print(f"\nSuccess! Custom image saved to: {result}")


# Example 4: Different image sizes for different platforms
def example_multi_platform():
    """Generate images for different social media platforms"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Multi-Platform Generation")
    print("="*60 + "\n")

    blog_url = "https://wordpress.org/news/2024/01/example-post/"
    brand = "MY BRAND"

    platforms = {
        "Facebook": (1200, 630),
        "Twitter": (1200, 675),
        "Instagram": (1080, 1080),
        "Pinterest": (1000, 1500)
    }

    for platform, (width, height) in platforms.items():
        print(f"\nGenerating for {platform} ({width}x{height})...")

        generator = BlogImageGenerator(output_dir=f"output/{platform.lower()}")
        result = generator.generate_from_url(
            blog_url=blog_url,
            brand_text=brand,
            width=width,
            height=height
        )

        if result:
            print(f"✓ {platform} image created")


if __name__ == '__main__':
    import sys

    examples = {
        '1': ('Basic Usage', example_basic),
        '2': ('Batch Processing', example_batch),
        '3': ('Custom Settings', example_custom),
        '4': ('Multi-Platform', example_multi_platform)
    }

    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        print("\nAvailable Examples:")
        print("-" * 40)
        for key, (name, _) in examples.items():
            print(f"  {key}. {name}")
        print("\nUsage: python example_usage.py <example_number>")
        print("Example: python example_usage.py 1\n")
        sys.exit(0)

    if choice in examples:
        name, func = examples[choice]
        func()
    else:
        print(f"Invalid example number: {choice}")
        print("Choose 1, 2, 3, or 4")
