# AI Sales Analyzer - Quick Start Guide

## 🚀 Installation & Setup

### 1. Install Dependencies
```bash
cd ai-excel-analyzer
pip install -r requirements.txt
```

**Key packages installed**:
- streamlit (web framework)
- pandas, openpyxl (data processing)
- plotly (charts)
- langchain, langchain-experimental, openai (AI features)

### 2. Configure API Key

**Option A: Use .env file (Recommended)**
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

**Option B: Enter in app**
- Leave .env as is
- Enter API key in sidebar when using the app

### 3. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📊 How to Use

### Step 1: Upload Data
1. Click "Browse files" in the left sidebar
2. Select your Excel (.xlsx) or CSV (.csv) file
3. Wait 2-5 seconds for automatic analysis

### Step 2: View Dashboard
Automatically displays:
- Total sales, order count, average order value
- Top 5 best-selling products (bar chart)
- Sales by state (bar chart)
- Daily sales trend (line chart)
- Business insights (AI-detected patterns)

### Step 3: Ask AI Questions (Optional)
Type questions like:
- "Which product sold the most on Monday?"
- "What was the total sales on Nov 20?"
- "Which state had the highest sales?"

### Step 4: Export Results
- Click "📊 Download Excel Report" for full analysis
- Click "📄 Download CSV Data" for raw data

---

## 📁 Data Format

Your file must have these columns (names can vary):

| Required Column | Accepted Names |
|----------------|----------------|
| Date | Date, Order Date, Created at |
| Order ID | Order ID, Order_ID, Order Number |
| Product Name | Product Name, Product_Name, Lineitem name |
| Quantity | Quantity, Qty |
| Price | Price, Unit Price |
| Customer State | Customer State, State, Shipping Province |
| Total | Total, Amount, Subtotal |

**Example format**:
```
Date       | Order_ID | Product_Name    | Quantity | Price | State | Total
2024-11-18 | 1001     | Hydrating Serum | 2        | 29.99 | CA    | 59.98
```

---

## 🧪 Test with Sample Data

Use the included sample data to test:

**Option 1: Download from app**
- Click "📊 Sample Data" in sidebar
- Upload the downloaded file

**Option 2: Use included file**
- Upload `sample_data/example_sales.xlsx`
- Contains 50+ real sales records

---

## 💰 Cost Information

### AI Features Cost
- **Model**: GPT-3.5-turbo (cost-optimized)
- **Cost per question**: ~$0.001
- **60% questions**: Answered locally (FREE)
- **30% questions**: From cache (FREE)
- **10% questions**: Use API (~$0.001 each)

**Estimated monthly cost**: $0.10-0.50

### Usage Limits
- Daily: 50 AI questions
- Weekly: 200 AI questions

Check usage in sidebar: "💰 API Usage"

---

## 🔒 Privacy & Security

✅ **Your data is safe**:
- Data only in browser memory
- Auto-deleted when you close browser
- No permanent storage
- HTTPS encrypted

⚠️ **OpenAI API**:
- Only AI questions are sent to OpenAI
- Not your entire dataset
- See [OpenAI Privacy Policy](https://openai.com/privacy)

---

## 🐛 Troubleshooting

### Import Error: langchain_experimental
```bash
pip install langchain-experimental>=0.0.47
```

### "Missing required columns" Error
- Download blank template from sidebar
- Check your column names match requirements
- System auto-maps common variants

### AI Not Working
- Check API key is entered correctly
- Verify you have API credits
- Dashboard works without AI

### App Won't Start
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version (need 3.10+)
python --version
```

---

## 📝 File Structure

```
ai-excel-analyzer/
├── app.py              # Main application
├── config.py           # Settings & UI text
├── requirements.txt    # Dependencies
├── .env               # Your API key (create from .env.example)
├── utils/             # Core modules
│   ├── data_processor.py
│   ├── analyzer.py
│   ├── ai_agent.py
│   └── ...
├── docs/              # Documentation
│   ├── USER_GUIDE.md
│   └── PRIVACY.md
└── sample_data/       # Example data
    └── example_sales.xlsx
```

---

## 🚀 Deployment to Streamlit Cloud (Free)

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

### 2. Deploy
1. Go to https://share.streamlit.io
2. Click "New app"
3. Connect your GitHub repository
4. Select `app.py` as main file
5. Add secrets (API key) in settings:
   ```toml
   OPENAI_API_KEY = "sk-your-key-here"
   ```
6. Click "Deploy"

### 3. Share
Your app will be live at: `https://your-app-name.streamlit.app`

---

## ✅ Verification Checklist

Before deploying, test:
- [ ] Upload sample data successfully
- [ ] Dashboard displays correctly
- [ ] Charts render properly
- [ ] AI assistant works (with API key)
- [ ] Export Excel works
- [ ] Export CSV works
- [ ] Template downloads work
- [ ] Mobile view looks good

---

## 📞 Support

For issues:
1. Check this guide
2. Review `docs/USER_GUIDE.md`
3. Check `docs/PRIVACY.md` for data questions

---

**Ready to analyze your sales data!** 🎉
