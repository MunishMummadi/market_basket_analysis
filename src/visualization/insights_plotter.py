import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Dict
import os
import logging

logger = logging.getLogger(__name__)

class InsightsVisualizer:
    def __init__(self, config: Dict):
        self.config = config
        self.output_dir = config['visualization']['output_dir']
        self.figure_size = config['visualization']['figure_size']
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set style
        plt.style.use(config['visualization']['style'])

    def plot_product_frequency(self, df: pd.DataFrame) -> None:
        """Plot product frequency distribution."""
        plt.figure(figsize=self.figure_size)
        
        # Calculate product frequencies
        product_freq = df.sum().sort_values(ascending=False)
        
        # Create bar plot
        sns.barplot(x=product_freq.values[:10], y=product_freq.index[:10])
        plt.title('Top 10 Most Common Products')
        plt.xlabel('Frequency')
        plt.ylabel('Product')
        
        # Save plot
        plt.tight_layout()
        plt.savefig(
            os.path.join(self.output_dir, 'product_frequency.png'),
            dpi=self.config['visualization']['dpi']
        )
        plt.close()

    def plot_rule_metrics(self, rules: pd.DataFrame) -> None:
        """Plot relationship between support, confidence and lift."""
        plt.figure(figsize=self.figure_size)
        
        sns.scatterplot(
            data=rules,
            x='support',
            y='confidence',
            size='lift',
            sizes=(50, 500),
            alpha=0.5
        )
        
        plt.title('Association Rules Metrics')
        plt.xlabel('Support')
        plt.ylabel('Confidence')
        
        plt.tight_layout()
        plt.savefig(
            os.path.join(self.output_dir, 'rule_metrics.png'),
            dpi=self.config['visualization']['dpi']
        )
        plt.close()