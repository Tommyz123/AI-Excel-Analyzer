#!/usr/bin/env python3
"""
AI Excel Analyzer - Comprehensive Validation Test Script
Tests all core functionalities of the application
"""

import sys
import os
import pandas as pd
import traceback
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.data_processor import FlexibleDataProcessor
from utils.pandas_agent import PandasAgent
from utils.analyzer import SalesAnalyzer
from utils.exporter import DataExporter
from utils.cost_controller import CostController
from config import Config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ValidationTester:
    """Comprehensive validation test suite"""

    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.api_key = os.getenv('OPENAI_API_KEY')

    def log_test(self, test_name, status, details=""):
        """Log test result"""
        result = {
            'test': test_name,
            'status': status,
            'details': details,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.results.append(result)

        symbol = "✅" if status == "PASS" else "❌"
        print(f"{symbol} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")

        if status == "PASS":
            self.passed += 1
        else:
            self.failed += 1

    def test_environment(self):
        """Test 1: Environment Configuration"""
        print("\n" + "="*60)
        print("TEST 1: Environment Configuration")
        print("="*60)

        # Check API key
        if self.api_key and self.api_key.startswith('sk-'):
            self.log_test("API Key Configuration", "PASS", "OpenAI API key found")
        else:
            self.log_test("API Key Configuration", "FAIL", "Invalid or missing API key")

        # Check sample data files
        sample_dir = Path('sample_data')
        if sample_dir.exists():
            xlsx_files = list(sample_dir.glob('*.xlsx'))
            self.log_test("Sample Data Files", "PASS", f"Found {len(xlsx_files)} sample files")
        else:
            self.log_test("Sample Data Files", "FAIL", "sample_data directory not found")

    def test_data_loading(self):
        """Test 2: Data Loading and Processing"""
        print("\n" + "="*60)
        print("TEST 2: Data Loading and Processing")
        print("="*60)

        try:
            # Find first sample file
            sample_file = Path('sample_data/30days_sample.xlsx')

            if not sample_file.exists():
                # Try any xlsx file
                sample_files = list(Path('sample_data').glob('*.xlsx'))
                if sample_files:
                    sample_file = sample_files[0]
                else:
                    self.log_test("Data Loading", "FAIL", "No sample data files found")
                    return None

            # Load data
            df = pd.read_excel(sample_file)
            self.log_test("Excel File Loading", "PASS",
                         f"Loaded {len(df)} rows, {len(df.columns)} columns")

            # Check required columns
            processor = FlexibleDataProcessor()
            required_cols = ['Date', 'Order ID', 'Product Name', 'Quantity', 'Price', 'Customer State', 'Total']

            # Try auto-mapping
            df_mapped = processor.auto_map_columns(df)
            missing_cols = set(required_cols) - set(df_mapped.columns)

            if not missing_cols:
                self.log_test("Column Mapping", "PASS", "All required columns present or mapped")
            else:
                self.log_test("Column Mapping", "FAIL", f"Missing columns: {missing_cols}")

            return df_mapped

        except Exception as e:
            self.log_test("Data Loading", "FAIL", str(e))
            return None

    def test_data_analysis(self, df):
        """Test 3: Data Analysis Functions"""
        print("\n" + "="*60)
        print("TEST 3: Data Analysis Functions")
        print("="*60)

        if df is None:
            self.log_test("Data Analysis", "SKIP", "No data available")
            return

        try:
            analyzer = SalesAnalyzer(df)

            # Test basic metrics
            metrics = analyzer.get_basic_metrics()
            if metrics and 'total_sales' in metrics:
                self.log_test("Basic Metrics Calculation", "PASS",
                             f"Total Sales: ${metrics['total_sales']:,.2f}")
            else:
                self.log_test("Basic Metrics Calculation", "FAIL", "Metrics not generated")

            # Test top products
            top_products = analyzer.get_top_products(n=5)
            if top_products is not None and len(top_products) > 0:
                self.log_test("Top Products Analysis", "PASS",
                             f"Found {len(top_products)} top products")
            else:
                self.log_test("Top Products Analysis", "FAIL", "No top products found")

            # Test sales by state
            state_sales = analyzer.get_sales_by_state()
            if state_sales is not None and len(state_sales) > 0:
                self.log_test("Sales by State Analysis", "PASS",
                             f"Analyzed {len(state_sales)} states")
            else:
                self.log_test("Sales by State Analysis", "FAIL", "No state data found")

            # Test daily sales trend
            daily_trend = analyzer.get_daily_sales_trend()
            if daily_trend is not None and len(daily_trend) > 0:
                self.log_test("Daily Sales Trend", "PASS",
                             f"Generated trend for {len(daily_trend)} days")
            else:
                self.log_test("Daily Sales Trend", "FAIL", "No trend data")

        except Exception as e:
            self.log_test("Data Analysis", "FAIL", f"Error: {str(e)}\n{traceback.format_exc()}")

    def test_ai_agent(self, df):
        """Test 4: AI Pandas Agent"""
        print("\n" + "="*60)
        print("TEST 4: AI Pandas Agent (Code Generation)")
        print("="*60)

        if df is None:
            self.log_test("AI Agent", "SKIP", "No data available")
            return

        if not self.api_key or not self.api_key.startswith('sk-'):
            self.log_test("AI Agent", "SKIP", "No valid API key")
            return

        try:
            agent = PandasAgent(df, self.api_key, debug_mode=True)

            # Test simple question
            question = "What is the total number of orders?"
            answer = agent.ask(question)

            if answer and len(answer) > 0:
                self.log_test("AI Q&A - Simple Query", "PASS", f"Answer: {answer[:100]}...")

                # Show generated code if available
                if hasattr(agent, 'last_generated_code') and agent.last_generated_code:
                    print(f"   Generated Code Preview:\n{agent.last_generated_code[:200]}...")
            else:
                self.log_test("AI Q&A - Simple Query", "FAIL", "Empty response")

            # Test complex question
            question2 = "What are the top 3 best-selling products by total sales?"
            answer2 = agent.ask(question2)

            if answer2 and len(answer2) > 0:
                self.log_test("AI Q&A - Complex Query", "PASS", f"Answer: {answer2[:100]}...")
            else:
                self.log_test("AI Q&A - Complex Query", "FAIL", "Empty response")

        except Exception as e:
            self.log_test("AI Agent", "FAIL", f"Error: {str(e)}\n{traceback.format_exc()}")

    def test_cost_controller(self):
        """Test 5: Cost Controller"""
        print("\n" + "="*60)
        print("TEST 5: Cost Controller")
        print("="*60)

        try:
            controller = CostController()

            # Test usage tracking
            can_use = controller.can_make_api_call()
            usage = controller.get_usage_stats()

            self.log_test("Cost Controller Initialization", "PASS",
                         f"Daily calls: {usage.get('daily_calls', 0)}, Can use API: {can_use}")

        except Exception as e:
            self.log_test("Cost Controller", "FAIL", str(e))

    def test_exporter(self, df):
        """Test 6: Data Exporter"""
        print("\n" + "="*60)
        print("TEST 6: Data Export Functionality")
        print("="*60)

        if df is None:
            self.log_test("Data Export", "SKIP", "No data available")
            return

        try:
            exporter = DataExporter()

            # Test DataFrame export
            excel_data = exporter.export_to_excel(df, filename="test_export.xlsx")

            if excel_data and len(excel_data) > 0:
                self.log_test("Excel Export", "PASS",
                             f"Generated {len(excel_data)} bytes")
            else:
                self.log_test("Excel Export", "FAIL", "No data generated")

        except Exception as e:
            self.log_test("Data Export", "FAIL", str(e))

    def test_ui_config(self):
        """Test 7: UI Configuration and Translations"""
        print("\n" + "="*60)
        print("TEST 7: UI Configuration and Translations")
        print("="*60)

        try:
            from config import UI_TEXT_EN, UI_TEXT_ZH

            # Check English texts
            if 'app_title' in UI_TEXT_EN:
                self.log_test("English UI Texts", "PASS",
                             f"Found {len(UI_TEXT_EN)} text entries")
            else:
                self.log_test("English UI Texts", "FAIL", "Missing text entries")

            # Check Chinese texts
            if 'app_title' in UI_TEXT_ZH:
                self.log_test("Chinese UI Texts", "PASS",
                             f"Found {len(UI_TEXT_ZH)} text entries")
            else:
                self.log_test("Chinese UI Texts", "FAIL", "Missing text entries")

        except Exception as e:
            self.log_test("UI Configuration", "FAIL", str(e))

    def generate_report(self):
        """Generate final test report"""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)

        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0

        print(f"Total Tests: {total}")
        print(f"Passed: {self.passed} ✅")
        print(f"Failed: {self.failed} ❌")
        print(f"Pass Rate: {pass_rate:.1f}%")

        # Determine overall status
        if pass_rate >= 90:
            status = "🎉 EXCELLENT"
        elif pass_rate >= 75:
            status = "✅ GOOD"
        elif pass_rate >= 50:
            status = "⚠️  NEEDS IMPROVEMENT"
        else:
            status = "❌ CRITICAL ISSUES"

        print(f"\nOverall Status: {status}")

        # Save detailed report
        report_path = "TEST_VALIDATION_REPORT.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# AI Excel Analyzer - Validation Test Report\n\n")
            f.write(f"**Test Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Overall Status:** {status}\n\n")
            f.write(f"## Summary\n\n")
            f.write(f"- Total Tests: {total}\n")
            f.write(f"- Passed: {self.passed} ✅\n")
            f.write(f"- Failed: {self.failed} ❌\n")
            f.write(f"- Pass Rate: {pass_rate:.1f}%\n\n")
            f.write(f"## Detailed Results\n\n")

            for result in self.results:
                status_emoji = "✅" if result['status'] == "PASS" else "❌"
                f.write(f"### {status_emoji} {result['test']}\n\n")
                f.write(f"- **Status:** {result['status']}\n")
                f.write(f"- **Time:** {result['timestamp']}\n")
                if result['details']:
                    f.write(f"- **Details:** {result['details']}\n")
                f.write("\n")

            f.write("\n## Application Access\n\n")
            f.write("The Streamlit application is running at:\n")
            f.write("- **Local URL:** http://localhost:8501\n\n")
            f.write("Open this URL in Chrome browser to test the UI.\n\n")

            f.write("## Testing Instructions for Chrome\n\n")
            f.write("1. Open Chrome browser\n")
            f.write("2. Navigate to http://localhost:8501\n")
            f.write("3. Test the following features:\n")
            f.write("   - Upload sample data file (sample_data/30days_sample.xlsx)\n")
            f.write("   - View dashboard and metrics\n")
            f.write("   - Ask questions in the Q&A section\n")
            f.write("   - Test data export functionality\n")
            f.write("   - Switch between English and Chinese languages\n")
            f.write("   - Test comparison features if available\n\n")

        print(f"\n📝 Detailed report saved to: {report_path}")

        return pass_rate >= 50  # Return success if pass rate >= 50%


def main():
    """Main test execution"""
    print("="*60)
    print("AI EXCEL ANALYZER - COMPREHENSIVE VALIDATION TEST")
    print("="*60)

    tester = ValidationTester()

    # Run all tests
    tester.test_environment()
    df = tester.test_data_loading()
    tester.test_data_analysis(df)
    tester.test_ai_agent(df)
    tester.test_cost_controller()
    tester.test_exporter(df)
    tester.test_ui_config()

    # Generate report
    success = tester.generate_report()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
