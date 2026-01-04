# AI Excel Analyzer 升级实施计划（最终对齐版 v4.0）

> **文档状态**: ✅ 已对齐 - 简单实现 + 预留升级空间
> **创建时间**: 2026-01-04
> **实施策略**: 渐进式3阶段部署
> **预估工作量**: **24-28小时（3-5天）** 快速交付版本
> **可选扩展**: **+12-14小时** V1.5+升级
> **风险等级**: 低（简化实施方案）
> **成功率预估**: 95%

---

## 📋 执行摘要

### 项目概述

将现有的 AI Excel 分析工具升级为**专业美观的100人桌面网页demo**。

### 设计哲学

**当前阶段**：快速实现核心功能，避免过度工程化
**未来考虑**：代码结构清晰，便于后续扩展和优化

### 核心改进点（对齐版特点）

✅ **简化实施** - 24-28小时，14个任务
✅ **预留扩展** - 代码结构清晰，便于提取模块
✅ **避免过度工程** - 不创建独立配置文件，函数集中定义
✅ **保持可扩展性** - 添加完整文档，函数职责单一

### 质量目标

**最终验收标准 (100分制):**
- 界面专业度: 40分
- 功能完整性: 30分
- 视觉质量: 20分
- 可用性: 10分
- **目标总分**: ≥ 90分 (优秀)

---

## 🚨 执行前必须完成的修复（P0）

### 修复 #1: 更新依赖文件

**文件**: `requirements.txt`

**当前问题**:
```txt
❌ 缺少 scipy       - 趋势线功能会崩溃
❌ 缺少 numpy       - 隐式依赖不安全
❌ 缺少 cachetools  - 性能优化受限（可选）
```

**修复方案** - 添加以下依赖:
```text
# 数据分析（新增）
scipy>=1.11.0,<1.15.0        # 趋势线回归分析
numpy>=1.24.0,<2.0.0         # 数值计算（显式依赖）
cachetools>=5.3.0,<6.0.0     # 简单缓存（可选，为未来优化预留）
```

**验证**:
```bash
pip install -r requirements.txt
python -c "import scipy; print('✅ scipy OK')"
python -c "import numpy; print('✅ numpy OK')"
```

---

## 📅 渐进式实施计划（3 Phases）

### 时间分配总览

```
阶段0: 准备工作                  2小时
阶段1: 视觉升级                  14小时
阶段2: 功能增强                  8小时
阶段3: 测试与交付                2小时
-------------------------------------------
总计:                           24-28小时
```

---

## 阶段0: 准备工作 (2小时)

**目标**: 确保环境就绪，避免后续阻塞

### 任务0.1: 环境准备与依赖更新（1小时）

```bash
# 1. 备份项目
git tag -a v1.0-backup -m "升级前备份"
git checkout -b feature/ui-upgrade

# 2. 更新 requirements.txt
# 添加 scipy、numpy、cachetools

# 3. 安装依赖
pip install -r requirements.txt

# 4. 验证
python -c "import scipy; import numpy; import cachetools; print('✅ OK')"
```

### 任务0.2: 运行基准测试（1小时）

```bash
streamlit run app.py

# 测试项目：
# - 上传sample_data
# - 查看图表渲染
# - 测试AI问答
# - 截图当前界面（对比用）
```

**验收标准**:
- [x] Git备份标签已创建
- [x] 所有新依赖安装成功
- [x] 现有功能测试通过

---

## 阶段1: 视觉升级 (14小时)

**目标**: 统一配色、优化图表、更新首页

### 任务1.1: CSS主题色统一（1小时）

**策略**: 在代码中集中定义常量，便于后续提取

**修改文件**: `app.py`

**步骤1** - CSS变量定义（便于主题切换）:
```css
<style>
:root {
    --primary-blue: #1f77b4;
    --accent-orange: #ff7f0e;
    --light-blue: #aec7e8;
    --success-green: #d4edda;
    --warning-yellow: #fff3cd;
    --danger-red: #f8d7da;
    --info-blue: #d1ecf1;
}
/* 将所有硬编码颜色替换为CSS变量 */
</style>
```

