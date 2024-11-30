import yaml
import pandas as pd
from typing import Dict, Any
import logging
import os

def load_config(config_path: str) -> Dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def setup_logging() -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def save_results(results: Dict[str, Any], config: Dict) -> None:
    """Save analysis results to Excel file."""
    output_path = os.path.join(
        config['reporting']['output_dir'],
        config['reporting']['excel_filename']
    )
    
    # Create output directory if it doesn't exist
    os.makedirs(config['reporting']['output_dir'], exist_ok=True)
    
    with pd.ExcelWriter(output_path) as writer:
        # Save frequent itemsets
        if 'frequent_itemsets' in results:
            results['frequent_itemsets'].to_excel(
                writer, 
                sheet_name='Frequent Itemsets',
                index=False
            )
        
        # Save association rules
        if 'rules' in results:
            results['rules'].to_excel(
                writer,
                sheet_name='Association Rules',
                index=False
            )