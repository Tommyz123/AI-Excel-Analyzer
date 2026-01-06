"""
AI Sales Analyzer - Main Application
Streamlit web application for automated sales analysis
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from config import Config, UI_TEXT_EN, UI_TEXT_ZH
from utils.data_processor import FlexibleDataProcessor
from utils.analyzer import SalesAnalyzer
from utils.pandas_agent import PandasAgent  # Changed from AIAgent
from utils.exporter import DataExporter
from utils.template_generator import TemplateGenerator
from utils.cost_controller import CostController


# ==================== Translation Function ====================
def t(key, **kwargs):
    """
    Get translated text based on current language

    Args:
        key: Translation key (e.g., 'hero_slogan_title')
        **kwargs: Format parameters (e.g., count=100, date='2024-01-15')

    Returns:
        Formatted text in current language
    """
    lang = st.session_state.get('language', 'en')
    text_dict = UI_TEXT_EN if lang == 'en' else UI_TEXT_ZH
    text = text_dict.get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except:
            return text
    return text


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
# Language setting (default to English)
if 'language' not in st.session_state:
    st.session_state.language = 'en'

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
                {t('hero_slogan_title')}
            </h1>
            <p style='font-size: 1.3rem; color: #86868B; font-weight: 400;'>
                {t('hero_slogan_subtitle')}
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # 3-Step Process Cards
    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 1rem;'>
            <h3 style='color: #1D1D1F; font-weight: 600;'>{t('hero_steps_title')}</h3>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class='saas-card' style='text-align: center; min-height: 240px;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>📤</div>
                <h4 style='color: {ChartColors.PRIMARY}; font-weight: 600; margin-bottom: 0.8rem;'>
                    {t('hero_step1_title')}
                </h4>
                <p style='color: #86868B; font-size: 0.95rem; line-height: 1.6;'>
                    {t('hero_step1_desc').replace(chr(10), '<br/>')}
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class='saas-card' style='text-align: center; min-height: 240px;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>🤖</div>
                <h4 style='color: {ChartColors.ACCENT}; font-weight: 600; margin-bottom: 0.8rem;'>
                    {t('hero_step2_title')}
                </h4>
                <p style='color: #86868B; font-size: 0.95rem; line-height: 1.6;'>
                    {t('hero_step2_desc').replace(chr(10), '<br/>')}
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class='saas-card' style='text-align: center; min-height: 240px;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>📊</div>
                <h4 style='color: #34C759; font-weight: 600; margin-bottom: 0.8rem;'>
                    {t('hero_step3_title')}
                </h4>
                <p style='color: #86868B; font-size: 0.95rem; line-height: 1.6;'>
                    {t('hero_step3_desc').replace(chr(10), '<br/>')}
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # Call to Action
    st.markdown(f"""
        <div style='text-align: center;'>
            <p style='color: #86868B; font-size: 1rem; margin-bottom: 1.5rem;'>
                {t('hero_get_started')}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Feature highlights
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    col_a, col_b, col_c, col_d = st.columns(4)

    features = [
        (t('hero_feature1_icon'), t('hero_feature1_title'), t('hero_feature1_desc')),
        (t('hero_feature2_icon'), t('hero_feature2_title'), t('hero_feature2_desc')),
        (t('hero_feature3_icon'), t('hero_feature3_title'), t('hero_feature3_desc')),
        (t('hero_feature4_icon'), t('hero_feature4_title'), t('hero_feature4_desc'))
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
    st.title(f"{Config.APP_ICON} {t('app_title')}")
    st.markdown(f"*{t('app_subtitle')}*")
    st.divider()


def show_sidebar():
    """Display sidebar with file upload and templates"""
    with st.sidebar:
        # ==================== Language Switcher (Top) ====================
        st.markdown(f"### 🌐 {t('language')}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "🇬🇧 English",
                use_container_width=True,
                type="primary" if st.session_state.language == 'en' else "secondary"
            ):
                st.session_state.language = 'en'
                st.rerun()

        with col2:
            if st.button(
                "🇨🇳 中文",
                use_container_width=True,
                type="primary" if st.session_state.language == 'zh' else "secondary"
            ):
                st.session_state.language = 'zh'
                st.rerun()

        st.divider()

        # ==================== File Upload Section ====================
        st.header(t("upload_section"))

        # 选择上传模式（单文件 or 多文件对比）
        upload_mode = st.radio(
            t('upload_mode_label'),
            [t('upload_mode_single'), t('upload_mode_multi')],
            key="upload_mode",
            help=t('upload_mode_multi_help')
        )

        # File uploader
        if upload_mode == t('upload_mode_single'):
            uploaded_file = st.file_uploader(
                t("upload_label"),
                type=['xlsx', 'csv'],
                help=t("upload_help")
            )
            uploaded_files = [uploaded_file] if uploaded_file else []
        else:
            uploaded_files = st.file_uploader(
                t('upload_mode_multi_help'),
                type=['xlsx', 'csv'],
                accept_multiple_files=True,
                help=t('upload_mode_multi_help')
            )
            if uploaded_files and not (2 <= len(uploaded_files) <= 3):
                st.warning(t('upload_mode_warning', count=len(uploaded_files)))
                uploaded_files = []

        # 文件标签（多文件模式）
        file_labels = []
        if upload_mode == t('upload_mode_multi') and uploaded_files and 2 <= len(uploaded_files) <= 3:
            st.markdown(t('file_labels_title'))
            st.caption(t('file_labels_caption'))

            for i, file in enumerate(uploaded_files):
                default_label = file.name.replace('.xlsx', '').replace('.csv', '')[:20]
                label = st.text_input(
                    t('file_label_input', num=i+1),
                    value=default_label,
                    key=f"file_label_{i}",
                    max_chars=20
                )
                file_labels.append(label)

        # API Key input
        st.divider()
        api_key = st.text_input(
            t("api_key_label"),
            type="password",
            help=t("api_key_help")
        )

        # Use config key if not provided
        if not api_key:
            api_key = Config.OPENAI_API_KEY

        # Templates section
        st.divider()
        st.subheader(t("template_section"))

        col1, col2 = st.columns(2)

        with col1:
            blank_template = TemplateGenerator.generate_blank_template()
            st.download_button(
                label=t("template_blank"),
                data=blank_template,
                file_name="sales_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help=t("template_blank_help")
            )

        with col2:
            sample_data = TemplateGenerator.generate_sample_data()
            st.download_button(
                label=t("template_sample"),
                data=sample_data,
                file_name="sales_sample.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help=t("template_sample_help")
            )

        # Format guide
        with st.expander(t("format_guide_title")):
            st.markdown(t("format_guide_content"))

        # Demo Data Loader (New Feature)
        st.divider()
        st.subheader("📦 体验Demo数据")

        demo_type = st.selectbox(
            "选择场景",
            ["", "电商场景 (E-commerce)", "餐饮场景 (Restaurant)", "零售场景 (Retail)"],
            key="demo_selector"
        )

        if demo_type and st.button("🚀 加载Demo数据", key="load_demo", use_container_width=True):
            with st.spinner("正在生成Demo数据..."):
                try:
                    if "电商" in demo_type:
                        demo_df = TemplateGenerator.generate_ecommerce_data()
                    elif "餐饮" in demo_type:
                        demo_df = TemplateGenerator.generate_restaurant_data()
                    else:
                        demo_df = TemplateGenerator.generate_retail_data()

                    st.session_state.df = demo_df
                    st.session_state.analyzer = SalesAnalyzer(demo_df)
                    st.session_state.ai_agent = None  # Reset AI agent
                    st.success(f"✅ {demo_type}数据已加载（{len(demo_df)}条记录）")
                    st.rerun()
                except Exception as e:
                    st.error(f"Demo数据加载失败: {str(e)}")

        # Privacy notice
        st.divider()
        with st.expander(t("privacy_title")):
            st.markdown(t("privacy_content"))
        
        # API usage stats (if AI agent exists)
        if st.session_state.ai_agent:
            show_api_usage()

        # 返回上传的文件列表和标签
        return uploaded_files, file_labels, api_key, upload_mode


# ==================== 工具函数（未来可提取为utils/formatting.py）====================
def safe_divide(numerator, denominator, fallback='N/A'):
    """
    安全除法，防止除零错误

    Args:
        numerator: 分子
        denominator: 分母
        fallback: 除零时的返回值

    Returns:
        除法结果或fallback值

    设计考虑：
    - ✅ 当前：在app.py中定义，避免文件碎片化
    - 🔄 未来：如需复用，可提取为 utils/formatting.py
    - 🔄 扩展性：添加文档字符串，便于测试和维护
    """
    if denominator == 0 or denominator is None:
        return fallback
    try:
        return numerator / denominator
    except (ZeroDivisionError, TypeError):
        return fallback


def format_currency(value, currency='$'):
    """
    格式化货币显示

    Args:
        value: 金额（可以是数字或'N/A'）
        currency: 货币符号

    Returns:
        格式化后的字符串（如$1,234.56或N/A）
    """
    if value == 'N/A' or value is None:
        return 'N/A'
    try:
        return f"{currency}{float(value):,.2f}"
    except (ValueError, TypeError):
        return 'N/A'


def format_number(value, precision=0):
    """格式化数字（千位分隔符）"""
    if value == 'N/A' or value is None:
        return 'N/A'
    try:
        if precision == 0:
            return f"{int(value):,}"
        else:
            return f"{float(value):,.{precision}f}"
    except (ValueError, TypeError):
        return 'N/A'
# ===============================================================================


# ==================== 图表创建函数（优化版）====================
def create_top_products_chart(analyzer):
    """
    创建Top Products横向条形图（优化版）

    升级内容：
    - 横向条形图（更美观）
    - 深蓝色渐变（ChartColors.PRIMARY）
    - 条内显示数值（白色文字）
    - 优化hover提示
    - 统一高度450px
    - 标题18px加粗居中
    """
    top_products = analyzer.get_top_products()

    if top_products.empty:
        return None

    fig = go.Figure(go.Bar(
        x=top_products.values,
        y=top_products.index,
        orientation='h',
        marker=dict(
            color=ChartColors.PRIMARY,
            line=dict(width=0)
        ),
        text=[f'{int(val):,}' for val in top_products.values],
        textposition='inside',
        textfont=dict(color='white', size=14, family='Inter'),
        hovertemplate=t('chart_top_products_hover')
    ))

    fig.update_layout(
        title=dict(
            text=t('chart_top_products_title'),
            font=dict(size=UIConfig.TITLE_FONT_SIZE, family='Inter', weight=600),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title=t('chart_top_products_ylabel'),
        yaxis_title='',
        height=UIConfig.CHART_HEIGHT,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=60, b=40),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            tickformat=',d'
        ),
        yaxis=dict(
            showgrid=False,
            autorange='reversed'  # Top product at the top
        ),
        font=dict(family='Inter', color='#1D1D1F')
    )

    return fig


