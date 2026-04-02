#!/usr/bin/env python3
"""
Link checker for allclaws Jekyll blog.

Checks all links in the generated site to ensure they are valid.
"""

import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, urljoin
from typing import Dict, List, Tuple, Set
import argparse

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False
    print("Warning: requests and/or beautifulsoup4 not installed.")
    print("Install with: pip install requests beautifulsoup4")


class LinkChecker:
    """Check links in HTML files."""

    def __init__(self, site_dir: str, base_url: str = "https://dz3ai.github.io/allclaws/"):
        self.site_dir = Path(site_dir)
        self.base_url = base_url.rstrip('/')
        self.results: List[Dict] = []
        self.checked_urls: Set[str] = set()
        self.session = None

    def _get_session(self):
        """Lazy init requests session."""
        if self.session is None:
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (compatible; allclaws-link-checker/1.0)'
            })
        return self.session

    def find_html_files(self) -> List[Path]:
        """Find all HTML files in the site directory."""
        return list(self.site_dir.rglob("*.html"))

    def extract_links(self, html_file: Path) -> List[Tuple[str, str]]:
        """Extract all links from an HTML file.

        Returns:
            List of (link_url, link_type) tuples.
        """
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')
        links = []

        # Check <a> tags
        for tag in soup.find_all('a', href=True):
            links.append((tag['href'], 'a'))

        # Check <link> tags (CSS, RSS, etc.)
        for tag in soup.find_all('link', href=True):
            links.append((tag['href'], 'link'))

        # Check <script> tags
        for tag in soup.find_all('script', src=True):
            links.append((tag['src'], 'script'))

        # Check <img> tags
        for tag in soup.find_all('img', src=True):
            links.append((tag['src'], 'img'))

        return links

    def check_internal_link(self, link: str, source_file: Path) -> Tuple[bool, str]:
        """Check if an internal link points to an existing file.

        Returns:
            (is_valid, error_message)
        """
        # Remove fragment
        link_without_fragment = link.split('#')[0]

        if not link_without_fragment or link_without_fragment == '/':
            return True, ""

        # Handle relative URLs
        if link.startswith('/'):
            # Absolute path relative to site root
            target_path = self.site_dir / link_without_fragment.lstrip('/')
        else:
            # Relative path
            target_path = source_file.parent / link_without_fragment

        # Try with .html extension if not present
        if not target_path.exists() and not target_path.suffix:
            target_path_html = target_path.with_suffix('.html')
            if target_path_html.exists():
                return True, ""

        # Check if file exists
        if target_path.exists():
            return True, ""
        elif target_path.is_dir():
            # Check for index.html inside directory
            index_path = target_path / 'index.html'
            if index_path.exists():
                return True, ""

        return False, f"File not found: {target_path}"

    def check_external_link(self, url: str) -> Tuple[bool, str, int]:
        """Check if an external URL is accessible.

        Returns:
            (is_valid, error_message, status_code)
        """
        if url in self.checked_urls:
            return True, "", 200

        try:
            session = self._get_session()
            response = session.head(url, timeout=10, allow_redirects=True)
            self.checked_urls.add(url)

            if response.status_code >= 400:
                return False, f"HTTP {response.status_code}", response.status_code

            return True, "", response.status_code
        except requests.RequestException as e:
            return False, str(e), 0

    def check_file(self, html_file: Path) -> List[Dict]:
        """Check all links in a single HTML file."""
        relative_file = html_file.relative_to(self.site_dir)
        links = self.extract_links(html_file)
        file_results = []

        for link, link_type in links:
            result = {
                'file': str(relative_file),
                'link': link,
                'type': link_type,
                'valid': True,
                'error': '',
                'status': 0,
            }

            parsed = urlparse(link)

            # Skip empty links, anchors, and mailto/tel
            if not link or link.startswith('#') or link.startswith('mailto:') or link.startswith('tel:'):
                continue

            # Internal links
            if not parsed.scheme or parsed.netloc == '' or link.startswith('/'):
                is_valid, error = self.check_internal_link(link, html_file)
                result['valid'] = is_valid
                result['error'] = error
            # External links
            elif parsed.scheme in ('http', 'https'):
                is_valid, error, status = self.check_external_link(link)
                result['valid'] = is_valid
                result['error'] = error
                result['status'] = status
            # Other schemes (javascript, data, etc.)
            else:
                result['valid'] = True  # Skip validation

            file_results.append(result)

        return file_results

    def check_all(self, skip_external: bool = False) -> List[Dict]:
        """Check all HTML files in the site directory."""
        html_files = self.find_html_files()
        all_results = []

        print(f"Found {len(html_files)} HTML files to check")

        for html_file in html_files:
            print(f"Checking: {html_file.relative_to(self.site_dir)}")
            file_results = self.check_file(html_file)
            all_results.extend(file_results)

        return all_results

    def print_results(self, results: List[Dict]):
        """Print the results of link checking."""
        invalid = [r for r in results if not r['valid']]

        print("\n" + "=" * 60)
        print("LINK CHECK RESULTS")
        print("=" * 60)

        print(f"\nTotal links checked: {len(results)}")
        print(f"Valid links: {len(results) - len(invalid)}")
        print(f"Invalid links: {len(invalid)}")

        if invalid:
            print("\n" + "-" * 60)
            print("INVALID LINKS:")
            print("-" * 60)

            # Group by file
            by_file: Dict[str, List[Dict]] = {}
            for result in invalid:
                file = result['file']
                if file not in by_file:
                    by_file[file] = []
                by_file[file].append(result)

            for file, file_results in sorted(by_file.items()):
                print(f"\n{file}:")
                for result in file_results:
                    print(f"  [{result['type']}] {result['link']}")
                    if result['error']:
                        print(f"    Error: {result['error']}")
                    if result['status']:
                        print(f"    Status: {result['status']}")

        print("\n" + "=" * 60)

        return len(invalid) == 0


