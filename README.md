# 🤖 AI Excel Analyzer

An intelligent Excel sales data analysis tool powered by AI code generation. Upload your sales data and ask questions in natural language - the AI will write and execute Python code to give you accurate answers.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

### 📊 Smart Data Analysis
- **AI-Powered Q&A**: Ask questions in natural language (English or Chinese)
- **Code Generation**: AI writes Python code to analyze your data with 100% accuracy
- **Auto-Correction**: Self-healing code execution with automatic retry logic
- **Multi-Language Support**: Full bilingual interface (English/Chinese)
- **Multi-File Comparison**: Compare 2-3 files side-by-side with growth analysis

### 📈 Interactive Dashboard
- Real-time sales metrics and KPIs
- Top products visualization
- Sales by state/region analysis
- Daily sales trends
- Anomaly detection
- Automated business insights

### 📤 Export & Templates
- Export analysis to Excel/CSV
- Download blank templates
- Sample data for testing
- Flexible data format support (auto-detects column names)

### 🔒 Privacy & Cost Control
- Local data processing (no storage)
- API usage tracking and limits
- Smart caching to minimize API costs
- 60% questions answered locally (FREE)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-excel-analyzer.git
cd ai-excel-analyzer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API key**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open your browser**
Navigate to `http://localhost:8501`

## 📖 Usage

### Single File Analysis

1. **Upload Your Data**
   - Click "Browse files" in the sidebar
   - Upload an Excel file (.xlsx) or CSV (.csv)
   - Supports flexible column names (auto-mapping)

2. **View Dashboard**
   - Automatic analysis and visualization
   - Key metrics displayed instantly
   - Interactive charts and graphs

3. **Ask Questions**
   - "What are the top 5 best-selling products?"
   - "Which state has the most orders?"
   - "How many orders on 2024-11-20?"
   - "What percentage of sales came from California?"

4. **Export Results**
   - Download analysis as Excel or CSV
   - Save reports for sharing

### Multi-File Comparison

1. **Select Comparison Mode**
   - Choose "📊 Multi-file Comparison" in sidebar
   - Upload 2-3 files simultaneously (Ctrl/Cmd + Click)

2. **Set File Labels**
   - Customize labels for each file (e.g., "November", "December")
   - Labels appear on all comparison charts

3. **View Comparison Dashboard**
   - Side-by-side metrics cards
   - Growth analysis (% change vs baseline)
   - Comparative charts (sales, orders, top products)
   - Daily trend overlay

See [docs/MULTI_FILE_COMPARISON_GUIDE.md](docs/MULTI_FILE_COMPARISON_GUIDE.md) for detailed instructions.

## 🏗️ Architecture

### Pandas Agent (Code Generation)
Unlike traditional chatbots that try to "guess" answers, this tool uses a **Pandas Agent** architecture:

1. **AI receives your question** + data structure (not the data itself)
2. **AI writes Python code** to answer the question
3. **System executes the code** safely in a controlled namespace
4. **AI formats the result** into natural language