def create_sales_by_state_chart(analyzer):
    """
    创建Sales by State柱状图（优化版）

    升级内容：
    - Top 3州用橙色高亮（ChartColors.ACCENT），其他用深蓝
    - 添加平均销售额参考线（灰色虚线）
    - Y轴格式化：$符号 + 千位分隔符
    - 柱顶显示金额
    - Hover显示：州名 + 金额 + 排名
    """
    state_sales = analyzer.get_sales_by_state()

    if state_sales.empty:
        return None

    # 识别Top 3州
    top3_states = set(state_sales.head(3).index)

    # 为每个州分配颜色（Top 3用橙色，其他用深蓝）
    colors = [ChartColors.ACCENT if state in top3_states else ChartColors.PRIMARY
              for state in state_sales.index]

    # 计算平均销售额
    avg_sales = state_sales.mean()

    # 为hover添加排名信息
    ranks = list(range(1, len(state_sales) + 1))

    fig = go.Figure(go.Bar(
        x=state_sales.index,
        y=state_sales.values,
        marker=dict(
            color=colors,
            line=dict(width=0)
        ),
        text=[f'${val:,.0f}' for val in state_sales.values],
        textposition='outside',
        textfont=dict(color='#1D1D1F', size=12, family='Inter'),
        customdata=ranks,
        hovertemplate=t('chart_sales_by_state_hover')
    ))

    # 添加平均线
    fig.add_hline(
        y=avg_sales,
        line_dash="dash",
        line_color='rgba(100,100,100,0.5)',
        line_width=2,
        annotation_text=t('chart_sales_by_state_avg_line', avg=avg_sales),
        annotation_position="right",
        annotation_font=dict(size=11, color='#86868B')
    )

    fig.update_layout(
        title=dict(
            text=t('chart_sales_by_state_title'),
            font=dict(size=UIConfig.TITLE_FONT_SIZE, family='Inter', weight=600),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title=t('chart_sales_by_state_xlabel'),
        yaxis_title=t('chart_sales_by_state_ylabel'),
        height=UIConfig.CHART_HEIGHT,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=60, b=40),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            tickformat='$,.0f',
            tickprefix='$'
        ),
        font=dict(family='Inter', color='#1D1D1F')
    )

    return fig


