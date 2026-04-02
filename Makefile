.PHONY: help test test-links build serve clean test-blog

help:
	@echo "Available targets:"
	@echo "  make build       - Build Jekyll site"
	@echo "  make serve       - Start Jekyll development server"
	@echo "  make test        - Run link checker on built site"
	@echo "  make test-blog   - Run blog link checker (no build required)"
	@echo "  make test-build  - Build site then run link checker"
	@echo "  make clean       - Clean Jekyll build artifacts"

build:
	@echo "Building Jekyll site..."
	@bundle exec jekyll build

serve:
	@echo "Starting Jekyll development server..."
	@bundle exec jekyll serve

test:
	@echo "Running link checker..."
	@./scripts/test_links.sh

test-build: build test

test-python:
	@echo "Running Python link checker..."
	@./scripts/test_links.py --build

clean:
	@echo "Cleaning Jekyll build artifacts..."
	@rm -rf _site .jekyll-cache .sass-cache

test-blog:
	@echo "Running blog link checker..."
	@python3 scripts/check_blog_links.py
