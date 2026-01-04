# AI Excel Analyzer 升级任务清单（对齐版）

> **版本**: v2.1 对齐版（预留扩展性）
> **优化时间**: 2026-01-04
> **项目规模**: 100人桌面网页demo
> **核心需求**: UI专业美观 + 功能完整 + 预留升级空间
> **预估总工时**: 24-28小时（3-5天）

---

## 📊 任务概览

- **总任务数**: 14个
- **已完成**: 0个
- **进行中**: 0个
- **待开始**: 14个

---

## 🎯 设计原则

**当前阶段**：快速实现核心功能，避免过度工程化
**未来考虑**：代码结构清晰，便于后续扩展和优化

### 简化策略（预留扩展性）
- 🔄 **配置管理**：在代码顶部集中定义常量（便于以后提取）
- 🔄 **工具函数**：保持函数独立性，添加完整文档（便于以后移动）
- 🔄 **版本检测**：用try-except简化，预留警告机制接口
- 🔄 **移动端**：保留CSS媒体查询结构，但不深度优化
- 🔄 **测试**：代码保持可测试性（函数职责单一）
- 🔄 **缓存**：数据查询保持函数化（便于以后加缓存装饰器）

---

## 第0阶段：准备工作（2小时）

### ☐ 任务0.1: 环境准备与依赖更新 ⭐⭐⭐
**优先级**: 最高 | **预估时间**: 1小时

**具体工作**:
- [ ] 备份项目：`git tag -a v1.0-backup -m "升级前备份"`
- [ ] 创建开发分支：`git checkout -b feature/ui-upgrade`
- [ ] 更新 `requirements.txt`（添加scipy、numpy、cachetools）
- [ ] 执行：`pip install -r requirements.txt`
- [ ] 验证：`python -c "import scipy; print('✅ scipy OK')"`

**修改文件**: `requirements.txt`

**新增依赖**:
```text
scipy>=1.11.0,<1.15.0        # 趋势线回归分析
numpy>=1.24.0,<2.0.0         # 数值计算（显式依赖）
cachetools>=5.3.0,<6.0.0     # 简单缓存（可选）
```

**验收标准**:
- ✓ scipy安装成功（趋势线功能需要）
- ✓ git备份标签已创建

---

### ☐ 任务0.2: 运行基准测试 ⭐
**优先级**: 高 | **预估时间**: 1小时

**具体工作**:
- [ ] 运行现有版本：`streamlit run app.py`
- [ ] 测试上传sample_data中的数据
- [ ] 记录加载时间、图表渲染时间
- [ ] 截图现有界面（对比用）
- [ ] 确认所有功能正常

---

## 第1阶段：视觉升级（14小时）

### ☐ 任务1.1: CSS主题色统一 ⭐
**优先级**: 最高 | **预估时间**: 1小时

**具体工作**:
1. 在CSS中定义CSS变量：
```css
:root {
    --primary-blue: #1f77b4;
    --accent-orange: #ff7f0e;
    --light-blue: #aec7e8;
    --success-green: #d4edda;
    --warning-yellow: #fff3cd;
    --danger-red: #f8d7da;
    --info-blue: #d1ecf1;
}
```

