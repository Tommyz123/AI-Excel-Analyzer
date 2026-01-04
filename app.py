"""
AI Sales Analyzer - Main Application
Streamlit web application for automated sales analysis
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from config import Config, UI_TEXT_EN as UI_TEXT
from utils.data_processor import FlexibleDataProcessor
from utils.analyzer import SalesAnalyzer
from utils.pandas_agent import PandasAgent  # Changed from AIAgent
from utils.exporter import DataExporter
from utils.template_generator import TemplateGenerator
from utils.cost_controller import CostController


# ==================== 配置常量（未来可提取为config_extended.py）====================
class ChartColors:
    """
    图表配色方案（便于统一修改和主题切换）

    设计考虑：
    - ✅ 当前：直接在代码中定义，简单快速
    - 🔄 未来：可一键提取为 config_extended.py（只需剪切粘贴+import）
    - 🔄 扩展性：便于支持多主题（深色模式、高对比度等）
    """
    PRIMARY = '#1f77b4'      # 深蓝 - 主要图表色
    ACCENT = '#ff7f0e'       # 橙色 - 强调/高亮色
    LIGHT_BLUE = '#aec7e8'   # 浅蓝 - 填充色
    APPLE_BLUE = '#007AFF'   # Apple蓝 - 按钮色
    SUCCESS = '#d4edda'      # 绿色 - 成功/机会背景
    WARNING = '#fff3cd'      # 黄色 - 警告背景
    DANGER = '#f8d7da'       # 红色 - 危险/错误背景
    INFO = '#d1ecf1'         # 信息蓝 - 提示背景

class UIConfig:
    """
    UI配置（便于后续扩展）

    设计考虑：
    - ✅ 当前：集中定义常量，避免魔法数字
    - 🔄 未来：可扩展为响应式配置、A/B测试等
    """
    CHART_HEIGHT = 450           # 图表默认高度
    CHART_HEIGHT_MOBILE = 300    # 移动端图表高度
    TITLE_FONT_SIZE = 18         # 图表标题字号
    LINE_WIDTH = 4               # 折线图线宽
    MARKER_SIZE = 8              # 数据点标记大小
    BORDER_RADIUS = 16           # 卡片圆角
# ===============================================================================


# Page configuration
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon=Config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Minimalist Clean Theme (Apple Style)
st.markdown("""
    <style>
        /* CSS Color Variables - Centralized Theme Management */
        :root {
            --primary-blue: #1f77b4;      /* Deep blue for primary charts */
            --accent-orange: #ff7f0e;     /* Orange for highlights/accents */
            --light-blue: #aec7e8;        /* Light blue for fills */
            --apple-blue: #007AFF;        /* Apple system blue for buttons */
            --success-green: #d4edda;     /* Success/opportunity background */
            --warning-yellow: #fff3cd;    /* Warning background */
            --danger-red: #f8d7da;        /* Danger/error background */
            --info-blue: #d1ecf1;         /* Info background */
            --text-primary: #1D1D1F;      /* Primary text color */
            --text-secondary: #86868B;    /* Secondary/muted text */
            --bg-primary: #F5F5F7;        /* Page background */
            --bg-card: #FFFFFF;           /* Card/widget background */
            --border-light: rgba(0,0,0,0.05);
        }

        /* Import Inter font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Global Reset & Typography */
        html, body, [class*="css"] {
            font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
            color: #1D1D1F !important;
            background-color: #F5F5F7 !important;
        }
        
        /* Hide default header and footer */
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Custom Navbar Styling - Glassmorphism */
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(0,0,0,0.05);
            padding: 0.8rem 2rem;
            z-index: 99999;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .navbar-brand {
            font-weight: 600;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #1D1D1F;
        }
        
        /* Adjust main content padding for fixed navbar */
        .main .block-container {
            padding-top: 6rem !important;
            max-width: 1200px !important;
        }
        
        /* Card Styling (Minimalist) */
        .saas-card {
            background-color: #FFFFFF;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
            margin-bottom: 20px;
            border: none;
            transition: transform 0.2s ease;
        }
        
        .saas-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
        }
        
        .metric-label {
            color: #86868B;
            font-size: 0.8rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 8px;
        }
        
        .metric-value {
            color: #1D1D1F;
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: -0.03em;
        }
        
        /* Streamlit Metric Override */
        div[data-testid="stMetric"] {
            background-color: #FFFFFF !important;
            border: none !important;
            padding: 20px !important;
            border-radius: 16px !important;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04) !important;
        }
        
        div[data-testid="stMetricLabel"] {
            color: #86868B !important;
        }
        
        div[data-testid="stMetricValue"] {
            color: #1D1D1F !important;
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid rgba(0,0,0,0.05) !important;
            top: 0 !important; /* Fix for some streamlit versions */
            padding-top: 4rem !important;
        }
        
        /* Button Styling - Apple Blue */
        div.stButton > button {
            background-color: #007AFF !important;
            color: white !important;
            border-radius: 999px !important; /* Pill shape */
            border: none !important;
            padding: 0.6rem 1.5rem !important;
            font-weight: 500 !important;
            font-size: 0.95rem !important;
            box-shadow: 0 2px 10px rgba(0, 122, 255, 0.2) !important;
            transition: all 0.2s ease !important;
        }
        
        div.stButton > button:hover {
            background-color: #0062CC !important;
            transform: scale(1.02);
            box-shadow: 0 4px 15px rgba(0, 122, 255, 0.3) !important;
        }
        
        /* Secondary/Download Buttons */
        div.stDownloadButton > button {
            background-color: #F5F5F7 !important;
            color: #007AFF !important;
            border: 1px solid rgba(0,0,0,0.05) !important;
        }
        
        div.stDownloadButton > button:hover {
            background-color: #E5E5EA !important;
            border-color: rgba(0,0,0,0.1) !important;
        }
        
        /* Inputs */
        .stTextInput input, .stSelectbox div[data-baseweb="select"] {
            border-radius: 12px !important;
            border: 1px solid #E5E5EA !important;
            background-color: #FFFFFF !important;
            padding: 10px !important;
        }
        
        .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
            border-color: #007AFF !important;
            box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1) !important;
        }
        
        /* Charts Container */
        .js-plotly-plot {
            background-color: #FFFFFF;
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
        }
        
    </style>
    
    <!-- Custom Navbar HTML -->
    <div class="navbar">
        <div class="navbar-brand">
            <span>📊</span> AI Sales Analyzer
        </div>
        <div style="font-size: 0.8rem; color: #86868B;">
            Professional Edition
        </div>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None