def build_jekyll(site_dir: Path):
    """Build the Jekyll site."""
    import subprocess

    print("Building Jekyll site...")

    # Check if _site exists
    site_path = site_dir / '_site'
    if site_path.exists():
        print(f"Site directory exists: {site_path}")

    # Try to build
    try:
        result = subprocess.run(
            ['bundle', 'exec', 'jekyll', 'build'],
            cwd=site_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print("Jekyll build successful")
            return site_path
        else:
            print(f"Jekyll build failed: {result.stderr}")
            return None
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"Could not build Jekyll: {e}")
        print("Trying to use existing _site directory...")
        if site_path.exists():
            return site_path
        return None


def main():
    parser = argparse.ArgumentParser(description='Check links in Jekyll site')
    parser.add_argument(
        '--site-dir',
        default='_site',
        help='Path to built Jekyll site directory (default: _site)'
    )
    parser.add_argument(
        '--build',
        action='store_true',
        help='Build Jekyll site before checking'
    )
    parser.add_argument(
        '--skip-external',
        action='store_true',
        help='Skip external link checking'
    )
    parser.add_argument(
        '--base-url',
        default='https://dz3ai.github.io/allclaws/',
        help='Base URL for the site'
    )

    args = parser.parse_args()

    if not HAS_DEPS:
        print("Error: Required dependencies not installed.")
        print("Run: pip install requests beautifulsoup4")
        sys.exit(1)

    # Get the project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    site_dir = project_root / args.site_dir

    if args.build:
        built_dir = build_jekyll(project_root)
        if built_dir:
            site_dir = built_dir
        else:
            print("Failed to build site, trying existing directory...")

    if not site_dir.exists():
        print(f"Error: Site directory not found: {site_dir}")
        print("Run with --build to build the Jekyll site first")
        sys.exit(1)

    print(f"Checking links in: {site_dir}")

    checker = LinkChecker(str(site_dir), args.base_url)
    results = checker.check_all(skip_external=args.skip_external)

    success = checker.print_results(results)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
