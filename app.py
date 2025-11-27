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


# Page configuration
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon=Config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    
    # Key metrics
    stats = analyzer.get_summary_stats()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            UI_TEXT["total_sales"],
            f"${stats['total_sales']:,.2f}"
        )
    
    with col2:
        st.metric(
            UI_TEXT["order_count"],
            f"{stats['order_count']:,}"
        )
    
    with col3:
        st.metric(
            UI_TEXT["avg_order"],
            f"${stats['avg_order_value']:.2f}"
        )
    
    st.divider()
    
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
    """Display AI Q&A interface"""
    st.divider()
    st.subheader(UI_TEXT["ai_qa_title"])
    st.markdown(f"*{UI_TEXT['ai_qa_subtitle']}*")
    
    # Initialize AI agent if not exists
    if st.session_state.ai_agent is None:
        try:
            st.session_state.ai_agent = PandasAgent(
                st.session_state.df,
                api_key
            )
        except Exception as e:
            st.error(f"Failed to initialize AI Agent: {str(e)}")
            return
    
    # Check if API key is valid
    # Simple validation: check if key exists and looks roughly right
    if not api_key or not api_key.strip() or api_key == "your-api-key-here":
        st.warning(UI_TEXT["error_api_key"])
        
        # Show debugging info
        with st.expander("🔍 API Key Debug Info"):
            if not api_key:
                st.error("❌ No API key provided")
                st.info("Please enter your OpenAI API key in the sidebar above, or add it to the .env file")
            elif not api_key.strip():
                st.error("❌ API key is empty or whitespace")
            elif api_key == "your-api-key-here":
                st.error("❌ API key is still the placeholder value")
                st.info("Please replace 'your-api-key-here' with your actual OpenAI API key")
            elif not api_key.startswith('sk-'):
                st.error("❌ API key format is invalid")
                st.info("OpenAI API keys should start with 'sk-'")
                st.code(f"Current key starts with: {api_key[:10]}...")
            else:
                st.warning("⚠️ API key looks valid but validation failed")
                st.code(f"Key: {api_key[:10]}...{api_key[-4:]}")
        
        st.info("💡 You can still use the dashboard and export features without AI.")
        return
    
    # Show API key status (success)
    with st.expander("✅ API Key Status"):
        st.success(f"API key configured: {api_key[:10]}...{api_key[-4:]}")
    
    # Example questions
    with st.expander("💡 Example Questions"):
        for example in UI_TEXT["ai_qa_examples"]:
            st.markdown(f"- {example}")
    
    # Question input
    question = st.text_input(
        "Your question:",
        placeholder=UI_TEXT["ai_qa_placeholder"]
    )
    
    if question:
        # Check API limits
        controller = CostController()
        can_call, message = controller.can_make_call()
        
        if not can_call:
            st.error(UI_TEXT["error_api_limit"].format(message=message))
            return
        
        # Get answer
        with st.spinner(UI_TEXT["ai_thinking"]):
            answer = st.session_state.ai_agent.ask(question)
            
            # Record API call (PandasAgent always uses API)
            controller.record_call()
        
        # Display answer
        st.markdown(UI_TEXT["ai_answer_prefix"])
        st.write(answer)


def main():
    """Main application logic"""
    show_header()
    
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
        # Welcome screen
        st.info(UI_TEXT["welcome_message"])
        st.markdown(UI_TEXT["usage_steps"])


if __name__ == "__main__":
    main()
