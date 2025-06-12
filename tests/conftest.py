"""
Shared test fixtures and utilities for the stock advisor test suite.
"""
import pytest
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the path to import main functions
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def process_data(data: pd.DataFrame) -> pd.DataFrame:
    """Sort by date so the last row reflects the latest close."""
    data.reset_index(inplace=True)
    data.sort_values("Date", inplace=True)
    data.reset_index(drop=True, inplace=True)
    return data


@pytest.fixture
def sample_stock_data():
    """Create sample stock data for testing."""
    dates = pd.date_range('2020-01-01', periods=100, freq='D')
    data = pd.DataFrame({
        'Date': dates,
        'Open': 100 + (pd.Series(range(100)) * 0.1) + (pd.Series(range(100)).apply(lambda x: x % 5)),
        'High': 102 + (pd.Series(range(100)) * 0.1) + (pd.Series(range(100)).apply(lambda x: x % 5)),
        'Low': 98 + (pd.Series(range(100)) * 0.1) + (pd.Series(range(100)).apply(lambda x: x % 5)),
        'Close': 100 + (pd.Series(range(100)) * 0.1),
        'Volume': 1000000 + (pd.Series(range(100)) * 10000),
        'Adj Close': 100 + (pd.Series(range(100)) * 0.1)
    })
    return data


@pytest.fixture
def valid_symbols():
    """List of valid stock symbols for testing."""
    return ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]


@pytest.fixture
def invalid_symbols():
    """List of invalid stock symbols for testing."""
    return ["INVALID123", "NOTREAL", "XYZ999", ""]


class TestDataValidator:
    """Utility class for validating stock data quality."""
    
    @staticmethod
    def validate_stock_data_structure(data: pd.DataFrame) -> bool:
        """Validate that the DataFrame has the required structure for stock data."""
        required_columns = ['Date', 'Open', 'High', 'Low', 'Close']
        
        if not isinstance(data, pd.DataFrame):
            return False
            
        if data.empty:
            return False
            
        for col in required_columns:
            if col not in data.columns:
                return False
                
        return True
    
    @staticmethod
    def validate_price_data(data: pd.DataFrame) -> bool:
        """Validate that price data makes sense (positive values, High >= Low, etc.)."""
        if not TestDataValidator.validate_stock_data_structure(data):
            return False
            
        # Check for positive prices
        price_columns = ['Open', 'High', 'Low', 'Close']
        for col in price_columns:
            if (data[col] <= 0).any():
                return False
                
        # Check that High >= Low
        if (data['High'] < data['Low']).any():
            return False
            
        return True
    
    @staticmethod
    def validate_date_range(data: pd.DataFrame, min_year: int = 2000) -> bool:
        """Validate that the data covers a reasonable date range."""
        if not TestDataValidator.validate_stock_data_structure(data):
            return False
            
        try:
            dates = pd.to_datetime(data['Date'])
            min_date = dates.min()
            max_date = dates.max()
            
            # Check that dates are in reasonable range
            if min_date.year < min_year:
                return False
                
            if max_date > datetime.now():
                return False
                
            # Check that dates are sorted
            if not dates.is_monotonic_increasing:
                return False
                
            return True
            
        except Exception:
            return False


@pytest.fixture
def data_validator():
    """Provide a data validator instance."""
    return TestDataValidator()


# Test markers for organization
pytest_plugins = []


def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests for individual components"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests for data source fallbacks"
    )
    config.addinivalue_line(
        "markers", "smoke: Quick smoke tests for basic functionality"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that may take longer to run (network dependent)"
    )
    config.addinivalue_line(
        "markers", "data_source: Tests specific to data source functionality"
    )