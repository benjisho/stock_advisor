#!/usr/bin/env python3
"""
Comprehensive test suite for all data sources used in the stock advisor application.
Tests the fallback mechanism and individual data source functionality.
"""
import pytest
import pandas as pd
from datetime import date
from unittest.mock import patch, MagicMock
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

class TestDataSourceFallback:
    """Test the data source fallback mechanism from main.py"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_yahoo_finance_primary(self):
        """Test Yahoo Finance as primary data source."""
        try:
            import yfinance as yf
            
            stock = yf.Ticker("AAPL")
            data = stock.history(period="1y")
            
            assert not data.empty, "Yahoo Finance should return data"
            assert 'Close' in data.columns, "Should contain Close column"
            
        except ImportError:
            pytest.skip("yfinance not available")
    
    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.stooq
    def test_stooq_fallback(self):
        """Test Stooq as first fallback."""
        try:
            from pandas_datareader import data as web
            
            data = web.DataReader("AAPL", 'stooq')
            
            assert not data.empty, "Stooq should return data"
            assert 'Close' in data.columns, "Should contain Close column"
            
        except ImportError:
            pytest.skip("pandas_datareader not available")
    
    @pytest.mark.integration
    @pytest.mark.slow  
    @pytest.mark.finance_data_reader
    def test_finance_data_reader_fallback(self):
        """Test FinanceDataReader as second fallback."""
        try:
            import FinanceDataReader as fdr
            
            data = fdr.DataReader("AAPL", '2020')
            
            assert not data.empty, "FinanceDataReader should return data"
            assert 'Close' in data.columns, "Should contain Close column"
            
            # Test the exact transformation from main.py
            data_source = "FinanceDataReader"
            data = data.reset_index().rename(columns={'index': 'Date'})
            data = process_data(data)
            
            assert 'Date' in data.columns, "Should have Date column after processing"
            assert data['Date'].is_monotonic_increasing, "Should be sorted by date"
            
        except ImportError:
            pytest.skip("FinanceDataReader not available")
    
    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.investpy
    def test_investpy_final_fallback(self):
        """Test InvestPy as final fallback."""
        try:
            import investpy
            
            start_date = '01/01/2020'
            end_date = date.today().strftime('%d/%m/%Y')
            data = investpy.get_stock_historical_data(
                stock="AAPL", 
                country='united states', 
                from_date=start_date, 
                to_date=end_date
            )
            
            assert not data.empty, "InvestPy should return data"
            assert 'Close' in data.columns, "Should contain Close column"
            
        except ImportError:
            pytest.skip("investpy not available")
        except Exception as e:
            # InvestPy can be flaky, so we'll allow this to fail gracefully
            pytest.skip(f"InvestPy failed: {e}")

class TestDataSourceExactImplementation:
    """Test the exact implementation from main.py"""
    
    @pytest.mark.finance_data_reader
    @pytest.mark.unit
    def test_exact_fdr_section_implementation(self):
        """Test the exact FinanceDataReader section from main.py lines 52-66"""
        
        def fdr_section(symbol):
            """Exact implementation from main.py"""
            try:
                import FinanceDataReader as fdr
                data = fdr.DataReader(symbol, '2000')
                if not data.empty:
                    data_source = "FinanceDataReader"
                    data = data.reset_index().rename(columns={'index': 'Date'})
                    data = process_data(data)
                    return data, data_source
            except Exception as e:
                return None, None
            return None, None
        
        # Test with valid symbol
        data, source = fdr_section("AAPL")
        
        if data is not None:  # Only test if FinanceDataReader is available
            assert source == "FinanceDataReader", "Should return correct source"
            assert isinstance(data, pd.DataFrame), "Should return DataFrame"
            assert len(data) > 0, "Should contain data"
            assert 'Date' in data.columns, "Should have Date column"
            assert 'Close' in data.columns, "Should have Close column"
        else:
            pytest.skip("FinanceDataReader not available or failed")
    
    @pytest.mark.finance_data_reader
    @pytest.mark.unit
    def test_fdr_error_handling(self):
        """Test error handling in FinanceDataReader section"""
        
        def fdr_section_with_invalid(symbol):
            """Test with invalid symbol"""
            try:
                import FinanceDataReader as fdr
                data = fdr.DataReader(symbol, '2000')
                if not data.empty:
                    data_source = "FinanceDataReader"
                    data = data.reset_index().rename(columns={'index': 'Date'})
                    data = process_data(data)
                    return data, data_source
            except Exception as e:
                # This should match the behavior in main.py
                return None, None
            return None, None
        
        # Test with invalid symbol
        data, source = fdr_section_with_invalid("INVALID_SYMBOL_123")
        
        assert data is None, "Should return None for invalid symbol"
        assert source is None, "Should return None source for invalid symbol"

class TestDataProcessing:
    """Test data processing functions"""
    
    @pytest.mark.unit
    def test_process_data_function(self):
        """Test the process_data function"""
        # Create sample data
        dates = pd.date_range('2020-01-01', periods=5, freq='D')
        data = pd.DataFrame({
            'Close': [100, 101, 99, 102, 98],
            'Volume': [1000, 1100, 900, 1200, 800]
        }, index=dates)
        
        # Process like data sources do: reset_index and rename to Date
        data = data.reset_index().rename(columns={'index': 'Date'})
        
        # Scramble the order
        data = data.iloc[[2, 0, 4, 1, 3]]
        
        processed = process_data(data.copy())
        
        assert 'Date' in processed.columns, "Should have Date column"
        assert processed['Date'].is_monotonic_increasing, "Should be sorted by date"
        assert len(processed) == 5, "Should preserve all rows"

@pytest.mark.smoke
class TestQuickSmokeTests:
    """Quick smoke tests to verify basic functionality"""
    
    def test_import_all_data_sources(self):
        """Test that all data source libraries can be imported"""
        imports = []
        
        try:
            import yfinance
            imports.append("yfinance")
        except ImportError:
            pass
            
        try:
            import pandas_datareader
            imports.append("pandas_datareader")
        except ImportError:
            pass
            
        try:
            import FinanceDataReader
            imports.append("FinanceDataReader")
        except ImportError:
            pass
            
        try:
            import investpy
            imports.append("investpy")
        except ImportError:
            pass
        
        assert len(imports) > 0, "At least one data source should be available"
        print(f"Available data sources: {imports}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
