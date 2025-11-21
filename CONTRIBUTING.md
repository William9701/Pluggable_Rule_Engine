# Contributing to Pluggable Rule Engine

First off, thank you for considering contributing to the Pluggable Rule Engine! It's people like you that make this project such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots if possible**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and explain which behavior you expected to see instead**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Include screenshots and animated GIFs in your pull request whenever possible
* Follow the Python/Django style guides
* Include thoughtfully-worded, well-structured tests
* Document new code based on the Django Documentation Style Guide
* End all files with a newline

## Development Setup

1. Fork the repo
2. Clone your fork
3. Create a virtual environment
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Run tests: `python manage.py test`

## Style Guidelines

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Python Style Guide

* Follow PEP 8
* Use meaningful variable names
* Add docstrings to all functions, classes, and modules
* Keep functions small and focused
* Use type hints where possible

### Django Style Guide

* Follow Django's coding style
* Use Django's built-in features when possible
* Write tests for all new features
* Ensure migrations are clean and atomic

## Testing

* Write unit tests for all new features
* Ensure all tests pass before submitting PR
* Aim for high test coverage (>90%)
* Test edge cases and error conditions

## Documentation

* Update README.md if needed
* Add docstrings to new functions/classes
* Update API documentation if endpoints change
* Include inline comments for complex logic

Thank you for contributing! 🎉