def create_daily_trend_chart(analyzer):
    """
    创建Daily Trend折线图（优化版 - 最复杂）

    升级内容：
    - 线条加粗到4px（UIConfig.LINE_WIDTH）
    - 线下区域填充蓝色渐变（15%透明度）
    - 添加趋势线（scipy线性回归，带降级处理）
    - 标注最高点和最低点（emoji + 金额）
    - 圆点标记增大到8px（UIConfig.MARKER_SIZE）
    - 日期格式：MM/DD，金额格式：$X,XXX
    """
    daily_trend = analyzer.get_daily_trend()

    if daily_trend.empty:
        return None

    # 准备数据
    dates = daily_trend.index
    sales = daily_trend.values

    # 创建主折线图
    fig = go.Figure()

    # 主折线（加粗 + 渐变填充）
    fig.add_trace(go.Scatter(
        x=dates,
        y=sales,
        mode='lines+markers',
        name=t('chart_daily_trend_trace_name'),
        line=dict(
            color=ChartColors.PRIMARY,
            width=UIConfig.LINE_WIDTH
        ),
        marker=dict(
            size=UIConfig.MARKER_SIZE,
            color=ChartColors.PRIMARY,
            line=dict(color='white', width=2)
        ),
        fill='tozeroy',
        fillcolor=f'rgba(31, 119, 180, 0.15)',  # 15% transparency
        hovertemplate=t('chart_daily_trend_hover')
    ))

    # 添加趋势线（scipy线性回归，带降级处理）
    try:
        from scipy import stats
        import numpy as np

        # 转换日期为数值（天数）
        x_numeric = np.arange(len(dates))
        y_numeric = np.array(sales)

        # 线性回归
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_numeric, y_numeric)
        trend_line = slope * x_numeric + intercept

        # 添加趋势线
        fig.add_trace(go.Scatter(
            x=dates,
            y=trend_line,
            mode='lines',
            name=t('chart_daily_trend_trend_legend', r2=r_value**2),
            line=dict(
                color=ChartColors.ACCENT,
                width=2,
                dash='dash'
            ),
            hovertemplate=t('chart_daily_trend_trend_hover')
        ))

    except ImportError:
        # scipy未安装，显示友好提示
        st.sidebar.warning(t('chart_daily_trend_warning'))
    except Exception as e:
        # 其他错误（如数据问题），静默失败
        print(f"趋势线计算失败: {e}")

    # 标注最高点和最低点
    if len(sales) > 0:
        max_idx = sales.argmax()
        min_idx = sales.argmin()

        # 最高点标注
        fig.add_annotation(
            x=dates[max_idx],
            y=sales[max_idx],
            text=t('chart_daily_trend_max_label', amount=sales[max_idx]),
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=ChartColors.SUCCESS,
            ax=0,
            ay=-60,
            bgcolor='rgba(212, 237, 218, 0.9)',
            bordercolor=ChartColors.PRIMARY,
            borderwidth=2,
            borderpad=6,
            font=dict(size=11, color='#1D1D1F', family='Inter')
        )

        # 最低点标注
        fig.add_annotation(
            x=dates[min_idx],
            y=sales[min_idx],
            text=t('chart_daily_trend_min_label', amount=sales[min_idx]),
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=ChartColors.DANGER,
            ax=0,
            ay=60,
            bgcolor='rgba(248, 215, 218, 0.9)',
            bordercolor=ChartColors.PRIMARY,
            borderwidth=2,
            borderpad=6,
            font=dict(size=11, color='#1D1D1F', family='Inter')
        )

    fig.update_layout(
        title=dict(
            text=t('chart_daily_trend_title'),
            font=dict(size=UIConfig.TITLE_FONT_SIZE, family='Inter', weight=600),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title=t('chart_daily_trend_xlabel'),
        yaxis_title=t('chart_daily_trend_ylabel'),
        height=UIConfig.CHART_HEIGHT,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=60, b=40),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            tickformat='%m/%d'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            tickformat='$,.0f',
            tickprefix='$'
        ),
        hovermode='x unified',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        font=dict(family='Inter', color='#1D1D1F')
    )

    return fig
