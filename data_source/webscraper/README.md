# Web Crawler

A robust and configurable web crawler that systematically browses and extracts content from websites while respecting domain boundaries and crawling constraints.

## Features

- **Configurable Crawling Depth**: Set how deep you want to crawl (1-10 levels)
- **Page Limit Control**: Specify maximum number of pages to crawl
- **Domain Boundary Respect**: Only crawls pages within the specified domain
- **Content Extraction**:
  - Clean text content
  - Page metadata (title, description, keywords)
  - URL structure analysis
- **Link Management**:
  - Automatic handling of relative and absolute URLs
  - Duplicate URL detection
  - File type filtering (ignores PDFs, images, etc.)
- **Data Export**:
  - Structured content in TXT format
  - Metadata in JSON format
  - Depth statistics analysis
- **Error Handling**:
  - Robust request management
  - Timeout protection
  - Invalid URL filtering

## Requirements

- Python 3.8 or higher
- Required packages listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone git@github.com:joshsoftware/chatbot.ai.git
cd data_source/webscraper
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from webcrawler import WebCrawler

crawler = WebCrawler("https://example.com", depth=2, max_pages=50)
crawler.crawl()
crawler.save_results()
```

### Configuration Parameters

- `base_url` (str): The starting URL for crawling
- `depth` (int): Crawling depth (1-10, default: 1)
- `max_pages` (int): Maximum number of pages to crawl (default: 50)

### Output Files

The crawler creates a timestamped directory (`website_data_YYYYMMDD_HHMMSS`) containing:

1. `clean_content.txt`: Contains extracted text content from all crawled pages
2. `metadata.json`: Contains metadata for all crawled pages
3. `depth_statistics.json`: Contains crawling statistics and depth analysis

### Output Format

#### metadata.json
```json
[
    {
        "title": "Page Title",
        "url": "https://example.com/page",
        "depth": 1,
        "description": "Page description",
        "keywords": "keyword1, keyword2"
    }
]
```

#### depth_statistics.json
```json
{
    "total_pages": 50,
    "max_depth_reached": 2,
    "pages_per_depth": {
        "0": 1,
        "1": 25,
        "2": 24
    }
}
```

## Customization

### Modifying User Agent

You can modify the User-Agent in the `get_page_data` method:

```python
headers = {
    'User-Agent': 'Your Custom User Agent String'
}
```

### Adjusting Request Timeout

The default timeout for requests is 30 seconds. Modify in the `get_page_data` method:

```python
response = requests.get(url, headers=headers, timeout=your_timeout)
```

## Error Handling

The crawler includes robust error handling:
- Connection timeouts
- Invalid URLs
- Missing page elements
- Network errors

Failed URLs are logged but don't stop the crawling process.

## Limitations

- Only crawls within the same domain as the base URL
- Ignores URLs ending with: .pdf, .jpg, .png, .gif, .jpeg, .doc, .docx
- Ignores URLs containing fragments (#)
- Maximum depth limit of 10 levels

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- Beautiful Soup for HTML parsing
- html2text for HTML to text conversion
- Requests library for HTTP requests

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.