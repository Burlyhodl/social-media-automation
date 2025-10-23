# Quick Start Guide

Get up and running with blog post image generation in 3 simple steps!

## Step 1: Setup

Run the automated setup script:

```bash
./setup.sh
```

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 2: Generate Your First Image

```bash
python src/cli.py "My First Blog Post" -s "This is amazing!"
```

Your image will be saved in the `output/` directory!

## Step 3: Try Batch Processing

Generate multiple images at once:

```bash
python src/batch_generator.py examples/blog_posts.json
```

This creates 5 example images in different styles.

## Next Steps

- Edit `config.json` to customize colors and sizes
- Create your own `blog_posts.json` file for batch processing
- Try different templates: `basic`, `gradient`, or `minimal`

## Common Commands

```bash
# Single image with basic template
python src/cli.py "Your Title" -s "Your Subtitle"

# Use gradient template
python src/cli.py "Your Title" -t gradient

# Custom output name
python src/cli.py "Your Title" -o my_image.png

# Batch process
python src/batch_generator.py your_posts.json
```

## Need Help?

Check out the full [README.md](README.md) for detailed documentation.
