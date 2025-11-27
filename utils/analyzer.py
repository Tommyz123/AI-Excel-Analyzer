"""
Sales Analyzer Module
Performs sales data analysis and generates business insights
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any


class SalesAnalyzer:
    """
    Sales analysis engine
    Calculates metrics, trends, and generates insights
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize analyzer with sales data
        
        Args:
            df: Cleaned sales dataframe
        """
        self.df = df
    
    def get_top_products(self, n: int = 5) -> pd.Series:
        """
        Get top N best-selling products by quantity
        
        Args:
            n: Number of top products to return
            
        Returns:
            pd.Series: Product names as index, quantities as values
        """
        return self.df.groupby('Product Name')['Quantity'].sum() \
                      .sort_values(ascending=False).head(n)
    
    def get_total_sales(self) -> float:
        """
        Calculate total sales amount
        
        Returns:
            float: Total sales in USD
        """
        return self.df['Total'].sum()
    
    def get_sales_by_state(self) -> pd.Series:
        """
        Calculate sales by state
        
        Returns:
            pd.Series: State codes as index, sales amounts as values (descending)
        """
        return self.df.groupby('Customer State')['Total'].sum() \
                      .sort_values(ascending=False)
    
    def get_daily_trend(self) -> pd.Series:
        """
        Calculate daily sales trend
        
        Returns:
            pd.Series: Dates as index, daily sales as values
        """
        return self.df.groupby(self.df['Date'].dt.date)['Total'].sum()
    
    def detect_anomalies(self) -> List[str]:
        """
        Detect unusual patterns in sales data
        
        Returns:
            List[str]: List of insight messages
        """
        insights = []
        
        if self.df.empty:
            return insights
        
        # Daily sales analysis
        daily_sales = self.get_daily_trend()
        
        if len(daily_sales) > 1:
            mean_sales = daily_sales.mean()
            std_sales = daily_sales.std()
            
            # Detect high sales days (> mean + 2*std)
            if std_sales > 0:
                high_threshold = mean_sales + 2 * std_sales
                high_days = daily_sales[daily_sales > high_threshold]
                
                if not high_days.empty:
                    best_day = high_days.idxmax()
                    best_amount = high_days.max()
                    insights.append(
                        f"🔥 Peak sales day: {best_day} (${best_amount:,.2f}) - "
                        f"{((best_amount/mean_sales - 1) * 100):.0f}% above average"
                    )
                
                # Detect low sales days (< mean - 2*std)
                low_threshold = mean_sales - 2 * std_sales
                low_days = daily_sales[daily_sales < low_threshold]
                
                if not low_days.empty:
                    worst_day = low_days.idxmin()
                    worst_amount = low_days.min()
                    insights.append(
                        f"⚠️ Low sales day: {worst_day} (${worst_amount:,.2f}) - "
                        f"{((1 - worst_amount/mean_sales) * 100):.0f}% below average"
                    )
        
        # Product performance insights
        top_products = self.get_top_products(n=1)
        if not top_products.empty:
            top_product = top_products.index[0]
            top_quantity = top_products.iloc[0]
            total_quantity = self.df['Quantity'].sum()
            percentage = (top_quantity / total_quantity * 100)
            
            if percentage > 30:
                insights.append(
                    f"⭐ '{top_product}' dominates sales with {percentage:.0f}% "
                    f"of total units sold ({int(top_quantity)} units)"
                )
        
        # State concentration
        state_sales = self.get_sales_by_state()
        if len(state_sales) > 0:
            top_state = state_sales.index[0]
            top_state_amount = state_sales.iloc[0]
            total_sales = self.get_total_sales()
            state_percentage = (top_state_amount / total_sales * 100)
            
            if state_percentage > 40:
                insights.append(
                    f"📍 {top_state} accounts for {state_percentage:.0f}% of total sales "
                    f"(${top_state_amount:,.2f})"
                )
        
        # Average order value insight
        avg_order = self.get_total_sales() / len(self.df)
        if avg_order > 100:
            insights.append(
                f"💰 High average order value: ${avg_order:.2f} per order"
            )
        elif avg_order < 20:
            insights.append(
                f"💡 Low average order value: ${avg_order:.2f} - consider upselling strategies"
            )
        
        return insights
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """
        Get summary statistics
        
        Returns:
            Dict: Summary statistics including order count, avg order value, etc.
        """
        total_sales = self.get_total_sales()
        order_count = len(self.df)
        avg_order_value = total_sales / order_count if order_count > 0 else 0
        
        # Unique products and states
        unique_products = self.df['Product Name'].nunique()
        unique_states = self.df['Customer State'].nunique()
        
        # Date range
        date_range_days = (self.df['Date'].max() - self.df['Date'].min()).days
        
        return {
            'total_sales': total_sales,
            'order_count': order_count,
            'avg_order_value': avg_order_value,
            'unique_products': unique_products,
            'unique_states': unique_states,
            'date_range_days': date_range_days,
            'avg_daily_sales': total_sales / max(date_range_days, 1)
        }
    
    def get_product_revenue(self, n: int = 5) -> pd.Series:
        """
        Get top N products by revenue (not just quantity)
        
        Args:
            n: Number of top products
            
        Returns:
            pd.Series: Product names as index, revenue as values
        """
        return self.df.groupby('Product Name')['Total'].sum() \
                      .sort_values(ascending=False).head(n)
    
    def get_weekday_pattern(self) -> pd.Series:
        """
        Analyze sales by day of week
        
        Returns:
            pd.Series: Day names as index, total sales as values
        """
        self.df['Weekday'] = self.df['Date'].dt.day_name()
        weekday_sales = self.df.groupby('Weekday')['Total'].sum()
        
        # Order by weekday
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return weekday_sales.reindex([day for day in day_order if day in weekday_sales.index])