2. 在Python代码中定义配色常量（便于后续提取）：
```python
# ==================== 配置常量（未来可提取为config_extended.py）====================
class ChartColors:
    """图表配色方案（便于统一修改和主题切换）"""
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

**修改文件**: `app.py`（CSS部分和顶部常量定义）

**设计考虑**:
- ✅ 当前：直接在代码中定义，简单快速
- 🔄 未来：可一键提取为 `config_extended.py`

**验收标准**:
- ✓ 主题色统一为深蓝 #1f77b4
- ✓ 常量已集中定义，便于提取

---

### ☐ 任务1.2: 首页重设计
**优先级**: 高 | **预估时间**: 2小时

**具体工作**:
- [ ] 添加slogan: "30秒看懂你的数据 - AI驱动的Excel分析"
- [ ] 创建3步流程卡片（上传→分析→导出）
- [ ] 使用统一配色和圆角样式
- [ ] 添加行动号召（CTA）

**修改文件**: `app.py`

**新增函数**: `show_hero_page()`

**验收标准**:
- ✓ Slogan醒目清晰
- ✓ 3步卡片并排显示
- ✓ 配色统一

---

### ☐ 任务1.3: Top Products图表优化 ⭐⭐⭐
**优先级**: 最高 | **预估时间**: 2.5小时

**具体工作**:
- [ ] 修改为横向条形图（更美观）
- [ ] 使用深蓝色渐变
- [ ] 条内显示数值（白色文字）
- [ ] 优化hover提示：产品名 + 销量
- [ ] 高度统一：450px
- [ ] 标题18px加粗居中

**修改文件**: `app.py`（第362-385行附近）

**新增函数**: `create_top_products_chart(analyzer)`

**验收标准**:
- ✓ 深蓝色渐变效果
- ✓ 条内数值清晰可读
- ✓ hover显示完整信息

---

### ☐ 任务1.4: Sales by State图表优化 ⭐⭐⭐
**优先级**: 最高 | **预估时间**: 2.5小时

**具体工作**:
- [ ] Top 3州用橙色高亮，其他用深蓝
- [ ] 添加平均销售额参考线（灰色虚线）
- [ ] Y轴格式化：$符号 + 千位分隔符
- [ ] 柱顶显示金额
- [ ] 优化hover：州名 + 金额 + 排名

**修改文件**: `app.py`（第387-404行附近）

**新增函数**: `create_sales_by_state_chart(analyzer)`

**验收标准**:
- ✓ Top 3橙色高亮明显
- ✓ 平均线显示清晰
- ✓ 金额格式正确

---

### ☐ 任务1.5: Daily Trend图表优化 ⭐⭐⭐
**优先级**: 最高 | **预估时间**: 3.5小时

**具体工作**:
- [ ] 线条加粗到4px
- [ ] 线下区域填充蓝色渐变（15%透明度）
- [ ] 添加趋势线（使用scipy线性回归，需处理scipy未安装情况）
- [ ] 标注最高点和最低点（emoji + 金额）
- [ ] 圆点标记增大到8px
- [ ] 日期格式：MM/DD，金额格式：$X,XXX

**修改文件**: `app.py`

**新增函数**: `create_daily_trend_chart(analyzer)`

**关键代码**（scipy降级处理）:
```python
# 简化的scipy降级处理（不创建单独模块）
try:
    from scipy import stats
    x = list(range(len(dates)))
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, sales)
    trend_line = [slope * i + intercept for i in x]

    fig.add_trace(go.Scatter(
        x=dates, y=trend_line,
        mode='lines',
        line=dict(dash='dash', color='#ff7f0e', width=2),
        name=f'趋势线 (R²={r_value**2:.2f})'
    ))
except ImportError:
    st.sidebar.warning("⚠️ 趋势线需要scipy：pip install scipy")
except Exception as e:
    print(f"趋势线计算失败: {e}")
```

**验收标准**:
- ✓ 渐变填充美观
- ✓ 趋势线显示（如scipy可用）
- ✓ 最高最低点标注清晰
- ✓ scipy未安装时显示警告但不崩溃

---

### ☐ 任务1.6: 指标卡片优化
**优先级**: 中 | **预估时间**: 1.5小时

**具体工作**:
- [ ] 统一卡片样式（圆角、阴影）
- [ ] 添加图标（💰📦📊）
- [ ] 数值格式化（千位分隔符、$符号）
- [ ] 防止除零错误：平均订单金额计算

**安全工具函数**（直接在app.py中定义，保持独立便于提取）:
```python
# ==================== 工具函数（未来可提取为utils/formatting.py）====================
def safe_divide(numerator, denominator, fallback='N/A'):
    """安全除法，防止除零错误"""
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

