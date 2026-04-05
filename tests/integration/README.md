# Integration Tests

This directory contains integration tests that test the interaction between multiple components or external systems.

## Files

- `test_data_sources.py` - Tests for data source fallback mechanisms
- `test_comprehensive_data_sources.py` - Comprehensive integration tests for all data sources

## Test Categories

Integration tests include:
- Data source fallback chain testing
- End-to-end workflow validation
- Cross-component interaction tests
- System behavior under failure conditions

## Running Integration Tests

```bash
# Run all integration tests
pytest tests/integration/ -v

# Run integration tests without slow network tests
pytest tests/integration/ -m "integration and not slow" -v

# Run with specific markers
pytest tests/integration/ -m "data_source" -v
```
