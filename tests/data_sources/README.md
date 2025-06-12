# Data Sources Tests

This directory contains tests specific to individual data sources used in the stock advisor application.

## Files

- `test_financedata_reader_comprehensive.py` - Comprehensive tests for FinanceDataReader API
- `test_yahoo_finance.py` - Tests for Yahoo Finance integration (via yfinance)
- `test_stooq.py` - Tests for Stooq data source (via pandas_datareader)
- `test_investpy.py` - Tests for InvestPy data source

## Test Categories

Each data source test file includes:
- Basic connectivity tests
- Data validation tests
- Error handling tests
- API-specific feature tests

## Running Data Source Tests

```bash
# Run all data source tests
pytest tests/data_sources/ -v

# Run specific data source tests
pytest tests/data_sources/test_financedata_reader_comprehensive.py -v

# Run with network dependency awareness
pytest tests/data_sources/ -m "not slow" -v  # Skip slow network tests
```
