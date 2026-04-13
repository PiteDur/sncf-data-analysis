# Contributing to SNCF Railway Network Analysis

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a branch** for your feature: `git checkout -b feature/your-feature-name`
4. **Make your changes** and test them
5. **Commit your changes**: `git commit -am 'Add your message'`
6. **Push to your branch**: `git push origin feature/your-feature-name`
7. **Create a Pull Request** describing your changes

## Development Setup

```bash
# Clone repository
git clone https://github.com/[your-username]/sncf-railway-analysis.git
cd sncf-railway-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd code/
pip install -r requirements.txt
```

## Running Tests & Validation

```bash
# Run the analysis pipeline
python main_fast.py

# Verify outputs
ls *.html  # Should see map files
ls plots/  # Should see PNG plots
```

## Code Style Guidelines

- **Python**: Follow PEP 8 style guide
- **Comments**: Use clear, descriptive comments
- **Docstrings**: Use docstrings for functions and classes
- **Naming**: Use descriptive variable names
- **Line length**: Keep lines to ~80 characters

### Example:
```python
def analyze_delays(data_df, min_delay_minutes=5):
    """
    Analyze train delays in the dataset.
    
    Parameters
    ----------
    data_df : pd.DataFrame
        Delay data with columns: delay_minutes, train_type, etc.
    min_delay_minutes : int
        Minimum delay duration to consider (default: 5)
    
    Returns
    -------
    dict
        Analysis results with statistics
    """
    pass
```

## Pull Request Process

1. **Update documentation** if you add new features
2. **Include a description** of what your PR does
3. **Reference related issues** (e.g., "Fixes #123")
4. **Add examples** if adding new functionality
5. **Test your changes** with the pipeline

## Types of Contributions

### Code Improvements
- Bug fixes
- Performance optimization
- New analysis features
- Code refactoring

### Data Enhancements
- Additional railway data sources
- Improved data quality checks
- New data validations

### Documentation
- Clarifying existing docs
- Adding examples
- Fixing typos
- Adding tutorials

### Visualizations
- New map types
- Additional plots
- Interactive dashboards
- Real-time monitoring

## Areas for Contribution

### High Priority
- [ ] Real-time delay data integration
- [ ] Predictive delay models (ML)
- [ ] Cascade failure analysis
- [ ] Performance optimization for large datasets

### Medium Priority
- [ ] Additional visualization types
- [ ] Web dashboard (Flask/Streamlit)
- [ ] API development
- [ ] Database integration

### Low Priority
- [ ] Code documentation improvements
- [ ] Unit test coverage
- [ ] Type hints (Python 3.9+)
- [ ] Example notebooks

## Reporting Issues

When reporting bugs, please include:

1. **Python version** and **environment** (Windows/Linux/Mac)
2. **Steps to reproduce** the issue
3. **Expected behavior**
4. **Actual behavior**
5. **Error message** (if any)
6. **Screenshot** (if applicable)

### Example Issue:
```
**Title:** Network map takes too long to generate

**Description:**
When running main_fast.py on large datasets, the map generation 
takes excessive time.

**Steps to Reproduce:**
1. Run `python main_fast.py`
2. Wait for "Creating network map..." step
3. It takes 10+ minutes

**Expected:** Should complete in < 2 minutes

**Environment:**
- Python 3.10.16
- Windows 10
- 16GB RAM
```

## Commit Message Guidelines

- **Be descriptive**: Explain what and why, not just what
- **Use present tense**: "Add feature" not "Added feature"
- **Start with verb**: "Fix", "Add", "Improve", "Refactor", etc.
- **Keep it concise**: < 72 characters for subject line

### Examples:
```
✓ Add delay propagation analysis
✓ Fix probability distribution normalization
✓ Improve map rendering performance
✗ stuff
✗ fixed
```

## Documentation Standards

- All **public functions** should have docstrings
- Include **parameter descriptions** with types
- Provide **return value descriptions**
- Add **usage examples** where appropriate
- Document **edge cases**

## Testing Your Changes

Before submitting a PR:

```bash
# Check Python syntax
python -m py_compile code/your_file.py

# Run the pipeline
cd code/
python main_fast.py

# Verify outputs exist
ls -la *.html
ls -la ../data/synthetic/
```

## Questions?

- **Documentation**: Check README.md, DATA_DICTIONARY.md
- **Examples**: See QUICK_START.md
- **Code**: Review existing Python files for patterns
- **Issues**: Check existing GitHub issues

## Community

- Be respectful and helpful to all contributors
- Constructive feedback only
- Celebrate contributions!

## License

By contributing to this project, you agree that your contributions will be
licensed under the MIT License.

---

**Thank you for contributing!** 🚄
