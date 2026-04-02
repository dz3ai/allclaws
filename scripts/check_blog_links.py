#!/usr/bin/env python3
"""
Blog link checker for allclaws Jekyll blog.
Only checks blog-related files (index, _posts, _layouts).

Usage:
    python scripts/check_blog_links.py
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict

class BlogLinkChecker:
    """Check links in Jekyll blog files."""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.results: List[Dict] = []

    def get_blog_files(self) -> List[Path]:
        """Get blog-related files only."""
        files = []
        # Index files
        files.append(self.project_root / 'index.md')
        files.append(self.project_root / 'blog.md')
        # Layout files
        files.extend(self.project_root.glob('_layouts/*.html'))
        # Post files
        files.extend(self.project_root.glob('_posts/*.md'))

        return [f for f in files if f.exists()]

    def is_liquid_variable(self, text: str) -> bool:
        """Check if text is a Jekyll Liquid variable."""
        return '{{' in text and '}}' in text

    def extract_links(self, file_path: Path) -> List[Tuple[str, str, int]]:
        """Extract links from file.

        Returns:
            List of (link, link_type, line_number) tuples.
        """
        links = []
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Markdown link pattern: [text](url)
        md_link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'

        # HTML patterns
        html_patterns = [
            (r'href="([^"]+)"', 'href'),
            (r"href='([^']+)'", 'href'),
            (r'src="([^"]+)"', 'src'),
            (r"src='([^']+)'", 'src'),
            (r'url\(["\']?([^"\'() )]+)["\']?\)', 'css-url'),
        ]

        for line_num, line in enumerate(lines, 1):
            # Check markdown links
            for match in re.finditer(md_link_pattern, line):
                link = match.group(2)
                if not self.is_liquid_variable(link):
                    links.append((link, 'markdown', line_num))

            # Check HTML/CSS links
            for pattern, link_type in html_patterns:
                for match in re.finditer(pattern, line):
                    link = match.group(1)
                    if not self.is_liquid_variable(link):
                        links.append((link, link_type, line_num))

            # Also check for Jekyll liquid tags: {% post_url 2024-01-01-title %}
            for match in re.finditer(r'{%\s*post_url\s+([^}%]+)\s*%}', line):
                links.append((match.group(1).strip(), 'post_url', line_num))

        return links

    def check_internal_link(self, link: str, source_file: Path) -> Tuple[bool, str]:
        """Check if internal link points to existing file.

        Returns:
            (is_valid, resolved_path_or_error)
        """
        # Remove fragment
        clean_link = link.split('#')[0]

        if not clean_link or clean_link == '/':
            return True, 'root'

        # Handle absolute URLs (from site root)
        if clean_link.startswith('/'):
            # For Jekyll with baseurl /allclaws
            clean_link = clean_link.lstrip('/')
            target = self.project_root / clean_link
        else:
            # Relative path
            target = source_file.parent / clean_link

        # Direct file match
        if target.exists():
            return True, str(target.relative_to(self.project_root))

        # Try with .html extension
        if target.with_suffix('.html').exists():
            return True, str(target.with_suffix('.html').relative_to(self.project_root))

        # Try with .md extension
        if target.with_suffix('.md').exists():
            return True, str(target.with_suffix('.md').relative_to(self.project_root))

        # Check if it's a directory with index
        if target.is_dir():
            for index_name in ['index.html', 'index.md']:
                if (target / index_name).exists():
                    return True, str((target / index_name).relative_to(self.project_root))

        # Special Jekyll baseurl handling (no baseurl now)
        # Keep for backwards compatibility in case /allclaws appears in links
        if clean_link.startswith('allclaws/'):
            clean_link = clean_link.replace('allclaws/', '')
            target = self.project_root / clean_link
            if target.exists() or target.with_suffix('.html').exists() or target.with_suffix('.md').exists():
                return True, f"baseurl: {clean_link}"

        # Asset files
        if 'assets/' in clean_link:
            asset_path = self.project_root / clean_link
            if asset_path.exists():
                return True, str(asset_path.relative_to(self.project_root))

        return False, f"not found: {clean_link}"

    def check_post_url(self, post_name: str, source_file: Path) -> Tuple[bool, str]:
        """Check Jekyll post_url tag.

        Returns:
            (is_valid, resolved_path_or_error)
        """
        # Jekyll post_url expects just the filename (YYYY-MM-DD-title.md)
        posts_dir = self.project_root / '_posts'

        # Check if file exists in _posts
        target = posts_dir / post_name
        if target.exists():
            return True, str(target.relative_to(self.project_root))

        # Try with .md extension
        if target.with_suffix('.md').exists():
            return True, str(target.with_suffix('.md').relative_to(self.project_root))

        return False, f"post not found: {post_name}"

    def check_file(self, file_path: Path) -> List[Dict]:
        """Check all links in a file."""
        relative_file = file_path.relative_to(self.project_root)
        links = self.extract_links(file_path)
        file_results = []

        for link, link_type, line_num in links:
            result = {
                'file': str(relative_file),
                'line': line_num,
                'link': link,
                'type': link_type,
                'valid': True,
                'error': '',
                'external': False,
            }

            # Skip empty links, anchors, and special protocols
            if not link or link == '#' or link.startswith('mailto:') or link.startswith('tel:'):
                continue
            if link.startswith('javascript:') or link.startswith('data:'):
                continue

            # Handle different link types
            if link_type == 'post_url':
                is_valid, message = self.check_post_url(link, file_path)
                result['valid'] = is_valid
                result['error'] = message if not is_valid else ''
            elif link.startswith('http://') or link.startswith('https://'):
                result['external'] = True
                # For external links, we just record them (could add HTTP checking later)
            else:
                is_valid, message = self.check_internal_link(link, file_path)
                result['valid'] = is_valid
                result['error'] = message if not is_valid else ''

            file_results.append(result)

        return file_results

    def check_all(self) -> List[Dict]:
        """Check all blog files."""
        files = self.get_blog_files()
        print(f"Found {len(files)} blog files to check\n")

        all_results = []

        for file_path in sorted(files):
            relative_file = file_path.relative_to(self.project_root)
            print(f"Checking: {relative_file}")
            file_results = self.check_file(file_path)
            all_results.extend(file_results)

        return all_results

    def print_results(self, results: List[Dict]):
        """Print results."""
        invalid = [r for r in results if not r['valid']]
        external = [r for r in results if r.get('external')]
        internal = [r for r in results if not r.get('external')]

        print("\n" + "=" * 60)
        print("BLOG LINK CHECK RESULTS")
        print("=" * 60)
        print(f"\nTotal links checked: {len(results)}")
        print(f"Internal links: {len(internal)}")
        print(f"External links: {len(external)}")
        print(f"Valid links: {len(results) - len(invalid)}")
        print(f"Invalid links: {len(invalid)}")

        if invalid:
            print("\n" + "-" * 60)
            print("INVALID LINKS:")
            print("-" * 60)

            for result in invalid:
                print(f"\n{result['file']}:{result['line']}")
                print(f"  [{result['type']}] {result['link']}")
                if result['error']:
                    print(f"  Error: {result['error']}")

        if external:
            print("\n" + "-" * 60)
            print(f"EXTERNAL LINKS ({len(external)}):")
            print("-" * 60)

            # Show unique external links
            unique_external = sorted(set(r['link'] for r in external))
            for url in unique_external[:30]:
                print(f"  {url}")
            if len(unique_external) > 30:
                print(f"  ... and {len(unique_external) - 30} more")

        print("\n" + "=" * 60)

        return len(invalid) == 0


def main():
    project_root = Path(__file__).parent.parent
    print(f"Project root: {project_root}\n")

    checker = BlogLinkChecker(str(project_root))
    results = checker.check_all()

    success = checker.print_results(results)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
