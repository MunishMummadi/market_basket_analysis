from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class MarketBasketAnalyzer:
    def __init__(self, config: Dict):
        self.config = config
        self.frequent_itemsets = None
        self.rules = None

    def generate_frequent_itemsets(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate frequent itemsets using Apriori algorithm."""
        logger.info("Generating frequent itemsets...")
        
        self.frequent_itemsets = apriori(
            df,
            min_support=self.config['min_support'],
            use_colnames=True
        )
        
        logger.info(f"Generated {len(self.frequent_itemsets)} frequent itemsets")
        return self.frequent_itemsets

    def generate_association_rules(self) -> pd.DataFrame:
        """Generate association rules from frequent itemsets."""
        if self.frequent_itemsets is None:
            raise ValueError("Generate frequent itemsets first!")
            
        logger.info("Generating association rules...")
        
        self.rules = association_rules(
            self.frequent_itemsets,
            metric="confidence",
            min_threshold=self.config['min_confidence']
        )
        
        # Sort rules by lift
        self.rules = self.rules.sort_values('lift', ascending=False)
        
        logger.info(f"Generated {len(self.rules)} association rules")
        return self.rules

    def get_top_rules(self, n: int = 10) -> pd.DataFrame:
        """Get top N rules by lift."""
        if self.rules is None:
            raise ValueError("Generate association rules first!")
            
        return self.rules.head(n)

    def get_product_recommendations(self, product: str) -> pd.DataFrame:
        """Get product recommendations based on a given product."""
        if self.rules is None:
            raise ValueError("Generate association rules first!")
            
        # Filter rules where the product is in antecedents
        product_rules = self.rules[
            self.rules['antecedents'].apply(lambda x: product in str(x))
        ]
        
        return product_rules.sort_values('confidence', ascending=False)