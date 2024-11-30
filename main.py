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



