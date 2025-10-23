# Social Media Automation - Blog Post Image Generator

Automated system for creating stunning blog post images from WordPress URLs. No more manual Illustrator work - just provide a blog post URL and get a professional, branded image instantly!

## Features

- Automatically fetches blog post data from WordPress
- Downloads featured images and extracts dominant colors
- Generates professional images with dynamic color overlays
- Customizable templates with HTML/CSS
- No Adobe Illustrator required
- Fast generation (2-5 seconds per image)
- Perfect for social media sharing (1200x630 optimal size)

## How It Works

1. **Input**: Blog post URL
2. **Fetch**: Extracts title and featured image via WordPress REST API
3. **Analyze**: Extracts dominant colors from the featured image
4. **Generate**: Creates branded image with dynamic overlays using Puppeteer
5. **Output**: High-quality PNG/JPEG ready for social media

## Project Structure

```
social-media-automation/
├── main.py                          # Main orchestration script
├── scripts/
│   ├── fetch_post_data.py          # WordPress data fetcher
│   ├── extract_colors.py           # Color extraction utility
│   └── generate_image.js           # Puppeteer image generator
├── templates/
│   └── blog-post-template.html     # HTML/CSS template
├── output/                          # Generated images
├── assets/                          # Downloaded images
├── requirements.txt                 # Python dependencies
└── package.json                     # Node.js dependencies
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm (comes with Node.js)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd social-media-automation
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies**
   ```bash
   npm install
   ```

That's it! You're ready to generate images.

## Quick Start

Generate an image from a blog post URL:

```bash
python main.py --url https://yourblog.com/my-awesome-post/
```

The generated image will be saved in the `output/` directory.

## Usage Examples

### Basic Usage

```bash
python main.py --url https://yourblog.com/my-post/
```

### Custom Brand Text

```bash
python main.py --url https://yourblog.com/my-post/ --brand "MY AWESOME BLOG"
```

### Different Image Size

```bash
python main.py --url https://yourblog.com/my-post/ --size 1920x1080
```

### JPEG Format (smaller file size)

```bash
python main.py --url https://yourblog.com/my-post/ --format jpeg
```

### Custom Overlay Color

```bash
python main.py --url https://yourblog.com/my-post/ --overlay "rgba(204, 85, 0, 0.75)"
```

### All Options Combined

```bash
python main.py \
  --url https://yourblog.com/my-post/ \
  --brand "TECH BLOG" \
  --size 1200x630 \
  --format png \
  --overlay "rgba(150, 50, 200, 0.7)"
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--url` | WordPress blog post URL (required) | - |
| `--brand` | Brand text to display | YOURBRAND.COM |
| `--size` | Image size (WIDTHxHEIGHT) | 1200x630 |
| `--format` | Output format (png or jpeg) | png |
| `--overlay` | Custom overlay color (RGBA) | Auto-detected |
| `--output-dir` | Output directory | output |

## Customizing the Template

The HTML/CSS template is located at `templates/blog-post-template.html`. You can customize:

- **Colors**: Modify CSS variables for burnt orange or any color scheme
- **Fonts**: Change Google Fonts imports or use custom fonts
- **Layout**: Adjust positioning, sizes, and decorative elements
- **Brand Strip**: Modify or remove the bottom brand strip
- **Overlays**: Adjust opacity, gradients, and blend modes

### Template Variables

The template uses CSS variables that are dynamically replaced:

```css
:root {
    --bg-image: url('...');           /* Background image */
    --overlay-color: rgba(...);        /* Main overlay color */
    --accent-color: rgba(...);         /* Accent gradient color */
    --width: 1200px;                   /* Image width */
    --height: 630px;                   /* Image height */
}
```

## Testing Individual Components

### Test WordPress Data Fetcher

```bash
python scripts/fetch_post_data.py https://yourblog.com/my-post/
```

### Test Color Extractor

```bash
python scripts/extract_colors.py https://example.com/image.jpg
```

### Test Image Generator (with JSON config)

```bash
node scripts/generate_image.js config.json
```

## Recommended Image Sizes

| Platform | Optimal Size | Aspect Ratio |
|----------|--------------|--------------|
| Facebook | 1200x630 | 1.91:1 |
| Twitter | 1200x675 | 16:9 |
| LinkedIn | 1200x627 | 1.91:1 |
| Instagram | 1080x1080 | 1:1 |
| Pinterest | 1000x1500 | 2:3 |

The default (1200x630) works great for most platforms!

## Troubleshooting

### Error: "No post found with slug"

- Ensure the blog post URL is correct and publicly accessible
- Check that the WordPress site has REST API enabled (standard for WordPress 4.7+)

### Error: "REST API 403 Forbidden" or "Scraping 403 Forbidden"

Some sites (including solartopps.com) have strict bot protection. Solutions:

**Option 1: Use Demo Mode**
```bash
python demo.py --manual
```
Then manually enter your blog post details.

**Option 2: Create Config Directly**
```bash
# Edit solar_topps_demo.json with your details
# Then run:
node scripts/generate_image.js solar_topps_demo.json
```

**Option 3: Use Browser Extension**
Install a browser extension to copy blog post metadata, then use manual mode.

### Error: "Node.js not found"

- Install Node.js from https://nodejs.org/
- Run `npm install` after installing Node.js

### Error: "Puppeteer Chrome download failed"

```bash
# Update to latest Puppeteer
npm install puppeteer@latest

# Or skip download and use system Chrome
PUPPETEER_SKIP_DOWNLOAD=true npm install
```

### Error: "No featured image found"

- The system will use a default placeholder image
- Ensure your blog post has a featured image set in WordPress
- Use manual mode to provide image URL directly

### Images look different than expected

- Adjust the HTML/CSS template to match your desired design
- Modify overlay colors with the `--overlay` option
- Check font loading (requires internet for Google Fonts)

## Advanced Usage

### Batch Processing Multiple Posts

Create a script to process multiple posts:

```python
import subprocess

urls = [
    "https://yourblog.com/post-1/",
    "https://yourblog.com/post-2/",
    "https://yourblog.com/post-3/"
]

for url in urls:
    subprocess.run(["python", "main.py", "--url", url])
```

### Integration with WordPress Webhooks

Set up a webhook in WordPress that calls this script when a new post is published.

### Custom Color Schemes

Modify the color extraction algorithm in `scripts/extract_colors.py` to prefer certain color ranges.

## Performance

- Average generation time: 2-5 seconds per image
- Image file size: 100-500 KB (PNG), 50-200 KB (JPEG)
- Memory usage: ~200 MB during generation
- Can process hundreds of images without manual intervention

## License

MIT License - Feel free to use and modify for your projects!

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Credits

Built with:
- Python (requests, Pillow, colorthief)
- Node.js & Puppeteer
- HTML/CSS templates
- Google Fonts

---

**Happy image generating!**