**步骤2** - Python配色常量（便于后续提取为config_extended.py）:
```python
# 在 app.py 顶部（import之后）
# ==================== 配置常量（未来可提取为config_extended.py）====================
class ChartColors:
    """图表配色方案（便于统一修改和主题切换）

    设计考虑：
    - 当前：直接在代码中定义，简单快速
    - 未来：可一键提取为 config_extended.py（剪切粘贴+import）
    """
    PRIMARY = '#1f77b4'      # 深蓝
    ACCENT = '#ff7f0e'       # 橙色
    LIGHT_BLUE = '#aec7e8'   # 浅蓝
    SUCCESS = '#d4edda'      # 绿色
    WARNING = '#fff3cd'      # 黄色
    DANGER = '#f8d7da'       # 红色
    INFO = '#d1ecf1'         # 信息蓝

class UIConfig:
    """UI配置（便于后续扩展）"""
    CHART_HEIGHT = 450
    CHART_HEIGHT_MOBILE = 300
    TITLE_FONT_SIZE = 18
    LINE_WIDTH = 4
    MARKER_SIZE = 8
# ===============================================================================
```

**测试检查点**:
- [ ] CSS主题色已更新
- [ ] Python常量已集中定义
- [ ] 所有颜色引用统一

---

### 任务1.2: 首页重设计（2小时）

**新增函数**: `show_hero_page()`

**实现内容**:
```python
def show_hero_page():
    """显示专业着陆页"""
    st.markdown(f"""
        <div class="hero-section" style="text-align: center; padding: 60px 20px;">
            <h1 style="font-size: 2.8rem; color: {ChartColors.PRIMARY};">
                📊 AI Excel Analyzer
            </h1>
            <p style="font-size: 1.3rem; color: #666;">
                30秒看懂你的数据 - AI驱动的Excel分析
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 3步流程卡片
    cols = st.columns(3)
    steps = [
        ("📤 上传数据", "支持Excel/CSV格式，最大50MB"),
        ("🤖 AI分析", "自动生成图表和业务洞察"),
        ("📊 导出报告", "一键下载完整分析报告")
    ]

    for col, (title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
                <div class="saas-card" style="text-align: center; padding: 35px 20px;">
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>
            """, unsafe_allow_html=True)
```

**测试检查点**:
- [ ] Slogan正确显示
- [ ] 3步卡片并排显示
- [ ] 配色符合新方案

---

### 任务1.3-1.5: 图表优化（8.5小时）

#### 子任务1.3: Top Products图表优化（2.5小时）

**新增函数**: `create_top_products_chart(analyzer)`

```python
def create_top_products_chart(analyzer):
    """创建Top Products横向条形图（优化版）"""
    import plotly.graph_objects as go

    top_products = analyzer.get_top_products(5)

    fig = go.Figure(go.Bar(
        x=top_products.values,
        y=top_products.index,
        orientation='h',
        marker=dict(
            color=ChartColors.PRIMARY,
            line=dict(width=0)
        ),
        text=[f'{val:,}' for val in top_products.values],
        textposition='inside',
        textfont=dict(color='white', size=14),
        hovertemplate='<b>%{y}</b><br>销量: %{x:,}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text='Top 5 Best-Selling Products',
            font=dict(size=UIConfig.TITLE_FONT_SIZE, weight='bold'),
            x=0.5,
            xanchor='center'
        ),
        height=UIConfig.CHART_HEIGHT,
        plot_bgcolor='#FFFFFF',
        showlegend=False
    )

    return fig
```

---

#### 子任务1.4: Sales by State图表优化（2.5小时）

**新增函数**: `create_sales_by_state_chart(analyzer)`

