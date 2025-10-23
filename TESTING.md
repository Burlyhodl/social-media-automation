# Testing Guide

This guide shows how to test the blog image automation system.

## Environment Requirements

- Python 3.8+
- Node.js 16+
- Internet connection for downloading images

## Installation

```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies
npm install
```

## Test Scenarios

### Scenario 1: Test with WordPress.org Blog (Public API)

```bash
python main.py --url https://wordpress.org/news/2024/01/wordpress-6-4-shirley/
```

**Expected Result:**
- Fetches post data via REST API
- Downloads featured image
- Extracts colors
- Generates 1200x630 image in `output/` folder

### Scenario 2: Test with Restricted API (Your Solar Topps Blog)

Your site has API restrictions, so we've created a demo mode:

```bash
python demo.py
```

**Expected Result:**
- Demonstrates complete workflow with sample data
- Shows color extraction process
- Creates configuration file for image generation
- Provides next steps for completing the process

### Scenario 3: Manual Mode

For any blog post where automated fetching doesn't work:

```bash
python demo.py --manual
```

Then enter:
- Title: Kilowatt-Hour (kWh) vs. Megawatt-Hour (MWh): What's the Difference?
- Image URL: (any public image URL)
- Brand: SOLARTOPPS.COM
- Slug: kwh-vs-mwh

### Scenario 4: Direct Image Generation

Using the pre-configured Solar Topps demo:

```bash
node scripts/generate_image.js solar_topps_demo.json
```

**Expected Result:**
- Generates image in 2-5 seconds
- Saves to `output/solar-topps-demo.png`
- Shows file size and confirmation message

## Testing Individual Components

### 1. WordPress Data Fetcher

```bash
# Test with public site
python scripts/fetch_post_data.py https://wordpress.org/news/2024/01/wordpress-6-4-shirley/

# Your site (will use scraping fallback)
python scripts/fetch_post_data.py https://www.solartopps.com/blog/kilowatt-hour-kwh-vs-megawatt-hour-mwh/
```

### 2. Color Extractor

```bash
# Test with any public image URL
python scripts/extract_colors.py https://picsum.photos/1200/630
```

### 3. Template Renderer

```bash
# Generate from config file
node scripts/generate_image.js demo_config.json

# Or from Solar Topps config
node scripts/generate_image.js solar_topps_demo.json
```

## Expected Outputs

### Successful Run

```
============================================================
BLOG POST IMAGE GENERATOR
============================================================

🔗 Blog URL: https://...

📡 Step 1: Fetching blog post data...
   ✓ Title: Your Blog Post Title
   ✓ Featured Image: https://...

🎨 Step 2: Extracting colors from image...
   ✓ Overlay Color: rgba(204, 85, 0, 0.75)
   ✓ Accent Color: rgba(255, 107, 0, 0.9)
   ✓ Palette: #cc5500, #ff6b00, #994000

⚙️  Step 3: Preparing image generation config...
   ✓ Config saved to: output/temp_config.json

🖼️  Step 4: Generating image with Puppeteer...
🎨 Starting image generation...
📄 Template: ./templates/blog-post-template.html
📐 Dimensions: 1200x630
🚀 Launching browser...
📝 Loading template...
📸 Capturing screenshot...
✅ Image generated successfully: output/your-post.png
📊 File size: 234.56 KB

============================================================
✅ SUCCESS! Image generated successfully
============================================================

📁 Output: output/your-post.png
📐 Size: 1200x630
📊 Format: PNG
============================================================
```

## Troubleshooting Test Issues

### Issue: "REST API 403 Forbidden"

**Cause:** Site has disabled public API access

**Solution:** The scraper fallback will automatically activate, or use demo mode

### Issue: "Image download 403 Forbidden"

**Cause:** Image host blocks automated downloads

**Solution:** Use a different image URL or save image locally first

### Issue: "Puppeteer Chrome download failed"

**Cause:** Network restrictions or older Puppeteer version

**Solution:**
```bash
# Update Puppeteer
npm install puppeteer@latest

# Or use puppeteer-core with system Chrome
npm install puppeteer-core
```

### Issue: "No module named 'colorthief'"

**Cause:** Python dependencies not installed

**Solution:**
```bash
pip install -r requirements.txt
```

## Customization Tests

### Test Custom Colors

```bash
python main.py --url YOUR_URL --overlay "rgba(150, 50, 200, 0.7)"
```

### Test Different Sizes

```bash
python main.py --url YOUR_URL --size 1920x1080
```

### Test JPEG Format

```bash
python main.py --url YOUR_URL --format jpeg
```

### Test Custom Brand

```bash
python main.py --url YOUR_URL --brand "MY BRAND"
```

## Performance Tests

### Batch Processing

Create a test script:

```python
import subprocess
import time

urls = [
    "https://example.com/post-1/",
    "https://example.com/post-2/",
    "https://example.com/post-3/"
]

start_time = time.time()

for url in urls:
    subprocess.run(["python", "main.py", "--url", url])

elapsed = time.time() - start_time
print(f"\nProcessed {len(urls)} images in {elapsed:.2f} seconds")
print(f"Average: {elapsed/len(urls):.2f} seconds per image")
```

**Expected:** 5-10 seconds per image including download time

## Visual Inspection

After generating an image, check:

1. **Background Image:** Is it properly displayed?
2. **Title Text:** Is it readable and properly sized?
3. **Overlays:** Do colors match or complement the background?
4. **Brand Strip:** Is it visible at the bottom?
5. **Decorative Elements:** Are they positioned correctly?
6. **Image Quality:** Is it sharp (2x pixel density)?

## Continuous Integration Tests

For automated testing in CI/CD:

```bash
#!/bin/bash
# test.sh

echo "Testing WordPress fetcher..."
python scripts/fetch_post_data.py https://wordpress.org/news/ || exit 1

echo "Testing color extractor..."
python scripts/extract_colors.py https://picsum.photos/800/600 || exit 1

echo "Testing template generation..."
node scripts/generate_image.js demo_config.json || exit 1

echo "All tests passed!"
```

## Success Criteria

A successful test should:

- ✓ Fetch blog post data (or use fallback)
- ✓ Download featured image
- ✓ Extract dominant colors
- ✓ Generate configuration file
- ✓ Create PNG/JPEG image file
- ✓ Image dimensions match specifications
- ✓ File size is reasonable (100-500KB for PNG)
- ✓ Process completes in under 10 seconds
- ✓ No error messages (warnings are OK)

## Next Steps

After successful testing:

1. Customize the HTML template for your brand
2. Adjust default colors if needed
3. Set up batch processing for multiple posts
4. Integrate with your WordPress workflow
5. Configure automated triggers (webhooks, cron jobs)

---

For more help, see README.md or QUICKSTART.md
