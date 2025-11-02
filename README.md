# GitHub Artist 🎨

Create beautiful art in your GitHub contribution graph! Turn your commit history into ASCII art that displays on your GitHub profile.

![GitHub Artist Banner](https://img.shields.io/badge/GitHub-Artist-success)
![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- 🎨 **Create ASCII art** in your GitHub contribution graph
- 📅 **Automatic date calculation** - finds optimal starting points (Sundays for alignment)
- 👀 **Live preview** - see what your art will look like before creating commits
- 🔤 **Extended character set** - supports uppercase, lowercase, numbers, and special characters
- 💪 **Flexible configuration** - customize spacing, commits per day, and more
- 🚀 **Modern tooling** - uses UV package manager for fast, reliable dependency management
- 📊 **Calendar view** - visualize your commit pattern week by week
- 🎯 **Smart alignment** - automatically aligns with GitHub's contribution grid

## 📦 Installation

### Using UV (Recommended)

```bash
# Install UV if you haven't already
pip install uv

# Clone the repository
git clone https://github.com/alemazzo/github-artist.git
cd github-artist

# Install the package
uv pip install -e .
```

### Using pip

```bash
git clone https://github.com/alemazzo/github-artist.git
cd github-artist
pip install -e .
```

## 🚀 Quick Start

### Preview your art

```bash
# Preview text before creating commits
github-artist preview "HELLO"
```

### Create your art

```bash
# Create art in your GitHub contribution graph
github-artist create your-username your-repo "HELLO"
```

### Show supported characters

```bash
# List all supported characters
github-artist chars

# Show preview of all characters
github-artist chars --show-all
```

## 📖 Usage Guide

### Basic Usage

The simplest way to create GitHub art:

```bash
github-artist create <username> <repo> <text>
```

Example:
```bash
github-artist create alemazzo my-art-repo "CODE"
```

### Advanced Usage

Customize your art with various options:

```bash
github-artist create alemazzo my-art-repo "HELLO" \
  --start-date 2024-01-01 \
  --spacing 2 \
  --commits 3 \
  --protocol ssh \
  --yes
```

### Command Reference

#### `create` - Create GitHub art

```bash
github-artist create <username> <repo> <text> [OPTIONS]
```

**Arguments:**
- `username` - Your GitHub username
- `repo` - Repository name (will be cloned if it doesn't exist)
- `text` - Text to create in the contribution graph

**Options:**
- `--start-date YYYY-MM-DD` - Start date (default: auto-calculated to next Sunday)
- `--spacing N` - Space between letters (default: 1)
- `--commits N` - Number of commits per day (default: 1, more commits = darker squares)
- `--weeks-advance N` - Start N weeks from now when auto-calculating (default: 1)
- `--protocol {https,ssh}` - Clone protocol (default: https)
- `--preview` - Preview only, don't create commits
- `--no-push` - Create commits but don't push to GitHub
- `-y, --yes` - Skip confirmation prompt

**Examples:**

```bash
# Basic usage with auto-calculated start date
github-artist create myusername github-art "HELLO"

# Start on a specific date
github-artist create myusername github-art "2024" --start-date 2024-01-07

# More spacing between letters for better readability
github-artist create myusername github-art "CODE" --spacing 2

# Make darker contributions with more commits per day
github-artist create myusername github-art "HI" --commits 5

# Preview before creating
github-artist create myusername github-art "TEST" --preview

# Skip confirmation prompt (useful for automation)
github-artist create myusername github-art "AUTO" --yes
```

#### `preview` - Preview your art

```bash
github-artist preview <text> [OPTIONS]
```

**Arguments:**
- `text` - Text to preview

**Options:**
- `--start-date YYYY-MM-DD` - Start date for preview
- `--spacing N` - Letter spacing
- `--commits N` - Commits per day
- `--weeks-advance N` - Weeks in advance

**Examples:**

```bash
# Simple preview
github-artist preview "HELLO WORLD"

# Preview with custom spacing
github-artist preview "CODE" --spacing 2

# Preview with specific start date
github-artist preview "2024" --start-date 2024-01-07
```

#### `chars` - Show supported characters

```bash
github-artist chars [OPTIONS]
```

**Options:**
- `--show-all` - Show visual preview of all characters

**Examples:**

```bash
# List supported characters
github-artist chars

# Show preview of each character
github-artist chars --show-all
```

## 🎨 Supported Characters

GitHub Artist supports:

- **Uppercase letters**: A-Z
- **Lowercase letters**: a-z
- **Numbers**: 0-9
- **Special characters**: . , ! ? - _ + = : ; ' " ( ) [ ] / \ @ # & < >
- **Symbols**: ❤ ★

Use `github-artist chars` to see the complete list!

## 📋 Examples

### Example 1: Create a simple greeting

```bash
github-artist create myusername greeting-repo "HELLO"
```

Output preview:
```
█  █ █████ █   █   █████
█  █ █     █   █   █   █
████ ████  █   █   █   █
█  █ █     █   █   █   █
█  █ █████ █████   █████
```

### Example 2: Show your code spirit

```bash
github-artist create myusername code-art "CODE" --spacing 2 --commits 3
```

### Example 3: Display the current year

```bash
github-artist create myusername year-2024 "2024" --start-date 2024-01-07
```

### Example 4: Create with lowercase for a different style

```bash
github-artist create myusername lowercase-art "hello world" --spacing 1
```

## 🔧 Configuration

### Using Configuration Files

Create a configuration file for reusable settings:

```bash
github-artist config --example
```

This creates `github-artist-config.json`:

```json
{
  "username": "your-username",
  "repo_name": "github-art",
  "protocol": "https",
  "text": "HELLO",
  "letter_spacing": 1,
  "commits_per_day": 1,
  "auto_calculate_start": true,
  "weeks_in_advance": 1,
  "preview_only": false,
  "auto_push": false
}
```

## 🎯 Best Practices

1. **Start on Sundays**: The auto-calculated start date always picks a Sunday for perfect alignment with GitHub's weekly grid.

2. **Preview first**: Always use `github-artist preview` to see how your art will look.

3. **Letter spacing**: Use `--spacing 2` for better readability with longer text.

4. **Commits per day**: Higher values (3-5) create darker squares, making the art more visible.

5. **Repository setup**: Create a dedicated repository for your GitHub art to keep it separate from your code projects.

## 📊 How It Works

1. **Character Matrix**: Each character is defined as a 7x4 (or similar) binary matrix
2. **Date Calculation**: Maps the matrix to dates, column by column (each column = 1 week)
3. **Commit Creation**: Creates commits with backdated timestamps for each active cell
4. **GitHub Display**: GitHub's contribution graph shows the commits as colored squares

## 🛠️ Development

### Project Structure

```
github-artist/
├── github_artist/           # Main package
│   ├── __init__.py
│   ├── cli.py              # Command-line interface
│   ├── core/               # Core functionality
│   │   ├── config.py       # Configuration management
│   │   ├── git_ops.py      # Git operations
│   │   └── preview.py      # Preview and visualization
│   ├── data/               # Data files
│   │   └── characters.py   # Character matrix definitions
│   └── utils/              # Utility modules
│       └── dates.py        # Date calculations
├── main.py                 # Entry point
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

### Running Tests

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest
```

### Adding New Characters

Edit `github_artist/data/characters.py` and add your character matrix to `CHAR_MATRICES`:

```python
"X": [
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0],
    [0, 0, 0, 0],
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
],
```

## ⚠️ Important Notes

- **GitHub limits**: GitHub's contribution graph shows the last year of contributions
- **Existing commits**: This tool creates new commits and won't affect your existing work
- **Repository**: Use a dedicated repository for art to avoid cluttering your code projects
- **Visibility**: Make sure your repository is public for the art to show on your profile
- **Time zones**: Commits are created with your local timezone

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Contribution

- Add more character matrices
- Improve character designs
- Add emoji support
- Create themes/templates
- Improve documentation
- Write tests

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**alemazzo**

- GitHub: [@alemazzo](https://github.com/alemazzo)

## 🌟 Acknowledgments

- Inspired by the GitHub contribution graph
- Built with ❤️ and Python
- Powered by UV package manager

## 📞 Support

- 🐛 [Report a bug](https://github.com/alemazzo/github-artist/issues)
- 💡 [Request a feature](https://github.com/alemazzo/github-artist/issues)
- 📖 [Documentation](https://github.com/alemazzo/github-artist)

---

**Happy Drawing! 🎨**

Made with ❤️ by the GitHub community