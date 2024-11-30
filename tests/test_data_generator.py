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