```python
def create_sales_by_state_chart(analyzer):
    """创建Sales by State柱状图（Top 3高亮 + 平均线）"""
    import plotly.graph_objects as go

    sales_by_state = analyzer.get_sales_by_state().head(10)

    # 识别Top 3用橙色高亮
    top3_states = sales_by_state.head(3).index
    colors = [
        ChartColors.ACCENT if state in top3_states
        else ChartColors.PRIMARY
        for state in sales_by_state.index
    ]

    # 计算平均值
    avg_sales = sales_by_state.mean()

    fig = go.Figure(go.Bar(
        x=sales_by_state.index,
        y=sales_by_state.values,
        marker=dict(color=colors, line=dict(width=0)),
        text=[f'${val:,.0f}' for val in sales_by_state.values],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>销售额: %{y:$,.2f}<extra></extra>'
    ))

    # 添加平均线
    fig.add_hline(
        y=avg_sales,
        line_dash="dash",
        line_color='rgba(100, 100, 100, 0.5)',
        annotation_text=f"平均: ${avg_sales:,.0f}",
        annotation_position="top right"
    )

    fig.update_layout(
        title='Sales by State (Top 10)',
        height=UIConfig.CHART_HEIGHT,
        yaxis=dict(tickprefix='$', tickformat=',.0f')
    )

    return fig
```

---

#### 子任务1.5: Daily Trend图表优化（3.5小时）

**最复杂的图表** - 趋势线 + 最高最低点标注 + 渐变填充

**新增函数**: `create_daily_trend_chart(analyzer)`

```python
def create_daily_trend_chart(analyzer):
    """创建Daily Trend折线图（趋势线 + 标注 + 渐变）"""
    import plotly.graph_objects as go

    daily_trend = analyzer.get_daily_trend()
    dates = daily_trend.index
    sales = daily_trend.values

    # 主折线
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=sales,
        mode='lines+markers',
        line=dict(color=ChartColors.PRIMARY, width=UIConfig.LINE_WIDTH),
        marker=dict(size=UIConfig.MARKER_SIZE, color=ChartColors.PRIMARY),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.15)',  # 15%透明度
        name='Daily Sales',
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>销售额: %{y:$,.2f}<extra></extra>'
    ))

    # 添加趋势线（简化的scipy降级处理）
    try:
        from scipy import stats

        x_numeric = list(range(len(dates)))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_numeric, sales)
        trend_line = [slope * x + intercept for x in x_numeric]

        fig.add_trace(go.Scatter(
            x=dates,
            y=trend_line,
            mode='lines',
            line=dict(dash='dash', color=ChartColors.ACCENT, width=2),
            name=f'趋势线 (R²={r_value**2:.2f})',
            hovertemplate='趋势: %{y:$,.2f}<extra></extra>'
        ))
    except ImportError:
        st.sidebar.warning("⚠️ 趋势线需要scipy：pip install scipy")
    except Exception as e:
        print(f"⚠️ 趋势线计算失败: {e}")

    # 标注最高点和最低点
    if len(sales) > 0:
        max_idx = sales.argmax()
        min_idx = sales.argmin()

        # 最高点
        fig.add_annotation(
            x=dates[max_idx],
            y=sales[max_idx],
            text=f"📈 最高<br>${sales[max_idx]:,.2f}",
            showarrow=True,
            arrowhead=2,
            ay=-50,
            bgcolor=ChartColors.SUCCESS,
            bordercolor=ChartColors.PRIMARY,
            borderwidth=2
        )

        # 最低点
        fig.add_annotation(
            x=dates[min_idx],
            y=sales[min_idx],
            text=f"📉 最低<br>${sales[min_idx]:,.2f}",
            showarrow=True,
            arrowhead=2,
            ay=50,
            bgcolor=ChartColors.WARNING,
            bordercolor=ChartColors.ACCENT,
            borderwidth=2
        )

    fig.update_layout(
        title='Daily Sales Trend',
        height=UIConfig.CHART_HEIGHT,
        xaxis=dict(tickformat='%m/%d'),
        yaxis=dict(tickprefix='$', tickformat=',.0f')
    )

    return fig
```

---

### 任务1.6: 指标卡片优化（1.5小时）

**新增工具函数**（直接在app.py中定义，保持独立便于提取）:

