"""
Comprehensive pytest suite for FinanceDataReader functionality
Consolidates all the individual test files into a proper pytest structure
MERGED FROM DUPLICATE FILES - COMPREHENSIVE VERSION
"""
import pytest
import pandas as pd
from datetime import date
from tests.conftest import process_data, TestDataValidator


class TestFinanceDataReaderBasic:
    """Basic functionality tests for FinanceDataReader"""
    
    @pytest.mark.unit
    @pytest.mark.data_source
    def test_financedata_reader_import(self):
        """Test that FinanceDataReader can be imported"""
        try:
            import FinanceDataReader as fdr
            assert hasattr(fdr, 'DataReader')
        except ImportError:
            pytest.fail("FinanceDataReader could not be imported")
    
    @pytest.mark.integration
    @pytest.mark.data_source
    @pytest.mark.slow
    @pytest.mark.parametrize("symbol", ["AAPL", "GOOGL", "MSFT"])
    def test_basic_data_retrieval(self, symbol):
        """Test basic data retrieval for major stocks"""
        import FinanceDataReader as fdr
        
        data = fdr.DataReader(symbol, '2020')
        
        assert not data.empty, f"No data returned for {symbol}"
        assert len(data) > 0, f"Empty dataset for {symbol}"
        
        # Validate data structure
        validator = TestDataValidator()
        
        # Reset index to get Date column (simulating main.py behavior)
        data_processed = data.reset_index().rename(columns={'index': 'Date'})
        
        assert validator.validate_stock_data_structure(data_processed), f"Invalid data structure for {symbol}"
        assert validator.validate_price_data(data_processed), f"Invalid price data for {symbol}"


class TestFinanceDataReaderExactMainCode:
    """Test the exact FinanceDataReader code section from main.py (lines 52-66)"""
    
    def _execute_exact_main_code(self, symbol):
        """Execute the exact FinanceDataReader code from main.py"""
        # Attempt FinanceDataReader (exact code from main.py lines 52-66)
        try:
            import FinanceDataReader as fdr
            data = fdr.DataReader(symbol, '2000')
            if not data.empty:
                data_source = "FinanceDataReader"
                data = data.reset_index().rename(columns={'index': 'Date'})
                data = process_data(data)
                return data, data_source
        except Exception as e:
            # This matches the exact behavior in main.py
            return None, None
        
        return None, None
    
    @pytest.mark.integration
    @pytest.mark.data_source
    @pytest.mark.slow
    @pytest.mark.parametrize("symbol", ["AAPL", "GOOGL", "MSFT", "TSLA"])
    def test_exact_main_code_execution(self, symbol):
        """Test the exact FinanceDataReader code section from main.py"""
        data, data_source = self._execute_exact_main_code(symbol)
        
        assert data is not None, f"Failed to retrieve data for {symbol}"
        assert data_source == "FinanceDataReader", f"Unexpected data source for {symbol}"
        
        # Validate the processed data
        assert len(data) > 0, f"Empty processed data for {symbol}"
        assert 'Date' in data.columns, f"Date column missing for {symbol}"
        assert 'Close' in data.columns, f"Close column missing for {symbol}"
        
        # Validate data is sorted by date (as done by process_data)
        dates = pd.to_datetime(data['Date'])
        assert dates.is_monotonic_increasing, f"Data not properly sorted for {symbol}"
    
    @pytest.mark.unit
    @pytest.mark.data_source
    def test_exact_main_code_with_invalid_symbol(self):
        """Test exact main code with invalid symbol"""
        data, data_source = self._execute_exact_main_code("INVALID_SYMBOL_123")
        
        # Should return None for both when symbol is invalid
        assert data is None
        assert data_source is None


