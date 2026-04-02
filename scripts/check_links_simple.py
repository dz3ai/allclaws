#!/usr/bin/env python3
"""
Simple link checker for allclaws Jekyll blog.
Checks links in source files without requiring Jekyll build.

Usage:
    python scripts/check_links_simple.py [--skip-external]
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Set

class SimpleLinkChecker:
    """Check links in Jekyll source files."""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.results: List[Dict] = []
        self.url_cache: Dict[str, bool] = {}

    def find_markdown_files(self) -> List[Path]:
        """Find all markdown files."""
        return list(self.project_root.rglob("*.md")) + list(self.project_root.rglob("*.html"))

    def extract_links_from_markdown(self, file_path: Path) -> List[Tuple[str, str, int]]:
        """Extract links from markdown file.

        Returns:
            List of (link, link_type, line_number) tuples.
        """
        links = []
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Markdown links: [text](url)
        md_link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'

        # HTML links
        html_patterns = [
            (r'href="([^"]+)"', 'href'),
            (r"href='([^']+)'", 'href'),
            (r'src="([^"]+)"', 'src'),
            (r"src='([^']+)'", 'src'),
        ]

        for line_num, line in enumerate(lines, 1):
            # Check markdown links
            for match in re.finditer(md_link_pattern, line):
                links.append((match.group(2), 'markdown', line_num))

            # Check HTML links
            for pattern, link_type in html_patterns:
                for match in re.finditer(pattern, line):
                    links.append((match.group(1), link_type, line_num))

        return links

    def normalize_internal_path(self, link: str, source_file: Path) -> Path:
        """Convert link to filesystem path."""
        # Remove fragment
        clean_link = link.split('#')[0]

        if not clean_link or clean_link == '/':
            return self.project_root / 'index.html'

        # Handle absolute URLs (from site root)
        if clean_link.startswith('/'):
            # For Jekyll, /blog/ -> blog/index.html
            clean_link = clean_link.lstrip('/')
            target = self.project_root / clean_link
        else:
            # Relative path
            target = source_file.parent / clean_link

        return target

    def check_internal_link(self, link: str, source_file: Path) -> Tuple[bool, str]:
        """Check if internal link points to existing file.

        Returns:
            (is_valid, resolved_path_or_error)
        """
        target = self.normalize_internal_path(link, source_file)

        # Direct file match
        if target.exists():
            return True, str(target)

        # Try with .html extension
        if target.with_suffix('.html').exists():
            return True, str(target.with_suffix('.html'))

        # Try with .md extension (for source files)
        if target.with_suffix('.md').exists():
            return True, str(target.with_suffix('.md'))

        # Check if it's a directory with index
        if target.is_dir():
            for index_name in ['index.html', 'index.md']:
                if (target / index_name).exists():
                    return True, str(target / index_name)

        # Special cases for Jekyll
        # /blog/ -> _posts/ or blog.md
        if 'blog' in link.lower():
            if (self.project_root / '_posts').exists():
                return True, f"_posts directory"

        # Asset files
        if link.startswith('/assets/'):
            asset_path = self.project_root / link.lstrip('/')
            if asset_path.exists():
                return True, str(asset_path)

        return False, f"File not found: {target}"

    def check_file(self, file_path: Path) -> List[Dict]:
        """Check all links in a file."""
        relative_file = file_path.relative_to(self.project_root)
        links = self.extract_links_from_markdown(file_path)
        file_results = []

        for link, link_type, line_num in links:
            result = {
                'file': str(relative_file),
                'line': line_num,
                'link': link,
                'type': link_type,
                'valid': True,
                'error': '',
            }

            # Skip empty links, anchors, and special protocols
            if not link or link.startswith('#') or link in ('mailto:', 'tel:'):
                continue

            if link.startswith('mailto:') or link.startswith('tel:') or link.startswith('javascript:'):
                continue

            # Check link type
            if link.startswith('http://') or link.startswith('https://'):
                # External link - just record it
                result['valid'] = True
                result['external'] = True
            else:
                # Internal link
                is_valid, message = self.check_internal_link(link, file_path)
                result['valid'] = is_valid
                result['error'] = message if not is_valid else ''
                result['external'] = False

            file_results.append(result)

        return file_results

    def check_all(self, skip_external: bool = False) -> List[Dict]:
        """Check all files in the project."""
        files = self.find_markdown_files()

        # Filter out node_modules, .git, etc.
        excluded_dirs = {'.git', 'node_modules', '.sass-cache', '.jekyll-cache', 'vendor'}
        files = [f for f in files if not any(
            excluded_dir in f.parts for excluded_dir in excluded_dirs
        )]

        print(f"Found {len(files)} source files to check\n")

        all_results = []

        for file_path in sorted(files):
            relative_file = file_path.relative_to(self.project_root)
            print(f"Checking: {relative_file}")
            file_results = self.check_file(file_path)

            # Filter external links if skipped
            if skip_external:
                file_results = [r for r in file_results if not r.get('external')]

            all_results.extend(file_results)

        return all_results

    def print_results(self, results: List[Dict]):
        """Print results."""
        invalid = [r for r in results if not r['valid']]
        external = [r for r in results if r.get('external')]
        internal = [r for r in results if not r.get('external')]

        print("\n" + "=" * 60)
        print("LINK CHECK RESULTS")
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
            for url in unique_external[:20]:  # Show first 20
                print(f"  {url}")
            if len(unique_external) > 20:
                print(f"  ... and {len(unique_external) - 20} more")

        print("\n" + "=" * 60)

        return len(invalid) == 0


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Check links in Jekyll source files')
    parser.add_argument(
        '--skip-external',
        action='store_true',
        help='Skip external links in results'
    )
    parser.add_argument(
        '--project-root',
        default='.',
        help='Path to project root (default: current directory)'
    )

    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    if not (project_root / '_config.yml').exists():
        print(f"Error: Not a Jekyll project: {project_root}")
        sys.exit(1)

    print(f"Project root: {project_root}\n")

    checker = SimpleLinkChecker(str(project_root))
    results = checker.check_all(skip_external=args.skip_external)

    success = checker.print_results(results)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
