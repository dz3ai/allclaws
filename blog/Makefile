.PHONY: help test test-links build serve clean test-blog check-links validate

# This Makefile lives in blog/ but operates on the Jekyll site at repo root.
# Run with: cd blog && make <target>

help:
	@echo "Available targets (run from blog/ directory):"
	@echo "  make build       - Build Jekyll site (from repo root)"
	@echo "  make serve       - Start Jekyll development server"
	@echo "  make test        - Run link checker on built site"
	@echo "  make test-blog   - Run blog link checker (no build required)"
	@echo "  make test-build  - Build site then run link checker"
	@echo "  make check-links FILE=../_posts/file.md - Check links in a markdown file"
	@echo "  make validate    - Run all validation checks"
	@echo "  make clean       - Clean Jekyll build artifacts"

build:
	@echo "Building Jekyll site..."
	@cd .. && bundle exec jekyll build

serve:
	@echo "Starting Jekyll development server..."
	@cd .. && bundle exec jekyll serve

test:
	@echo "Running link checker..."
	@../scripts/test_links.sh

test-build: build test

test-python:
	@echo "Running Python link checker..."
	@../scripts/test_links.py --build

clean:
	@echo "Cleaning Jekyll build artifacts..."
	@rm -rf ../_site ../.jekyll-cache ../.sass-cache

test-blog:
	@echo "Running blog link checker..."
	@python3 ../scripts/check_blog_links.py

check-links:
	@if [ -z "$(FILE)" ]; then \
		echo "Usage: make check-links FILE=../_posts/file.md"; \
		exit 1; \
	fi
	@../scripts/check-links.sh $(FILE)

validate: check-links
	@echo "Running all validation checks..."
	@echo "✓ Links validated"
	@echo "✓ Validation complete"
