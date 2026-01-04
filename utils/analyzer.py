"""
Sales Analyzer Module
Performs sales data analysis and generates business insights
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any


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
                        'title': f'销售高峰日: {best_day}',
                        'detail': f'该日销售额 ${best_amount:,.2f}，比日均高 {pct_above:.1f}%。分析该日的营销活动或外部因素，可复制成功经验。',
                        'color': '#d4edda'
                    })

        # 2. 高客单价机会（新增）
        avg_order = safe_divide(total_sales, total_orders, fallback=0)
        if avg_order != 'N/A' and avg_order != 0 and avg_order > 50:
            insights.append({
                'category': 'opportunity',
                'emoji': '💎',
                'title': f'客单价较高: ${avg_order:,.2f}',
                'detail': f'平均订单价值超过 $50，说明客户购买力强。建议推出高价值产品组合或会员计划，进一步提升客单价。',
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
                    'title': f'销售呈增长趋势: +{growth:.1f}%',
                    'detail': f'近期销售额相比前期增长 {growth:.1f}%，业务呈现良好增长态势。保持当前策略并考虑加大投入。',
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
                    'title': f'销售低谷日: {worst_day}',
                    'detail': f'该日销售额 ${worst_amount:,.2f}，比日均低 {pct_below:.1f}%。需要识别低销售日的原因（如周末、节假日），调整运营策略。',
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
                    'title': f'产品集中度高: {percentage:.0f}%',
                    'detail': f'"{top_product}" 占总销量的 {percentage:.0f}%（{int(top_quantity)} 件）。过度依赖单一产品存在风险，建议拓展产品线。',
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
                    'title': f'地区集中度高: {top_state} {state_percentage:.0f}%',
                    'detail': f'{top_state} 州占总销售额的 {state_percentage:.0f}%（${top_state_amount:,.2f}）。地区过度集中存在风险，建议拓展其他市场。',
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
                    pattern = "周末" if diff > 0 else "工作日"
                    insights.append({
                        'category': 'trend',
                        'emoji': '📅',
                        'title': f'{pattern}销售更强: {abs(diff):.0f}%',
                        'detail': f'{pattern}的日均销售额比{"工作日" if pattern=="周末" else "周末"}高 {abs(diff):.0f}%。可针对性安排促销活动和库存。',
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
                    'title': f'Top 3产品贡献度: {top3_pct:.0f}%',
                    'detail': f'Top 3 产品占总销量的 {top3_pct:.0f}%，显示出明显的"头部效应"。应重点维护这些明星产品的供应链和营销。',
                    'color': '#d1ecf1'
                })

        # 9. 订单量vs销售额分析（新增）
        if total_orders > 0 and avg_order != 'N/A' and avg_order != 0:
            # 客单价分类
            if avg_order < 30:
                category_label = "低客单价高频次"
                suggestion = "适合走量策略，可通过组合促销提升客单价"
            elif avg_order < 80:
                category_label = "中等客单价"
                suggestion = "平衡型业务，可同时关注拉新和提升客单价"
            else:
                category_label = "高客单价低频次"
                suggestion = "适合精细化运营，注重客户关系维护"

            insights.append({
                'category': 'trend',
                'emoji': '💹',
                'title': f'业务模式: {category_label}',
                'detail': f'当前平均订单价值 ${avg_order:.2f}，共 {total_orders:,} 单。{suggestion}。',
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
                    'title': f'价格差异较大: CV={cv:.0f}%',
                    'detail': f'产品价格变异系数为 {cv:.0f}%，说明价格跨度大。可考虑进行价格带分层管理，针对不同客群制定策略。',
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
