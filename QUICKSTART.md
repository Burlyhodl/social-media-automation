# Quick Start Guide

Get up and running in 5 minutes!

## Installation

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install Node.js dependencies
npm install
```

## Generate Your First Image

```bash
python main.py --url https://wordpress.org/news/2024/01/example-post/
```

Replace the URL with your actual WordPress blog post URL.

## What Happens?

1. The script fetches your blog post data from WordPress
2. Downloads the featured image
3. Extracts dominant colors for the overlay
4. Generates a beautiful 1200x630 image
5. Saves it to the `output/` folder

## Customize It

### Change the Brand Text

```bash
python main.py --url YOUR_URL --brand "MY BLOG"
```

### Use JPEG Instead of PNG

```bash
python main.py --url YOUR_URL --format jpeg
```

### Different Size

```bash
python main.py --url YOUR_URL --size 1920x1080
```

## Next Steps

- Customize the template in `templates/blog-post-template.html`
- Adjust colors, fonts, and layout to match your brand
- Read the full README.md for advanced options

## Need Help?

Check the troubleshooting section in README.md or open an issue on GitHub.

## Common Issues

**"No post found with slug"**
- Make sure the WordPress URL is correct and publicly accessible

**"Node.js not found"**
- Install Node.js from https://nodejs.org/
- Run `npm install` after installation

**"No featured image found"**
- The script will use a default image
- Add a featured image to your WordPress post for best results

---

That's it! You're ready to automate your blog post images.
