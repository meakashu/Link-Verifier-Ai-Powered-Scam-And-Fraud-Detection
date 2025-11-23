# Contributing to AI-Powered Link Verifier

Thank you for your interest in contributing to the AI-Powered Link Verifier project! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Guidelines](#contribution-guidelines)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## 📜 Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow. Please be respectful, inclusive, and professional in all interactions.

## 🚀 Getting Started

1. **Fork the Repository**: Click the "Fork" button on GitHub
2. **Clone Your Fork**: `git clone https://github.com/yourusername/link-verifier.git`
3. **Create a Branch**: `git checkout -b feature/your-feature-name`

## 🛠️ Development Setup

### Prerequisites

- Python 3.7 or higher
- pip package manager
- Git

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/yourusername/link-verifier.git
cd link-verifier

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your API keys
```

## 📝 Contribution Guidelines

### Types of Contributions

We welcome various types of contributions:

- 🐛 **Bug Fixes**: Fix issues and bugs
- ✨ **New Features**: Add new functionality
- 📚 **Documentation**: Improve documentation
- 🎨 **UI/UX Improvements**: Enhance user interface
- ⚡ **Performance**: Optimize code performance
- 🧪 **Tests**: Add or improve tests

### Before You Start

1. Check existing issues and pull requests to avoid duplicates
2. Open an issue first for major changes to discuss the approach
3. For small fixes, feel free to submit a pull request directly

## 🔄 Pull Request Process

### Creating a Pull Request

1. **Update Your Fork**: Keep your fork up to date with the main repository
   ```bash
   git remote add upstream https://github.com/originalowner/link-verifier.git
   git fetch upstream
   git merge upstream/main
   ```

2. **Create Your Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Your Changes**
   - Write clean, readable code
   - Follow coding standards
   - Add tests if applicable
   - Update documentation

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add amazing feature"
   ```
   Use clear, descriptive commit messages following [Conventional Commits](https://www.conventionalcommits.org/).

5. **Push to Your Fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill out the pull request template
   - Submit the pull request

### Pull Request Checklist

- [ ] Code follows the project's style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated (if applicable)
- [ ] All tests pass
- [ ] No merge conflicts
- [ ] Branch is up to date with main

## 💻 Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use meaningful variable and function names
- Add docstrings to functions and classes

### Example

```python
def analyze_url(url: str) -> dict:
    """
    Analyze a URL for potential security threats.
    
    Args:
        url (str): The URL to analyze
        
    Returns:
        dict: Analysis results with verdict and confidence score
    """
    # Implementation here
    pass
```

### JavaScript Style Guide

- Use ES6+ features
- Follow consistent naming conventions (camelCase for variables/functions)
- Add comments for complex logic
- Keep functions small and focused

### Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example:**
```
feat(analyzer): add QR code analysis feature

Add functionality to analyze URLs extracted from QR codes
with enhanced threat detection capabilities.

Closes #123
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=app tests/
```

### Writing Tests

- Write tests for new features
- Ensure tests are independent and repeatable
- Use descriptive test names
- Aim for good test coverage

## 📚 Documentation

### Code Documentation

- Add docstrings to all functions and classes
- Use clear, concise descriptions
- Include parameter and return type information
- Add examples for complex functions

### README Updates

- Update README.md if you add new features
- Keep installation instructions current
- Update usage examples if needed

## 🐛 Reporting Bugs

### Before Submitting a Bug Report

1. Check if the bug has already been reported
2. Try to reproduce the bug
3. Check if it's a known issue

### Bug Report Template

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
A clear description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
- OS: [e.g., macOS 12.0]
- Python version: [e.g., 3.9.0]
- Browser: [e.g., Chrome 95]

**Additional context**
Add any other context about the problem here.
```

## ✨ Suggesting Features

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
A description of alternative solutions or features.

**Additional context**
Add any other context or screenshots about the feature request.
```

## 📞 Getting Help

If you need help or have questions:

- Open an issue with the `question` label
- Check existing documentation
- Review closed issues and pull requests
- Contact the maintainer: [meakash22dotin@gmail.com](mailto:meakash22dotin@gmail.com)

## 👨‍💻 Project Maintainer

**Akash Kumar Singh**

- 📧 Email: [meakash22dotin@gmail.com](mailto:meakash22dotin@gmail.com)
- 🌐 GitHub: [@akashkumarsingh](https://github.com/akashkumarsingh)
- 📅 Copyright: © 2025 Akash Kumar Singh. All rights reserved.

## 🙏 Thank You

Thank you for contributing to the AI-Powered Link Verifier project! Your contributions help make this tool better for everyone.

---

**Remember**: All contributions are welcome, no matter how small. Every contribution makes a difference!