```python
# ==================== 工具函数（未来可提取为utils/formatting.py）====================
def safe_divide(numerator, denominator, fallback='N/A'):
    """
    安全除法，防止除零错误

    设计考虑：
    - 当前：在app.py中定义，避免文件碎片化
    - 未来：如需复用，可提取为 utils/formatting.py
    - 函数签名保持稳定，便于后续添加装饰器

    Args:
        numerator: 分子
        denominator: 分母
        fallback: 除零时的返回值

    Returns:
        除法结果或fallback值
    """
    if denominator == 0 or denominator is None:
        return fallback
    try:
        return numerator / denominator
    except (ZeroDivisionError, TypeError):
        return fallback

def format_currency(value, currency='$'):
    """格式化货币显示"""
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
```

**新增函数**: `show_enhanced_metrics(analyzer)`

```python
def show_enhanced_metrics(analyzer):
    """显示增强的指标卡片"""
    total_sales = analyzer.get_total_sales()
    total_orders = len(analyzer.df)
    avg_order = safe_divide(total_sales, total_orders)

    col1, col2, col3 = st.columns(3)

    metrics = [
        {'label': 'Total Sales', 'value': format_currency(total_sales), 'icon': '💰'},
        {'label': 'Total Orders', 'value': format_number(total_orders), 'icon': '📦'},
        {'label': 'Average Order', 'value': format_currency(avg_order), 'icon': '📊'}
    ]

    for col, metric in zip([col1, col2, col3], metrics):
        with col:
            st.markdown(f"""
                <div class="saas-card metric-card" style="text-align: center; padding: 25px;">
                    <div style="color: #86868B; font-size: 0.9rem; margin-bottom: 12px;">
                        {metric['icon']} {metric['label']}
                    </div>
                    <div style="font-size: 2.2rem; font-weight: 700; color: {ChartColors.PRIMARY};">
                        {metric['value']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
```

---

### 任务1.7: 2列布局实现（2小时）

```python
def show_dashboard(analyzer):
    """Dashboard主函数（2列布局）"""

    # 指标卡片
    show_enhanced_metrics(analyzer)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2列布局：图表 + AI对话
    col_charts, col_chat = st.columns([2, 1])

    with col_charts:
        # 所有图表
        st.plotly_chart(create_top_products_chart(analyzer), use_container_width=True)
        st.plotly_chart(create_sales_by_state_chart(analyzer), use_container_width=True)
        st.plotly_chart(create_daily_trend_chart(analyzer), use_container_width=True)

    with col_chat:
        st.subheader("💬 AI Assistant")

        # 快捷问题按钮
        questions = [
            "哪个产品卖得最好？",
            "本周销售比上周如何？",
            "哪个州销售额最高？",
            "销售趋势是上升还是下降？",
            "平均订单金额是多少？"
        ]

        for q in questions:
            if st.button(q, key=f"quick_{hash(q)}", use_container_width=True):
                # 触发AI查询
                st.session_state.user_question = q
```

---

## 阶段2: 功能增强 (8小时)

### 任务2.1: AI洞察扩展到10条（4小时）

**修改文件**: `utils/analyzer.py`

**安全工具函数**（在analyzer.py顶部定义，保持独立便于复用）:

```python
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
```

**重写detect_anomalies方法**:

