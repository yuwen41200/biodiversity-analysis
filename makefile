# Makefile for Sphinx documentation

.PHONY: all
all: docs

.PHONY: docs
docs:
	sphinx-build -b html . docs

.PHONY: rebuild
rebuild:
	rm -rf docs/*
	sphinx-build -b html . docs

.PHONY: clean
clean:
	find . -name '*.py[co]' -delete
	find . -name '__pycache__' -delete
