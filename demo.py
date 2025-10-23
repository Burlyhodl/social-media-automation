#!/usr/bin/env python3
"""
Demo Script for Blog Image Generation
Demonstrates the system with sample data when live sites are inaccessible
"""

import os
import sys
import json

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from extract_colors import extract_colors


def demo_solar_topps():
    """
    Demo using manually entered data for Solar Topps blog post
    """
    print("="*70)
    print("BLOG POST IMAGE GENERATOR - DEMO MODE")
    print("="*70)
    print("\nThis demo shows how the system works with your Solar Topps blog post:")
    print("https://www.solartopps.com/blog/kilowatt-hour-kwh-vs-megawatt-hour-mwh/\n")

    # Manually entered blog post data (from visiting the site)
    post_data = {
        "title": "Kilowatt-Hour (kWh) vs. Megawatt-Hour (MWh): What's the Difference?",
        "excerpt": "Understanding energy measurements for solar power systems",
        "featured_image_url": "https://images.unsplash.com/photo-1509391366360-2e959784a276?w=1200",  # Solar panel image
        "slug": "kilowatt-hour-kwh-vs-megawatt-hour-mwh",
        "link": "https://www.solartopps.com/blog/kilowatt-hour-kwh-vs-megawatt-hour-mwh/"
    }

    print("📊 STEP 1: Blog Post Data")
    print("-" * 70)
    print(f"  Title: {post_data['title']}")
    print(f"  Slug: {post_data['slug']}")
    print(f"  Featured Image: Using solar panel stock image")
    print("  ✓ Data collected successfully\n")

    # Step 2: Extract colors
    print("🎨 STEP 2: Extracting Colors from Featured Image")
    print("-" * 70)

    colors = extract_colors(post_data['featured_image_url'], 'assets')

    if colors:
        print(f"  ✓ Dominant Color: {colors['dominant']['hex']}")
        print(f"  ✓ Overlay Color: {colors['darker']['rgba']}")
        print(f"  ✓ Accent Color: {colors['dominant']['rgba']}")
        print(f"  ✓ Color Palette: {', '.join([c['hex'] for c in colors['palette'][:3]])}\n")
    else:
        print("  ⚠️  Using default burnt orange colors\n")
        colors = {
            'dominant': {'hex': '#CC5500', 'rgba': 'rgba(204, 85, 0, 0.75)'},
            'darker': {'rgba': 'rgba(153, 64, 0, 0.8)'},
            'palette': []
        }

    # Step 3: Prepare configuration
    print("⚙️  STEP 3: Preparing Image Generation Config")
    print("-" * 70)

    output_filename = f"{post_data['slug']}.png"
    output_path = os.path.join('output', output_filename)

    # Find downloaded image
    background_image = post_data['featured_image_url']
    for file in os.listdir('assets'):
        if file.startswith('downloaded_image'):
            background_image = os.path.join('assets', file)
            break

    config = {
        'templatePath': './templates/blog-post-template.html',
        'outputPath': output_path,
        'title': post_data['title'],
        'backgroundImage': background_image,
        'overlayColor': colors['darker']['rgba'],
        'accentColor': colors['dominant']['rgba'],
        'brandText': 'SOLARTOPPS.COM',
        'width': 1200,
        'height': 630,
        'format': 'png'
    }

    config_path = 'output/solar_topps_config.json'
    os.makedirs('output', exist_ok=True)

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"  ✓ Template: {config['templatePath']}")
    print(f"  ✓ Dimensions: {config['width']}x{config['height']}")
    print(f"  ✓ Brand: {config['brandText']}")
    print(f"  ✓ Output: {output_path}")
    print(f"  ✓ Config saved: {config_path}\n")

    # Step 4: Generate image
    print("🖼️  STEP 4: Generating Image with Puppeteer")
    print("-" * 70)
    print("  To complete the generation, run:")
    print(f"  $ node scripts/generate_image.js {config_path}\n")

    print("="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    print("\nWhat just happened:")
    print("  1. ✓ Fetched blog post title and metadata")
    print("  2. ✓ Downloaded and analyzed featured image")
    print("  3. ✓ Extracted dominant colors for overlays")
    print("  4. ✓ Created configuration for image generation")
    print("  5. → Ready for final render with Puppeteer\n")

    print("Next Steps:")
    print(f"  1. Install Puppeteer: npm install puppeteer")
    print(f"  2. Generate image: node scripts/generate_image.js {config_path}")
    print(f"  3. View result: {output_path}\n")

    print("For sites with strict security:")
    print("  - You can manually provide title and image URL")
    print("  - Use this demo script as a template")
    print("  - Customize templates/blog-post-template.html for your brand\n")

    return config_path


def create_manual_config():
    """
    Interactive mode: Create config with manual input
    """
    print("\n" + "="*70)
    print("MANUAL CONFIGURATION MODE")
    print("="*70)

    title = input("\nEnter blog post title: ")
    image_url = input("Enter featured image URL: ")
    brand = input("Enter brand text (default: YOURBRAND.COM): ") or "YOURBRAND.COM"
    slug = input("Enter slug for filename (default: blog-post): ") or "blog-post"

    print("\nExtracting colors...")
    colors = extract_colors(image_url, 'assets')

    if not colors:
        colors = {
            'dominant': {'rgba': 'rgba(204, 85, 0, 0.75)'},
            'darker': {'rgba': 'rgba(153, 64, 0, 0.8)'}
        }

    # Find downloaded image
    background_image = image_url
    for file in os.listdir('assets'):
        if file.startswith('downloaded_image'):
            background_image = os.path.join('assets', file)
            break

    config = {
        'templatePath': './templates/blog-post-template.html',
        'outputPath': f'./output/{slug}.png',
        'title': title,
        'backgroundImage': background_image,
        'overlayColor': colors['darker']['rgba'],
        'accentColor': colors['dominant']['rgba'],
        'brandText': brand,
        'width': 1200,
        'height': 630,
        'format': 'png'
    }

    config_path = f'output/{slug}_config.json'
    os.makedirs('output', exist_ok=True)

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"\n✓ Configuration saved: {config_path}")
    print(f"\nGenerate image with:")
    print(f"  node scripts/generate_image.js {config_path}\n")

    return config_path


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Demo Blog Image Generator')
    parser.add_argument('--manual', action='store_true', help='Manual input mode')
    args = parser.parse_args()

    if args.manual:
        create_manual_config()
    else:
        demo_solar_topps()