```python
from typing import List, Dict, Any

def detect_anomalies(self) -> List[Dict[str, Any]]:
    """
    检测销售数据异常并生成分类洞察

    Returns:
        List[Dict]: 每个洞察包含：
            - category: 'opportunity' | 'risk' | 'trend'
            - emoji: 对应emoji
            - title: 洞察标题
            - detail: 详细说明
            - color: 背景色
    """
    insights = []

    if self.df.empty:
        return insights

    # 基础统计
    daily_sales = self.get_daily_trend()
    total_sales = self.get_total_sales()
    total_orders = len(self.df)

    if len(daily_sales) < 1:
        return insights

    mean_sales = daily_sales.mean()
    std_sales = daily_sales.std()

    # ========== 机会类洞察 (Opportunities) ==========

    # 洞察1: 销售高峰日
    if std_sales > 0:
        high_threshold = mean_sales + 2 * std_sales
        high_days = daily_sales[daily_sales > high_threshold]

        if not high_days.empty:
            best_day = high_days.idxmax()
            best_amount = high_days.max()
            pct_above = safe_percentage_change(best_amount, mean_sales)

            if pct_above != 'N/A':
                insights.append({
                    'category': 'opportunity',
                    'emoji': '🔥',
                    'title': f'销售高峰日: {best_day}',
                    'detail': f'该日销售额 ${best_amount:,.2f}，比日均高 {pct_above:.1f}%。分析该日的营销活动或外部因素，可复制成功经验。',
                    'color': '#d4edda'
                })

    # 洞察2: 高客单价机会
    avg_order = safe_divide(total_sales, total_orders)
    if avg_order != 'N/A' and avg_order > 50:
        insights.append({
            'category': 'opportunity',
            'emoji': '💎',
            'title': f'客单价较高: ${avg_order:,.2f}',
            'detail': f'平均订单价值超过 $50，说明客户购买力强。建议推出高价值产品组合或会员计划。',
            'color': '#d4edda'
        })

    # 洞察3: 增长趋势
    if len(daily_sales) >= 4:
        mid_point = len(daily_sales) // 2
        first_half_avg = daily_sales[:mid_point].mean()
        second_half_avg = daily_sales[mid_point:].mean()
        growth_rate = safe_percentage_change(second_half_avg, first_half_avg)

        if growth_rate != 'N/A' and growth_rate > 10:
            insights.append({
                'category': 'opportunity',
                'emoji': '📈',
                'title': f'销售持续增长 ({growth_rate:.1f}%)',
                'detail': f'数据后半段销售比前半段增长 {growth_rate:.1f}%，趋势向好。建议增加库存和营销投入。',
                'color': '#d4edda'
            })

    # ========== 风险类洞察 (Risks) ==========

    # 洞察4: 销售低谷日
    if std_sales > 0:
        low_threshold = mean_sales - 2 * std_sales
        low_days = daily_sales[daily_sales < low_threshold]

        if not low_days.empty:
            worst_day = low_days.idxmin()
            worst_amount = low_days.min()
            pct_below = safe_percentage_change(worst_amount, mean_sales)

            if pct_below != 'N/A':
                insights.append({
                    'category': 'risk',
                    'emoji': '⚠️',
                    'title': f'销售低谷日: {worst_day}',
                    'detail': f'该日销售额仅 ${worst_amount:,.2f}，比日均低 {abs(pct_below):.1f}%。需调查原因。',
                    'color': '#fff3cd'
                })

    # 洞察5: 产品集中度风险
    if 'Product Name' in self.df.columns:
        all_product_sales = self.df.groupby('Product Name')['Quantity'].sum()
        if len(all_product_sales) > 0:
            top_product_sales = all_product_sales.max()
            total_quantity = all_product_sales.sum()
            concentration_pct = safe_divide(top_product_sales, total_quantity)

            if concentration_pct != 'N/A' and concentration_pct > 0.4:
                top_product_name = all_product_sales.idxmax()
                insights.append({
                    'category': 'risk',
                    'emoji': '⚠️',
                    'title': '产品集中度过高',
                    'detail': f'"{top_product_name}" 占总销量 {concentration_pct*100:.1f}%。过度依赖单一产品存在风险。',
                    'color': '#fff3cd'
                })

    # 洞察6: 地区集中度风险
    if 'Customer State' in self.df.columns:
        state_sales = self.get_sales_by_state()
        if len(state_sales) > 0:
            top_state_sales = state_sales.iloc[0]
            concentration_pct = safe_divide(top_state_sales, total_sales)

            if concentration_pct != 'N/A' and concentration_pct > 0.5:
                top_state = state_sales.index[0]
                insights.append({
                    'category': 'risk',
                    'emoji': '🗺️',
                    'title': f'地区过度集中: {top_state}',
                    'detail': f'{top_state} 州占总销售额 {concentration_pct*100:.0f}%。建议拓展其他地区市场。',
                    'color': '#fff3cd'
                })

    # ========== 趋势类洞察 (Trends) ==========

    # 洞察7-10 类似实现...
    # （完整代码见计划文档）

    return insights[:10]  # 最多返回10条
```

