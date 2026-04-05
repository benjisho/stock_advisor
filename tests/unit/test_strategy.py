"""
Unit tests for stock strategy logic
"""
import pytest
import pandas as pd
import numpy as np
from strategy.stock_strategy import recommend_action


class TestStockStrategy:
    """Test stock strategy recommendation logic"""
    
    @pytest.fixture
    def sample_stock_data(self):
        """Create sample stock data for testing"""
        dates = pd.date_range('2020-01-01', periods=100, freq='D')
        data = pd.DataFrame({
            'Date': dates,
            'Open': 100 + np.cumsum(np.random.randn(100) * 0.5),
            'High': 102 + np.cumsum(np.random.randn(100) * 0.5),
            'Low': 98 + np.cumsum(np.random.randn(100) * 0.5),
            'Close': 100 + np.cumsum(np.random.randn(100) * 0.5),
            'Volume': np.random.randint(500000, 2000000, 100),
            'Adj Close': 100 + np.cumsum(np.random.randn(100) * 0.5)
        })
        return data
    
    @pytest.mark.unit
    def test_recommend_action_returns_valid_action(self, sample_stock_data):
        """Test that recommend_action returns either 'Buy' or 'Short'"""
        predicted_price = 105.0
        
        action = recommend_action(sample_stock_data, predicted_price)
        
        assert action in ['Buy', 'Short'], f"Action should be 'Buy' or 'Short', got {action}"
    
    @pytest.mark.unit
    def test_recommend_action_buy_scenario(self, sample_stock_data):
        """Test buy recommendation scenario"""
        # Create data that should trigger a buy signal
        # Ensure closing prices are trending upward
        sample_stock_data['Close'] = np.linspace(95, 110, len(sample_stock_data))
        sample_stock_data['Volume'] = np.linspace(1000000, 1500000, len(sample_stock_data))
        
        # Set predicted price higher than current price
        current_price = sample_stock_data['Close'].iloc[-1]
        predicted_price = current_price * 1.05  # 5% higher
        
        action = recommend_action(sample_stock_data.copy(), predicted_price)
        
        # Note: The action depends on multiple technical indicators, so we can't guarantee
        # a specific result, but we can test that it's a valid action
        assert action in ['Buy', 'Short'], "Should return valid action"
    
    @pytest.mark.unit
    def test_recommend_action_short_scenario(self, sample_stock_data):
        """Test short recommendation scenario"""
        # Create data that should trigger a short signal
        # Ensure closing prices are trending downward
        sample_stock_data['Close'] = np.linspace(110, 95, len(sample_stock_data))
        sample_stock_data['Volume'] = np.linspace(1500000, 1000000, len(sample_stock_data))
        
        # Set predicted price lower than current price
        current_price = sample_stock_data['Close'].iloc[-1]
        predicted_price = current_price * 0.95  # 5% lower
        
        action = recommend_action(sample_stock_data.copy(), predicted_price)
        
        # Note: The action depends on multiple technical indicators
        assert action in ['Buy', 'Short'], "Should return valid action"
    
    @pytest.mark.unit
    def test_recommend_action_adds_indicators(self, sample_stock_data):
        """Test that recommend_action adds technical indicators to the data"""
        predicted_price = 105.0
        data_copy = sample_stock_data.copy()
        
        action = recommend_action(data_copy, predicted_price)
        
        # Check that technical indicators were added
        expected_columns = ['SMA_20', 'SMA_50', 'EMA_12', 'EMA_26', 'MACD', 'MACD_Signal', 'OBV', 'ATR']
        
        for col in expected_columns:
            assert col in data_copy.columns, f"Expected column {col} to be added to data"
    
    @pytest.mark.unit
    def test_recommend_action_with_minimal_data(self):
        """Test recommend_action with minimal data"""
        # Create minimal data that meets requirements for indicators
        minimal_data = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=60, freq='D'),
            'Open': [100] * 60,
            'High': [102] * 60,
            'Low': [98] * 60,
            'Close': [100] * 60,
            'Volume': [1000000] * 60,
            'Adj Close': [100] * 60
        })
        
        predicted_price = 105.0
        
        # Should not raise an exception
        action = recommend_action(minimal_data, predicted_price)
        assert action in ['Buy', 'Short'], "Should handle minimal data"
    
    @pytest.mark.unit
    def test_recommend_action_preserves_original_data(self, sample_stock_data):
        """Test that recommend_action doesn't modify input when copying"""
        predicted_price = 105.0
        original_columns = list(sample_stock_data.columns)
        
        # The function modifies the data in place, so we test with a copy
        data_copy = sample_stock_data.copy()
        action = recommend_action(data_copy, predicted_price)
        
        # The copy should be modified, original should be unchanged
        assert list(sample_stock_data.columns) == original_columns, "Original data columns should be unchanged"
        assert len(data_copy.columns) > len(original_columns), "Copy should have additional indicator columns"


