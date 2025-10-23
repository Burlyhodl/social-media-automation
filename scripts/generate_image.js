#!/usr/bin/env node
/**
 * Image Generation Script using Puppeteer
 * Renders HTML template and captures screenshot
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

/**
 * Generate blog post image from template
 *
 * @param {Object} config - Configuration object
 * @param {string} config.templatePath - Path to HTML template
 * @param {string} config.outputPath - Path to save generated image
 * @param {string} config.title - Blog post title
 * @param {string} config.backgroundImage - URL or path to background image
 * @param {string} config.overlayColor - RGBA color for overlay
 * @param {string} config.accentColor - RGBA color for accent
 * @param {string} config.brandText - Text for brand strip (optional)
 * @param {number} config.width - Image width (default: 1200)
 * @param {number} config.height - Image height (default: 630)
 * @param {string} config.format - Image format: 'png' or 'jpeg' (default: 'png')
 */
async function generateImage(config) {
    const {
        templatePath,
        outputPath,
        title = 'Blog Post Title',
        backgroundImage,
        overlayColor = 'rgba(204, 85, 0, 0.75)',
        accentColor = 'rgba(255, 107, 0, 0.9)',
        brandText = 'YOURBRAND.COM',
        width = 1200,
        height = 630,
        format = 'png'
    } = config;

    console.log('🎨 Starting image generation...');
    console.log(`📄 Template: ${templatePath}`);
    console.log(`📐 Dimensions: ${width}x${height}`);

    let browser;

    try {
        // Read template
        if (!fs.existsSync(templatePath)) {
            throw new Error(`Template not found: ${templatePath}`);
        }

        let htmlContent = fs.readFileSync(templatePath, 'utf8');

        // Replace CSS variables and content
        htmlContent = htmlContent.replace(/--bg-image: url\([^)]+\);/,
            `--bg-image: url('${backgroundImage}');`);
        htmlContent = htmlContent.replace(/--overlay-color: [^;]+;/,
            `--overlay-color: ${overlayColor};`);
        htmlContent = htmlContent.replace(/--accent-color: [^;]+;/,
            `--accent-color: ${accentColor};`);
        htmlContent = htmlContent.replace(/--width: [^;]+;/,
            `--width: ${width}px;`);
        htmlContent = htmlContent.replace(/--height: [^;]+;/,
            `--height: ${height}px;`);

        // Replace title text
        htmlContent = htmlContent.replace(
            /<h1 class="title"[^>]*>.*?<\/h1>/s,
            `<h1 class="title" id="titleText">${escapeHtml(title)}</h1>`
        );

        // Replace brand text
        htmlContent = htmlContent.replace(
            /<div class="brand-text">.*?<\/div>/,
            `<div class="brand-text">${escapeHtml(brandText)}</div>`
        );

        // Launch browser
        console.log('🚀 Launching browser...');
        browser = await puppeteer.launch({
            headless: 'new',
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu'
            ]
        });

        const page = await browser.newPage();

        // Set viewport to exact dimensions
        await page.setViewport({
            width: width,
            height: height,
            deviceScaleFactor: 2 // For high-DPI displays
        });

        // Load HTML content
        console.log('📝 Loading template...');
        await page.setContent(htmlContent, {
            waitUntil: 'networkidle0'
        });

        // Wait a bit for fonts to load
        await page.waitForTimeout(1000);

        // Ensure output directory exists
        const outputDir = path.dirname(outputPath);
        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }

        // Take screenshot
        console.log('📸 Capturing screenshot...');
        await page.screenshot({
            path: outputPath,
            type: format,
            quality: format === 'jpeg' ? 90 : undefined,
            clip: {
                x: 0,
                y: 0,
                width: width,
                height: height
            }
        });

        console.log(`✅ Image generated successfully: ${outputPath}`);

        // Get file size
        const stats = fs.statSync(outputPath);
        const fileSizeKB = (stats.size / 1024).toFixed(2);
        console.log(`📊 File size: ${fileSizeKB} KB`);

        return {
            success: true,
            outputPath: outputPath,
            fileSize: stats.size
        };

    } catch (error) {
        console.error('❌ Error generating image:', error.message);
        return {
            success: false,
            error: error.message
        };
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Load configuration from JSON file
 */
function loadConfigFromFile(configPath) {
    if (!fs.existsSync(configPath)) {
        throw new Error(`Config file not found: ${configPath}`);
    }
    const configContent = fs.readFileSync(configPath, 'utf8');
    return JSON.parse(configContent);
}

// CLI usage
if (require.main === module) {
    const args = process.argv.slice(2);

    if (args.length === 0) {
        console.log('Usage:');
        console.log('  node generate_image.js <config.json>');
        console.log('  node generate_image.js --title "Title" --bg "image.jpg" --output "out.png"');
        console.log('\nConfig JSON format:');
        console.log(JSON.stringify({
            templatePath: './templates/blog-post-template.html',
            outputPath: './output/image.png',
            title: 'Your Blog Post Title',
            backgroundImage: 'https://example.com/image.jpg',
            overlayColor: 'rgba(204, 85, 0, 0.75)',
            accentColor: 'rgba(255, 107, 0, 0.9)',
            brandText: 'YOURBRAND.COM',
            width: 1200,
            height: 630,
            format: 'png'
        }, null, 2));
        process.exit(1);
    }

    // Check if first argument is a JSON file
    if (args[0].endsWith('.json')) {
        const config = loadConfigFromFile(args[0]);
        generateImage(config)
            .then(result => {
                process.exit(result.success ? 0 : 1);
            });
    } else {
        // Parse command line arguments
        const config = {
            templatePath: './templates/blog-post-template.html',
            outputPath: './output/image.png'
        };

        for (let i = 0; i < args.length; i += 2) {
            const key = args[i].replace('--', '');
            const value = args[i + 1];

            switch (key) {
                case 'title':
                    config.title = value;
                    break;
                case 'bg':
                case 'background':
                    config.backgroundImage = value;
                    break;
                case 'output':
                    config.outputPath = value;
                    break;
                case 'overlay':
                    config.overlayColor = value;
                    break;
                case 'accent':
                    config.accentColor = value;
                    break;
                case 'brand':
                    config.brandText = value;
                    break;
                case 'width':
                    config.width = parseInt(value);
                    break;
                case 'height':
                    config.height = parseInt(value);
                    break;
                case 'format':
                    config.format = value;
                    break;
            }
        }

        generateImage(config)
            .then(result => {
                process.exit(result.success ? 0 : 1);
            });
    }
}

module.exports = { generateImage };
