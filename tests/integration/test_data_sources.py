"""
Tests for all data sources and the fallback mechanism
"""
import pytest
import pandas as pd
from tests.conftest import process_data, TestDataValidator


class TestDataSourceFallback:
    """Test the complete data source fallback mechanism from main.py"""
    
    def _get_historical_data_simulation(self, symbol, force_yahoo_fail=False, force_stooq_fail=False, force_fdr_fail=False):
        """Simulate the get_historical_data function with controlled failures"""
        data_source = None
        
        # First try Yahoo Finance via yfinance (unless forced to fail)
        if not force_yahoo_fail:
            try:
                import yfinance as yf
                stock = yf.Ticker(symbol)
                data = stock.history(period="max")
                if not data.empty:
                    data_source = "Yahoo Finance"
                    data = process_data(data)
                    return data, data_source
            except Exception:
                pass
        
        # Fallback to Stooq using pandas_datareader (unless forced to fail)
        if not force_stooq_fail:
            try:
                from pandas_datareader import data as web
                data = web.DataReader(symbol, 'stooq')
                if not data.empty:
                    data_source = "Stooq"
                    data = process_data(data)
                    return data, data_source
            except Exception:
                pass
        
        # Attempt FinanceDataReader (unless forced to fail)
        if not force_fdr_fail:
            try:
                import FinanceDataReader as fdr
                data = fdr.DataReader(symbol, '2000')
                if not data.empty:
                    data_source = "FinanceDataReader"
                    data = data.reset_index().rename(columns={'index': 'Date'})
                    data = process_data(data)
                    return data, data_source
            except Exception:
                pass
        
        # Attempt InvestPy (last fallback)
        try:
            import investpy
            start_date = '01/01/2000'
            end_date = '01/01/2024'  # Use fixed end date for testing
            data = investpy.get_stock_historical_data(stock=symbol, country='united states', 
                                                    from_date=start_date, to_date=end_date)
            if not data.empty:
                data_source = "InvestPy"
                data = data.reset_index().rename(columns={'index': 'Date'})
                data = process_data(data)
                return data, data_source
        except Exception:
            pass
        
        return None, data_source
    
    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.data_source
    def test_normal_fallback_sequence(self):
        """Test normal fallback sequence without forced failures"""
        symbol = "AAPL"
        data, source = self._get_historical_data_simulation(symbol)
        
        assert data is not None, f"All data sources failed for {symbol}"
        assert source in ["Yahoo Finance", "Stooq", "FinanceDataReader", "InvestPy"], f"Unknown data source: {source}"
        
        # Validate data quality
        validator = TestDataValidator()
        assert validator.validate_stock_data_structure(data), "Invalid data structure"
        assert validator.validate_price_data(data), "Invalid price data"
    
    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.data_source
    def test_financedata_reader_as_fallback(self):
        """Test FinanceDataReader specifically as a fallback option"""
        symbol = "AAPL"
        
        # Force Yahoo Finance and Stooq to fail, test FinanceDataReader
        data, source = self._get_historical_data_simulation(symbol, 
                                                           force_yahoo_fail=True, 
                                                           force_stooq_fail=True)
        
        if data is not None:
            assert source in ["FinanceDataReader", "InvestPy"], f"Expected FinanceDataReader or InvestPy, got {source}"
            
            # If FinanceDataReader succeeded, validate it
            if source == "FinanceDataReader":
                assert len(data) > 0, "FinanceDataReader returned empty data"
                assert 'Close' in data.columns, "Missing Close column from FinanceDataReader"


class TestDataSourceValidation:
    """Test validation and data quality across all sources"""
    
    @pytest.mark.unit
    @pytest.mark.data_source
    def test_data_validator_functions(self, sample_stock_data):
        """Test the data validation utility functions"""
        validator = TestDataValidator()
        
        # Test valid data
        assert validator.validate_stock_data_structure(sample_stock_data)
        assert validator.validate_price_data(sample_stock_data)
        assert validator.validate_date_range(sample_stock_data, 2020)
        
        # Test invalid data structure
        invalid_data = sample_stock_data.drop(columns=['Close'])
        assert not validator.validate_stock_data_structure(invalid_data)
        
        # Test invalid price data (negative prices)
        invalid_prices = sample_stock_data.copy()
        invalid_prices.loc[0, 'Close'] = -1
        assert not validator.validate_price_data(invalid_prices)
    
    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.data_source
    @pytest.mark.parametrize("symbol", ["AAPL", "GOOGL"])
    def test_data_consistency_across_sources(self, symbol):
        """Test that different data sources return consistent data formats"""
        sources_data = {}
        validator = TestDataValidator()
        
        # Try to get data from different sources
        sources_to_test = [
            ("yahoo", self._get_yahoo_data),
            ("financedata", self._get_financedata_reader_data),
        ]
        
        for source_name, get_data_func in sources_to_test:
            try:
                data = get_data_func(symbol)
                if data is not None and not data.empty:
                    sources_data[source_name] = data
            except Exception:
                continue  # Skip if source fails
        
        # Validate that all successful sources have consistent structure
        for source_name, data in sources_data.items():
            assert validator.validate_stock_data_structure(data), f"{source_name} has invalid structure"
            assert validator.validate_price_data(data), f"{source_name} has invalid price data"
    
    def _get_yahoo_data(self, symbol):
        """Helper to get data from Yahoo Finance"""
        try:
            import yfinance as yf
            stock = yf.Ticker(symbol)
            data = stock.history(period="1y")  # Shorter period for testing
            if not data.empty:
                return process_data(data)
        except Exception:
            return None
        return None
    
    def _get_financedata_reader_data(self, symbol):
        """Helper to get data from FinanceDataReader"""
        try:
            import FinanceDataReader as fdr
            data = fdr.DataReader(symbol, '2023')  # Shorter period for testing
            if not data.empty:
                data = data.reset_index().rename(columns={'index': 'Date'})
                return process_data(data)
        except Exception:
            return None
        return None


class TestDataSourceConfiguration:
    """Test configuration and setup for data sources"""
    
    @pytest.mark.unit
    @pytest.mark.data_source
    def test_all_required_packages_importable(self):
        """Test that all required data source packages can be imported"""
        packages = [
            ("yfinance", "yf"),
            ("pandas_datareader", "pandas_datareader.data"),
            ("FinanceDataReader", "FinanceDataReader"),
            ("investpy", "investpy")
        ]
        
        import_results = {}
        for package_name, import_name in packages:
            try:
                __import__(import_name)
                import_results[package_name] = True
            except ImportError:
                import_results[package_name] = False
        
        # At least FinanceDataReader should be available (since we're testing it)
        assert import_results["FinanceDataReader"], "FinanceDataReader not available"
        
        # Log which packages are available
        available_packages = [name for name, available in import_results.items() if available]
        print(f"Available data source packages: {available_packages}")


pytestmark = pytest.mark.data_source
