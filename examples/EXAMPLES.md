# GitHub Artist Examples

This directory contains examples of how to use GitHub Artist.

## Quick Examples

### 1. Preview Your Art

Before creating commits, always preview your art:

```bash
# Simple preview
github-artist preview "HELLO"

# Preview with custom spacing
github-artist preview "CODE" --spacing 2

# Preview with more commits per day (darker squares)
github-artist preview "2024" --commits 5
```

### 2. Create Simple Art

```bash
# Basic usage - creates art with auto-calculated start date
github-artist create myusername my-art-repo "HELLO"

# Skip the confirmation prompt
github-artist create myusername my-art-repo "CODE" --yes
```

### 3. Custom Start Date

```bash
# Start on a specific Sunday (always use Sundays for alignment)
github-artist create myusername my-art-repo "2024" --start-date 2024-01-07

# Start 2 weeks from now instead of default 1 week
github-artist create myusername my-art-repo "HI" --weeks-advance 2
```

### 4. Customize Appearance

```bash
# Add more spacing between letters for readability
github-artist create myusername my-art-repo "WORLD" --spacing 2

# Make darker contributions with more commits per day
github-artist create myusername my-art-repo "STAR" --commits 5

# Combine options
github-artist create myusername my-art-repo "CODE 2024" --spacing 2 --commits 3
```

### 5. Preview Only Mode

```bash
# See what it looks like without creating any commits
github-artist create myusername my-art-repo "TEST" --preview
```

### 6. Working with SSH

```bash
# Use SSH protocol instead of HTTPS
github-artist create myusername my-art-repo "HELLO" --protocol ssh
```

### 7. Manual Push Control

```bash
# Create commits but don't push automatically
github-artist create myusername my-art-repo "CODE" --no-push

# Then you can manually review and push:
# cd my-art-repo && git log && git push
```

## Complete Workflow Examples

### Example 1: Creating Your Name

```bash
# 1. Preview your name first
github-artist preview "JOHN"

# 2. Create with good spacing
github-artist create johndoe name-art "JOHN" --spacing 2 --commits 3 --yes
```

### Example 2: Show Your Code Pride

```bash
# 1. Preview
github-artist preview "I ❤ CODE"

# 2. Create
github-artist create developer code-love "I ❤ CODE" --spacing 1 --commits 4
```

### Example 3: Year Display

```bash
# Display the year starting on New Year's Day (find next Sunday)
github-artist preview "2024"

# Create with darker commits
github-artist create myusername year-2024 "2024" --commits 5 --spacing 2
```

### Example 4: Professional Greeting

```bash
# Preview a professional greeting
github-artist preview "Hello World!" --spacing 2

# Create it
github-artist create developer hello-world "Hello World!" --spacing 2 --commits 2
```

## Configuration File Usage

### Create a Configuration File

```bash
# Generate example configuration
github-artist config --example --output my-config.json
```

Edit `my-config.json`:

```json
{
  "username": "myusername",
  "repo_name": "github-art",
  "protocol": "https",
  "text": "HELLO",
  "letter_spacing": 2,
  "commits_per_day": 3,
  "start_date": null,
  "auto_calculate_start": true,
  "weeks_in_advance": 1,
  "preview_only": false,
  "auto_push": true
}
```

## Character Support Examples

### Using Different Character Sets

```bash
# Uppercase letters
github-artist preview "GITHUB"

# Lowercase letters
github-artist preview "github"

# Mixed case
github-artist preview "GitHub"

# Numbers
github-artist preview "2024"

# Special characters
github-artist preview "Hello!"

# Symbols
github-artist preview "CODE ★"

# Hearts
github-artist preview "I ❤ CODE"
```

## Tips and Best Practices

### 1. Always Preview First

```bash
github-artist preview "YOUR TEXT" --spacing 2
```

### 2. Start on Sundays

The tool automatically calculates Sunday start dates for perfect alignment:

```bash
# Auto-calculated Sunday start
github-artist create user repo "TEXT"

# Or specify a Sunday manually
github-artist create user repo "TEXT" --start-date 2024-01-07
```

### 3. Adjust Spacing for Readability

```bash
# Default spacing (1)
github-artist preview "COMPACT"

# More spacing for longer text
github-artist preview "READABLE" --spacing 2

# Even more for very long text
github-artist preview "SPACIOUS" --spacing 3
```

### 4. Control Contribution Intensity

```bash
# Light (1 commit per day)
github-artist create user repo "LIGHT" --commits 1

# Medium (3 commits per day)
github-artist create user repo "MEDIUM" --commits 3

# Dark (5 commits per day)
github-artist create user repo "DARK" --commits 5
```

### 5. Use Dedicated Repositories

Create separate repositories for each art piece:

```bash
github-artist create myuser hello-art "HELLO"
github-artist create myuser year-art "2024"
github-artist create myuser name-art "JOHN"
```

## Troubleshooting

### Issue: Start date not on Sunday

**Solution**: Use auto-calculate or specify a Sunday:

```bash
# Let it auto-calculate
github-artist create user repo "TEXT"

# Or specify a Sunday
github-artist create user repo "TEXT" --start-date 2024-01-07
```

### Issue: Art doesn't show on profile

**Solution**: Make sure:
1. Repository is public
2. Commits were pushed (`--no-push` wasn't used)
3. Commits are within the last year
4. Your GitHub profile is public

### Issue: Art looks wrong

**Solution**: Always preview first:

```bash
github-artist preview "YOUR TEXT" --spacing 2
```

## Advanced Examples

### Scripted Creation

Create a script to generate multiple art pieces:

```bash
#!/bin/bash

# Create multiple art pieces
github-artist create myuser art-2024 "2024" --yes
sleep 1
github-artist create myuser art-code "CODE" --spacing 2 --yes
sleep 1
github-artist create myuser art-star "★" --commits 5 --yes
```

### Preview Multiple Options

```bash
#!/bin/bash

# Preview different spacing options
echo "Spacing 1:"
github-artist preview "CODE" --spacing 1

echo -e "\n\nSpacing 2:"
github-artist preview "CODE" --spacing 2

echo -e "\n\nSpacing 3:"
github-artist preview "CODE" --spacing 3
```

## More Help

- Run `github-artist --help` for command overview
- Run `github-artist <command> --help` for specific command help
- Run `github-artist chars` to see supported characters
- Check the [main README](../README.md) for full documentation
