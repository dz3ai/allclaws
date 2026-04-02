#!/usr/bin/env python3
"""
GitHub Pages deployment validator.

Checks the deployed site for 404 errors and common configuration issues.

Usage:
    python3 scripts/validate_github_pages.py [--url BASE_URL]

Example:
    python3 scripts/validate_github_pages.py --url https://dz3ai.github.io/allclaws
"""

import argparse
import sys
import re
from urllib.parse import urljoin, urlparse
from typing import List, Tuple, Dict

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False
    print("Warning: requests and/or beautifulsoup4 not installed.")
    print("Install with: pip install requests beautifulsoup4")


class GitHubPagesValidator:
    """Validate a deployed GitHub Pages site."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.results: List[Dict] = []
        self.checked: set = set()

    def check_url(self, url: str) -> Tuple[bool, int, str]:
        """Check a single URL.

        Returns:
            (success, status_code, error_message)
        """
        if url in self.checked:
            return True, 200, ""
        self.checked.add(url)

        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            return (response.status_code < 400, response.status_code, "")
        except requests.RequestException as e:
            return False, 0, str(e)

    def extract_links(self, html: str) -> List[str]:
        """Extract all href links from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        links = []

        for tag in soup.find_all('a', href=True):
            href = tag['href']
            # Skip anchors, mailto, tel
            if href and not href.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
                links.append(href)

        return links

    def check_base_url_patterns(self) -> List[Dict]:
        """Check common URL patterns based on baseurl."""
        patterns = [
            ('', 'Root'),
            ('/blog/', 'Blog index'),
        ]

        # Try to find posts from sitemap or common patterns
        results = []

        for path, name in patterns:
            url = urljoin(self.base_url, path)
            success, status, error = self.check_url(url)
            results.append({
                'type': 'pattern',
                'name': name,
                'url': url,
                'success': success,
                'status': status,
                'error': error,
            })

        return results

    def check_page_links(self, path: str = '') -> List[Dict]:
        """Check all links on a specific page."""
        url = urljoin(self.base_url, path)
        results = []

        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return [{
                    'type': 'page_load',
                    'url': url,
                    'success': False,
                    'status': response.status_code,
                    'error': f"Failed to load page",
                }]

            links = self.extract_links(response.text)

            for link in links[:50]:  # Limit to first 50 links
                # Convert relative URLs to absolute
                absolute = urljoin(url, link)

                # Only check internal links
                parsed_base = urlparse(self.base_url)
                parsed_link = urlparse(absolute)

                if parsed_link.netlink == parsed_base.netlink:
                    success, status, error = self.check_url(absolute)
                    results.append({
                        'type': 'internal_link',
                        'source': url,
                        'url': absolute,
                        'success': success,
                        'status': status,
                        'error': error,
                    })

        except requests.RequestException as e:
            results.append({
                'type': 'page_error',
                'url': url,
                'success': False,
                'status': 0,
                'error': str(e),
            })

        return results

    def diagnose_config_issues(self) -> List[str]:
        """Diagnose configuration issues from 404 patterns."""
        issues = []

        # Check root
        success, status, _ = self.check_url(self.base_url)
        if not success and status == 404:
            issues.append("Root URL returns 404 - check GitHub Pages source branch")

        # Check if links are missing baseurl
        success, status, _ = self.check_url(urljoin(self.base_url, '/blog/'))
        if not success and status == 404:
            # Try without /repo/ in path
            parsed = urlparse(self.base_url)
            base_no_repo = parsed.scheme + '://' + parsed.netlink
            success2, status2, _ = self.check_url(urljoin(base_no_repo, '/blog/'))
            if success2:
                issues.append(f"Links missing baseurl - use | relative_url filter in templates")
                issues.append(f"Check _config.yml: baseurl should be '{parsed.path}'")

        return issues

    def validate(self) -> Dict:
        """Run full validation."""
        print(f"Validating: {self.base_url}\n")

        all_results = []

        # Check base URL
        print("Checking base URL patterns...")
        pattern_results = self.check_base_url_patterns()
        all_results.extend(pattern_results)

        # Check blog page for post links
        print("Checking blog page links...")
        blog_results = self.check_page_links('/blog/')
        all_results.extend(blog_results)

        # Diagnose issues
        print("\nDiagnosing configuration issues...")
        issues = self.diagnose_config_issues()

        return {
            'results': all_results,
            'issues': issues,
            'base_url': self.base_url,
        }

    def print_report(self, validation: Dict):
        """Print validation report."""
        results = validation['results']
        issues = validation['issues']
        base_url = validation['base_url']

        print("\n" + "=" * 60)
        print("GITHUB PAGES VALIDATION REPORT")
        print("=" * 60)
        print(f"\nBase URL: {base_url}")

        # Summary
        total = len(results)
        failed = sum(1 for r in results if not r['success'])
        print(f"\nLinks checked: {total}")
        print(f"Failed: {failed}")
        print(f"Success rate: {100 * (total - failed) // total if total else 0}%")

        # Failed links
        if failed:
            print("\n" + "-" * 60)
            print("FAILED LINKS:")
            print("-" * 60)

            for r in results:
                if not r['success']:
                    print(f"\n[{r['type']}] {r['url']}")
                    print(f"  Status: {r['status']}")
                    if r.get('error'):
                        print(f"  Error: {r['error']}")

        # Configuration issues
        if issues:
            print("\n" + "-" * 60)
            print("CONFIGURATION ISSUES DETECTED:")
            print("-" * 60)

            for issue in issues:
                print(f"  ⚠️  {issue}")

        print("\n" + "=" * 60)

        return failed == 0 and not issues


def main():
    parser = argparse.ArgumentParser(description='Validate GitHub Pages deployment')
    parser.add_argument(
        '--url',
        default='https://dz3ai.github.io/allclaws',
        help='Base URL of the GitHub Pages site'
    )

    args = parser.parse_args()

    if not HAS_DEPS:
        print("Error: Required dependencies not installed.")
        print("Run: pip install requests beautifulsoup4")
        sys.exit(1)

    validator = GitHubPagesValidator(args.url)
    validation = validator.validate()
    success = validator.print_report(validation)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