class TestFinanceDataReaderEdgeCases:
    """Test edge cases and error conditions"""
    
    @pytest.mark.unit
    @pytest.mark.data_source
    @pytest.mark.parametrize("symbol", ["INVALID123", "NOTREAL", "XYZ999"])
    def test_invalid_symbols(self, symbol):
        """Test handling of invalid stock symbols"""
        import FinanceDataReader as fdr
        
        with pytest.raises(Exception):
            data = fdr.DataReader(symbol, '2000')
            # If no exception is raised but data is empty, that's also acceptable
            if data.empty:
                pytest.skip(f"No data returned for {symbol} (expected)")
    
    @pytest.mark.integration
    @pytest.mark.data_source
    @pytest.mark.slow
    @pytest.mark.parametrize("start_year", ["2020", "2022", "2024"])
    def test_different_date_ranges(self, start_year):
        """Test different starting date ranges"""
        import FinanceDataReader as fdr
        
        data = fdr.DataReader('AAPL', start_year)
        
        if not data.empty:
            min_date = data.index.min()
            assert min_date.year >= int(start_year), f"Data doesn't start from {start_year}"
    
    @pytest.mark.unit
    def test_data_processing_function(self, sample_stock_data):
        """Test the process_data function used in main.py"""
        # Create test data with unsorted dates
        unsorted_data = sample_stock_data.copy()
        unsorted_data = unsorted_data.sample(frac=1).reset_index(drop=True)  # Shuffle
        
        processed_data = process_data(unsorted_data)
        
        # Should be sorted by date
        dates = pd.to_datetime(processed_data['Date'])
        assert dates.is_monotonic_increasing, "Data not properly sorted by process_data"
        
        # Should have all original data
        assert len(processed_data) == len(sample_stock_data), "Data lost during processing"


class TestFinanceDataReaderFallbackScenario:
    """Test FinanceDataReader in the context of the fallback scenario"""
    
    @pytest.mark.integration
    @pytest.mark.data_source
    @pytest.mark.slow
    def test_fallback_scenario_simulation(self, valid_symbols):
        """Simulate the scenario where FinanceDataReader is used as fallback"""
        # This simulates when Yahoo Finance and Stooq fail, and FinanceDataReader is used
        
        for symbol in valid_symbols[:2]:  # Test first 2 symbols to keep test time reasonable
            # Execute the exact fallback code
            try:
                import FinanceDataReader as fdr
                data = fdr.DataReader(symbol, '2000')
                if not data.empty:
                    data_source = "FinanceDataReader"
                    data = data.reset_index().rename(columns={'index': 'Date'})
                    data = process_data(data)
                    
                    # Assertions for successful fallback
                    assert len(data) > 0, f"No data in fallback for {symbol}"
                    assert data_source == "FinanceDataReader", f"Wrong source in fallback for {symbol}"
                    
                    # Validate we can get current price (as main.py does)
                    current_price = float(data['Close'].iloc[-1])
                    assert current_price > 0, f"Invalid current price for {symbol}"
                    
                else:
                    pytest.fail(f"FinanceDataReader fallback failed for {symbol}")
                    
            except Exception as e:
                pytest.fail(f"FinanceDataReader fallback exception for {symbol}: {e}")


class TestFinanceDataReaderIntegration:
    """Integration tests that validate the complete workflow"""
    
    @pytest.mark.integration
    @pytest.mark.data_source
    @pytest.mark.slow
    def test_complete_data_workflow(self):
        """Test the complete data workflow as used in main.py"""
        symbol = "AAPL"
        
        # Execute the complete workflow
        try:
            import FinanceDataReader as fdr
            data = fdr.DataReader(symbol, '2000')
            
            if not data.empty:
                data_source = "FinanceDataReader"
                data = data.reset_index().rename(columns={'index': 'Date'})
                data = process_data(data)
                
                # Test all the operations that main.py would do
                current_price = round(float(data['Close'].iloc[-1]), 2)
                
                # Validate data for ML usage (as main.py does)
                data_copy = data.copy()
                data_copy['Date_Num'] = (data_copy['Date'] - data_copy['Date'].min()).dt.days
                
                assert 'Date_Num' in data_copy.columns, "Date_Num column not created"
                assert len(data_copy) > 100, "Insufficient data for ML"  # Need reasonable amount of data
                assert current_price > 0, "Invalid current price"
                
                # Validate we can prepare data for sklearn (as main.py does)
                X = data_copy[['Date_Num']].values
                y = data_copy['Close'].values
                
                assert len(X) == len(y), "X and y length mismatch"
                assert len(X) > 0, "No data for ML"
                
        except Exception as e:
            pytest.fail(f"Complete workflow failed: {e}")
    
    @pytest.mark.smoke
    @pytest.mark.data_source
    def test_smoke_basic_functionality(self):
        """Quick smoke test to verify basic functionality"""
        try:
            import FinanceDataReader as fdr
            # Quick test with recent data
            data = fdr.DataReader('AAPL', '2024')
            
            assert not data.empty, "Smoke test failed - no data returned"
            assert len(data) > 0, "Smoke test failed - empty dataset"
            
        except Exception as e:
            pytest.fail(f"Smoke test failed: {e}")


# Mark all tests in this module as data_source tests
pytestmark = pytest.mark.data_source
