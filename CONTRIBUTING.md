# Contributing to Punch-Out AI Agent

Thank you for your interest in contributing! This project welcomes contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, emulator version, Python version)
- Screenshots or logs if applicable

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:
- Clear description of the feature
- Use case / motivation
- Potential implementation approach
- Any relevant examples

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**: `git commit -m "Add feature: description"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Open a Pull Request**

## Development Guidelines

### Code Style

**Python:**
- Follow PEP 8 style guide
- Use type hints where appropriate
- Include docstrings for classes and functions
- Keep functions focused and single-purpose

**Lua:**
- Use consistent indentation (2 or 4 spaces)
- Comment complex logic
- Keep functions modular
- Use descriptive variable names

### Testing

- Add unit tests for new Python features
- Test with actual emulator when possible
- Verify against multiple opponents
- Check performance impact

### Documentation

- Update README.md for user-facing changes
- Add technical details to ARCHITECTURE.md
- Include code comments for complex algorithms
- Update SETUP.md for configuration changes

## Areas for Contribution

### Easy (Good First Issues)

- [ ] Add support for more NES emulators
- [ ] Improve debug visualization
- [ ] Add more opponent patterns to config
- [ ] Write additional unit tests
- [ ] Improve documentation with examples
- [ ] Create video tutorials

### Medium

- [ ] Implement pattern learning persistence (save/load)
- [ ] Add data collection for training ML models
- [ ] Create performance benchmarking tools
- [ ] Implement replay analysis system
- [ ] Add support for other Punch-Out versions
- [ ] Build configuration GUI

### Advanced

- [ ] Implement machine learning decision engine
- [ ] Add real-time Lua ↔ Python communication
- [ ] Create visual pattern recognition (screen capture)
- [ ] Implement Q-learning or policy gradients
- [ ] Build TAS-level frame-perfect timing
- [ ] Create multi-fight tournament system

## Project Structure

```
Punch-Out_Agent/
├── lua/              # Emulator interface scripts
├── python/           # AI logic and algorithms
├── config/           # Configuration files
├── docs/             # Documentation
├── examples.py       # Usage examples
└── requirements.txt  # Python dependencies
```

## Testing Your Changes

### Python Tests
```bash
python python/test_punchout_ai.py
```

### Lua Syntax Check
```bash
luac -p lua/punchout_agent.lua
```

### Integration Test
1. Load ROM in emulator
2. Run modified Lua script
3. Test against multiple opponents
4. Verify expected behavior

## Code Review Process

All contributions go through code review:
1. Automated tests must pass
2. Code style must be consistent
3. Documentation must be updated
4. Changes must be tested
5. At least one maintainer approval required

## Community Guidelines

- Be respectful and constructive
- Help others learn
- Share knowledge and insights
- Give credit where due
- Follow the Code of Conduct

## Research and Academic Use

This project is designed for educational purposes:
- Cite this repository if used in research
- Share your findings with the community
- Contribute back improvements
- Respect game copyrights

## Questions?

- Open a GitHub issue for technical questions
- Start a discussion for general questions
- Check existing issues first

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Attribution

Contributors will be acknowledged in:
- Git commit history
- GitHub contributors page
- Release notes for significant contributions

## Thanks!

Every contribution, no matter how small, helps make this project better. We appreciate your time and effort!

---

**Happy Coding! 🥊**
