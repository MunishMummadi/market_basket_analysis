# Market Basket Analysis Project

## Overview
This project implements market basket analysis using the Apriori algorithm to discover association rules in transaction data. It includes data generation, analysis, visualization, and reporting capabilities.

## Features
- Generate realistic transaction data with product associations
- Discover frequent itemsets using Apriori algorithm
- Generate and analyze association rules
- Visualize product frequencies and rule metrics
- Export results to Excel for further analysis

## Project Structure
```
market_basket_analysis/
├── config/              # Configuration files
├── src/                # Source code
│   ├── data/           # Data generation
│   ├── features/       # Analysis functions
│   ├── visualization/  # Plotting functions
│   └── utils/          # Helper functions
├── tests/              # Unit tests
├── reports/            # Output reports and figures
└── notebooks/          # Jupyter notebooks
```

## Installation
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Configure parameters in `config/config.yaml`
2. Run the analysis:
   ```bash
   python main.py
   ```
3. Find results in the `reports/` directory

## Testing
Run tests using pytest:
```bash
pytest tests/
```

## Configuration
Key parameters in `config/config.yaml`:

### Data Generation
- `min_support`: Minimum support threshold for frequent itemsets (default: 0.01)
- `min_confidence`: Minimum confidence threshold for rules (default: 0.5)
- `max_transactions`: Number of transactions to generate (default: 1000)
- `min_items_per_transaction`: Minimum items per transaction (default: 1)
- `max_items_per_transaction`: Maximum items per transaction (default: 5)

### Visualization
- `figure_size`: Size of output figures [width, height]
- `style`: Matplotlib style to use (default: 'seaborn')
- `dpi`: Resolution of output figures (default: 300)
- `output_dir`: Directory for saving figures

### Reporting
- `output_dir`: Directory for saving reports
- `excel_filename`: Name of the Excel output file

## Analysis Output
The analysis generates several outputs:

1. Visualizations:
   - Product frequency distribution
   - Rule metrics scatter plot (support vs. confidence)

2. Excel Reports:
   - Frequent itemsets with support metrics
   - Association rules with confidence and lift metrics

3. Logging:
   - Detailed execution logs with timing and statistics

## Code Examples

### Basic Usage
```python
from src.data.data_generator import TransactionGenerator
from src.features.association_rules import MarketBasketAnalyzer

# Generate data
generator = TransactionGenerator(config['data'])
df = generator.generate_dataset()

# Perform analysis
analyzer = MarketBasketAnalyzer(config['data'])
frequent_itemsets = analyzer.generate_frequent_itemsets(df)
rules = analyzer.generate_association_rules()

# Get recommendations for a specific product
recommendations = analyzer.get_product_recommendations('Bread')
```

### Customizing Visualization
```python
from src.visualization.insights_plotter import InsightsVisualizer

# Create custom visualizations
visualizer = InsightsVisualizer(config)
visualizer.plot_product_frequency(df)
visualizer.plot_rule_metrics(rules)
```