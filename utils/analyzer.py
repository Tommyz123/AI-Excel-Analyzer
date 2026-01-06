"""
Sales Analyzer Module
Performs sales data analysis and generates business insights
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any
import streamlit as st


def t(key, **kwargs):
    """获取翻译文本"""
    from config import UI_TEXT_EN, UI_TEXT_ZH
    lang = st.session_state.get('language', 'en')
    text_dict = UI_TEXT_EN if lang == 'en' else UI_TEXT_ZH
    text = text_dict.get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except:
            return text
    return text


# ==================== 工具函数（保持独立性，便于提取或测试）====================
def safe_divide(numerator, denominator, fallback='N/A'):
    """
    安全除法（与app.py中的函数保持一致）

    设计考虑：
    - 未来可提取为utils/math_utils.py统一管理
    - 函数签名保持稳定，方便后续添加装饰器（如缓存、日志）
    """
    if denominator == 0 or denominator is None:
        return fallback
    try:
        return numerator / denominator
    except (ZeroDivisionError, TypeError):
        return fallback


def safe_percentage_change(current, previous):
    """
    安全计算百分比变化

    Returns:
        float: 百分比变化（如25.5表示增长25.5%）
        str: 'N/A'（如果计算失败）
    """
    result = safe_divide(current - previous, previous, fallback=None)
    if result is None or result == 'N/A':
        return 'N/A'
    return round(result * 100, 1)
# ===============================================================================


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
    
    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """
        检测销售数据异常并生成分类洞察（扩展版 - 最多10条）

        Returns:
            List[Dict]: 每个洞察包含：
                - category: 'opportunity' | 'risk' | 'trend'
                - emoji: 对应emoji
                - title: 洞察标题
                - detail: 详细说明
                - color: 背景色（用于UI显示）
        """
        insights = []

        if self.df.empty:
            return insights

        total_sales = self.get_total_sales()
        total_orders = len(self.df)
        daily_sales = self.get_daily_trend()

        # === 机会类洞察 (Opportunities) ===

        # 1. 销售高峰日（机会）
        if len(daily_sales) > 1:
            mean_sales = daily_sales.mean()
            std_sales = daily_sales.std()

            if std_sales > 0:
                high_threshold = mean_sales + 2 * std_sales
                high_days = daily_sales[daily_sales > high_threshold]

                if not high_days.empty:
                    best_day = high_days.idxmax()
                    best_amount = high_days.max()
                    pct_above = safe_percentage_change(best_amount, mean_sales)

                    insights.append({
                        'category': 'opportunity',
                        'emoji': '🔥',
                        'title': t('insight_high_peak_title', date=best_day),
                        'detail': t('insight_high_peak_detail', amount=best_amount, pct=pct_above),
                        'color': '#d4edda'
                    })

        # 2. 高客单价机会（新增）
        avg_order = safe_divide(total_sales, total_orders, fallback=0)
        if avg_order != 'N/A' and avg_order != 0 and avg_order > 50:
            insights.append({
                'category': 'opportunity',
                'emoji': '💎',
                'title': t('insight_high_customer_value_title', avg=avg_order),
                'detail': t('insight_high_customer_value_detail'),
                'color': '#d4edda'
            })

        # 3. 增长趋势（新增）
        if len(daily_sales) >= 3:
            # 简单的趋势判断：最后3天平均 vs 前面几天平均
            last_3 = daily_sales.tail(3).mean()
            first_half = daily_sales.head(len(daily_sales) // 2).mean()
            growth = safe_percentage_change(last_3, first_half)

            if growth != 'N/A' and growth > 10:
                insights.append({
                    'category': 'opportunity',
                    'emoji': '📈',
                    'title': t('insight_growth_trend_title', growth=growth),
                    'detail': t('insight_growth_trend_detail', growth=growth),
                    'color': '#d4edda'
                })

        # === 风险类洞察 (Risks) ===

        # 4. 销售低谷日（风险）
        if len(daily_sales) > 1 and std_sales > 0:
            low_threshold = mean_sales - 2 * std_sales
            low_days = daily_sales[daily_sales < low_threshold]

            if not low_days.empty:
                worst_day = low_days.idxmin()
                worst_amount = low_days.min()
                pct_below = safe_percentage_change(mean_sales - worst_amount, mean_sales)

                insights.append({
                    'category': 'risk',
                    'emoji': '⚠️',
                    'title': t('insight_low_day_title', date=worst_day),
                    'detail': t('insight_low_day_detail', amount=worst_amount, pct=pct_below),
                    'color': '#f8d7da'
                })

        # 5. 产品集中度风险（优化）
        top_products = self.get_top_products(n=1)
        if not top_products.empty:
            top_product = top_products.index[0]
            top_quantity = top_products.iloc[0]
            total_quantity = self.df['Quantity'].sum()
            percentage = safe_divide(top_quantity * 100, total_quantity, fallback=0)

            if percentage != 'N/A' and percentage > 30:
                insights.append({
                    'category': 'risk',
                    'emoji': '⭐',
                    'title': t('insight_product_concentration_title', pct=percentage),
                    'detail': t('insight_product_concentration_detail', product=top_product, pct=percentage, qty=int(top_quantity)),
                    'color': '#fff3cd'
                })

        # 6. 地区集中度风险（新增）
        state_sales = self.get_sales_by_state()
        if len(state_sales) > 0:
            top_state = state_sales.index[0]
            top_state_amount = state_sales.iloc[0]
            state_percentage = safe_divide(top_state_amount * 100, total_sales, fallback=0)

            if state_percentage != 'N/A' and state_percentage > 40:
                insights.append({
                    'category': 'risk',
                    'emoji': '📍',
                    'title': t('insight_region_concentration_title', state=top_state, pct=state_percentage),
                    'detail': t('insight_region_concentration_detail', state=top_state, pct=state_percentage, amount=top_state_amount),
                    'color': '#fff3cd'
                })

        # === 趋势类洞察 (Trends) ===

        # 7. 周末vs工作日模式（新增）
        if 'Date' in self.df.columns and len(self.df) > 7:
            self.df['Weekday'] = self.df['Date'].dt.dayofweek  # 0=Monday, 6=Sunday
            weekend_sales = self.df[self.df['Weekday'] >= 5]['Total'].sum()
            weekday_sales = self.df[self.df['Weekday'] < 5]['Total'].sum()
            weekend_days = len(self.df[self.df['Weekday'] >= 5])
            weekday_days = len(self.df[self.df['Weekday'] < 5])

            avg_weekend = safe_divide(weekend_sales, weekend_days, fallback=0)
            avg_weekday = safe_divide(weekday_sales, weekday_days, fallback=0)

            if avg_weekend != 'N/A' and avg_weekday != 'N/A' and avg_weekend != 0 and avg_weekday != 0:
                diff = safe_percentage_change(avg_weekend, avg_weekday)
                if diff != 'N/A' and abs(diff) > 15:
                    pattern_key = t('insight_weekend_label') if diff > 0 else t('insight_weekday_label')
                    opposite_key = t('insight_weekday_label') if diff > 0 else t('insight_weekend_label')
                    insights.append({
                        'category': 'trend',
                        'emoji': '📅',
                        'title': t('insight_weekend_pattern_title', pattern=pattern_key, diff=abs(diff)),
                        'detail': t('insight_weekend_pattern_detail', pattern=pattern_key, opposite=opposite_key, diff=abs(diff)),
                        'color': '#d1ecf1'
                    })

        # 8. Top 3产品贡献度（新增）
        top3_products = self.get_top_products(n=3)
        if len(top3_products) >= 3:
            top3_quantity = top3_products.sum()
            total_quantity = self.df['Quantity'].sum()
            top3_pct = safe_divide(top3_quantity * 100, total_quantity, fallback=0)

            if top3_pct != 'N/A' and top3_pct > 0:
                insights.append({
                    'category': 'trend',
                    'emoji': '🏆',
                    'title': t('insight_top3_contribution_title', pct=top3_pct),
                    'detail': t('insight_top3_contribution_detail', pct=top3_pct),
                    'color': '#d1ecf1'
                })

        # 9. 订单量vs销售额分析（新增）
        if total_orders > 0 and avg_order != 'N/A' and avg_order != 0:
            # 客单价分类
            if avg_order < 30:
                category_label = t('insight_business_model_low_freq')
                suggestion = t('insight_business_model_suggestion_low')
            elif avg_order < 80:
                category_label = t('insight_business_model_mid')
                suggestion = t('insight_business_model_suggestion_mid')
            else:
                category_label = t('insight_business_model_high_value')
                suggestion = t('insight_business_model_suggestion_high')

            insights.append({
                'category': 'trend',
                'emoji': '💹',
                'title': t('insight_business_model_title', category=category_label),
                'detail': t('insight_business_model_detail', avg=avg_order, orders=total_orders, suggestion=suggestion),
                'color': '#d1ecf1'
            })

        # 10. 价格分散度（新增）
        if 'Price' in self.df.columns:
            price_std = self.df['Price'].std()
            price_mean = self.df['Price'].mean()
            cv = safe_divide(price_std * 100, price_mean, fallback=0)  # 变异系数

            if cv != 'N/A' and cv > 50:
                insights.append({
                    'category': 'trend',
                    'emoji': '💰',
                    'title': t('insight_price_dispersion_title', cv=cv),
                    'detail': t('insight_price_dispersion_detail', cv=cv),
                    'color': '#d1ecf1'
                })

        return insights[:10]  # 最多返回10条
    
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

    def get_week_comparison(self) -> Dict[str, Any]:
        """
        本周vs上周对比（最近7天 vs 之前7天）

        Returns:
            Dict or None: {
                'current_week': float,      # 本周销售额
                'previous_week': float,     # 上周销售额
                'growth_rate': float/str,   # 增长率（百分比）或'N/A'
                'status': str,              # 'increase' 或 'decrease'
                'current_orders': int,      # 本周订单数
                'previous_orders': int      # 上周订单数
            }
            如果数据不足14天，返回None
        """
        if 'Date' not in self.df.columns:
            return None

        df_sorted = self.df.sort_values('Date')

        # 检查数据范围（需要至少14天数据）
        date_range = (df_sorted['Date'].max() - df_sorted['Date'].min()).days
        if date_range < 14:
            return None

        # 获取最近14天数据
        latest_date = df_sorted['Date'].max()
        two_weeks_ago = latest_date - pd.Timedelta(days=14)
        recent_data = df_sorted[df_sorted['Date'] > two_weeks_ago]

        # 分割本周和上周（各7天）
        one_week_ago = latest_date - pd.Timedelta(days=7)
        current_week_data = recent_data[recent_data['Date'] > one_week_ago]
        previous_week_data = recent_data[recent_data['Date'] <= one_week_ago]

        # 计算指标
        current_week_sales = current_week_data['Total'].sum()
        previous_week_sales = previous_week_data['Total'].sum()
        current_week_orders = len(current_week_data)
        previous_week_orders = len(previous_week_data)

        # 计算增长率（使用安全函数）
        growth_rate = safe_percentage_change(current_week_sales, previous_week_sales)

        return {
            'current_week': current_week_sales,
            'previous_week': previous_week_sales,
            'growth_rate': growth_rate,
            'status': 'increase' if (growth_rate != 'N/A' and growth_rate > 0) else 'decrease',
            'current_orders': current_week_orders,
            'previous_orders': previous_week_orders
        }

    def get_month_comparison(self) -> Dict[str, Any]:
        """
        本月vs上月对比（最近30天 vs 之前30天）

        Returns:
            Dict or None: 同get_week_comparison结构
            如果数据不足60天，返回None
        """
        if 'Date' not in self.df.columns:
            return None

        df_sorted = self.df.sort_values('Date')

        # 检查数据范围（需要至少60天数据）
        date_range = (df_sorted['Date'].max() - df_sorted['Date'].min()).days
        if date_range < 60:
            return None

        # 获取最近60天数据
        latest_date = df_sorted['Date'].max()
        two_months_ago = latest_date - pd.Timedelta(days=60)
        recent_data = df_sorted[df_sorted['Date'] > two_months_ago]

        # 分割本月和上月（各30天）
        one_month_ago = latest_date - pd.Timedelta(days=30)
        current_month_data = recent_data[recent_data['Date'] > one_month_ago]
        previous_month_data = recent_data[recent_data['Date'] <= one_month_ago]

        # 计算指标
        current_month_sales = current_month_data['Total'].sum()
        previous_month_sales = previous_month_data['Total'].sum()
        current_month_orders = len(current_month_data)
        previous_month_orders = len(previous_month_data)

        # 计算增长率
        growth_rate = safe_percentage_change(current_month_sales, previous_month_sales)

        return {
            'current_month': current_month_sales,
            'previous_month': previous_month_sales,
            'growth_rate': growth_rate,
            'status': 'increase' if (growth_rate != 'N/A' and growth_rate > 0) else 'decrease',
            'current_orders': current_month_orders,
            'previous_orders': previous_month_orders
        }
