# main.py
import os
from src.data.data_generator import TransactionGenerator
from src.features.association_rules import MarketBasketAnalyzer
from src.visualization.insights_plotter import InsightsVisualizer
from src.utils.helpers import load_config, setup_logging, save_results
import logging

def main():
    # Setup
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Load configuration
    config_path = os.path.join('config', 'config.yaml')
    config = load_config(config_path)
    
    try:
        # Generate data
        logger.info("Generating transaction data...")
        generator = TransactionGenerator(config['data'])
        df = generator.generate_dataset()
        
        # Perform market basket analysis
        logger.info("Performing market basket analysis...")
        analyzer = MarketBasketAnalyzer(config['data'])
        frequent_itemsets = analyzer.generate_frequent_itemsets(df)
        rules = analyzer.generate_association_rules()
        
        # Create visualizations
        logger.info("Generating visualizations...")
        visualizer = InsightsVisualizer(config)
        visualizer.plot_product_frequency(df)
        visualizer.plot_rule_metrics(rules)
        
        # Save results
        logger.info("Saving results...")
        results = {
            'frequent_itemsets': frequent_itemsets,
            'rules': rules
        }
        save_results(results, config)
        
        logger.info("Analysis completed successfully!")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()

# tests/test_data_generator.py
import pytest
from src.data.data_generator import TransactionGenerator
import pandas as pd

@pytest.fixture
def config():
    return {
        'min_items_per_transaction': 1,
        'max_items_per_transaction': 5,
        'max_transactions': 100
    }

def test_transaction_generator_init(config):
    generator = TransactionGenerator(config)
    assert isinstance(generator.products, list)
    assert len(generator.products) > 0

def test_generate_transaction(config):
    generator = TransactionGenerator(config)
    transaction = generator.generate_transaction()
    
    assert isinstance(transaction, list)
    assert len(transaction) >= config['min_items_per_transaction']
    assert len(transaction) <= config['max_items_per_transaction']

def test_generate_dataset(config):
    generator = TransactionGenerator(config)
    df = generator.generate_dataset()
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == config['max_transactions']
    assert all(df.isin([0, 1]).all())

# tests/test_association_rules.py
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