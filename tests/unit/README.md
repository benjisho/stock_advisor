# Unit Tests

This directory contains unit tests for individual components and functions.

## Files

- `test_indicators.py` - Tests for technical indicators
- `test_strategy.py` - Tests for stock strategy logic
- `test_data_processing.py` - Tests for data processing functions

## Test Categories

Unit tests include:
- Individual function testing
- Component isolation tests
- Edge case validation
- Input/output validation

## Running Unit Tests

```bash
# Run all unit tests (fast)
pytest tests/unit/ -v

# Run specific unit test file
pytest tests/unit/test_indicators.py -v

# Run with coverage
pytest tests/unit/ --cov=indicators --cov=strategy -v
```
