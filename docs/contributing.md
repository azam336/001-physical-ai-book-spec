---
sidebar_position: 11
title: Contributing
description: Guidelines for contributing to the Physical AI book
keywords: [contributing, guidelines, pull request, open source]
---

# Contributing

Thank you for your interest in contributing to **Introduction to Physical AI**! This guide will help you get started.

## Ways to Contribute

### For Everyone

| Contribution Type | Description | Difficulty |
|-------------------|-------------|------------|
| Report typos | Fix spelling or grammar errors | Easy |
| Improve clarity | Suggest clearer explanations | Easy |
| Ask questions | Help identify confusing content | Easy |
| Share projects | Showcase what you've built | Easy |

### For Developers

| Contribution Type | Description | Difficulty |
|-------------------|-------------|------------|
| Fix bugs | Correct errors in code examples | Medium |
| Add examples | Create new code demonstrations | Medium |
| Improve tests | Expand test coverage | Medium |
| Add diagrams | Create visual explanations | Medium |

### For Experts

| Contribution Type | Description | Difficulty |
|-------------------|-------------|------------|
| Write content | Author new sections or exercises | Hard |
| Review PRs | Provide technical review | Hard |
| Translate | Help localize the book | Hard |

---

## Getting Started

### 1. Set Up Your Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR-USERNAME/physical-ai-book.git
cd physical-ai-book

# Install dependencies
npm install

# Start development server
npm run start
```

### 2. Find Something to Work On

- Check [issues labeled `good first issue`](https://github.com/physical-ai-book/physical-ai-book/labels/good%20first%20issue)
- Look at [issues labeled `help wanted`](https://github.com/physical-ai-book/physical-ai-book/labels/help%20wanted)
- Review the [project board](https://github.com/physical-ai-book/physical-ai-book/projects) for priorities

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-fix-name
```

---

## Content Guidelines

### Writing Style

- **Be concise**: Use simple, clear language
- **Be practical**: Include working code examples
- **Be inclusive**: Avoid jargon without explanation
- **Be encouraging**: Help readers build confidence

### Code Examples

All code examples must:

1. **Run successfully** on supported platforms (Windows 10+, Linux Ubuntu 20.04+)
2. **Include comments** explaining key concepts
3. **Follow PEP 8** style guidelines
4. **Have tests** in the `code-examples/tests/` directory

Example format:

```python
"""
Brief description of what this example demonstrates.
"""
import pybullet as p
import pybullet_data

# Connect to physics simulation
physics_client = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Load the ground plane
plane_id = p.loadURDF("plane.urdf")

# Your example code here
# ...

# Clean up
p.disconnect()
```

### Markdown Formatting

- Use ATX-style headers (`#`, `##`, `###`)
- Include frontmatter with `title`, `description`, and `keywords`
- Add alt text to all images
- Use fenced code blocks with language identifiers

---

## Pull Request Process

### Before Submitting

1. **Test locally**: Run `npm run build` to verify no errors
2. **Run code tests**: Execute `pytest code-examples/tests/`
3. **Check formatting**: Ensure consistent style
4. **Update documentation**: If your change affects usage

### Submitting Your PR

1. Push your branch to your fork
2. Open a pull request against `main`
3. Fill out the PR template completely
4. Link any related issues

### PR Template

```markdown
## Description
[Brief description of changes]

## Type of Change
- [ ] Bug fix
- [ ] New content
- [ ] Code example improvement
- [ ] Documentation update

## Checklist
- [ ] I have tested my changes locally
- [ ] Code examples run without errors
- [ ] Tests pass
- [ ] I have updated relevant documentation

## Related Issues
Closes #[issue number]
```

### Review Process

1. A maintainer will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged
4. You'll be added to CONTRIBUTORS.md

---

## Code of Conduct

We are committed to providing a welcoming environment. Please:

- Be respectful and constructive
- Focus on the work, not the person
- Accept feedback gracefully
- Help others learn

See our full [Code of Conduct](https://github.com/physical-ai-book/physical-ai-book/blob/main/CODE_OF_CONDUCT.md).

---

## Development Setup

### Prerequisites

- **Node.js 18+** for Docusaurus
- **Python 3.9+** for code examples
- **Git** for version control

### Project Structure

```
physical-ai-book/
├── docs/                    # Book content (Markdown)
│   ├── chapter-01-*.md
│   ├── chapter-02-*.md
│   ├── chapter-03-*.md
│   ├── chapter-04-*.md
│   ├── chapter-05-*.md
│   ├── glossary.md
│   ├── contributing.md
│   └── resources/
├── code-examples/           # Python examples
│   ├── chapter-01/
│   ├── chapter-02/
│   ├── chapter-03/
│   ├── chapter-04/
│   ├── chapter-05/
│   └── tests/
├── static/                  # Images and assets
├── src/                     # Docusaurus customizations
├── docusaurus.config.js     # Site configuration
└── sidebars.js              # Navigation structure
```

### Useful Commands

```bash
# Start development server
npm run start

# Build for production
npm run build

# Run Python tests
pytest code-examples/tests/

# Check for broken links
npm run build && npm run serve
```

---

## Questions?

- Open a [discussion](https://github.com/physical-ai-book/physical-ai-book/discussions)
- Check the [troubleshooting guide](./resources/troubleshooting)
- Review existing [issues](https://github.com/physical-ai-book/physical-ai-book/issues)

Thank you for helping make Physical AI education accessible to everyone!
