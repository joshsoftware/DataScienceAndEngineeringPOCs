import requests
from bs4 import BeautifulSoup
import html2text
import json
from urllib.parse import urlparse, urljoin
from datetime import datetime
import os
import re
from collections import deque

class WebCrawler:
    def __init__(self, base_url, depth=1, max_pages=50):
        """
        Initialize the web crawler.
        
        Args:
            base_url (str): The main website URL to start crawling from
            depth (int): How deep to crawl (1-10, where 1 is minimum and 10 is maximum)
            max_pages (int): Maximum number of pages to crawl
        """
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.depth = max(1, min(10, depth))  # Ensure depth is between 1 and 10
        self.max_pages = max_pages
        self.visited_urls = set()
        # Store URLs with their depth: (url, depth_level)
        self.urls_to_visit = deque([(base_url, 0)])
        self.collected_data = []
        
    def is_valid_url(self, url):
        """Check if URL is valid and belongs to the same domain."""
        try:
            parsed = urlparse(url)
            return (
                parsed.netloc == self.base_domain and
                not url.endswith(('.pdf', '.jpg', '.png', '.gif', '.jpeg', '.doc', '.docx')) and
                '#' not in url
            )
        except:
            return False

    def extract_links(self, soup, current_url, current_depth):
        """
        Extract valid links from the page.
        
        Args:
            soup: BeautifulSoup object
            current_url: The URL being processed
            current_depth: Current depth level
            
        Returns:
            set: Set of (url, new_depth) tuples
        """
        links = set()
        if current_depth >= self.depth:
            return links
            
        for link in soup.find_all('a', href=True):
            url = link['href']
            absolute_url = urljoin(current_url, url)
            if self.is_valid_url(absolute_url):
                links.add((absolute_url, current_depth + 1))
        return links

    def clean_text(self, text):
        """Clean the text by removing links, extra spaces, and formatting issues."""
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'(?:[\w-]+/)+[\w-]+(?:\.\w+)?', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = '\n'.join(line.strip() for line in text.split('\n'))
        return text.strip()

    def get_page_data(self, url, current_depth):
        """Get data from a single webpage."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.extract()

            # Extract new links with depth
            new_links = self.extract_links(soup, url, current_depth)
            for link, new_depth in new_links:
                if link not in self.visited_urls:
                    self.urls_to_visit.append((link, new_depth))

            # Extract text
            html = str(soup)
            html2text_instance = html2text.HTML2Text()
            html2text_instance.ignore_links = True
            html2text_instance.ignore_images = True
            html2text_instance.ignore_emphasis = True
            html2text_instance.body_width = 0
            text = html2text_instance.handle(html)
            text = self.clean_text(text)

            # Extract metadata
            try:
                page_title = soup.title.string.strip() if soup.title else "No Title"
                page_title = self.clean_text(page_title)
            except:
                page_title = urlparse(url).path[1:].replace("/", "-") or "No Title"

            meta_description = soup.find("meta", attrs={"name": "description"})
            description = self.clean_text(meta_description.get("content")) if meta_description else "No description available"

            meta_keywords = soup.find("meta", attrs={"name": "keywords"})
            keywords = self.clean_text(meta_keywords.get("content")) if meta_keywords else "No keywords available"

            return {
                'url': url,
                'depth': current_depth,
                'title': page_title,
                'description': description,
                'keywords': keywords,
                'content': text
            }

        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            return None

    def crawl(self):
        """Start the crawling process."""
        while self.urls_to_visit and len(self.visited_urls) < self.max_pages:
            current_url, current_depth = self.urls_to_visit.popleft()
            if current_url in self.visited_urls:
                continue
                
            print(f"\nCrawling {len(self.visited_urls) + 1}/{self.max_pages} (Depth: {current_depth}/{self.depth}): {current_url}")
            page_data = self.get_page_data(current_url, current_depth)
            
            if page_data:
                self.collected_data.append(page_data)
                self.visited_urls.add(current_url)
                print(f"Successfully processed: {current_url}")
            else:
                print(f"Failed to process: {current_url}")

    def save_results(self):
        """Save the crawled data to files."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = f'website_data_{timestamp}'
        os.makedirs(output_dir, exist_ok=True)

        # Save metadata
        metadata = [{
            'title': item['title'],
            'url': item['url'],
            'depth': item['depth'],
            'description': item['description'],
            'keywords': item['keywords']
        } for item in self.collected_data]
        
        metadata_filename = os.path.join(output_dir, 'metadata.json')
        with open(metadata_filename, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)

        # Save content
        content_filename = os.path.join(output_dir, 'clean_content.txt')
        with open(content_filename, 'w', encoding='utf-8') as f:
            for item in self.collected_data:
                f.write(f"\n{'='*80}\n")
                f.write(f"URL: {item['url']}\n")
                f.write(f"Depth: {item['depth']}\n")
                f.write(f"Title: {item['title']}\n")
                f.write(f"Description: {item['description']}\n")
                f.write(f"Keywords: {item['keywords']}\n")
                f.write(f"\n--- Content ---\n\n")
                f.write(item['content'])
                f.write(f"\n{'='*80}\n")

        # Save depth analysis
        depth_stats = {}
        for item in self.collected_data:
            depth = item['depth']
            if depth not in depth_stats:
                depth_stats[depth] = 0
            depth_stats[depth] += 1
            
        stats_filename = os.path.join(output_dir, 'depth_statistics.json')
        with open(stats_filename, 'w', encoding='utf-8') as f:
            json.dump({
                'total_pages': len(self.visited_urls),
                'max_depth_reached': max(depth_stats.keys()),
                'pages_per_depth': depth_stats
            }, f, indent=4)

        print(f"\nCrawling complete!")
        print(f"Processed {len(self.visited_urls)} pages")
        print(f"Maximum depth reached: {max(depth_stats.keys())}")
        print(f"Content saved to: {content_filename}")
        print(f"Metadata saved to: {metadata_filename}")
        print(f"Depth statistics saved to: {stats_filename}")

if __name__ == "__main__":
    base_url = "https://joshsoftware.com"
    crawler = WebCrawler(base_url, depth=3, max_pages=10)
    crawler.crawl()
    crawler.save_results()