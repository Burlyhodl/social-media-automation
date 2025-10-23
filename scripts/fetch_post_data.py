#!/usr/bin/env python3
"""
WordPress Post Data Fetcher
Extracts blog post metadata from WordPress sites via REST API
"""

import requests
import re
import json
from urllib.parse import urlparse, urljoin
from typing import Dict, Optional
from bs4 import BeautifulSoup


class WordPressPostFetcher:
    """Fetches blog post data from WordPress sites"""

    def __init__(self, post_url: str):
        self.post_url = post_url
        self.parsed_url = urlparse(post_url)
        self.base_url = f"{self.parsed_url.scheme}://{self.parsed_url.netloc}"

    def extract_post_slug(self) -> str:
        """Extract the post slug from the URL"""
        path = self.parsed_url.path.strip('/')
        # Get the last segment of the path as the slug
        segments = path.split('/')
        return segments[-1] if segments else ''

    def fetch_post_data(self) -> Optional[Dict]:
        """
        Fetch post data from WordPress REST API with web scraping fallback
        Returns dict with: title, excerpt, featured_image_url, author, date
        """
        slug = self.extract_post_slug()

        if not slug:
            print(f"Error: Could not extract post slug from URL: {self.post_url}")
            return None

        # Try REST API first
        api_url = urljoin(self.base_url, f'/wp-json/wp/v2/posts?slug={slug}')

        try:
            print(f"Fetching post data from: {api_url}")
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()

            posts = response.json()

            if not posts or len(posts) == 0:
                print(f"No post found with slug: {slug}")
                print("Falling back to web scraping...")
                return self._scrape_post_data()

            post = posts[0]  # Get first matching post

            # Extract featured image URL if available
            featured_image_url = None
            if post.get('featured_media') and post['featured_media'] > 0:
                media_id = post['featured_media']
                media_url = urljoin(self.base_url, f'/wp-json/wp/v2/media/{media_id}')

                try:
                    media_response = requests.get(media_url, timeout=10)
                    media_response.raise_for_status()
                    media_data = media_response.json()

                    # Try to get the largest available image
                    if 'source_url' in media_data:
                        featured_image_url = media_data['source_url']
                    elif 'media_details' in media_data and 'sizes' in media_data['media_details']:
                        sizes = media_data['media_details']['sizes']
                        # Prefer full, then large, then medium
                        for size in ['full', 'large', 'medium_large', 'medium']:
                            if size in sizes and 'source_url' in sizes[size]:
                                featured_image_url = sizes[size]['source_url']
                                break

                except Exception as e:
                    print(f"Warning: Could not fetch featured image: {e}")

            # Clean HTML from title and excerpt
            title = self._strip_html(post.get('title', {}).get('rendered', 'Untitled'))
            excerpt = self._strip_html(post.get('excerpt', {}).get('rendered', ''))

            result = {
                'title': title,
                'excerpt': excerpt,
                'featured_image_url': featured_image_url,
                'author': post.get('author', ''),
                'date': post.get('date', ''),
                'link': post.get('link', self.post_url),
                'slug': slug
            }

            print(f"Successfully fetched post: {title}")
            return result

        except requests.exceptions.RequestException as e:
            print(f"REST API error: {e}")
            print("Falling back to web scraping...")
            return self._scrape_post_data()

    def _scrape_post_data(self) -> Optional[Dict]:
        """
        Fallback method: Scrape post data directly from the HTML page
        """
        try:
            print(f"Scraping post data from: {self.post_url}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            response = requests.get(self.post_url, timeout=10, headers=headers, allow_redirects=True)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract title - try multiple common selectors
            title = None
            title_selectors = [
                'h1.entry-title',
                'h1.post-title',
                'h1[class*="title"]',
                'article h1',
                'h1'
            ]

            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    break

            # Fallback to meta tags or page title
            if not title:
                og_title = soup.find('meta', property='og:title')
                if og_title:
                    title = og_title.get('content', '')
                else:
                    title_tag = soup.find('title')
                    title = title_tag.get_text(strip=True) if title_tag else 'Untitled'

            # Extract featured image - try multiple methods
            featured_image_url = None

            # Try Open Graph image
            og_image = soup.find('meta', property='og:image')
            if og_image:
                featured_image_url = og_image.get('content')

            # Try common WordPress image selectors
            if not featured_image_url:
                img_selectors = [
                    'img.wp-post-image',
                    'img.attachment-post-thumbnail',
                    'div.post-thumbnail img',
                    'figure.wp-block-post-featured-image img',
                    'article img'
                ]

                for selector in img_selectors:
                    img = soup.select_one(selector)
                    if img:
                        featured_image_url = img.get('src') or img.get('data-src')
                        if featured_image_url:
                            # Make absolute URL
                            if featured_image_url.startswith('//'):
                                featured_image_url = f"{self.parsed_url.scheme}:{featured_image_url}"
                            elif featured_image_url.startswith('/'):
                                featured_image_url = urljoin(self.base_url, featured_image_url)
                            break

            # Extract excerpt/description
            excerpt = ''
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                excerpt = meta_desc.get('content', '')
            else:
                og_desc = soup.find('meta', property='og:description')
                if og_desc:
                    excerpt = og_desc.get('content', '')

            slug = self.extract_post_slug()

            result = {
                'title': title,
                'excerpt': excerpt,
                'featured_image_url': featured_image_url,
                'author': '',
                'date': '',
                'link': self.post_url,
                'slug': slug
            }

            print(f"Successfully scraped post: {title}")
            if featured_image_url:
                print(f"Found featured image: {featured_image_url}")

            return result

        except Exception as e:
            print(f"Error scraping post data: {e}")
            return None

    @staticmethod
    def _strip_html(html_text: str) -> str:
        """Remove HTML tags from text"""
        clean = re.sub('<.*?>', '', html_text)
        # Decode HTML entities
        clean = clean.replace('&amp;', '&')
        clean = clean.replace('&lt;', '<')
        clean = clean.replace('&gt;', '>')
        clean = clean.replace('&quot;', '"')
        clean = clean.replace('&#039;', "'")
        clean = clean.replace('&rsquo;', "'")
        clean = clean.replace('&lsquo;', "'")
        clean = clean.replace('&rdquo;', '"')
        clean = clean.replace('&ldquo;', '"')
        return clean.strip()


def fetch_wordpress_post(url: str) -> Optional[Dict]:
    """
    Convenience function to fetch WordPress post data

    Args:
        url: Full URL to WordPress blog post

    Returns:
        Dictionary with post data or None if failed
    """
    fetcher = WordPressPostFetcher(url)
    return fetcher.fetch_post_data()


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python fetch_post_data.py <blog_post_url>")
        sys.exit(1)

    url = sys.argv[1]
    data = fetch_wordpress_post(url)

    if data:
        print("\n" + "="*50)
        print("POST DATA")
        print("="*50)
        print(json.dumps(data, indent=2))
    else:
        print("Failed to fetch post data")
        sys.exit(1)