**修改文件**: `app.py`

**新增函数**: `show_enhanced_metrics(analyzer)`

**设计考虑**:
- ✅ 当前：在app.py中集中定义，避免文件碎片化
- 🔄 未来：如需复用，可提取为 `utils/formatting.py`

**验收标准**:
- ✓ 卡片样式统一
- ✓ 数值格式化正确
- ✓ 无除零错误

---

### ☐ 任务1.7: 2列布局实现
**优先级**: 高 | **预估时间**: 2小时

**具体工作**:
- [ ] 左侧2/3宽度：图表区域
- [ ] 右侧1/3宽度：AI对话框
- [ ] 添加5个快捷问题按钮
- [ ] 对话历史最多10条

**修改文件**: `app.py`

**验收标准**:
- ✓ 2列布局比例正确
- ✓ 快捷按钮可点击
- ✓ 对话框滚动流畅

---

## 第2阶段：功能增强（8小时）

### ☐ 任务2.1: AI洞察扩展到10条 ⭐⭐
**优先级**: 中 | **预估时间**: 4小时

**具体工作**:
- [ ] 在 `utils/analyzer.py` 重写 `detect_anomalies()` 方法
- [ ] 实现10种洞察检测（分3类：机会/风险/趋势）
- [ ] 返回结构化字典列表

**新增洞察类型**:

**机会类** (Opportunities):
1. 销售高峰日（已有，需优化）
2. 高客单价机会（新增）
3. 增长趋势（新增）

**风险类** (Risks):
4. 销售低谷日（已有，需优化）
5. 产品集中度风险（已有，需优化）
6. 地区集中度风险（新增）

**趋势类** (Trends):
7. 周末vs工作日模式（新增）
8. Top 3产品贡献度（新增）
9. 订单量vs销售额相关性（新增）
10. 价格分散度（新增）

**返回格式**:
```python
{
    'category': 'opportunity' | 'risk' | 'trend',
    'emoji': '🔥',
    'title': '标题',
    'detail': '详细说明',
    'color': '#d4edda'  # 背景色
}
```

**安全工具函数**（在analyzer.py顶部定义，保持独立便于复用）:
```python
# ==================== 工具函数（保持独立性，便于提取或测试）====================
def safe_divide(numerator, denominator, fallback='N/A'):
    """安全除法（与app.py中的函数保持一致）

    设计考虑：
    - 未来可提取为utils/math_utils.py统一管理
    - 函数签名保持稳定，方便后续添加装饰器
    """
    if denominator == 0 or denominator is None:
        return fallback
    try:
        return numerator / denominator
    except (ZeroDivisionError, TypeError):
        return fallback

def safe_percentage_change(current, previous):
    """安全计算百分比变化"""
    result = safe_divide(current - previous, previous, fallback=None)
    if result is None or result == 'N/A':
        return 'N/A'
    return round(result * 100, 1)
# ===============================================================================
```

**在app.py中显示**（新增函数 `show_categorized_insights(analyzer)`）

**修改文件**:
- `utils/analyzer.py`
- `app.py`（显示部分）

**扩展性考虑**:
- 🔄 未来统一：可将safe_divide提取到utils/math_utils.py
- 🔄 测试友好：函数职责单一，易于编写单元测试
- 🔄 装饰器扩展：未来可添加@lru_cache优化性能

**验收标准**:
- ✓ 生成8-10条洞察
- ✓ 3分类显示清晰（3列布局）
- ✓ 业务语言通俗易懂

---

### ☐ 任务2.2: 3套Demo数据生成 ⭐⭐
**优先级**: 高 | **预估时间**: 2.5小时

**具体工作**:
- [ ] 在 `utils/template_generator.py` 添加3个函数：
  - `generate_ecommerce_data()` - 电商（服装、电子、家居）
  - `generate_restaurant_data()` - 餐饮（主食、饮料、甜点）
  - `generate_retail_data()` - 零售（快消品）