**Benefits:**
- ✅ 100% accuracy (calculations done by Python, not AI estimation)
- ✅ Handles any question (not limited to pre-defined queries)
- ✅ Token-efficient (doesn't send full dataset to AI)
- ✅ Cost-effective (smart caching + local answers)

## 📁 Project Structure

```
ai-excel-analyzer/
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration settings & bilingual UI text
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── QUICKSTART.md                   # Quick start guide
├── utils/
│   ├── pandas_agent.py             # AI code generation engine
│   ├── analyzer.py                 # Data analysis logic
│   ├── comparison_analyzer.py      # Multi-file comparison logic
│   ├── data_processor.py           # Data validation & flexible column mapping
│   ├── exporter.py                 # Export functionality (Excel/CSV)
│   ├── template_generator.py       # Template and sample data generator
│   └── cost_controller.py          # API usage tracking & limits
├── docs/
│   ├── USER_GUIDE.md               # Detailed user guide
│   ├── PRIVACY.md                  # Privacy and security information
│   └── MULTI_FILE_COMPARISON_GUIDE.md  # Multi-file comparison tutorial
├── sample_data/                    # Sample datasets for testing
└── .streamlit/
    └── config.toml                 # Streamlit configuration
```

## ⚙️ Configuration

### Environment Variables (.env)
```env
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o-mini
MAX_DAILY_API_CALLS=1000
MAX_WEEKLY_API_CALLS=5000
```

### Customization
- Modify `config.py` to adjust settings
- Change model, temperature, max tokens
- Configure API rate limits
- Customize bilingual UI text

### Supported Data Formats
The system automatically recognizes common column name variations:

| Required Data | Accepted Column Names |
|--------------|----------------------|
| Date | Date, Order Date, Created at |
| Order ID | Order ID, Order_ID, Order Number |
| Product Name | Product Name, Product_Name, Lineitem name |
| Quantity | Quantity, Qty, Lineitem quantity |
| Price | Price, Unit Price, Lineitem price |
| Customer State | Customer State, State, Shipping Province |
| Total | Total, Amount, Subtotal |

## 🔒 Security & Privacy

- ✅ API keys stored locally in `.env` (not committed to Git)
- ✅ Data processed locally (not stored on servers)
- ✅ Code execution sandboxed (limited to pandas operations)
- ✅ No data persistence (analysis happens in memory)
- ✅ HTTPS encrypted connection
- ✅ OpenAI API only receives questions, not full datasets

For more details, see [docs/PRIVACY.md](docs/PRIVACY.md)

## 🛠️ Tech Stack

- **Frontend**: Streamlit with custom CSS (Apple-inspired design)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly (interactive charts)
- **AI**: OpenAI GPT-4o-mini
- **Code Execution**: Python `exec()` with controlled namespace
- **Internationalization**: Built-in bilingual support (EN/ZH)

## 📊 Example Questions

**Sales Analysis:**
- "What is the total sales for this week?"
- "Show me the average order value"
- "Which day had the highest sales?"

**Product Insights:**
- "Top 10 products by revenue"
- "Which product has the highest unit price?"
- "How many units of Product X were sold?"

**Geographic Analysis:**
- "Sales breakdown by state"
- "Which state has the most orders?"
- "What percentage of sales came from New York?"

**Time-Based Queries:**
- "Sales trend over the past 7 days"
- "How many orders on Monday?"
- "Compare weekday vs weekend sales"

## 💰 Cost Optimization

### Smart Answer Routing
1. **Local Answers (60%)**: Simple queries answered without API (~$0.00)
2. **Cached Answers (30%)**: Previously asked questions (~$0.00)
3. **API Calls (10%)**: Complex queries requiring code generation (~$0.001 each)

### Usage Tracking
- Real-time API usage display in sidebar
- Daily and weekly usage limits
- Cost estimates and warnings
- Automatic caching to minimize costs

**Estimated monthly cost**: $0.10-0.50 for typical usage

## 🌐 Language Support

The application supports full bilingual interface:
- English (EN)
- 中文简体 (ZH)

Switch language using the selector in the top navigation bar. All UI elements, error messages, and insights are automatically translated.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [docs/USER_GUIDE.md](docs/USER_GUIDE.md) - Detailed user guide
- [docs/PRIVACY.md](docs/PRIVACY.md) - Privacy and security information
- [docs/MULTI_FILE_COMPARISON_GUIDE.md](docs/MULTI_FILE_COMPARISON_GUIDE.md) - Multi-file comparison tutorial

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI](https://openai.com/)
- Inspired by ChatGPT's Advanced Data Analysis
- UI design inspired by Apple's design principles

## 📧 Support

For questions or support, please:
1. Check the [QUICKSTART.md](QUICKSTART.md) guide
2. Review the [docs/](docs/) folder for detailed documentation
3. Open an issue on GitHub

---

**⭐ If you find this project useful, please consider giving it a star!**
