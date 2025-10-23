# Social Media Automation - Blog Post Image Generator

Complete social media automation system with burnt orange templates for creating professional blog post images.

## Features

- **Automated Image Generation**: Create stunning blog post images with just a title and subtitle
- **Multiple Templates**: Choose from Basic, Gradient, or Minimal designs
- **Burnt Orange Branding**: Beautiful color palette featuring burnt orange (#CC5500) theme
- **Batch Processing**: Generate multiple images at once from JSON file
- **Customizable**: Easy-to-use configuration file for colors, fonts, and dimensions
- **CLI Tools**: Command-line interface for quick image generation
- **High Quality**: Outputs optimized PNG images (1200x630px, perfect for social media)

## Installation

### Quick Setup

Run the setup script to automatically create a virtual environment and install dependencies:

```bash
./setup.sh
```

### Manual Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Method 1: CLI Tool (Single Image)

Generate a single blog post image using the command-line interface:

```bash
# Basic usage
python src/cli.py "Your Blog Post Title"

# With subtitle
python src/cli.py "Your Blog Post Title" -s "An engaging subtitle"

# Choose a template
python src/cli.py "Your Title" -s "Subtitle" -t gradient

# Specify output filename
python src/cli.py "Your Title" -o my_custom_image.png

# Use custom config
python src/cli.py "Your Title" -c config.json
```

**Template Options:**
- `basic` - Clean design with header/footer bars and accent stripe
- `gradient` - Smooth gradient background from burnt orange to cream
- `minimal` - Simple design with accent lines

### Method 2: Batch Processing (Multiple Images)

Generate multiple images at once from a JSON file:

```bash
python src/batch_generator.py examples/blog_posts.json
```

**JSON Format:**
```json
[
  {
    "title": "Your Blog Post Title",
    "subtitle": "Optional subtitle text",
    "template": "basic",
    "output": "output_filename.png"
  }
]
```

### Method 3: Python API

Use the image generator in your own Python scripts:

```python
from src.image_generator import BlogImageGenerator

# Initialize generator
generator = BlogImageGenerator()

# Create basic template
generator.create_basic_template(
    title="My Blog Post Title",
    subtitle="An engaging subtitle",
    output_filename="my_image.png"
)

# Create gradient template
generator.create_gradient_template(
    title="Another Great Post",
    subtitle="With beautiful gradients",
    output_filename="gradient_image.png"
)

# Create minimal template
generator.create_minimal_template(
    title="Clean Design",
    subtitle="Less is more",
    output_filename="minimal_image.png"
)
```

## Configuration

Customize the image generation by editing `config.json`:

```json
{
  "width": 1200,
  "height": 630,
  "output_dir": "output",
  "font_title_size": 72,
  "font_subtitle_size": 36,
  "primary_color": "#CC5500",
  "background_color": "#FFF8DC",
  "text_color": "#2C2C2C"
}
```

**Configuration Options:**
- `width` / `height`: Image dimensions (default: 1200x630px for social media)
- `output_dir`: Directory for generated images
- `font_title_size` / `font_subtitle_size`: Font sizes for text
- `primary_color`: Main burnt orange color
- `background_color`: Background color (cream by default)
- `text_color`: Text color for titles

## Color Palette

The burnt orange theme includes:

- **Burnt Orange**: `#CC5500` - Primary brand color
- **Dark Orange**: `#A64400` - Darker accent
- **Light Orange**: `#FF6A13` - Lighter accent
- **Cream**: `#FFF8DC` - Background color
- **Dark Gray**: `#2C2C2C` - Text color
- **White**: `#FFFFFF` - Highlights

## Project Structure

```
social-media-automation/
├── src/
│   ├── image_generator.py  # Core image generation class
│   ├── batch_generator.py  # Batch processing script
│   └── cli.py              # Command-line interface
├── templates/              # Template files (for future expansion)
├── output/                 # Generated images (created automatically)
├── examples/
│   └── blog_posts.json    # Example batch processing file
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
├── setup.sh              # Setup script
└── README.md             # This file
```

## Examples

The `examples/blog_posts.json` file contains 5 sample blog posts. Generate them all with:

```bash
python src/batch_generator.py examples/blog_posts.json
```

This will create:
- getting_started.png
- 10_tips.png
- visual_content.png
- automation_workflow.png
- brand_identity.png

## Requirements

- Python 3.8 or higher
- Pillow (PIL) 10.0.0 or higher

## Tips

1. **Social Media Sizes**: The default 1200x630px is perfect for:
   - Facebook posts
   - Twitter cards
   - LinkedIn posts
   - Blog headers

2. **Text Length**: Keep titles under 50 characters for best results. Longer titles will be wrapped automatically.

3. **Customization**: Edit `config.json` to match your brand colors and preferences.

4. **Batch Processing**: Create a JSON file with all your blog posts and generate all images at once.

## Troubleshooting

**Issue**: Font not found / text appears small
**Solution**: The generator automatically tries multiple system fonts. If issues persist, install DejaVu fonts:
```bash
# Ubuntu/Debian
sudo apt-get install fonts-dejavu

# macOS (using Homebrew)
brew install font-dejavu
```

**Issue**: Permission denied on setup.sh
**Solution**: Make the script executable:
```bash
chmod +x setup.sh
```

## Future Enhancements

- [ ] Add more template designs
- [ ] Support for custom background images
- [ ] Logo/watermark placement
- [ ] Video thumbnail generation
- [ ] Integration with popular CMS platforms
- [ ] GUI interface

## License

This project is open source and available for use in your projects.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
