import pytest
from src.features.association_rules import MarketBasketAnalyzer
import pandas as pd
import numpy as np

@pytest.fixture
def config():
    return {
        'min_support': 0.01,
        'min_confidence': 0.5
    }

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'Bread': [1, 1, 1, 0],
        'Milk': [1, 0, 1, 1],
        'Eggs': [0, 1, 1, 0]
    })

def test_market_basket_analyzer_init(config):
    analyzer = MarketBasketAnalyzer(config)
    assert analyzer.config == config

def test_generate_frequent_itemsets(config, sample_data):
    analyzer = MarketBasketAnalyzer(config)
    itemsets = analyzer.generate_frequent_itemsets(sample_data)
    
    assert isinstance(itemsets, pd.DataFrame)
    assert 'support' in itemsets.columns

def test_generate_association_rules(config, sample_data):
    analyzer = MarketBasketAnalyzer(config)
    analyzer.generate_frequent_itemsets(sample_data)
    rules = analyzer.generate_association_rules()
    
    assert isinstance(rules, pd.DataFrame)
    assert all(col in rules.columns for col in ['antecedents', 'consequents', 'confidence', 'lift'])