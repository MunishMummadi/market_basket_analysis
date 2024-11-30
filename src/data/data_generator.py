import numpy as np
import pandas as pd
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class TransactionGenerator:
    def __init__(self, config: Dict):
        self.config = config
        self.products = [
            'Bread', 'Milk', 'Eggs', 'Cheese', 'Butter',
            'Coffee', 'Tea', 'Sugar', 'Cereal', 'Yogurt',
            'Juice', 'Water', 'Chips', 'Cookies', 'Fruit'
        ]
        
        # Product associations for more realistic data
        self.product_associations = {
            'Bread': ['Butter', 'Cheese', 'Eggs'],
            'Coffee': ['Sugar', 'Milk'],
            'Tea': ['Sugar', 'Milk'],
            'Cereal': ['Milk'],
            'Cookies': ['Milk']
        }

    def generate_transaction(self) -> List[str]:
        """Generate a single transaction with realistic product combinations."""
        n_items = np.random.randint(
            self.config['min_items_per_transaction'],
            self.config['max_items_per_transaction'] + 1
        )
        
        # Start with a random product
        transaction = [np.random.choice(self.products)]
        
        # Add associated products with higher probability
        while len(transaction) < n_items:
            if transaction[-1] in self.product_associations and np.random.random() < 0.7:
                # Add an associated product
                associated_products = [p for p in self.product_associations[transaction[-1]] 
                                    if p not in transaction]
                if associated_products:
                    transaction.append(np.random.choice(associated_products))
            else:
                # Add a random product
                available_products = [p for p in self.products if p not in transaction]
                if available_products:
                    transaction.append(np.random.choice(available_products))
                    
        return sorted(transaction)

    def generate_dataset(self) -> pd.DataFrame:
        """Generate a dataset of transactions."""
        logger.info(f"Generating {self.config['max_transactions']} transactions...")
        
        transactions = [
            self.generate_transaction() 
            for _ in range(self.config['max_transactions'])
        ]
        
        # Convert to one-hot encoded format
        df = pd.DataFrame([{prod: 1 for prod in trans} for trans in transactions])
        df = df.fillna(0)
        
        logger.info(f"Generated dataset with shape {df.shape}")
        return df