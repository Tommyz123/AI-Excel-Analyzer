# AI Sales Analyzer - User Guide

## Quick Start

### Step 1: Access the Application
Open your web browser and navigate to the application URL.

### Step 2: Upload Your Sales Data
1. Click the **"Browse files"** button in the left sidebar
2. Select your Shopify Excel or CSV export file
3. Wait 2-5 seconds for automatic analysis

### Step 3: View Your Dashboard
The dashboard automatically displays:
- **Total Sales**: Your total revenue for the period
- **Order Count**: Number of orders
- **Average Order Value**: Revenue per order
- **Top 5 Products**: Best-selling items by quantity
- **Sales by State**: Geographic distribution
- **Daily Trend**: Sales over time
- **Business Insights**: AI-detected patterns and anomalies

### Step 4: Ask Questions (Optional)
Use the AI Assistant to ask questions in plain English:
- "Which product sold the most on Monday?"
- "What was the total sales on Nov 20?"
- "Which state had the highest sales?"

### Step 5: Export Results
Download your analysis:
- **Excel Report**: Multi-sheet workbook with all metrics
- **CSV Data**: Raw data for further analysis

---

## Data Format Requirements

Your file must contain these columns (column names may vary):

| Column | Description | Example |
|--------|-------------|---------|
| **Date** | Order date | 2024-11-18 |
| **Order ID** | Unique order number | 1001 |
| **Product Name** | Product name | Hydrating Serum |
| **Quantity** | Number of items | 2 |
| **Price** | Unit price in USD | 29.99 |
| **Customer State** | US state code | CA |
| **Total** | Total amount in USD | 59.98 |

**Note**: The system automatically recognizes common Shopify column name variants like "Order Date", "Created at", "Lineitem name", etc.

---

## Using Templates

### Blank Template
Download an empty Excel file with the correct column structure. Use this to:
- Understand the required format
- Manually create test data
- Share format requirements with your team

### Sample Data
Download a file with 50 rows of realistic sample data. Use this to:
- Test the application
- See what insights look like
- Learn how to use features

---

## AI Assistant Tips

### What Works Best
✅ Specific questions about your data  
✅ Questions about trends and patterns  
✅ Comparisons (e.g., "Monday vs Friday sales")  
✅ Simple calculations

### What to Avoid
❌ Questions about data you haven't uploaded  
❌ Questions requiring external information  
❌ Very complex multi-step analysis

### Cost Optimization
The AI Assistant is designed to be cost-efficient:
- **60% of questions** are answered locally (no cost)
- **30% of questions** use cached answers (no cost)
- **Only 10%** require API calls (~$0.001 each)

**Daily Limit**: 50 AI questions  
**Weekly Limit**: 200 AI questions

---

## Privacy & Security

### Your Data is Safe
✅ **No Storage**: Data only exists in your browser's memory  
✅ **Auto-Delete**: Automatically cleared when you close the browser  
✅ **No Database**: We don't save any of your information  
✅ **HTTPS**: All connections are encrypted

### OpenAI API Usage
When you use the AI Assistant:
- Your question and relevant data are sent to OpenAI
- OpenAI processes the request and returns an answer
- OpenAI's privacy policy applies: https://openai.com/privacy

### Recommendations
- Use your own OpenAI API key for maximum privacy
- Don't include sensitive customer information in AI questions
- Download and delete reports after viewing

---

## Troubleshooting

### "Missing required columns" Error
**Problem**: Your file doesn't have the required columns  
**Solution**:
1. Download the blank template to see the correct format
2. Check if your columns have different names
3. The system auto-maps common variants, but very unusual names may not work

### "Invalid file format" Error
**Problem**: File type not supported  
**Solution**: Only .xlsx and .csv files are supported. If you have a different format, save it as Excel or CSV first.

### AI Assistant Not Working
**Problem**: No API key configured  
**Solution**:
1. Enter your OpenAI API key in the sidebar
2. Or use the default key if provided
3. You can still use all other features without AI

### Charts Not Displaying
**Problem**: Browser compatibility  
**Solution**: Use a modern browser (Chrome, Firefox, Safari, Edge - latest versions)

---

## Frequently Asked Questions

**Q: How long does analysis take?**  
A: Usually 2-5 seconds for 200-500 rows of data.

**Q: Can I analyze multiple weeks at once?**  
A: Yes, upload a file with data from multiple weeks. The system will analyze all of it together.

**Q: What's the maximum file size?**  
A: 10 MB, which is enough for thousands of orders.

**Q: Can I use this on my phone?**  
A: Yes! The interface is mobile-friendly.

**Q: Is there a cost to use this?**  
A: The application is free. AI features use OpenAI API which costs ~$0.01-0.50/month depending on usage.

**Q: Can I save my analysis?**  
A: Yes, use the export buttons to download Excel or CSV reports.

**Q: What if my Shopify export has different column names?**  
A: The system automatically recognizes common variants. If it doesn't work, download our template.

---

## Support

For issues or questions:
- Check this guide first
- Review the format guide in the sidebar
- Download sample data to test
- Contact support: [your-email]

---

*Last updated: November 2024*
