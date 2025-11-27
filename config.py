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
    """
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
    """
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
