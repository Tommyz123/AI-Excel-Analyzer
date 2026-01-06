"""
Configuration file for AI Sales Analyzer
Contains all UI text (Bilingual: English & Chinese) and application settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

# UI Text Configuration - English
UI_TEXT_EN = {
    # App Header
    "app_title": "AI Sales Analyzer",
    "app_subtitle": "Upload Excel, Auto-Analyze, AI-Powered Insights",
    "language": "Language",
    
    # Sidebar
    "upload_section": "📁 Upload Sales Data",
    "upload_label": "Choose Excel or CSV file",
    "upload_help": "Supports Shopify exported sales reports",
    "api_key_label": "OpenAI API Key (Optional)",
    "api_key_help": "Leave empty to use default key",
    
    # Main Interface
    "welcome_message": "👈 Please upload your sales data file to start analysis",
    "success_upload": "✅ Successfully loaded {count} sales records",
    "processing": "🔄 Processing your data...",
    
    # Metrics Cards
    "total_sales": "Total Sales",
    "order_count": "Orders",
    "avg_order": "Avg Order Value",
    
    # Chart Titles
    "top_products": "📊 Top 5 Best-Selling Products",
    "daily_trend": "📈 Daily Sales Trend",
    "state_sales": "🗺️ Sales by State",
    "insights": "💡 Business Insights",
    
    # AI Q&A
    "ai_qa_title": "🤖 AI Assistant",
    "ai_qa_subtitle": "Ask me anything about your sales data...",
    "ai_qa_placeholder": "e.g., Which product sold the most on Monday?",
    "ai_qa_examples": [
        "Which product sold the most on Monday?",
        "What was the total sales on Nov 20?",
        "Which state had the highest sales?",
        "Show me the average order value"
    ],
    "ai_thinking": "🤔 AI is thinking...",
    "ai_answer_prefix": "**Answer:**",
    "ai_cached": "💾 Cached answer (no API cost)",
    "ai_local": "⚡ Answered locally (no API cost)",
    
    # Export
    "export_section": "📥 Export Analysis Results",
    "export_excel": "📊 Download Excel Report",
    "export_csv": "📄 Download CSV Data",
    
    # Templates
    "template_section": "📋 Data Templates",
    "template_blank": "📄 Blank Template",
    "template_sample": "📊 Sample Data",
    "template_blank_help": "Download empty template with correct columns",
    "template_sample_help": "Download sample data to test the app",
    
    # Privacy
    "privacy_title": "🔒 Privacy & Security",
    "privacy_content": """
    **Your Data is Safe:**
    
    ✅ No storage - data only in memory  
    ✅ Auto-deleted when you close browser  
    ✅ OpenAI API only for AI questions  
    ✅ No tracking or analytics  
    ✅ HTTPS encrypted connection
    """,
    
    # Error Messages
    "error_missing_columns": "❌ Your file is missing required columns: {columns}",
    "error_invalid_format": "❌ Invalid file format. Please upload .xlsx or .csv file",
    "error_file_too_large": "❌ File too large. Maximum size is {max_size}MB",
    "error_api_key": "⚠️ Please enter your OpenAI API Key in the sidebar to use AI features",
    "error_api_limit": "⚠️ {message}",
    "error_general": "❌ An error occurred: {error}",
    
    # Warnings
    "warning_data_quality": "⚠️ Data Quality Warnings",
    "warning_negative_qty": "⚠️ Found negative quantities - these may be returns/refunds",
    "warning_negative_total": "⚠️ Found negative totals - these may be refunds",
    "warning_date_range": "ℹ️ Data spans {days} days - consider analyzing by week",
    "warning_missing_values": "⚠️ Column '{column}' has {percent:.1f}% missing values",
    
    # Usage Guide
    "usage_steps": """
    ### How to Use:
    1. 📤 Upload your Shopify exported Excel/CSV file
    2. 📊 View automated sales analysis dashboard
    3. 🤖 Ask questions using AI assistant
    4. 📥 Download reports as needed
    
    ### Required Data Format:
    Your file must contain these columns:  
    `Date`, `Order ID`, `Product Name`, `Quantity`, `Price`, `Customer State`, `Total`
    """,
    
    # Format Guide
    "format_guide_title": "ℹ️ Data Format Guide",
    "format_guide_content": """
    **Required Columns:**
    - `Date`: Order date (YYYY-MM-DD)
    - `Order ID`: Unique order number
    - `Product Name`: Product name
    - `Quantity`: Number of items
    - `Price`: Unit price (USD)
    - `Customer State`: US state code (e.g., CA, NY)
    - `Total`: Total amount (USD)

    **Example:**
    | Date | Order ID | Product Name | Quantity | Price | Customer State | Total |
    |------|----------|--------------|----------|-------|----------------|-------|
    | 2024-11-18 | 1001 | Serum | 2 | 29.99 | CA | 59.98 |
    """,

    # ============= NEW KEYS FOR LANGUAGE SWITCHING =============

    # Hero Page
    "hero_slogan_title": "Understand Your Data in 30 Seconds",
    "hero_slogan_subtitle": "AI-Driven Excel Analysis - Making Data Insights Simple",
    "hero_steps_title": "Get Started in Three Steps",
    "hero_step1_title": "1. Upload Excel",
    "hero_step1_desc": "Supports .xlsx, .xls, .csv formats\nAuto-detect headers and data types\nFlexible format handling",
    "hero_step2_title": "2. AI Analysis",
    "hero_step2_desc": "Auto-generate visualization charts\nDiscover business insights\nProvide optimization suggestions",
    "hero_step3_title": "3. Export Report",
    "hero_step3_desc": "One-click export\nSave analysis results\nShare with team anytime",
    "hero_get_started": "👈 Upload files from the left sidebar to start, or load Demo data to experience",

    # Hero Features (4 cards)
    "hero_feature1_icon": "⚡",
    "hero_feature1_title": "Fast Analysis",
    "hero_feature1_desc": "Process data in seconds",
    "hero_feature2_icon": "🎯",
    "hero_feature2_title": "Precise Insights",
    "hero_feature2_desc": "AI-powered intelligence",
    "hero_feature3_icon": "📈",
    "hero_feature3_title": "Professional Charts",
    "hero_feature3_desc": "Visual presentation",
    "hero_feature4_icon": "🔒",
    "hero_feature4_title": "Data Security",
    "hero_feature4_desc": "Local processing",

    # Upload Mode
    "upload_mode_label": "Upload Mode",
    "upload_mode_single": "📄 Single File Analysis",
    "upload_mode_multi": "📊 Multi-File Comparison (2-3 files)",
    "upload_mode_multi_help": "Multi-file comparison: Upload 2-3 files for comparative analysis",
    "upload_mode_warning": "⚠️ Please upload 2-3 files (current: {count})",

    # File Labels
    "file_labels_title": "### 📝 Set File Labels",
    "file_labels_caption": "Give each file a name for easy comparison (e.g., November, December, January)",
    "file_label_input": "File {num} Label",

    # Demo Data
    "demo_section_title": "📦 Try Demo Data",
    "demo_scenario_label": "Select Scenario",
    "demo_scenario_ecommerce": "E-commerce Scenario",
    "demo_scenario_restaurant": "Restaurant Scenario",
    "demo_scenario_retail": "Retail Scenario",
    "demo_load_button": "🚀 Load Demo Data",
    "demo_loading": "Generating demo data...",
    "demo_success": "✅ {scenario} data loaded ({count} records)",
    "demo_error": "Demo data loading failed: {error}",

    # Chart Titles and Labels
    "chart_top_products_title": "🏆 Top 5 Best-Selling Products",
    "chart_top_products_ylabel": "Quantity (units)",
    "chart_top_products_hover": "<b>%{{y}}</b><br>Quantity: %{{x:,}} units<extra></extra>",
    "chart_sales_by_state_title": "📍 Sales Distribution by State",
    "chart_sales_by_state_xlabel": "State",
    "chart_sales_by_state_ylabel": "Sales ($)",
    "chart_sales_by_state_avg_line": "Average: ${avg:,.0f}",
    "chart_sales_by_state_hover": "<b>%{{x}}</b><br>Sales: $%{{y:,.2f}}<br>Rank: #%{{customdata}}<extra></extra>",
    "chart_daily_trend_title": "📊 Daily Sales Trend",
    "chart_daily_trend_xlabel": "Date",
    "chart_daily_trend_ylabel": "Sales ($)",
    "chart_daily_trend_max_label": "📈 Highest\n${amount:,.0f}",
    "chart_daily_trend_min_label": "📉 Lowest\n${amount:,.0f}",
    "chart_daily_trend_trend_legend": "Trend Line (R²={r2:.2f})",
    "chart_daily_trend_hover": "<b>%{{x|%m/%d}}</b><br>Sales: $%{{y:,.2f}}<extra></extra>",
    "chart_daily_trend_trend_hover": "<b>Trend</b><br>$%{{y:,.2f}}<extra></extra>",
    "chart_daily_trend_trace_name": "Daily Sales",
    "chart_daily_trend_warning": "⚠️ Trend line requires scipy library: `pip install scipy`",
    "chart_no_product_data": "No product data available",
    "chart_no_state_data": "No state sales data available",
    "chart_no_trend_data": "No daily sales data available",

    # Metrics Section
    "metrics_section_title": "### 📈 Core Metrics",
    "metrics_total_sales_label": "💰 Total Sales",
    "metrics_total_sales_subtitle": "{days} days of data",
    "metrics_order_count_label": "📦 Orders",
    "metrics_order_count_subtitle": "{products} unique products",
    "metrics_avg_order_label": "📊 Avg Order Value",
    "metrics_avg_order_subtitle": "Per order average",

    # Comparison Analysis (Week/Month)
    "comparison_section_title": "📊 Period Comparison Analysis",
    "comparison_growth_label_week": "Weekly Sales Growth",
    "comparison_growth_label_month": "Monthly Sales Growth",
    "comparison_current_week_label": "💰 This Week Sales",
    "comparison_current_week_subtitle": "{orders} orders",
    "comparison_previous_week_label": "📦 Last Week Sales",
    "comparison_previous_week_subtitle": "{orders} orders",
    "comparison_vs_label_week": "This Week vs Last Week",
    "comparison_vs_label_month": "This Month vs Last Month",
    "comparison_current_month_label": "💰 This Month Sales",
    "comparison_current_month_subtitle": "{orders} orders",
    "comparison_previous_month_label": "📦 Last Month Sales",
    "comparison_previous_month_subtitle": "{orders} orders",

    # Insights Section
    "insights_section_title": "🤖 AI Business Insights",
    "insights_category_opportunity": "🔥 Opportunities ({count})",
    "insights_category_risk": "⚠️ Risks ({count})",
    "insights_category_trend": "📊 Trends ({count})",
    "insights_no_data": "📊 No anomaly insights available",

    # Insights Templates (for analyzer.py)
    "insight_high_peak_title": "Sales Peak: {date}",
    "insight_high_peak_detail": "Sales on this day reached ${amount:,.2f}, {pct:.1f}% above average. Analyze marketing activities on this day to replicate success.",
    "insight_high_customer_value_title": "High Customer Value: ${avg:,.2f}",
    "insight_high_customer_value_detail": "Average order value exceeds $50, indicating strong purchasing power. Consider launching premium product bundles or membership programs to further increase order value.",
    "insight_growth_trend_title": "Growing Sales Trend: +{growth:.1f}%",
    "insight_growth_trend_detail": "Recent sales increased {growth:.1f}% compared to earlier period, showing healthy business growth. Maintain current strategy and consider scaling up.",
    "insight_low_day_title": "Sales Valley: {date}",
    "insight_low_day_detail": "Sales on this day reached ${amount:,.2f}, {pct:.1f}% below average. Need to identify causes of low-sales days (e.g., weekends, holidays) and adjust operations.",
    "insight_product_concentration_title": "High Product Concentration: {pct:.0f}%",
    "insight_product_concentration_detail": '"{product}" accounts for {pct:.0f}% of total sales ({qty:,} units). Over-reliance on single product poses risk, recommend diversifying product line.',
    "insight_region_concentration_title": "High Regional Concentration: {state} {pct:.0f}%",
    "insight_region_concentration_detail": "{state} accounts for {pct:.0f}% of total sales (${amount:,.2f}). Regional over-concentration poses risk, recommend expanding to other markets.",
    "insight_weekend_pattern_title": "{pattern} Sales Stronger: {diff:.0f}%",
    "insight_weekend_pattern_detail": "{pattern} daily average sales are {diff:.0f}% higher than {opposite}. Consider targeted promotions and inventory planning.",
    "insight_weekend_label": "Weekend",
    "insight_weekday_label": "Weekday",
    "insight_top3_contribution_title": "Top 3 Product Contribution: {pct:.0f}%",
    "insight_top3_contribution_detail": 'Top 3 products account for {pct:.0f}% of total sales, showing clear "head effect". Focus on maintaining supply chain and marketing for these star products.',
    "insight_business_model_title": "Business Model: {category}",
    "insight_business_model_detail": "Current average order value ${avg:.2f}, total {orders:,} orders. {suggestion}.",
    "insight_business_model_low_freq": "Low value, high frequency",
    "insight_business_model_mid": "Medium value",
    "insight_business_model_high_value": "High value, low frequency",
    "insight_business_model_suggestion_low": "Suitable for volume strategy, can increase order value through combo promotions",
    "insight_business_model_suggestion_mid": "Balanced business, can focus on both customer acquisition and increasing order value",
    "insight_business_model_suggestion_high": "Suitable for refined operations, focus on customer relationship management",
    "insight_price_dispersion_title": "Large Price Variation: CV={cv:.0f}%",
    "insight_price_dispersion_detail": "Product price coefficient of variation is {cv:.0f}%, indicating wide price range. Consider tiered price band management with strategies for different customer segments.",

    # Multi-File Comparison
    "multifile_title": "📊 Multi-File Comparison Analysis",
    "multifile_summary_title": "📈 Summary Comparison",
    "multifile_growth_title": "📊 Growth Analysis",
    "multifile_growth_subtitle": "Baseline: {baseline}",
    "multifile_charts_title": "📊 Comparison Charts",
    "multifile_chart_summary_title": "Sales, Orders, Average Order Comparison",
    "multifile_chart_summary_xlabel": "Metrics",
    "multifile_chart_summary_ylabel": "Value",
    "multifile_top_products_title": "🏆 Top Product Comparison",
    "multifile_top_products_subtitle": "Top 5 Product Sales Comparison",
    "multifile_daily_trend_title": "📈 Daily Sales Trend Comparison",
    "multifile_date_range_title": "📅 Data Range",

    # AI Assistant (Multi-File Mode)
    "ai_multifile_title": "🤖 AI Data Analysis Assistant",
    "ai_dataset_selector_label": "Select dataset to analyze",
    "ai_dataset_selector_format": "📊 {label} ({count} records)",
    "ai_dataset_selector_help": "Select a dataset for AI assistant to analyze",
    "ai_dataset_size_label": "Dataset Size",
    "ai_current_dataset_info": "💡 Currently analyzing: **{label}** dataset",

    # Multi-File Comparison - Dashboard
    "multifile_summary_metrics_title": "📈 Summary Metrics",
    "multifile_summary_total_sales": "Total Sales",
    "multifile_summary_order_count": "Orders",
    "multifile_summary_avg_order": "Avg Order",
    "multifile_growth_change_label": "Sales Change",
    "multifile_growth_order_qty": "Order Qty:",
    "multifile_growth_avg_order": "Avg Order:",
    "multifile_chart_products_title": "### 🏆 Top Product Comparison",
    "multifile_chart_trends_title": "### 📈 Daily Sales Trend Comparison",
    "multifile_chart_axis_metrics": "Metrics",
    "multifile_chart_axis_value": "Value",
    "multifile_chart_axis_product": "Product",
    "multifile_chart_axis_quantity": "Quantity",
    "multifile_chart_axis_date": "Date",
    "multifile_chart_axis_sales": "Sales ($)",
    "multifile_date_range_start": "Start:",
    "multifile_date_range_end": "End:",
    "multifile_date_range_days": "Days:",
    "multifile_date_range_no_data": "No date information",

    # Multi-File Upload Flow
    "multifile_processing": "Processing multiple files...",
    "multifile_success": "✅ {count} files loaded! Total {records} records",
    "multifile_warning_title": "⚠️ Data Quality Warnings",
    "multifile_error_failed": "Multi-file comparison failed: {error}",
    "multifile_error_format": "Please check file format. All files should have the same column structure.",
    "multifile_ai_title": "🤖 AI Data Analysis Assistant",
    "multifile_ai_selector_label": "Select dataset to analyze",
    "multifile_ai_selector_help": "Choose a dataset for AI assistant to analyze",
    "multifile_ai_dataset_size": "Dataset Size",
    "multifile_ai_dataset_unit": "records",
    "multifile_ai_current_info": "💡 Currently analyzing: **{label}** dataset",

    # Comparison Analyzer (for comparison_analyzer.py)
    "comparison_error_file_count": "Comparison feature supports 2-3 files",
    "comparison_default_label": "Dataset {num}",
    "comparison_error_label_mismatch": "Number of labels must match number of files",

    # View Raw Data
    "view_raw_data": "📄 View Raw Data"
}

# UI Text Configuration - Chinese (中文)
UI_TEXT_ZH = {
    # App Header
    "app_title": "AI 销售分析工具",
    "app_subtitle": "上传Excel，自动分析，AI智能洞察",
    "language": "语言",
    
    # Sidebar
    "upload_section": "📁 上传销售数据",
    "upload_label": "选择 Excel 或 CSV 文件",
    "upload_help": "支持 Shopify 导出的销售报表",
    "api_key_label": "OpenAI API 密钥（可选）",
    "api_key_help": "留空则使用默认密钥",
    
    # Main Interface
    "welcome_message": "👈 请上传您的销售数据文件开始分析",
    "success_upload": "✅ 成功加载 {count} 条销售记录",
    "processing": "🔄 正在处理您的数据...",
    
    # Metrics Cards
    "total_sales": "总销售额",
    "order_count": "订单数",
    "avg_order": "平均订单金额",
    
    # Chart Titles
    "top_products": "📊 Top 5 畅销产品",
    "daily_trend": "📈 每日销售趋势",
    "state_sales": "🗺️ 各州销售分布",
    "insights": "💡 商业洞察",
    
    # AI Q&A
    "ai_qa_title": "🤖 AI 助手",
    "ai_qa_subtitle": "向我提问关于您的销售数据...",
    "ai_qa_placeholder": "例如：周一哪个产品卖得最好？",
    "ai_qa_examples": [
        "周一哪个产品卖得最好？",
        "11月20日的总销售额是多少？",
        "哪个州的销售额最高？",
        "平均订单金额是多少？"
    ],
    "ai_thinking": "🤔 AI 正在思考...",
    "ai_answer_prefix": "**回答：**",
    "ai_cached": "💾 缓存回答（无API成本）",
    "ai_local": "⚡ 本地回答（无API成本）",
    
    # Export
    "export_section": "📥 导出分析结果",
    "export_excel": "📊 下载 Excel 报告",
    "export_csv": "📄 下载 CSV 数据",
    
    # Templates
    "template_section": "📋 数据模板",
    "template_blank": "📄 空白模板",
    "template_sample": "📊 示例数据",
    "template_blank_help": "下载包含正确列的空白模板",
    "template_sample_help": "下载示例数据测试应用",
    
    # Privacy
    "privacy_title": "🔒 隐私与安全",
    "privacy_content": """
    **您的数据是安全的：**
    
    ✅ 不存储 - 数据仅在内存中  
    ✅ 关闭浏览器后自动删除  
    ✅ OpenAI API 仅用于AI问答  
    ✅ 无跟踪或分析  
    ✅ HTTPS 加密连接
    """,
    
    # Error Messages
    "error_missing_columns": "❌ 您的文件缺少必需的列：{columns}",
    "error_invalid_format": "❌ 无效的文件格式。请上传 .xlsx 或 .csv 文件",
    "error_file_too_large": "❌ 文件过大。最大大小为 {max_size}MB",
    "error_api_key": "⚠️ 请在侧边栏输入您的 OpenAI API 密钥以使用 AI 功能",
    "error_api_limit": "⚠️ {message}",
    "error_general": "❌ 发生错误：{error}",
    
    # Warnings
    "warning_data_quality": "⚠️ 数据质量警告",
    "warning_negative_qty": "⚠️ 发现负数量 - 这些可能是退货/退款",
    "warning_negative_total": "⚠️ 发现负总额 - 这些可能是退款",
    "warning_date_range": "ℹ️ 数据跨度 {days} 天 - 建议按周分析",
    "warning_missing_values": "⚠️ 列 '{column}' 有 {percent:.1f}% 缺失值",
    
    # Usage Guide
    "usage_steps": """
    ### 使用方法：
    1. 📤 上传您的 Shopify 导出的 Excel/CSV 文件
    2. 📊 查看自动生成的销售分析仪表板
    3. 🤖 使用 AI 助手提问
    4. 📥 根据需要下载报告
    
    ### 所需数据格式：
    您的文件必须包含这些列：  
    `Date`, `Order ID`, `Product Name`, `Quantity`, `Price`, `Customer State`, `Total`
    """,
    
    # Format Guide
    "format_guide_title": "ℹ️ 数据格式指南",
    "format_guide_content": """
    **必需列：**
    - `Date`: 订单日期 (YYYY-MM-DD)
    - `Order ID`: 唯一订单号
    - `Product Name`: 产品名称
    - `Quantity`: 商品数量
    - `Price`: 单价 (USD)
    - `Customer State`: 美国州代码 (例如 CA, NY)
    - `Total`: 总金额 (USD)

    **示例：**
    | Date | Order ID | Product Name | Quantity | Price | Customer State | Total |
    |------|----------|--------------|----------|-------|----------------|-------|
    | 2024-11-18 | 1001 | 精华液 | 2 | 29.99 | CA | 59.98 |
    """,

    # ============= NEW KEYS FOR LANGUAGE SWITCHING =============

    # Hero Page
    "hero_slogan_title": "30秒看懂你的数据",
    "hero_slogan_subtitle": "AI驱动的Excel分析 - 让数据洞察变得简单",
    "hero_steps_title": "三步开始分析",
    "hero_step1_title": "1. 上传Excel",
    "hero_step1_desc": "支持 .xlsx, .xls, .csv 格式\n自动识别表头和数据类型\n灵活的格式处理",
    "hero_step2_title": "2. AI分析",
    "hero_step2_desc": "自动生成可视化图表\n发现业务洞察\n提供优化建议",
    "hero_step3_title": "3. 导出报告",
    "hero_step3_desc": "一键导出\n保存分析结果\n随时分享给团队",
    "hero_get_started": "👈 从左侧边栏上传文件开始，或加载Demo数据体验",

    # Hero Features (4 cards)
    "hero_feature1_icon": "⚡",
    "hero_feature1_title": "快速分析",
    "hero_feature1_desc": "秒级处理数据",
    "hero_feature2_icon": "🎯",
    "hero_feature2_title": "精准洞察",
    "hero_feature2_desc": "AI驱动智能",
    "hero_feature3_icon": "📈",
    "hero_feature3_title": "专业图表",
    "hero_feature3_desc": "可视化呈现",
    "hero_feature4_icon": "🔒",
    "hero_feature4_title": "数据安全",
    "hero_feature4_desc": "本地处理",

    # Upload Mode
    "upload_mode_label": "上传模式",
    "upload_mode_single": "📄 单文件分析",
    "upload_mode_multi": "📊 多文件对比 (2-3个文件)",
    "upload_mode_multi_help": "多文件对比：上传2-3个文件进行对比分析",
    "upload_mode_warning": "⚠️ 请上传2-3个文件（当前：{count}个）",

    # File Labels
    "file_labels_title": "### 📝 为文件设置标签",
    "file_labels_caption": "给每个文件起个名字，方便对比（如：11月、12月、1月）",
    "file_label_input": "文件 {num} 标签",

    # Demo Data
    "demo_section_title": "📦 试用Demo数据",
    "demo_scenario_label": "选择场景",
    "demo_scenario_ecommerce": "电商场景",
    "demo_scenario_restaurant": "餐饮场景",
    "demo_scenario_retail": "零售场景",
    "demo_load_button": "🚀 加载Demo数据",
    "demo_loading": "正在生成Demo数据...",
    "demo_success": "✅ {scenario}数据加载成功（{count}条记录）",
    "demo_error": "Demo数据加载失败：{error}",

    # Chart Titles and Labels
    "chart_top_products_title": "🏆 Top 5 畅销产品",
    "chart_top_products_ylabel": "销量（件）",
    "chart_top_products_hover": "<b>%{{y}}</b><br>销量：%{{x:,}}件<extra></extra>",
    "chart_sales_by_state_title": "📍 各州销售分布",
    "chart_sales_by_state_xlabel": "州",
    "chart_sales_by_state_ylabel": "销售额（$）",
    "chart_sales_by_state_avg_line": "平均值：${avg:,.0f}",
    "chart_sales_by_state_hover": "<b>%{{x}}</b><br>销售额：$%{{y:,.2f}}<br>排名：#%{{customdata}}<extra></extra>",
    "chart_daily_trend_title": "📊 每日销售趋势",
    "chart_daily_trend_xlabel": "日期",
    "chart_daily_trend_ylabel": "销售额（$）",
    "chart_daily_trend_max_label": "📈 最高\n${amount:,.0f}",
    "chart_daily_trend_min_label": "📉 最低\n${amount:,.0f}",
    "chart_daily_trend_trend_legend": "趋势线（R²={r2:.2f}）",
    "chart_daily_trend_hover": "<b>%{{x|%m/%d}}</b><br>销售额：$%{{y:,.2f}}<extra></extra>",
    "chart_daily_trend_trend_hover": "<b>趋势</b><br>$%{{y:,.2f}}<extra></extra>",
    "chart_daily_trend_trace_name": "每日销售额",
    "chart_daily_trend_warning": "⚠️ 趋势线需要 scipy 库：`pip install scipy`",
    "chart_no_product_data": "暂无产品数据",
    "chart_no_state_data": "暂无州销售数据",
    "chart_no_trend_data": "暂无每日销售数据",

    # Metrics Section
    "metrics_section_title": "### 📈 核心指标",
    "metrics_total_sales_label": "💰 总销售额",
    "metrics_total_sales_subtitle": "{days}天数据",
    "metrics_order_count_label": "📦 订单数",
    "metrics_order_count_subtitle": "{products}种产品",
    "metrics_avg_order_label": "📊 平均订单",
    "metrics_avg_order_subtitle": "每单均价",

    # Comparison Analysis (Week/Month)
    "comparison_section_title": "📊 周期对比分析",
    "comparison_growth_label_week": "周销售增长",
    "comparison_growth_label_month": "月销售增长",
    "comparison_current_week_label": "💰 本周销售",
    "comparison_current_week_subtitle": "{orders}个订单",
    "comparison_previous_week_label": "📦 上周销售",
    "comparison_previous_week_subtitle": "{orders}个订单",
    "comparison_vs_label_week": "本周 vs 上周",
    "comparison_vs_label_month": "本月 vs 上月",
    "comparison_current_month_label": "💰 本月销售",
    "comparison_current_month_subtitle": "{orders}个订单",
    "comparison_previous_month_label": "📦 上月销售",
    "comparison_previous_month_subtitle": "{orders}个订单",

    # Insights Section
    "insights_section_title": "🤖 AI商业洞察",
    "insights_category_opportunity": "🔥 机会（{count}个）",
    "insights_category_risk": "⚠️ 风险（{count}个）",
    "insights_category_trend": "📊 趋势（{count}个）",
    "insights_no_data": "📊 暂无异常洞察",

    # Insights Templates (for analyzer.py)
    "insight_high_peak_title": "销售高峰日：{date}",
    "insight_high_peak_detail": "该日销售额 ${amount:,.2f}，比日均高 {pct:.1f}%。分析该日的营销活动或外部因素，可复制成功经验。",
    "insight_high_customer_value_title": "高客单价：${avg:,.2f}",
    "insight_high_customer_value_detail": "平均订单金额超过$50，说明客户购买力较强。可考虑推出高端产品组合或会员计划，进一步提升客单价。",
    "insight_growth_trend_title": "增长趋势：+{growth:.1f}%",
    "insight_growth_trend_detail": "最近销售额比早期增长了 {growth:.1f}%，显示业务健康增长。保持当前策略并考虑扩大规模。",
    "insight_low_day_title": "销售低谷日：{date}",
    "insight_low_day_detail": "该日销售额 ${amount:,.2f}，比日均低 {pct:.1f}%。需识别低销售日的成因（如周末、节假日），调整运营策略。",
    "insight_product_concentration_title": "产品集中度高：{pct:.0f}%",
    "insight_product_concentration_detail": '"{product}"占总销售额的 {pct:.0f}%（{qty:,}件）。过度依赖单一产品有风险，建议丰富产品线。',
    "insight_region_concentration_title": "区域集中度高：{state} {pct:.0f}%",
    "insight_region_concentration_detail": "{state}占总销售额的 {pct:.0f}%（${amount:,.2f}）。区域过度集中有风险，建议拓展其他市场。",
    "insight_weekend_pattern_title": "{pattern}销售更强：{diff:.0f}%",
    "insight_weekend_pattern_detail": "{pattern}日均销售额比{opposite}高 {diff:.0f}%。可针对性促销和库存规划。",
    "insight_weekend_label": "周末",
    "insight_weekday_label": "工作日",
    "insight_top3_contribution_title": "Top 3产品贡献：{pct:.0f}%",
    "insight_top3_contribution_detail": 'Top 3产品占总销售额的 {pct:.0f}%，呈现明显"头部效应"。重点维护这些明星产品的供应链和营销。',
    "insight_business_model_title": "业务模式：{category}",
    "insight_business_model_detail": "当前平均订单金额 ${avg:.2f}，共 {orders:,}个订单。{suggestion}。",
    "insight_business_model_low_freq": "低值高频",
    "insight_business_model_mid": "中值",
    "insight_business_model_high_value": "高值低频",
    "insight_business_model_suggestion_low": "适合走量策略，可通过组合促销提升客单价",
    "insight_business_model_suggestion_mid": "业务均衡，可同时关注拉新和提升客单价",
    "insight_business_model_suggestion_high": "适合精细化运营，注重客户关系管理",
    "insight_price_dispersion_title": "价格波动大：CV={cv:.0f}%",
    "insight_price_dispersion_detail": "产品价格变异系数为 {cv:.0f}%，说明价格分布较广。建议分层价格带管理，针对不同客户群制定策略。",

    # Multi-File Comparison
    "multifile_title": "📊 多文件对比分析",
    "multifile_summary_title": "📈 汇总对比",
    "multifile_growth_title": "📊 增长分析",
    "multifile_growth_subtitle": "基准：{baseline}",
    "multifile_charts_title": "📊 对比图表",
    "multifile_chart_summary_title": "销售额、订单数、平均订单对比",
    "multifile_chart_summary_xlabel": "指标",
    "multifile_chart_summary_ylabel": "数值",
    "multifile_top_products_title": "🏆 畅销产品对比",
    "multifile_top_products_subtitle": "Top 5产品销量对比",
    "multifile_daily_trend_title": "📈 每日销售趋势对比",
    "multifile_date_range_title": "📅 数据范围",

    # AI Assistant (Multi-File Mode)
    "ai_multifile_title": "🤖 AI数据分析助手",
    "ai_dataset_selector_label": "选择要分析的数据集",
    "ai_dataset_selector_format": "📊 {label}（{count}条记录）",
    "ai_dataset_selector_help": "选择一个数据集供AI助手分析",
    "ai_dataset_size_label": "数据集大小",
    "ai_current_dataset_info": "💡 当前分析：**{label}** 数据集",

    # Multi-File Comparison - Dashboard
    "multifile_summary_metrics_title": "📈 汇总指标",
    "multifile_summary_total_sales": "总销售额",
    "multifile_summary_order_count": "订单数",
    "multifile_summary_avg_order": "平均订单",
    "multifile_growth_change_label": "销售额变化",
    "multifile_growth_order_qty": "订单量：",
    "multifile_growth_avg_order": "平均订单：",
    "multifile_chart_products_title": "### 🏆 Top产品对比",
    "multifile_chart_trends_title": "### 📈 每日销售趋势对比",
    "multifile_chart_axis_metrics": "指标",
    "multifile_chart_axis_value": "数值",
    "multifile_chart_axis_product": "产品",
    "multifile_chart_axis_quantity": "销量",
    "multifile_chart_axis_date": "日期",
    "multifile_chart_axis_sales": "销售额 ($)",
    "multifile_date_range_start": "开始：",
    "multifile_date_range_end": "结束：",
    "multifile_date_range_days": "天数：",
    "multifile_date_range_no_data": "无日期信息",

    # Multi-File Upload Flow
    "multifile_processing": "正在处理多个文件...",
    "multifile_success": "✅ {count}个文件已加载！总计 {records}条记录",
    "multifile_warning_title": "⚠️ 数据质量警告",
    "multifile_error_failed": "多文件对比失败：{error}",
    "multifile_error_format": "请检查文件格式是否正确。所有文件应包含相同的列结构。",
    "multifile_ai_title": "🤖 AI 数据分析助手",
    "multifile_ai_selector_label": "选择要分析的数据集",
    "multifile_ai_selector_help": "选择一个数据集，AI助手将分析该数据集",
    "multifile_ai_dataset_size": "数据集大小",
    "multifile_ai_dataset_unit": "条",
    "multifile_ai_current_info": "💡 当前正在分析：**{label}**数据集",

    # Comparison Analyzer (for comparison_analyzer.py)
    "comparison_error_file_count": "对比功能支持2-3个文件",
    "comparison_default_label": "数据集 {num}",
    "comparison_error_label_mismatch": "标签数量必须与文件数量一致",

    # View Raw Data
    "view_raw_data": "📄 查看原始数据"
}

# Default to English, but can be changed
UI_TEXT = UI_TEXT_EN

# Application Configuration
class Config:
    """Application configuration"""
    
    # OpenAI Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "300"))
    OPENAI_TEMPERATURE = 0
    OPENAI_TIMEOUT = 15
    
    # App Settings
    APP_TITLE = os.getenv("APP_TITLE", "AI Sales Analyzer")
    APP_ICON = os.getenv("APP_ICON", "📊")
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    
    # API Cost Control
    MAX_DAILY_API_CALLS = int(os.getenv("MAX_DAILY_API_CALLS", "1000"))
    MAX_WEEKLY_API_CALLS = int(os.getenv("MAX_WEEKLY_API_CALLS", "5000"))
    
    # Data Validation
    REQUIRED_COLUMNS = os.getenv(
        "REQUIRED_COLUMNS",
        "Date,Order ID,Product Name,Quantity,Price,Customer State,Total"
    ).split(",")
    
    # Column Mappings (for Shopify compatibility)
    COLUMN_MAPPINGS = {
        'Date': ['Date', 'Order Date', 'Created at', 'date', 'order_date'],
        'Order ID': ['Order ID', 'Order_ID', 'Order Number', 'Name', 'order_id', 'id', 'Order'],
        'Product Name': ['Product Name', 'Product_Name', 'Lineitem name', 'Title', 'product', 'item', 'Product'],
        'Quantity': ['Quantity', 'Lineitem quantity', 'Qty', 'quantity', 'qty'],
        'Price': ['Price', 'Lineitem price', 'Unit Price', 'price', 'unit_price'],
        'Customer State': ['Customer State', 'Shipping Province', 'State', 'state', 'province', 'Shipping State'],
        'Total': ['Total', 'Subtotal', 'Amount', 'total', 'amount']
    }
