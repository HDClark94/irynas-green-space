# Entry points for working on this site.
#
#   make art      regenerate the leaf artwork
#   make serve    run the site locally
#   make format   apply the formatting the CI check enforces
#
# Generated artwork is committed, so you only need `make art` when changing how
# it looks. See scripts/README.md.

PYTHON ?= python3

.PHONY: help art photos serve build format check check-products clean

help:
	@grep -E '^[a-z-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-8s\033[0m %s\n", $$1, $$2}'

art: ## Regenerate banner, logo, favicon and offering tiles
	$(PYTHON) scripts/artwork.py

photos: ## Rebuild responsive WebP variants for photographs in assets/img/
	$(PYTHON) scripts/photos.py

serve: ## Serve locally at http://localhost:4000 (needs Ruby 3.x + ImageMagick)
	bundle exec jekyll serve --livereload

build: ## Production build into _site
	JEKYLL_ENV=production bundle exec jekyll build

format: ## Apply Prettier formatting (CI enforces this)
	npx prettier . --write

check: check-products ## Everything CI runs: formatting and price integrity
	npx prettier . --check

check-products: ## Verify every cost breakdown sums to its price
	$(PYTHON) scripts/check_products.py

clean: ## Remove build output and local raster previews
	rm -rf _site .jekyll-cache
	rm -f assets/img/*.png assets/img/offerings/*.png