- [ ] 每套250-350条记录，7-14天时间范围
- [ ] 在sidebar添加下拉选择器
- [ ] 自动加载并分析

**修改文件**:
- `utils/template_generator.py`
- `app.py`（sidebar部分）

**验收标准**:
- ✓ 3套数据真实合理
- ✓ 切换流畅（<2秒）
- ✓ 每套数据都能展示所有功能

---

### ☐ 任务2.3: 周/月对比功能
**优先级**: 中 | **预估时间**: 1.5小时

**具体工作**:
- [ ] 在 `utils/analyzer.py` 添加方法：`get_week_comparison()`
- [ ] 自动检测数据范围（>=14天显示周对比）
- [ ] 显示3个对比卡片：销售额、订单量、平均订单
- [ ] 增长率：绿↑正增长，红↓负增长

**安全计算**:
```python
# 安全计算增长率
growth = safe_percentage_change(current, previous)
color = 'green' if growth > 0 else 'red'
arrow = '↑' if growth > 0 else '↓'
```

**修改文件**:
- `utils/analyzer.py`
- `app.py`

**验收标准**:
- ✓ 增长率计算准确
- ✓ 颜色和箭头显示正确
- ✓ 数据不足时不显示

---

## 第3阶段：测试与交付（2小时）

### ☐ 任务3.1: 全面测试 ⭐⭐⭐
**优先级**: 最高 | **预估时间**: 1小时

**功能测试**:
- [ ] 首页3步流程显示
- [ ] 3个图表升级效果
- [ ] AI洞察10条分类
- [ ] 周/月对比（测试不同数据范围）
- [ ] 3套Demo数据切换
- [ ] AI问答功能

**边缘测试**:
- [ ] 空数据上传
- [ ] 单行数据
- [ ] 数据<14天（不显示对比）
- [ ] scipy未安装（趋势线降级）

**性能测试**:
- [ ] 500行数据<5秒加载

**浏览器测试**:
- [ ] Chrome（主要测试）
- [ ] Edge（简单验证）

**验收标准**:
- ✓ 所有功能测试通过
- ✓ 边缘情况处理正确
- ✓ 性能符合要求

---

### ☐ 任务3.2: 准备交付物 ⭐
**优先级**: 高 | **预估时间**: 1小时

**具体工作**:
- [ ] 截图8张（首页、图表、洞察、对比、Demo）
- [ ] 更新README.md（新功能说明）
- [ ] 整理代码注释
- [ ] 创建git commit: `git commit -m "UI升级: 专业图表+10条AI洞察+Demo数据"`
- [ ] 创建标签: `git tag -a v1.4.0 -m "UI升级版本"`

**交付清单**:
- ✓ 升级后的代码
- ✓ 8张功能截图
- ✓ 更新的README.md
- ✓ requirements.txt

---

## 📈 进度追踪

| 阶段 | 任务数 | 预估时间 | 完成状态 |
|------|-------|---------|---------|
| **阶段0：准备** | 2个 | 2小时 | ⏳ 0/2 |
| **阶段1：视觉** | 7个 | 14小时 | ⏳ 0/7 |
| **阶段2：功能** | 3个 | 8小时 | ⏳ 0/3 |
| **阶段3：测试** | 2个 | 2小时 | ⏳ 0/2 |
| **总计** | 14个 | **24小时** | ⏳ 0/14 |
| **建议缓冲** | - | 4小时 | - |
| **实际预估** | - | **28小时** | - |

**总体进度**: 0/14 (0%)

---

## 📊 文件修改清单

