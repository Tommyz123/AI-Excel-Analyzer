# 🤖 AI Sales Analyzer

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
- **Multi-Language Support**: Responds in the same language as your question

### 📈 Interactive Dashboard
- Real-time sales metrics and KPIs
- Top products visualization
- Sales by state/region analysis
- Daily sales trends
- Anomaly detection

### 📤 Export & Templates
- Export analysis to Excel/CSV
- Download blank templates
- Sample data for testing

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-sales-analyzer.git
cd ai-sales-analyzer
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

### 1. Upload Your Data
- Click "Browse files" in the sidebar
- Upload an Excel file (.xlsx) with sales data
- Required columns: Date, Order ID, Product Name, Quantity, Price, Customer State, Total

### 2. View Dashboard
- Automatic analysis and visualization
- Key metrics displayed instantly
- Interactive charts and graphs

### 3. Ask Questions
Examples:
- "What are the top 5 best-selling products?"
- "Which state has the most orders?"
- "How many orders on 2024-11-20?"
- "What percentage of sales came from California?"
- "Which product sold most on a specific date?"

### 4. Export Results
- Download analysis as Excel or CSV
- Save reports for sharing

## 🏗️ Architecture

### Pandas Agent (Code Generation)
Unlike traditional chatbots that try to "guess" answers, this tool uses a **Pandas Agent** architecture:

1. **AI receives your question** + data structure (not the data itself)
2. **AI writes Python code** to answer the question
3. **System executes the code** safely
4. **AI formats the result** into natural language

**Benefits:**
- ✅ 100% accuracy (calculations done by Python, not AI estimation)
- ✅ Handles any question (not limited to pre-defined queries)
- ✅ Token-efficient (doesn't send full dataset to AI)

## 📁 Project Structure

```
ai-sales-analyzer/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── utils/
│   ├── pandas_agent.py   # AI code generation engine
│   ├── analyzer.py       # Data analysis logic
│   ├── data_processor.py # Data validation & cleaning
│   ├── exporter.py       # Export functionality
│   └── cost_controller.py # API usage tracking
└── .streamlit/
    └── config.toml       # Streamlit configuration
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
- Change model, temperature, max tokens, etc.
- Configure API rate limits

## 🔒 Security & Privacy

- ✅ API keys stored locally in `.env` (not committed to Git)
- ✅ Data processed locally (not sent to external servers except OpenAI API)
- ✅ Code execution sandboxed (limited to pandas operations)
- ✅ No data persistence (analysis happens in memory)

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **AI**: OpenAI GPT-4o-mini
- **Code Execution**: Python `exec()` with controlled namespace

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

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI](https://openai.com/)
- Inspired by ChatGPT's Advanced Data Analysis

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**⭐ If you find this project useful, please consider giving it a star!**