# ===============================================================================


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


def show_enhanced_metrics(analyzer):
    """
    显示优化后的指标卡片

    升级内容：
    - 使用safe_divide防止除零错误
    - 使用format_currency和format_number统一格式化
    - 添加图标（💰📦📊）
    - 统一卡片样式（圆角、阴影）
    """
    stats = analyzer.get_summary_stats()

    # 安全计算平均订单价值
    avg_order = safe_divide(stats['total_sales'], stats['order_count'], fallback=0)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class="saas-card">
                <div class="metric-label">{t("metrics_total_sales_label")}</div>
                <div class="metric-value">{format_currency(stats['total_sales'])}</div>
                <div style="font-size: 0.85rem; color: #86868B; margin-top: 8px;">
                    {t('metrics_total_sales_subtitle', days=stats['date_range_days'])}
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="saas-card">
                <div class="metric-label">{t("metrics_order_count_label")}</div>
                <div class="metric-value">{format_number(stats['order_count'])}</div>
                <div style="font-size: 0.85rem; color: #86868B; margin-top: 8px;">
                    {t('metrics_order_count_subtitle', products=stats['unique_products'])}
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="saas-card">
                <div class="metric-label">{t("metrics_avg_order_label")}</div>
                <div class="metric-value">{format_currency(avg_order)}</div>
                <div style="font-size: 0.85rem; color: #86868B; margin-top: 8px;">
                    {t('metrics_avg_order_subtitle')}
                </div>
            </div>
        """, unsafe_allow_html=True)


def show_comparison_section(analyzer):
    """
    显示周/月对比section

    升级内容：
    - 自动检测数据范围（>=14天显示周对比，>=60天显示月对比）
    - 增长率：绿↑正增长，红↓负增长
    - 3个对比卡片：销售额、订单量、平均订单
    """
    week_comp = analyzer.get_week_comparison()
    month_comp = analyzer.get_month_comparison()

    # 如果两个对比都不可用，不显示
    if week_comp is None and month_comp is None:
        return

    st.markdown("---")
    st.subheader("📊 期间对比分析")

    # 优先显示周对比（数据更新鲜）
    comparison = week_comp if week_comp is not None else month_comp
    period_type = "周" if week_comp is not None else "月"
    current_key = 'current_week' if week_comp is not None else 'current_month'
    previous_key = 'previous_week' if week_comp is not None else 'previous_month'

    col1, col2, col3 = st.columns(3)

    # 卡片1：增长率
    with col1:
        growth = comparison['growth_rate']

        if growth == 'N/A':
            arrow = ""
            color = "#86868B"
            growth_display = "N/A"
        elif growth > 0:
            arrow = "↑"
            color = "#28a745"  # 绿色
            growth_display = f"+{growth:.1f}%"
        elif growth < 0:
            arrow = "↓"
            color = "#dc3545"  # 红色
            growth_display = f"{growth:.1f}%"
        else:
            arrow = "→"
            color = "#86868B"
            growth_display = "0%"

        st.markdown(f"""
            <div class="saas-card" style="text-align: center; padding: 25px;">
                <div style="color: #86868B; font-size: 0.9rem; margin-bottom: 12px;">
                    {period_type}销售额增长
                </div>
                <div style="font-size: 2.5rem; font-weight: 700; color: {color}; margin: 10px 0;">
                    {arrow} {growth_display}
                </div>
                <div style="font-size: 0.8rem; color: #86868B; margin-top: 10px;">
                    本{period_type} vs 上{period_type}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 卡片2：本周销售额
    with col2:
        current_sales = comparison[current_key]
        st.markdown(f"""
            <div class="saas-card" style="text-align: center; padding: 25px;">
                <div style="color: #86868B; font-size: 0.9rem; margin-bottom: 12px;">
                    💰 本{period_type}销售
                </div>
                <div style="font-size: 2.2rem; font-weight: 700; color: {ChartColors.PRIMARY}; margin: 10px 0;">
                    ${current_sales:,.2f}
                </div>
                <div style="font-size: 0.8rem; color: #86868B; margin-top: 10px;">
                    {comparison['current_orders']} 笔订单
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 卡片3：上周销售额
    with col3:
        previous_sales = comparison[previous_key]
        st.markdown(f"""
            <div class="saas-card" style="text-align: center; padding: 25px;">
                <div style="color: #86868B; font-size: 0.9rem; margin-bottom: 12px;">
                    📦 上{period_type}销售
                </div>
                <div style="font-size: 2.2rem; font-weight: 700; color: #86868B; margin: 10px 0;">
                    ${previous_sales:,.2f}
                </div>
                <div style="font-size: 0.8rem; color: #86868B; margin-top: 10px;">
                    {comparison['previous_orders']} 笔订单
                </div>
            </div>
        """, unsafe_allow_html=True)


def show_categorized_insights(analyzer):
    """
    显示分类洞察（3列布局 - 机会/风险/趋势）

    升级内容：
    - 按category分组显示
    - 使用expander折叠面板节省空间
    - 每个洞察有emoji、标题、详细说明
    - 背景色区分不同类别
    """
    insights = analyzer.detect_anomalies()

    if not insights:
        st.info("📊 暂无异常洞察数据")
        return

    st.subheader("🤖 AI 业务洞察")

    # 按类别分组
    opportunities = [i for i in insights if i['category'] == 'opportunity']
    risks = [i for i in insights if i['category'] == 'risk']
    trends = [i for i in insights if i['category'] == 'trend']

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div style="background: {ChartColors.SUCCESS}; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 1rem;">
                <h4 style="margin: 0; color: #1D1D1F;">{t('insights_category_opportunity', count=len(opportunities))}</h4>
            </div>
        """, unsafe_allow_html=True)

        for insight in opportunities:
            with st.expander(f"{insight['emoji']} {insight['title']}", expanded=False):
                st.markdown(f"""
                    <div style="background-color: {insight['color']};
                                padding: 15px; border-radius: 8px;
                                border-left: 4px solid {ChartColors.PRIMARY};">
                        {insight['detail']}
                    </div>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style="background: {ChartColors.WARNING}; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 1rem;">
                <h4 style="margin: 0; color: #1D1D1F;">{t('insights_category_risk', count=len(risks))}</h4>
            </div>
        """, unsafe_allow_html=True)

        for insight in risks:
            with st.expander(f"{insight['emoji']} {insight['title']}", expanded=False):
                st.markdown(f"""
                    <div style="background-color: {insight['color']};
                                padding: 15px; border-radius: 8px;
                                border-left: 4px solid {ChartColors.ACCENT};">
                        {insight['detail']}
                    </div>
                """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div style="background: {ChartColors.INFO}; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 1rem;">
                <h4 style="margin: 0; color: #1D1D1F;">{t('insights_category_trend', count=len(trends))}</h4>
            </div>
        """, unsafe_allow_html=True)

        for insight in trends:
            with st.expander(f"{insight['emoji']} {insight['title']}", expanded=False):
                st.markdown(f"""
                    <div style="background-color: {insight['color']};
                                padding: 15px; border-radius: 8px;
                                border-left: 4px solid #007AFF;">
                        {insight['detail']}
                    </div>
                """, unsafe_allow_html=True)


def show_dashboard(analyzer: SalesAnalyzer):
    """Display main dashboard with metrics and charts"""
    
    # Key metrics (优化版卡片 - 使用safe_divide和格式化函数)
    with st.container():
        st.markdown("### 📈 核心指标")
        show_enhanced_metrics(analyzer)
    
    st.markdown("---")
    
    # Charts
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Top 5 Products (优化版图表)
        fig1 = create_top_products_chart(analyzer)
        if fig1:
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("暂无产品数据")
    
    with col_right:
        # Sales by State (优化版图表)
        fig2 = create_sales_by_state_chart(analyzer)
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("暂无州销售数据")
    
    # Daily Trend (full width) - 优化版图表
    fig3 = create_daily_trend_chart(analyzer)
    if fig3:
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("暂无每日销售数据")
    
    # Period Comparison (周/月对比)
    show_comparison_section(analyzer)

    # Business Insights (优化版 - 分类显示)
    st.divider()
    show_categorized_insights(analyzer)


def show_export_section(analyzer: SalesAnalyzer):
    """Display export options"""
    st.divider()
    st.subheader(t("export_section"))

    exporter = DataExporter(analyzer)

    col1, col2 = st.columns(2)

    with col1:
        excel_data = exporter.export_to_excel()
        st.download_button(
            label=t("export_excel"),
            data=excel_data,
            file_name=exporter.get_filename('xlsx'),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with col2:
        csv_data = exporter.export_to_csv()
        st.download_button(
            label=t("export_csv"),
            data=csv_data,
            file_name=exporter.get_filename('csv'),
            mime="text/csv"
        )


def show_ai_assistant(analyzer: SalesAnalyzer, api_key: str):
    """Display AI Q&A interface with chat history and download"""
    st.divider()
    st.subheader(t("ai_qa_title"))
    st.markdown(f"*{t('ai_qa_subtitle')}*")
    
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
        st.warning(t("error_api_key"))
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
                st.write(f"👋 {t('ai_qa_subtitle')}")
                st.markdown("**您可以试着问我：**")
                for example in t("ai_qa_examples")[:3]:
                    st.markdown(f"- {example}")

        # Question input
        if question := st.chat_input(t("ai_qa_placeholder")):
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": question})

            # Display user message immediately
            with st.chat_message("user"):
                st.write(question)

            # Check API limits
            controller = CostController()
            can_call, message = controller.can_make_call()

            if not can_call:
                st.error(t("error_api_limit", message=message))
                return

            # Get answer
            with st.chat_message("assistant"):
                with st.spinner(t("ai_thinking")):
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


def show_comparison_dashboard(comparison_analyzer):
    """
    显示多文件对比仪表板

    Args:
        comparison_analyzer: ComparisonAnalyzer实例
    """
    from utils.comparison_analyzer import ComparisonAnalyzer

    st.title(t('multifile_title'))

    # ========== 汇总指标卡片 ==========
    st.subheader(t('multifile_summary_metrics_title'))

    metrics = comparison_analyzer.get_summary_metrics()

    # 创建对比卡片
    cols = st.columns(len(metrics['labels']))

    for i, label in enumerate(metrics['labels']):
        with cols[i]:
            st.markdown(f"""
                <div class="saas-card" style="text-align: center; padding: 25px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                    <h3 style="color: white; margin-bottom: 15px;">{label}</h3>
                    <div style="font-size: 2.2rem; font-weight: 700; margin: 10px 0;">
                        ${metrics['total_sales'][i]:,.0f}
                    </div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">
                        {t('multifile_summary_total_sales')}
                    </div>
                    <hr style="border-color: rgba(255,255,255,0.3); margin: 15px 0;">
                    <div style="font-size: 1.5rem; font-weight: 600;">
                        {metrics['total_orders'][i]:,}
                    </div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">
                        {t('multifile_summary_order_count')}
                    </div>
                    <hr style="border-color: rgba(255,255,255,0.3); margin: 15px 0;">
                    <div style="font-size: 1.5rem; font-weight: 600;">
                        ${metrics['avg_order_value'][i]:,.2f}
                    </div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">
                        {t('multifile_summary_avg_order')}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # ========== 增长分析 ==========
    growth_analysis = comparison_analyzer.get_growth_analysis()

    if growth_analysis:
        st.markdown("---")
        st.subheader(t('multifile_growth_title'))
        st.caption(t('multifile_growth_subtitle', baseline=growth_analysis['baseline']))

        growth_cols = st.columns(len(growth_analysis['comparisons']))

        for i, comp in enumerate(growth_analysis['comparisons']):
            with growth_cols[i]:
                # 销售额增长
                sales_growth = comp['sales_growth']
                arrow = "↑" if sales_growth > 0 else "↓"
                color = "#28a745" if sales_growth > 0 else "#dc3545"

                st.markdown(f"""
                    <div class="saas-card" style="text-align: center; padding: 20px;">
                        <h4>{comp['label']}</h4>
                        <div style="font-size: 2rem; font-weight: 700; color: {color}; margin: 15px 0;">
                            {arrow} {abs(sales_growth):.1f}%
                        </div>
                        <div style="font-size: 0.9rem; color: #666;">
                            {t('multifile_growth_change_label')}
                        </div>
                        <hr style="margin: 15px 0;">
                        <div style="font-size: 1.2rem; color: {color};">
                            {t('multifile_growth_order_qty')} {arrow} {abs(comp['orders_growth']):.1f}%
                        </div>
                        <div style="font-size: 1.2rem; color: {color};">
                            {t('multifile_growth_avg_order')} {arrow} {abs(comp['avg_order_growth']):.1f}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    # ========== 对比图表 ==========
    st.markdown("---")
    st.subheader(t('multifile_charts_title'))

    # 1. 销售额对比柱状图
    fig_sales = go.Figure()

    for i, label in enumerate(metrics['labels']):
        fig_sales.add_trace(go.Bar(
            name=label,
            x=[t('multifile_summary_total_sales'), t('multifile_summary_order_count'), t('multifile_summary_avg_order')],
            y=[metrics['total_sales'][i], metrics['total_orders'][i], metrics['avg_order_value'][i]],
            text=[f"${metrics['total_sales'][i]:,.0f}", f"{metrics['total_orders'][i]:,}", f"${metrics['avg_order_value'][i]:,.2f}"],
            textposition='auto'
        ))

    fig_sales.update_layout(
        title=t('multifile_chart_summary_title'),
        barmode='group',
        height=450,
        xaxis_title=t('multifile_chart_axis_metrics'),
        yaxis_title=t('multifile_chart_axis_value')
    )

    st.plotly_chart(fig_sales, use_container_width=True)

    # 2. Top产品对比
    st.markdown(t('multifile_chart_products_title'))

    top_products_comparison = comparison_analyzer.get_top_products_comparison(5)

    fig_products = go.Figure()

    for label, products in top_products_comparison.items():
        fig_products.add_trace(go.Bar(
            name=label,
            x=products.index,
            y=products.values,
            text=products.values,
            textposition='auto'
        ))

    fig_products.update_layout(
        title=t('multifile_top_products_subtitle'),
        barmode='group',
        height=450,
        xaxis_title=t('multifile_chart_axis_product'),
        yaxis_title=t('multifile_chart_axis_quantity')
    )

    st.plotly_chart(fig_products, use_container_width=True)

    # 3. 每日趋势对比
    st.markdown(t('multifile_chart_trends_title'))

    daily_trends = comparison_analyzer.get_daily_trend_comparison()

    fig_trends = go.Figure()

    for label, trend in daily_trends.items():
        fig_trends.add_trace(go.Scatter(
            name=label,
            x=trend.index,
            y=trend.values,
            mode='lines+markers',
            marker=dict(size=6),
            line=dict(width=3)
        ))

    fig_trends.update_layout(
        title=t('multifile_daily_trend_title'),
        height=450,
        xaxis_title=t('multifile_chart_axis_date'),
        yaxis_title=t('multifile_chart_axis_sales'),
        hovermode='x unified'
    )

    st.plotly_chart(fig_trends, use_container_width=True)

    # ========== 日期范围信息 ==========
    st.markdown("---")
    st.subheader(t('multifile_date_range_title'))

    date_ranges = comparison_analyzer.get_date_ranges()

    date_cols = st.columns(len(date_ranges))

    for i, dr in enumerate(date_ranges):
        with date_cols[i]:
            if dr['start_date']:
                st.info(f"""
**{dr['label']}**
- {t('multifile_date_range_start')} {dr['start_date'].date()}
- {t('multifile_date_range_end')} {dr['end_date'].date()}
- {t('multifile_date_range_days')} {dr['days']}
                """)
            else:
                st.warning(f"{dr['label']}: {t('multifile_date_range_no_data')}")


def main():
    """Main application logic"""
    # show_header() # Disabled for custom navbar

    # Sidebar
    uploaded_files, file_labels, api_key, upload_mode = show_sidebar()
    
    # Main content
    if uploaded_files and len(uploaded_files) > 0:
        # ========== 多文件对比模式 ==========
        if upload_mode == t('upload_mode_multi') and 2 <= len(uploaded_files) <= 3:
            try:
                with st.spinner(t('multifile_processing')):
                    from utils.comparison_analyzer import ComparisonAnalyzer

                    processor = FlexibleDataProcessor()
                    dataframes = []
                    all_warnings = []

                    # 处理每个文件
                    for i, file in enumerate(uploaded_files):
                        df, warnings = processor.process_file(file)
                        dataframes.append(df)

                        if warnings:
                            all_warnings.extend([f"[{file_labels[i] if file_labels else file.name}] {w}" for w in warnings])

                    # 创建对比分析器
                    comparison_analyzer = ComparisonAnalyzer(
                        dataframes=dataframes,
                        labels=file_labels if file_labels else [f.name for f in uploaded_files]
                    )

                    st.session_state.comparison_analyzer = comparison_analyzer

                # 成功消息
                total_records = sum([len(df) for df in dataframes])
                st.success(t('multifile_success', count=len(uploaded_files), records=total_records))

                # 显示警告
                if all_warnings:
                    with st.expander(t('multifile_warning_title'), expanded=False):
                        for warning in all_warnings:
                            st.warning(warning)

                # 显示对比仪表板
                show_comparison_dashboard(comparison_analyzer)

                # ========== AI助手区域（多文件对比模式）==========
                st.markdown("---")
                st.subheader(t('multifile_ai_title'))

                # 数据集选择器（2列布局）
                col1, col2 = st.columns([2, 1])

                with col1:
                    selected_dataset_idx = st.selectbox(
                        t('multifile_ai_selector_label'),
                        options=range(len(comparison_analyzer.labels)),
                        format_func=lambda i: f"📊 {comparison_analyzer.labels[i]} ({len(comparison_analyzer.dataframes[i])} {t('multifile_ai_dataset_unit')})",
                        key="ai_dataset_selector",
                        help=t('multifile_ai_selector_help')
                    )

                with col2:
                    st.metric(
                        label=t('multifile_ai_dataset_size'),
                        value=f"{len(comparison_analyzer.dataframes[selected_dataset_idx])} {t('multifile_ai_dataset_unit')}",
                        delta=None
                    )

                # 设置当前分析对象（供AI助手使用）
                st.session_state.df = comparison_analyzer.dataframes[selected_dataset_idx]
                st.session_state.analyzer = comparison_analyzer.analyzers[selected_dataset_idx]

                # 提示信息
                st.info(t('multifile_ai_current_info', label=comparison_analyzer.labels[selected_dataset_idx]))

                # 调用现有AI助手（无需修改）
                show_ai_assistant(st.session_state.analyzer, api_key)

            except Exception as e:
                st.error(t('multifile_error_failed', error=str(e)))
                st.info(t('multifile_error_format'))

        # ========== 单文件分析模式 ==========
        elif len(uploaded_files) == 1:
            uploaded_file = uploaded_files[0]

            try:
                with st.spinner(t("processing")):
                    processor = FlexibleDataProcessor()
                    df, warnings = processor.process_file(uploaded_file)

                    # Store in session state
                    st.session_state.df = df
                    st.session_state.analyzer = SalesAnalyzer(df)
                    st.session_state.ai_agent = None  # Reset AI agent for new data

                # Success message
                st.success(t("success_upload", count=len(df)))

                # Show warnings if any
                if warnings:
                    with st.expander(t("warning_data_quality"), expanded=True):
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
                st.error(t("error_general", error=str(e)))
                st.info("Please check your file format and try again. Download our template for reference.")

    else:
        # Hero/Welcome screen with redesigned UI
        show_hero_page()


if __name__ == "__main__":
    main()