**在app.py中的显示**:

```python
def show_categorized_insights(analyzer):
    """显示分类洞察（3列布局）"""
    insights = analyzer.detect_anomalies()

    if not insights:
        st.info("📊 暂无洞察数据")
        return

    st.subheader("🤖 AI 业务洞察")

    # 按类别分组
    opportunities = [i for i in insights if i['category'] == 'opportunity']
    risks = [i for i in insights if i['category'] == 'risk']
    trends = [i for i in insights if i['category'] == 'trend']

    col1, col2, col3 = st.columns(3)

    # 机会列
    with col1:
        st.markdown(f"""
            <div style="background: #d4edda; padding: 15px; border-radius: 8px; text-align: center;">
                <h4>🔥 机会 ({len(opportunities)})</h4>
            </div>
        """, unsafe_allow_html=True)

        for insight in opportunities:
            with st.expander(f"{insight['emoji']} {insight['title']}"):
                st.markdown(f"""
                    <div style="background-color: {insight['color']};
                                padding: 15px; border-radius: 8px;
                                border-left: 4px solid #1f77b4;">
                        {insight['detail']}
                    </div>
                """, unsafe_allow_html=True)

    # 风险列和趋势列类似...
```

---

### 任务2.2: 3套Demo数据生成（2.5小时）

**修改文件**: `utils/template_generator.py`

**新增3个方法**:

```python
@staticmethod
def generate_ecommerce_data() -> pd.DataFrame:
    """生成电商场景数据"""
    import random
    from datetime import datetime, timedelta

    products = {
        'Wireless Headphones': (79.99, 149.99),
        'Smart Watch': (199.99, 399.99),
        'Laptop Stand': (29.99, 59.99),
        'USB-C Hub': (39.99, 79.99),
        'Mechanical Keyboard': (89.99, 179.99),
        'Webcam HD': (49.99, 99.99),
        'Mouse Wireless': (19.99, 49.99),
        'Monitor 27"': (249.99, 499.99),
        'Desk Lamp LED': (29.99, 69.99),
        'Phone Stand': (14.99, 29.99)
    }

    states = ['CA', 'NY', 'TX', 'FL', 'IL']
    start_date = datetime.now() - timedelta(days=14)

    data = []
    for i in range(300):
        product = random.choice(list(products.keys()))
        price_range = products[product]
        price = random.uniform(*price_range)
        quantity = random.randint(1, 3)

        # 周末订单更多
        day_offset = random.randint(0, 13)
        order_date = start_date + timedelta(days=day_offset)

        data.append({
            'Date': order_date,
            'Order ID': f'EC{1000+i}',
            'Product Name': product,
            'Quantity': quantity,
            'Price': price,
            'Customer State': random.choice(states),
            'Total': price * quantity
        })

    return pd.DataFrame(data)

# 类似实现 generate_restaurant_data() 和 generate_retail_data()
```

**在app.py的sidebar中添加**:

```python
st.sidebar.markdown("---")
st.sidebar.subheader("📦 或加载Demo数据")

demo_type = st.sidebar.selectbox(
    "选择Demo类型",
    ["", "电商场景", "餐饮场景", "零售场景"],
    key="demo_selector"
)

if demo_type and st.sidebar.button("🚀 加载Demo", key="load_demo"):
    with st.spinner("正在生成Demo数据..."):
        if demo_type == "电商场景":
            demo_df = TemplateGenerator.generate_ecommerce_data()
        elif demo_type == "餐饮场景":
            demo_df = TemplateGenerator.generate_restaurant_data()
        else:
            demo_df = TemplateGenerator.generate_retail_data()

        st.session_state.analyzer = SalesAnalyzer(demo_df)
        st.success(f"✅ {demo_type}数据已加载（{len(demo_df)}条记录）")
        st.rerun()
```

