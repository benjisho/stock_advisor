"""
Unit tests for technical indicators
"""
import pytest
import pandas as pd
import numpy as np
from indicators.moving_averages import (
    simple_moving_average,
    exponential_moving_average,
    bollinger_bands,
    relative_strength_index,
    stochastic_oscillator,
    macd,
    on_balance_volume,
    average_true_range
)


class TestMovingAverages:
    """Test moving average indicators"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample stock data for testing"""
        dates = pd.date_range('2020-01-01', periods=50, freq='D')
        data = pd.DataFrame({
            'Date': dates,
            'Open': 100 + np.random.randn(50) * 2,
            'High': 102 + np.random.randn(50) * 2,
            'Low': 98 + np.random.randn(50) * 2,
            'Close': 100 + np.random.randn(50) * 2,
            'Volume': 1000000 + np.random.randint(-100000, 100000, 50)
        })
        return data
    
    @pytest.mark.unit
    def test_simple_moving_average(self, sample_data):
        """Test Simple Moving Average calculation"""
        sma = simple_moving_average(sample_data, window=10)
        
        assert len(sma) == len(sample_data), "SMA should have same length as input data"
        assert sma.iloc[:9].isna().all(), "First 9 values should be NaN for window=10"
        assert not sma.iloc[9:].isna().any(), "Values after window should not be NaN"
        
        # Test that SMA is actually the mean of the window
        manual_sma = sample_data['Close'].iloc[5:15].mean()
        assert abs(sma.iloc[14] - manual_sma) < 0.001, "SMA calculation should match manual calculation"
    
    @pytest.mark.unit
    def test_exponential_moving_average(self, sample_data):
        """Test Exponential Moving Average calculation"""
        ema = exponential_moving_average(sample_data, span=12)
        
        assert len(ema) == len(sample_data), "EMA should have same length as input data"
        assert not ema.isna().any(), "EMA should not have NaN values"
        assert ema.iloc[0] == sample_data['Close'].iloc[0], "First EMA value should equal first close price"
    
    @pytest.mark.unit
    def test_bollinger_bands(self, sample_data):
        """Test Bollinger Bands calculation"""
        upper, lower = bollinger_bands(sample_data, window=20, num_std_dev=2)
        
        assert len(upper) == len(sample_data), "Upper band should have same length as input"
        assert len(lower) == len(sample_data), "Lower band should have same length as input"
        
        # Upper band should always be higher than lower band
        valid_indices = ~(upper.isna() | lower.isna())
        assert (upper[valid_indices] >= lower[valid_indices]).all(), "Upper band should be >= lower band"
    
    @pytest.mark.unit
    def test_relative_strength_index(self, sample_data):
        """Test RSI calculation"""
        rsi = relative_strength_index(sample_data, window=14)
        
        assert len(rsi) == len(sample_data), "RSI should have same length as input data"
        
        # RSI should be between 0 and 100
        valid_rsi = rsi.dropna()
        assert (valid_rsi >= 0).all() and (valid_rsi <= 100).all(), "RSI should be between 0 and 100"
    
    @pytest.mark.unit
    def test_macd(self, sample_data):
        """Test MACD calculation"""
        macd_line, signal_line = macd(sample_data, span_fast=12, span_slow=26, span_signal=9)
        
        assert len(macd_line) == len(sample_data), "MACD line should have same length as input"
        assert len(signal_line) == len(sample_data), "Signal line should have same length as input"
        assert not macd_line.isna().all(), "MACD line should have some valid values"
        assert not signal_line.isna().all(), "Signal line should have some valid values"
    
    @pytest.mark.unit
    def test_on_balance_volume(self, sample_data):
        """Test On-Balance Volume calculation"""
        obv = on_balance_volume(sample_data)
        
        assert len(obv) == len(sample_data), "OBV should have same length as input data"
        assert not obv.isna().any(), "OBV should not have NaN values"
        
        # First OBV value should equal first volume
        assert obv.iloc[0] == sample_data['Volume'].iloc[0], "First OBV should equal first volume"
    
    @pytest.mark.unit
    def test_average_true_range(self, sample_data):
        """Test Average True Range calculation"""
        atr = average_true_range(sample_data, window=14)
        
        assert len(atr) == len(sample_data), "ATR should have same length as input data"
        
        # ATR should be positive
        valid_atr = atr.dropna()
        assert (valid_atr >= 0).all(), "ATR should be non-negative"


class TestIndicatorEdgeCases:
    """Test edge cases for indicators"""
    
    @pytest.mark.unit
    def test_empty_dataframe(self):
        """Test indicators with empty DataFrame"""
        empty_df = pd.DataFrame(columns=['Close', 'High', 'Low', 'Volume'])
        
        sma = simple_moving_average(empty_df, window=10)
        assert len(sma) == 0, "SMA of empty data should be empty"
    
    @pytest.mark.unit
    def test_insufficient_data(self):
        """Test indicators with insufficient data"""
        small_df = pd.DataFrame({
            'Close': [100, 101, 99],
            'High': [102, 103, 101],
            'Low': [98, 99, 97],
            'Volume': [1000, 1100, 900]
        })
        
        sma = simple_moving_average(small_df, window=10)
        assert sma.isna().all(), "SMA with insufficient data should be all NaN"
    
    @pytest.mark.unit
    def test_single_value_data(self):
        """Test indicators with single data point"""
        single_df = pd.DataFrame({
            'Close': [100],
            'High': [102],
            'Low': [98],
            'Volume': [1000]
        })
        
        ema = exponential_moving_average(single_df, span=12)
        assert len(ema) == 1, "EMA of single value should have length 1"
        assert ema.iloc[0] == 100, "EMA of single value should equal that value"


@pytest.mark.unit
class TestIndicatorPerformance:
    """Test performance characteristics of indicators"""
    
    def test_large_dataset_performance(self):
        """Test indicators with large dataset"""
        # Create large dataset
        large_data = pd.DataFrame({
            'Close': np.random.randn(10000) + 100,
            'High': np.random.randn(10000) + 102,
            'Low': np.random.randn(10000) + 98,
            'Volume': np.random.randint(100000, 2000000, 10000)
        })
        
        import time
        start_time = time.time()
        
        # Test that indicators can handle large datasets
        sma = simple_moving_average(large_data, window=50)
        ema = exponential_moving_average(large_data, span=20)
        rsi = relative_strength_index(large_data, window=14)
        
        end_time = time.time()
        
        # Should complete within reasonable time (5 seconds)
        assert (end_time - start_time) < 5, "Indicators should handle large datasets efficiently"
        assert len(sma) == 10000, "SMA should handle large datasets"
        assert len(ema) == 10000, "EMA should handle large datasets"
        assert len(rsi) == 10000, "RSI should handle large datasets"
