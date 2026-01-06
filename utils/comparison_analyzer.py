"""
Multi-File Comparison Analyzer
支持2-3个文件的对比分析
"""

import pandas as pd
from typing import List, Dict, Any
from .analyzer import SalesAnalyzer
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


class ComparisonAnalyzer:
    """
    多文件对比分析器

    功能：
    - 支持2-3个文件同时对比
    - 对比指标：销售额、订单量、平均订单、Top产品等
    - 生成并排对比图表
    """

    def __init__(self, dataframes: List[pd.DataFrame], labels: List[str] = None):
        """
        初始化对比分析器

        Args:
            dataframes: 数据框列表（2-3个）
            labels: 文件标签（如："11月", "12月", "1月"）
        """
        if not (2 <= len(dataframes) <= 3):
            raise ValueError(t('comparison_error_file_count'))

        self.dataframes = dataframes
        self.count = len(dataframes)

        # 为每个数据框创建分析器
        self.analyzers = [SalesAnalyzer(df) for df in dataframes]

        # 设置标签
        if labels is None:
            self.labels = [t('comparison_default_label', num=i+1) for i in range(self.count)]
        else:
            if len(labels) != len(dataframes):
                raise ValueError(t('comparison_error_label_mismatch'))
            self.labels = labels

    def get_summary_metrics(self) -> Dict[str, List[Any]]:
        """
        获取所有数据集的汇总指标

        Returns:
            Dict: {
                'labels': [...],
                'total_sales': [...],
                'total_orders': [...],
                'avg_order_value': [...],
                'unique_products': [...],
                'unique_states': [...]
            }
        """
        metrics = {
            'labels': self.labels,
            'total_sales': [],
            'total_orders': [],
            'avg_order_value': [],
            'unique_products': [],
            'unique_states': []
        }

        for analyzer in self.analyzers:
            # 销售额
            metrics['total_sales'].append(analyzer.get_total_sales())

            # 订单量
            metrics['total_orders'].append(len(analyzer.df))

            # 平均订单金额
            total_sales = analyzer.get_total_sales()
            total_orders = len(analyzer.df)
            avg_order = total_sales / total_orders if total_orders > 0 else 0
            metrics['avg_order_value'].append(avg_order)

            # 产品数量
            if 'Product Name' in analyzer.df.columns:
                metrics['unique_products'].append(analyzer.df['Product Name'].nunique())
            else:
                metrics['unique_products'].append(0)

            # 州数量
            if 'Customer State' in analyzer.df.columns:
                metrics['unique_states'].append(analyzer.df['Customer State'].nunique())
            else:
                metrics['unique_states'].append(0)

        return metrics

    def get_top_products_comparison(self, top_n: int = 5) -> Dict[str, pd.Series]:
        """
        对比各数据集的Top产品

        Args:
            top_n: 显示前N名产品

        Returns:
            Dict: {
                'label1': Series(产品: 销量),
                'label2': Series(产品: 销量),
                ...
            }
        """
        comparison = {}

        for label, analyzer in zip(self.labels, self.analyzers):
            top_products = analyzer.get_top_products(top_n)
            comparison[label] = top_products

        return comparison

    def get_sales_by_state_comparison(self, top_n: int = 10) -> Dict[str, pd.Series]:
        """
        对比各数据集的州销售额

        Args:
            top_n: 显示前N个州

        Returns:
            Dict: {
                'label1': Series(州: 销售额),
                'label2': Series(州: 销售额),
                ...
            }
        """
        comparison = {}

        for label, analyzer in zip(self.labels, self.analyzers):
            sales_by_state = analyzer.get_sales_by_state().head(top_n)
            comparison[label] = sales_by_state

        return comparison

    def get_daily_trend_comparison(self) -> Dict[str, pd.Series]:
        """
        对比各数据集的每日销售趋势

        Returns:
            Dict: {
                'label1': Series(日期: 销售额),
                'label2': Series(日期: 销售额),
                ...
            }
        """
        comparison = {}

        for label, analyzer in zip(self.labels, self.analyzers):
            daily_trend = analyzer.get_daily_trend()
            comparison[label] = daily_trend

        return comparison

    def get_growth_analysis(self) -> Dict[str, Any]:
        """
        计算增长分析（基于第一个文件作为基准）

        Returns:
            Dict: {
                'baseline': str,  # 基准标签
                'comparisons': [
                    {
                        'label': str,
                        'sales_growth': float (百分比),
                        'orders_growth': float,
                        'avg_order_growth': float,
                        'status': 'increase' | 'decrease'
                    },
                    ...
                ]
            }
        """
        if self.count < 2:
            return None

        baseline_analyzer = self.analyzers[0]
        baseline_sales = baseline_analyzer.get_total_sales()
        baseline_orders = len(baseline_analyzer.df)
        baseline_avg = baseline_sales / baseline_orders if baseline_orders > 0 else 0

        comparisons = []

        for i in range(1, self.count):
            current_analyzer = self.analyzers[i]
            current_sales = current_analyzer.get_total_sales()
            current_orders = len(current_analyzer.df)
            current_avg = current_sales / current_orders if current_orders > 0 else 0

            # 计算增长率
            sales_growth = ((current_sales - baseline_sales) / baseline_sales * 100) if baseline_sales > 0 else 0
            orders_growth = ((current_orders - baseline_orders) / baseline_orders * 100) if baseline_orders > 0 else 0
            avg_order_growth = ((current_avg - baseline_avg) / baseline_avg * 100) if baseline_avg > 0 else 0

            comparisons.append({
                'label': self.labels[i],
                'sales_growth': round(sales_growth, 1),
                'orders_growth': round(orders_growth, 1),
                'avg_order_growth': round(avg_order_growth, 1),
                'status': 'increase' if sales_growth > 0 else 'decrease'
            })

        return {
            'baseline': self.labels[0],
            'comparisons': comparisons
        }

    def get_date_ranges(self) -> List[Dict[str, Any]]:
        """
        获取各数据集的日期范围

        Returns:
            List[Dict]: [
                {
                    'label': str,
                    'start_date': datetime,
                    'end_date': datetime,
                    'days': int
                },
                ...
            ]
        """
        date_ranges = []

        for label, df in zip(self.labels, self.dataframes):
            if 'Date' in df.columns:
                min_date = df['Date'].min()
                max_date = df['Date'].max()
                days = (max_date - min_date).days

                date_ranges.append({
                    'label': label,
                    'start_date': min_date,
                    'end_date': max_date,
                    'days': days
                })
            else:
                date_ranges.append({
                    'label': label,
                    'start_date': None,
                    'end_date': None,
                    'days': 0
                })

        return date_ranges