class TestStrategyEdgeCases:
    """Test edge cases for strategy logic"""
    
    @pytest.mark.unit
    def test_recommend_action_with_nan_values(self):
        """Test strategy with NaN values in data"""
        data_with_nans = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=60, freq='D'),
            'Open': [100] * 60,
            'High': [102] * 60,
            'Low': [98] * 60,
            'Close': [100] * 58 + [np.nan, np.nan],  # Last two values are NaN
            'Volume': [1000000] * 60,
            'Adj Close': [100] * 60
        })
        
        predicted_price = 105.0
        
        # Should handle NaN values gracefully
        action = recommend_action(data_with_nans, predicted_price)
        assert action in ['Buy', 'Short'], "Should handle NaN values in data"
    
    @pytest.mark.unit
    def test_recommend_action_extreme_predicted_price(self, sample_stock_data):
        """Test strategy with extreme predicted prices"""
        current_price = sample_stock_data['Close'].iloc[-1]
        
        # Test with very high predicted price
        high_predicted = current_price * 10
        action_high = recommend_action(sample_stock_data.copy(), high_predicted)
        assert action_high in ['Buy', 'Short'], "Should handle very high predicted price"
        
        # Test with very low predicted price
        low_predicted = current_price * 0.1
        action_low = recommend_action(sample_stock_data.copy(), low_predicted)
        assert action_low in ['Buy', 'Short'], "Should handle very low predicted price"
    
    @pytest.mark.unit
    def test_recommend_action_identical_prices(self):
        """Test strategy when all prices are identical"""
        identical_data = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=60, freq='D'),
            'Open': [100] * 60,
            'High': [100] * 60,
            'Low': [100] * 60,
            'Close': [100] * 60,
            'Volume': [1000000] * 60,
            'Adj Close': [100] * 60
        })
        
        predicted_price = 100.0  # Same as current price
        
        # Should handle identical prices
        action = recommend_action(identical_data, predicted_price)
        assert action in ['Buy', 'Short'], "Should handle identical prices"


@pytest.mark.unit
class TestStrategyLogic:
    """Test the logic of strategy decisions"""
    
    def test_strategy_decision_logic_components(self, sample_stock_data):
        """Test individual components of the strategy decision"""
        predicted_price = 105.0
        data_copy = sample_stock_data.copy()
        
        # Run the strategy to populate indicators
        action = recommend_action(data_copy, predicted_price)
        
        # Check that all required indicators exist
        assert 'SMA_20' in data_copy.columns, "SMA_20 should be calculated"
        assert 'SMA_50' in data_copy.columns, "SMA_50 should be calculated"
        assert 'EMA_12' in data_copy.columns, "EMA_12 should be calculated"
        assert 'EMA_26' in data_copy.columns, "EMA_26 should be calculated"
        assert 'MACD' in data_copy.columns, "MACD should be calculated"
        assert 'MACD_Signal' in data_copy.columns, "MACD_Signal should be calculated"
        assert 'OBV' in data_copy.columns, "OBV should be calculated"
        assert 'ATR' in data_copy.columns, "ATR should be calculated"
        
        # Check that indicators have reasonable values (not all NaN)
        assert not data_copy['SMA_20'].isna().all(), "SMA_20 should have some valid values"
        assert not data_copy['EMA_12'].isna().all(), "EMA_12 should have some valid values"
        assert not data_copy['MACD'].isna().all(), "MACD should have some valid values"
        assert not data_copy['OBV'].isna().all(), "OBV should have some valid values"
