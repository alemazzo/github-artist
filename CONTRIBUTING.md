# Contributing to GitHub Artist

Thank you for your interest in contributing to GitHub Artist! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
- Git
- UV package manager (recommended) or pip

### Setting Up Development Environment

1. Fork and clone the repository:
```bash
git clone https://github.com/your-username/github-artist.git
cd github-artist
```

2. Install UV (if not already installed):
```bash
pip install uv
```

3. Install the package in development mode:
```bash
uv pip install -e .
```

4. Install development dependencies:
```bash
pip install pytest
```

## 🧪 Running Tests

Run the test suite to ensure everything works:

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_characters.py

# Run with coverage
pytest tests/ --cov=github_artist
```

## 📝 Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep lines under 100 characters when practical
- Use meaningful variable and function names

### Example Function Style

```python
def calculate_something(value: int, option: str = "default") -> dict:
    """
    Brief description of what the function does.
    
    Args:
        value: Description of the value parameter
        option: Description of the option parameter (default: "default")
        
    Returns:
        Dictionary with the results
        
    Raises:
        ValueError: When value is negative
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    
    return {"result": value}
```

## 🎨 Adding New Characters

To add support for new characters:

1. Edit `github_artist/data/characters.py`
2. Add your character matrix to the `CHAR_MATRICES` dictionary
3. Ensure the matrix is exactly 7 rows tall
4. Each cell should be 0 (empty) or 1 (filled)

Example:
```python
"X": [
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
],
```

3. Test your character:
```bash
python -m github_artist.cli preview "X"
```

4. Add tests in `tests/test_characters.py` if appropriate

## 🐛 Bug Reports

When reporting bugs, please include:

- Python version
- Operating system
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Error messages (if any)

Use the GitHub issue template and label the issue as "bug".

## 💡 Feature Requests

For feature requests:

- Check if the feature has already been requested
- Clearly describe the feature and its use case
- Explain why it would be valuable
- Consider providing examples or mockups

Label the issue as "enhancement".

## 🔧 Pull Request Process

1. **Create a branch**: Use a descriptive name
   ```bash
   git checkout -b feature/my-new-feature
   # or
   git checkout -b fix/bug-description
   ```

2. **Make your changes**: 
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**:
   ```bash
   pytest tests/
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   # or
   git commit -m "fix: bug description"
   ```

   Use conventional commit messages:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for adding tests
   - `refactor:` for code refactoring

5. **Push to your fork**:
   ```bash
   git push origin feature/my-new-feature
   ```

6. **Open a Pull Request**:
   - Provide a clear description of the changes
   - Reference any related issues
   - Ensure all tests pass
   - Wait for review

## 📚 Documentation

When adding features:

- Update the README.md if the feature is user-facing
- Add docstrings to new functions and classes
- Update examples if behavior changes
- Consider adding usage examples

## 🎯 Areas for Contribution

Here are some areas where contributions are especially welcome:

### High Priority
- [ ] Additional character designs
- [ ] Improved character matrices for better visibility
- [ ] More emoji support
- [ ] Better error messages

### Medium Priority
- [ ] Performance optimizations
- [ ] Additional output formats
- [ ] Template system for common patterns
- [ ] Interactive mode improvements

### Low Priority
- [ ] Web interface
- [ ] CI/CD improvements
- [ ] Additional documentation
- [ ] More examples

## 🤝 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Personal attacks
- Trolling or insulting comments
- Publishing others' private information
- Other unethical or unprofessional conduct

## 📞 Getting Help

- Open an issue for bugs or features
- Join discussions in existing issues
- Reach out to maintainers for questions

## 🏆 Recognition

Contributors will be:
- Listed in the project's contributors
- Mentioned in release notes for significant contributions
- Credited in the README for major features

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to GitHub Artist! Your efforts help make this project better for everyone. 🎨✨
