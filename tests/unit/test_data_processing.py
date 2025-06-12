"""
Unit tests for data processing functions
"""
import pytest
import pandas as pd
import numpy as np
from tests.conftest import process_data


class TestDataProcessing:
    """Test data processing utilities"""
    
    @pytest.fixture
    def unsorted_stock_data(self):
        """Create unsorted stock data for testing that matches actual usage"""
        dates = pd.date_range('2020-01-01', periods=10, freq='D')
        data = pd.DataFrame({
            'Close': np.random.randn(10) + 100,
            'Volume': np.random.randint(100000, 200000, 10)
        }, index=dates)
        
        # Shuffle the data to make it unsorted
        shuffled = data.sample(frac=1)
        
        # Transform it like data sources do: reset_index and rename to Date
        shuffled = shuffled.reset_index().rename(columns={'index': 'Date'})
        
        return shuffled
    
    @pytest.mark.unit
    def test_process_data_sorts_by_date(self, unsorted_stock_data):
        """Test that process_data sorts data by date"""
        processed = process_data(unsorted_stock_data.copy())
        
        # Check that dates are sorted
        dates = pd.to_datetime(processed['Date'])
        assert dates.is_monotonic_increasing, "Data should be sorted by date"
    
    @pytest.mark.unit
    def test_process_data_preserves_all_data(self, unsorted_stock_data):
        """Test that process_data preserves all data rows"""
        original_length = len(unsorted_stock_data)
        processed = process_data(unsorted_stock_data.copy())
        
        assert len(processed) == original_length, "All data rows should be preserved"
    
    @pytest.mark.unit
    def test_process_data_adds_date_column(self, unsorted_stock_data):
        """Test that process_data adds Date column"""
        processed = process_data(unsorted_stock_data.copy())
        
        assert 'Date' in processed.columns, "Date column should be added"
        assert processed['Date'].notna().all(), "Date column should not have NaN values"
    
    @pytest.mark.unit
    def test_process_data_resets_index(self, unsorted_stock_data):
        """Test that process_data resets index properly"""
        processed = process_data(unsorted_stock_data.copy())
        
        # Index should be range index starting from 0
        expected_index = pd.RangeIndex(len(processed))
        assert processed.index.equals(expected_index), "Index should be reset to range index"
    
    @pytest.mark.unit
    def test_process_data_preserves_columns(self, unsorted_stock_data):
        """Test that process_data preserves original columns"""
        original_columns = set(unsorted_stock_data.columns)
        processed = process_data(unsorted_stock_data.copy())
        
        # Should have all original columns plus Date
        expected_columns = original_columns.union({'Date'})
        actual_columns = set(processed.columns)
        
        assert expected_columns.issubset(actual_columns), "All original columns should be preserved"
    
    @pytest.mark.unit
    def test_process_data_with_empty_dataframe(self):
        """Test process_data with empty DataFrame"""
        empty_df = pd.DataFrame(columns=['Date', 'Close', 'Volume'])
        processed = process_data(empty_df.copy())
        
        assert len(processed) == 0, "Empty DataFrame should remain empty"
        assert 'Date' in processed.columns, "Date column should still be present"
    
    @pytest.mark.unit
    def test_process_data_with_single_row(self):
        """Test process_data with single row"""
        single_row = pd.DataFrame({
            'Date': [pd.Timestamp('2020-01-01')],
            'Close': [100.0],
            'Volume': [1000000]
        })
        
        processed = process_data(single_row.copy())
        
        assert len(processed) == 1, "Single row should be preserved"
        assert 'Date' in processed.columns, "Date column should be present"
        assert processed['Date'].iloc[0] == pd.Timestamp('2020-01-01'), "Date should be correct"
    
    @pytest.mark.unit
    def test_process_data_modifies_in_place(self, unsorted_stock_data):
        """Test that process_data modifies the DataFrame in place"""
        original_id = id(unsorted_stock_data)
        processed = process_data(unsorted_stock_data)
        
        # Should return the same DataFrame object (modified in place)
        assert id(processed) == original_id, "Should modify DataFrame in place"
    
    @pytest.mark.unit
    def test_process_data_handles_datetime_index(self):
        """Test process_data with data that has already been processed like data sources do"""
        dates = pd.date_range('2020-01-01', periods=5, freq='D')
        # Simulate what data sources do: create DataFrame with datetime index, then reset and rename
        data = pd.DataFrame({
            'Close': [100, 101, 99, 102, 98],
            'Volume': [1000, 1100, 900, 1200, 800]
        }, index=dates)
        
        # Process like data sources do
        data = data.reset_index().rename(columns={'index': 'Date'})
        
        processed = process_data(data.copy())
        
        assert 'Date' in processed.columns, "Date column should be present"
        assert len(processed) == 5, "All rows should be preserved"
        
        # Check that dates are properly sorted
        dates_sorted = pd.to_datetime(processed['Date'])
        assert dates_sorted.is_monotonic_increasing, "Dates should be sorted"


class TestDataProcessingEdgeCases:
    """Test edge cases for data processing"""
    
    @pytest.mark.unit
    def test_process_data_with_duplicate_dates(self):
        """Test process_data with duplicate dates"""
        duplicate_dates = [pd.Timestamp('2020-01-01')] * 3
        data = pd.DataFrame({
            'Date': duplicate_dates,
            'Close': [100, 101, 99],
            'Volume': [1000, 1100, 900]
        })
        
        processed = process_data(data.copy())
        
        assert len(processed) == 3, "All rows should be preserved even with duplicate dates"
        assert 'Date' in processed.columns, "Date column should be present"
    
    @pytest.mark.unit
    def test_process_data_with_missing_values(self):
        """Test process_data with missing values"""
        dates = pd.date_range('2020-01-01', periods=5, freq='D')
        data = pd.DataFrame({
            'Date': dates,
            'Close': [100, np.nan, 99, 102, np.nan],
            'Volume': [1000, 1100, np.nan, 1200, 800]
        })
        
        processed = process_data(data.copy())
        
        assert len(processed) == 5, "All rows should be preserved including those with NaN"
        assert 'Date' in processed.columns, "Date column should be present"
        
        # NaN values should be preserved
        assert processed['Close'].isna().sum() == 2, "NaN values in Close should be preserved"
        assert processed['Volume'].isna().sum() == 1, "NaN values in Volume should be preserved"
    
    @pytest.mark.unit
    def test_process_data_performance_large_dataset(self):
        """Test process_data performance with large dataset"""
        # Create large dataset that simulates data source output
        dates = pd.date_range('2000-01-01', periods=10000, freq='D')
        large_data = pd.DataFrame({
            'Close': np.random.randn(10000) + 100,
            'Volume': np.random.randint(100000, 200000, 10000)
        }, index=dates)
        
        # Process like data sources do: reset and rename
        large_data = large_data.reset_index().rename(columns={'index': 'Date'})
        
        # Shuffle to make unsorted
        large_data = large_data.sample(frac=1)
        
        import time
        start_time = time.time()
        
        processed = process_data(large_data.copy())
        
        end_time = time.time()
        
        # Should complete within reasonable time (2 seconds)
        assert (end_time - start_time) < 2, "Should handle large datasets efficiently"
        assert len(processed) == 10000, "All data should be preserved"
        
        # Check sorting
        dates = pd.to_datetime(processed['Date'])
        assert dates.is_monotonic_increasing, "Large dataset should be properly sorted"