---

### 任务2.3: 周/月对比功能（1.5小时）

**在analyzer.py中新增方法**:

```python
def get_week_comparison(self) -> Dict[str, Any]:
    """
    计算本周vs上周对比

    Returns:
        Dict or None: 对比数据或None（数据不足）
    """
    if 'Date' not in self.df.columns:
        return None

    df_sorted = self.df.sort_values('Date')

    # 检查数据是否>14天
    date_range = (df_sorted['Date'].max() - df_sorted['Date'].min()).days
    if date_range < 14:
        return None

    # 获取最近14天数据
    latest_date = df_sorted['Date'].max()
    two_weeks_ago = latest_date - pd.Timedelta(days=14)
    recent_data = df_sorted[df_sorted['Date'] > two_weeks_ago]

    # 分割本周和上周
    one_week_ago = latest_date - pd.Timedelta(days=7)
    current_week = recent_data[recent_data['Date'] > one_week_ago]['Total'].sum()
    previous_week = recent_data[recent_data['Date'] <= one_week_ago]['Total'].sum()

    growth_rate = safe_percentage_change(current_week, previous_week)

    return {
        'current_week': current_week,
        'previous_week': previous_week,
        'growth_rate': growth_rate,
        'status': 'increase' if growth_rate > 0 else 'decrease'
    }
```

**在app.py中显示**:

```python
def show_comparison_metrics(analyzer):
    """显示周/月对比（如果数据足够）"""
    week_comp = analyzer.get_week_comparison()

    if week_comp is None:
        return  # 数据不足，不显示

    st.markdown("### 📊 期间对比")
    col1, col2, col3 = st.columns(3)

    with col1:
        growth = week_comp['growth_rate']
        arrow = '↑' if growth > 0 else '↓'

        st.metric(
            label="销售额增长",
            value=f"{abs(growth):.1f}%",
            delta=f"{arrow} 本周vs上周",
            delta_color="normal" if growth > 0 else "inverse"
        )
```

---

## 阶段3: 测试与交付 (2小时)

### 任务3.1: 全面测试（1小时）

**功能测试清单**:
- [ ] 首页3步流程显示
- [ ] 3个图表升级效果（颜色、趋势线、标注）
- [ ] AI洞察10条分类
- [ ] 周/月对比
- [ ] 3套Demo数据切换
- [ ] AI问答功能

**边缘测试**:
- [ ] 空数据上传 → 友好提示
- [ ] 单行数据 → 不崩溃
- [ ] 数据<14天 → 不显示对比
- [ ] scipy未安装 → 趋势线降级

**性能测试**:
- [ ] 500行数据 < 5秒加载

**浏览器测试**:
- [ ] Chrome
- [ ] Edge

---

### 任务3.2: 准备交付物（1小时）

```bash
# 1. 截图
# 2. 更新README.md
# 3. 整理代码注释
# 4. 创建commit
git add .
git commit -m "UI升级: 专业图表+10条AI洞察+Demo数据"
git tag -a v1.4.0 -m "UI升级版本"
```

---

## 📊 成功标准（100分制）

- [ ] 界面专业度（40分）
- [ ] 功能完整性（30分）
- [ ] 视觉质量（20分）
- [ ] 可用性（10分）

**目标总分**: ≥90分（优秀）

---

## 🚀 未来升级路径（V1.5+）

### 代码结构优化（+2小时）
- 提取 `ChartColors` → `config_extended.py`
- 统一工具函数 → `utils/formatting.py`

### 性能优化（+3小时）
- 添加缓存装饰器

### 移动端深度优化（+3小时）
- 触摸优化、手势支持

### 测试框架（+4小时）
- 30+单元测试

### 多主题支持（+2小时）
- 深色模式、高对比度

**总升级成本**: 12-14小时（可选）

---

**计划版本**: v4.0 最终对齐版（预留扩展性）
**创建时间**: 2026-01-04
**当前预期**: 24-28小时（V1.4完成）
**扩展潜力**: +12-14小时（V1.5+可选升级）
**预期成功率**: 95%
