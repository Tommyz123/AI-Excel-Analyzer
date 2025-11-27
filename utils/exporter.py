"""
Data Exporter Module
Handles exporting analysis results to Excel and CSV
"""

import pandas as pd
from io import BytesIO
from datetime import datetime


class DataExporter:
    """
    Export sales analysis to various formats
    """
    
    def __init__(self, analyzer):
        """
        Initialize exporter
        
        Args:
            analyzer: SalesAnalyzer instance
        """
        self.analyzer = analyzer
    
    def export_to_excel(self) -> BytesIO:
        """
        Export analysis results to Excel with multiple sheets
        
        Returns:
            BytesIO: Excel file in memory
        """
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Sheet 1: Summary
            stats = self.analyzer.get_summary_stats()
            summary_df = pd.DataFrame({
                'Metric': [
                    'Total Sales',
                    'Number of Orders',
                    'Average Order Value',
                    'Unique Products',
                    'Unique States',
                    'Date Range (days)',
                    'Average Daily Sales'
                ],
                'Value': [
                    f"${stats['total_sales']:,.2f}",
                    stats['order_count'],
                    f"${stats['avg_order_value']:.2f}",
                    stats['unique_products'],
                    stats['unique_states'],
                    stats['date_range_days'],
                    f"${stats['avg_daily_sales']:,.2f}"
                ]
            })
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Sheet 2: Top Products (by quantity)
            top_products = self.analyzer.get_top_products(n=10)
            top_products_df = pd.DataFrame({
                'Product Name': top_products.index,
                'Quantity Sold': top_products.values
            })
            top_products_df.to_excel(writer, sheet_name='Top Products', index=False)
            
            # Sheet 3: Top Products (by revenue)
            top_revenue = self.analyzer.get_product_revenue(n=10)
            top_revenue_df = pd.DataFrame({
                'Product Name': top_revenue.index,
                'Revenue': top_revenue.values
            })
            top_revenue_df.to_excel(writer, sheet_name='Top Revenue', index=False)
            
            # Sheet 4: Sales by State
            state_sales = self.analyzer.get_sales_by_state()
            state_sales_df = pd.DataFrame({
                'State': state_sales.index,
                'Total Sales': state_sales.values
            })
            state_sales_df.to_excel(writer, sheet_name='Sales by State', index=False)
            
            # Sheet 5: Daily Trend
            daily_trend = self.analyzer.get_daily_trend()
            daily_trend_df = pd.DataFrame({
                'Date': daily_trend.index,
                'Sales': daily_trend.values
            })
            daily_trend_df.to_excel(writer, sheet_name='Daily Trend', index=False)
            
            # Sheet 6: Insights
            insights = self.analyzer.detect_anomalies()
            if insights:
                insights_df = pd.DataFrame({
                    'Insight': insights
                })
                insights_df.to_excel(writer, sheet_name='Insights', index=False)
        
        output.seek(0)
        return output
    
    def export_to_csv(self) -> BytesIO:
        """
        Export raw data to CSV
        
        Returns:
            BytesIO: CSV file in memory
        """
        output = BytesIO()
        self.analyzer.df.to_csv(output, index=False, encoding='utf-8-sig')
        output.seek(0)
        return output
    
    def get_filename(self, extension: str) -> str:
        """
        Generate filename with timestamp
        
        Args:
            extension: File extension (e.g., 'xlsx', 'csv')
            
        Returns:
            str: Filename
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"sales_report_{timestamp}.{extension}"