| 文件 | 修改类型 | 预估改动行数 | 任务编号 |
|------|---------|------------|---------|
| `requirements.txt` | 新增 | +3行 | 0.1 |
| `app.py` | 重构 | ~200行（CSS、图表函数、布局） | 1.1-1.7 |
| `utils/analyzer.py` | 重写 | ~150行（detect_anomalies、对比功能） | 2.1, 2.3 |
| `utils/template_generator.py` | 新增 | ~100行（3套Demo数据） | 2.2 |
| `README.md` | 更新 | ~50行 | 3.2 |

**总代码量**: 约500行新增/修改（可控范围）

---

## 🎯 评分目标（100分制）

### 界面专业度（40分）
- [ ] 首页简洁清晰（10分）- 任务1.2
- [ ] 图表配色统一专业（15分）- 任务1.1, 1.3-1.5
- [ ] AI对话框流畅（15分）- 任务1.7

### 功能完整性（30分）
- [ ] 周/月对比准确（10分）- 任务2.3
- [ ] AI洞察有价值（10分）- 任务2.1
- [ ] 样本数据多样化（10分）- 任务2.2

### 视觉质量（20分）
- [ ] 图表精美专业（15分）- 任务1.3-1.5
- [ ] UI整体一致性（5分）- 任务1.1, 1.2, 1.6

### 可用性（10分）
- [ ] 无bug运行（5分）- 任务3.1
- [ ] 加载速度快（5分）- 任务3.1

**目标总分**: ≥90分（优秀）

---

## 🛡️ 风险控制

### Git备份策略
```bash
# 开始前
git tag -a v1.0-backup -m "升级前备份"

# 阶段完成后
git commit -m "阶段X完成"
git tag -a v1.x-phaseX

# 出问题时
git reset --hard v1.0-backup
```

### 快速回滚方案
保留原代码注释版本：
```python
# 旧版本（备份）
# fig = px.bar(data)

# 新版本
fig = go.Figure(go.Bar(...))
```

---

## 🔑 成功关键因素

1. ✅ **先做依赖更新**（任务0.1）- 避免后续scipy报错
2. ✅ **CSS主题色统一**（任务1.1）- 保证视觉一致性
3. ✅ **图表优化是重点**（任务1.3-1.5）- 占评分15分
4. ✅ **简单实用优先** - 代码保持可扩展性，但不过度工程化

---

## 🚀 未来升级路径（V1.5+）

当前版本（V1.4）完成后，如果需要进一步升级，已预留以下扩展点：

### 代码结构优化（+2小时）
- 提取 `ChartColors` → `config_extended.py`
- 统一工具函数 → `utils/formatting.py` + `utils/math_utils.py`

### 性能优化（+3小时）
- 添加缓存装饰器（已预留函数化接口）

### 移动端深度优化（+3小时）
- 当前已预留媒体查询结构，只需增强细节

### 测试框架（+4小时）
- 当前代码已保持可测试性（函数职责单一）

### 多主题支持（+2小时）
- 已使用CSS变量，只需扩展主题定义

**总升级成本**: 12-14小时（可选，按需实施）

---

## 📌 注意事项

1. **备份**: 开始前务必备份（git tag）
2. **顺序**: 严格按照0→1→2→3阶段执行
3. **测试**: 每个阶段完成后简单测试
4. **文档**: 及时更新本文档中的完成状态
5. **简单优先**: 代码直接写在对应文件中，保持可扩展性

---

## 🎉 总结

这个**对齐版todolist**特点：
- ✅ 快速交付（24-28小时）
- ✅ 简单实用（避免过度工程化）
- ✅ **预留升级空间**（代码结构清晰，便于扩展）
- ✅ 重视UI美观和专业度

**与原版对比**:
- 保留了简化版的14个任务和时间估算
- 增加了代码设计考虑和扩展性说明
- 明确了未来升级路径（+12-14小时可选）
- 工具函数保持独立性，便于后续提取

---

*最后更新: 2026-01-04*
*版本: v2.1 对齐版（预留扩展性）*
*当前预期: 24-28小时（V1.4完成）*
*扩展潜力: +12-14小时（V1.5+可选升级）*