if 'ai_agent' not in st.session_state:
    st.session_state.ai_agent = None

# Clear AI cache on startup or when new data is uploaded
import os
if 'cache_cleared' not in st.session_state:
    cache_file = '.qa_cache.json'
    if os.path.exists(cache_file):
        try:
            os.remove(cache_file)
        except:
            pass
    st.session_state.cache_cleared = True



def show_hero_page():
    """
    Display hero/welcome page with slogan and 3-step process

    设计考虑：
    - 使用ChartColors配色保持一致性
    - 简洁的3步流程说明
    - 友好的视觉引导
    """
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # Hero Slogan
    st.markdown(f"""
        <div style='text-align: center; padding: 3rem 1rem 2rem 1rem;'>
            <h1 style='font-size: 2.8rem; font-weight: 700; color: {ChartColors.PRIMARY};
                       margin-bottom: 1rem; letter-spacing: -0.02em;'>
                30秒看懂你的数据
            </h1>
            <p style='font-size: 1.3rem; color: #86868B; font-weight: 400;'>
                AI驱动的Excel分析 - 让数据洞察变得简单
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # 3-Step Process Cards
    st.markdown("""
        <div style='text-align: center; margin-bottom: 1rem;'>
            <h3 style='color: #1D1D1F; font-weight: 600;'>三步开始分析</h3>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class='saas-card' style='text-align: center; min-height: 240px;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>📤</div>
                <h4 style='color: {ChartColors.PRIMARY}; font-weight: 600; margin-bottom: 0.8rem;'>
                    1. 上传Excel
                </h4>
                <p style='color: #86868B; font-size: 0.95rem; line-height: 1.6;'>
                    支持 .xlsx, .xls, .csv 格式<br/>
                    自动识别表头和数据类型<br/>
                    灵活处理各种格式
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class='saas-card' style='text-align: center; min-height: 240px;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>🤖</div>
                <h4 style='color: {ChartColors.ACCENT}; font-weight: 600; margin-bottom: 0.8rem;'>
                    2. AI分析
                </h4>
                <p style='color: #86868B; font-size: 0.95rem; line-height: 1.6;'>
                    自动生成可视化图表<br/>
                    智能发现业务洞察<br/>
                    提供优化建议
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class='saas-card' style='text-align: center; min-height: 240px;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>📊</div>
                <h4 style='color: #34C759; font-weight: 600; margin-bottom: 0.8rem;'>
                    3. 导出报告
                </h4>
                <p style='color: #86868B; font-size: 0.95rem; line-height: 1.6;'>
                    一键导出PDF报告<br/>
                    保存分析结果<br/>
                    随时分享团队
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # Call to Action
    st.markdown("""
        <div style='text-align: center;'>
            <p style='color: #86868B; font-size: 1rem; margin-bottom: 1.5rem;'>
                👈 从左侧边栏上传文件开始，或加载Demo数据体验
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Feature highlights
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    col_a, col_b, col_c, col_d = st.columns(4)

    features = [
        ("⚡", "快速分析", "秒级处理数据"),
        ("🎯", "精准洞察", "AI驱动智能"),
        ("📈", "专业图表", "可视化呈现"),
        ("🔒", "数据安全", "本地处理")
    ]

    for col, (icon, title, desc) in zip([col_a, col_b, col_c, col_d], features):
        with col:
            st.markdown(f"""
                <div style='text-align: center; padding: 1rem;'>
                    <div style='font-size: 2rem; margin-bottom: 0.5rem;'>{icon}</div>
                    <div style='font-weight: 600; color: #1D1D1F; margin-bottom: 0.3rem;'>{title}</div>
                    <div style='font-size: 0.85rem; color: #86868B;'>{desc}</div>
                </div>
            """, unsafe_allow_html=True)


def show_header():
    """Display application header"""
    st.title(f"{Config.APP_ICON} {UI_TEXT['app_title']}")
    st.markdown(f"*{UI_TEXT['app_subtitle']}*")
    st.divider()


def show_sidebar():
    """Display sidebar with file upload and templates"""
    with st.sidebar:
        st.header(UI_TEXT["upload_section"])
        
        # File uploader
        uploaded_file = st.file_uploader(
            UI_TEXT["upload_label"],
            type=['xlsx', 'csv'],
            help=UI_TEXT["upload_help"]
        )
        
        # API Key input
        st.divider()
        api_key = st.text_input(
            UI_TEXT["api_key_label"],
            type="password",
            help=UI_TEXT["api_key_help"]
        )
        
        # Use config key if not provided
        if not api_key:
            api_key = Config.OPENAI_API_KEY
        
        # Templates section
        st.divider()
        st.subheader(UI_TEXT["template_section"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            blank_template = TemplateGenerator.generate_blank_template()
            st.download_button(
                label=UI_TEXT["template_blank"],
                data=blank_template,
                file_name="sales_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help=UI_TEXT["template_blank_help"]
            )
        
        with col2:
            sample_data = TemplateGenerator.generate_sample_data()
            st.download_button(
                label=UI_TEXT["template_sample"],
                data=sample_data,
                file_name="sales_sample.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help=UI_TEXT["template_sample_help"]
            )
        
        # Format guide
        with st.expander(UI_TEXT["format_guide_title"]):
            st.markdown(UI_TEXT["format_guide_content"])
        
        # Privacy notice
        st.divider()
        with st.expander(UI_TEXT["privacy_title"]):
            st.markdown(UI_TEXT["privacy_content"])
        
        # API usage stats (if AI agent exists)
        if st.session_state.ai_agent:
            show_api_usage()
        
        return uploaded_file, api_key


def show_api_usage():
    """Display API usage statistics"""
    controller = CostController()
    stats = controller.get_usage_stats()
    
    st.divider()
    st.subheader("💰 API Usage")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Today",
            f"{stats['daily_calls']}/{stats['daily_limit']}"
        )
    with col2:
        st.metric(
            "This Week",
            f"{stats['weekly_calls']}/{stats['weekly_limit']}"
        )
    
    st.metric(
        "Est. Monthly Cost",
        f"${stats['estimated_cost_month']:.2f}"
    )
    
    # Progress bar
    daily_progress = stats['daily_calls'] / stats['daily_limit']
    st.progress(daily_progress, text=f"Daily: {daily_progress*100:.0f}%")


def show_dashboard(analyzer: SalesAnalyzer):
    """Display main dashboard with metrics and charts"""
    
    # Key metrics (Custom SaaS Cards)
    with st.container():
        st.markdown("### 📈 核心指标")
        stats = analyzer.get_summary_stats()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="saas-card">
                    <div class="metric-label">{UI_TEXT["total_sales"]}</div>
                    <div class="metric-value">${stats['total_sales']:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="saas-card">
                    <div class="metric-label">{UI_TEXT["order_count"]}</div>
                    <div class="metric-value">{stats['order_count']:,}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="saas-card">
                    <div class="metric-label">{UI_TEXT["avg_order"]}</div>
                    <div class="metric-value">${stats['avg_order_value']:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Top 5 Products
        st.subheader(UI_TEXT["top_products"])
        top_products = analyzer.get_top_products()
        
        fig1 = px.bar(
            x=top_products.values,
            y=top_products.index,
            orientation='h',
            labels={'x': 'Quantity Sold', 'y': 'Product'},
            color=top_products.values,
            color_continuous_scale='Blues'
        )
        fig1.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_right:
        # Sales by State
        st.subheader(UI_TEXT["state_sales"])
        state_sales = analyzer.get_sales_by_state()
        
        fig2 = px.bar(
            x=state_sales.index,
            y=state_sales.values,
            labels={'x': 'State', 'y': 'Sales ($)'},
            color=state_sales.values,
            color_continuous_scale='Greens'
        )
        fig2.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Daily Trend (full width)
    st.subheader(UI_TEXT["daily_trend"])
    daily_trend = analyzer.get_daily_trend()
    
    fig3 = px.line(
        x=daily_trend.index,
        y=daily_trend.values,
        labels={'x': 'Date', 'y': 'Sales ($)'},
        markers=True
    )
    fig3.update_traces(line_color='#FF6B6B', line_width=3)
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)
    
    # Business Insights
    st.divider()
    st.subheader(UI_TEXT["insights"])
    insights = analyzer.detect_anomalies()
    
    if insights:
        for insight in insights:
            st.info(insight)
    else:
        st.info("No unusual patterns detected. Sales are consistent!")


def show_export_section(analyzer: SalesAnalyzer):
    """Display export options"""
    st.divider()
    st.subheader(UI_TEXT["export_section"])
    
    exporter = DataExporter(analyzer)
    
    col1, col2 = st.columns(2)
    
    with col1:
        excel_data = exporter.export_to_excel()
        st.download_button(
            label=UI_TEXT["export_excel"],
            data=excel_data,
            file_name=exporter.get_filename('xlsx'),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col2:
        csv_data = exporter.export_to_csv()
        st.download_button(
            label=UI_TEXT["export_csv"],
            data=csv_data,
            file_name=exporter.get_filename('csv'),
            mime="text/csv"
        )


def show_ai_assistant(analyzer: SalesAnalyzer, api_key: str):
    """Display AI Q&A interface with chat history and download"""
    st.divider()
    st.subheader(UI_TEXT["ai_qa_title"])
    st.markdown(f"*{UI_TEXT['ai_qa_subtitle']}*")
    
    # Initialize AI agent if not exists
    if st.session_state.ai_agent is None:
        try:
            st.session_state.ai_agent = PandasAgent(
                st.session_state.df,
                api_key,
                debug_mode=True  # Enable debug mode to show generated code
            )
        except Exception as e:
            st.error(f"Failed to initialize AI Agent: {str(e)}")
            return
            
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Check if API key is valid
    if not api_key or not api_key.strip() or api_key == "your-api-key-here":
        st.warning(UI_TEXT["error_api_key"])
        return

    # Chat Interface Container
    with st.container():
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Welcome message if history is empty
        if not st.session_state.chat_history:
            with st.chat_message("assistant"):
                st.write(f"👋 {UI_TEXT['ai_qa_subtitle']}")
                st.markdown("**您可以试着问我：**")
                for example in UI_TEXT["ai_qa_examples"][:3]:
                    st.markdown(f"- {example}")

        # Question input
        if question := st.chat_input(UI_TEXT["ai_qa_placeholder"]):
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": question})
            
            # Display user message immediately
            with st.chat_message("user"):
                st.write(question)

            # Check API limits
            controller = CostController()
            can_call, message = controller.can_make_call()
            
            if not can_call:
                st.error(UI_TEXT["error_api_limit"].format(message=message))
                return
            
            # Get answer
            with st.chat_message("assistant"):
                with st.spinner(UI_TEXT["ai_thinking"]):
                    answer = st.session_state.ai_agent.ask(question)
                    
                    # Record API call
                    controller.record_call()
                    
                    st.markdown(answer)
                    
                    # Add assistant response to history
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})

    # Download Chat History
    if st.session_state.chat_history:
        st.divider()
        chat_text = "AI Sales Analyzer - Chat History\n================================\n\n"
        for msg in st.session_state.chat_history:
            role = "User" if msg["role"] == "user" else "AI"
            chat_text += f"{role}:\n{msg['content']}\n\n{'-'*40}\n\n"
            
        st.download_button(
            label="📥 下载对话记录",
            data=chat_text,
            file_name="chat_history.txt",
            mime="text/plain"
        )


def main():
    """Main application logic"""
    # show_header() # Disabled for custom navbar
    
    # Sidebar
    uploaded_file, api_key = show_sidebar()
    
    # Main content
    if uploaded_file is not None:
        # Process file
        try:
            with st.spinner(UI_TEXT["processing"]):
                processor = FlexibleDataProcessor()
                df, warnings = processor.process_file(uploaded_file)
                
                # Store in session state
                st.session_state.df = df
                st.session_state.analyzer = SalesAnalyzer(df)
                st.session_state.ai_agent = None  # Reset AI agent for new data
            
            # Success message
            st.success(UI_TEXT["success_upload"].format(count=len(df)))
            
            # Show warnings if any
            if warnings:
                with st.expander(UI_TEXT["warning_data_quality"], expanded=True):
                    for warning in warnings:
                        st.warning(warning)
            
            # Display dashboard
            show_dashboard(st.session_state.analyzer)
            
            # Export section
            show_export_section(st.session_state.analyzer)
            
            # AI Assistant
            show_ai_assistant(st.session_state.analyzer, api_key)
            
            # Raw data (collapsible)
            with st.expander("📄 View Raw Data"):
                st.dataframe(df, use_container_width=True)
        
        except Exception as e:
            st.error(UI_TEXT["error_general"].format(error=str(e)))
            st.info("Please check your file format and try again. Download our template for reference.")
    
    else:
        # Hero/Welcome screen with redesigned UI
        show_hero_page()


if __name__ == "__main__":
    main()
