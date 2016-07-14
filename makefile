# Makefile for Sphinx documentation

.PHONY: all
all: docs

.PHONY: docs
docs:
	sphinx-build -b html . docs

.PHONY: clean
clean:
	rm -rf docs/*
