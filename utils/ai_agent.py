"""
AI Agent Module
Handles natural language Q&A with cost optimization
- Answer caching
- GPT-3.5-turbo for cost efficiency
"""

import pandas as pd
import hashlib
import json
import os
from typing import Tuple
from openai import OpenAI
from config import Config


class AnswerCache:
    """
    Cache for AI answers to avoid repeated API calls
    """
    
    def __init__(self, cache_file=".qa_cache.json"):
        self.cache_file = cache_file
        self.cache = self._load_cache()
    
    def _load_cache(self) -> dict:
        """Load cache from file"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        """Save cache to file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f)
        except:
            pass  # Fail silently if can't save
    
    def get_cache_key(self, question: str, data_hash: str) -> str:
        """
        Generate cache key from question and data hash
        
        Args:
            question: User question
            data_hash: Hash of the dataframe
            
        Returns:
            str: Cache key
        """
        combined = f"{question.lower().strip()}_{data_hash}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def get(self, question: str, data_hash: str) -> str:
        """Get cached answer"""
        key = self.get_cache_key(question, data_hash)
        return self.cache.get(key)
    
    def set(self, question: str, data_hash: str, answer: str):
        """Save answer to cache"""
        key = self.get_cache_key(question, data_hash)
        self.cache[key] = answer
        self._save_cache()


class AIAgent:
    """
    AI Agent for natural language Q&A
    Uses GPT-3.5-turbo for cost efficiency
    """
    
    def __init__(self, df: pd.DataFrame, analyzer, api_key: str = None):
        """
        Initialize AI agent
        
        Args:
            df: Sales dataframe
            analyzer: SalesAnalyzer instance
            api_key: OpenAI API key (optional, uses config if not provided)
        """
        self.df = df
        self.analyzer = analyzer
        self.api_key = api_key or Config.OPENAI_API_KEY
        
        # Initialize cache
        self.cache = AnswerCache()
        
        # Calculate data hash for caching
        self.data_hash = hashlib.md5(df.to_json().encode()).hexdigest()
        
        # Initialize OpenAI client (lazy loading)
        self._client = None
    
    def _init_client(self):
        """Initialize OpenAI client (lazy loading)"""
        if self._client is None and self.api_key:
            try:
                self._client = OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}")
                self._client = None
    
    def ask(self, question: str) -> Tuple[str, str]:
        """
        Ask a question about the sales data
        
        Args:
            question: Natural language question
            
        Returns:
            Tuple[str, str]: (answer, source) where source is 'cache' or 'api'
        """
        # Check cache first
        cached_answer = self.cache.get(question, self.data_hash)
        if cached_answer:
            return cached_answer, 'cache'
        
        # Use API for all questions to ensure accuracy
        answer = self.ask_api(question)
        
        # Cache the API answer
        self.cache.set(question, self.data_hash, answer)
        return answer, 'api'
    
    def ask_api(self, question: str) -> str:
        """
        Ask question using OpenAI API directly
        
        Args:
            question: User question
            
        Returns:
            str: AI-generated answer
        """
        if not self.api_key:
            return "⚠️ OpenAI API key not configured. Please add your API key to use AI features."
        
        self._init_client()
        
        if self._client is None:
            return "❌ Failed to initialize OpenAI client. Please check your API key."
        
        try:
            # Prepare comprehensive data summary for context
            # Get unique dates and products
            unique_dates = sorted(self.df['Date'].unique())
            unique_products = self.df['Product Name'].unique()
            
            # Get detailed groupings for summary
            orders_by_state = self.df.groupby('Customer State').size().sort_values(ascending=False)
            orders_by_date = self.df.groupby('Date').size()
            sales_by_state = self.df.groupby('Customer State')['Total'].sum().sort_values(ascending=False)
            daily_sales = self.df.groupby('Date')['Total'].sum().to_dict()
            product_sales = self.df.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False)
            
            # Get complete data in CSV format (compact and AI-readable)
            complete_data_csv = self.df.to_csv(index=False)
            
            summary = f"""
=== QUICK REFERENCE SUMMARY ===
(Use this for simple questions like totals, averages, top products)

OVERVIEW:
- Total Sales: ${self.df['Total'].sum():,.2f}
- Total Orders: {len(self.df)}
- Average Order Value: ${self.df['Total'].mean():.2f}
- Date Range: {self.df['Date'].min()} to {self.df['Date'].max()}
- Products: {len(unique_products)} unique products
- States: {len(self.df['Customer State'].unique())} states

TOP 5 PRODUCTS (by quantity sold):
{product_sales.head().to_string()}

ORDERS BY STATE (sorted by count):
{chr(10).join([f"  {state}: {count} orders" for state, count in orders_by_state.head(10).items()])}

SALES BY STATE (sorted by amount):
{chr(10).join([f"  {state}: ${amount:,.2f}" for state, amount in sales_by_state.head(10).items()])}

ORDERS BY DATE:
{chr(10).join([f"  {date}: {count} orders" for date, count in orders_by_date.items()])}

DAILY SALES TOTALS:
{chr(10).join([f"  {date}: ${amount:,.2f}" for date, amount in daily_sales.items()])}

ALL PRODUCT SALES (Total Quantity):
{product_sales.to_string()}

DAILY TOP PRODUCTS (Most sold product for each date):
{chr(10).join([f"  {date}: {self.df[self.df['Date'] == date].groupby('Product Name')['Quantity'].sum().idxmax()} ({self.df[self.df['Date'] == date].groupby('Product Name')['Quantity'].sum().max()} units)" for date in unique_dates])}


=== COMPLETE DATA TABLE ===
(Use this for complex questions requiring filtering, grouping, or specific date analysis)

{complete_data_csv}


=== CRITICAL INSTRUCTIONS ===

1. **For SIMPLE questions** (total sales, top products, state rankings):
   → Use the QUICK REFERENCE SUMMARY above
   → Answer directly from the summary statistics

2. **For COMPLEX questions** (specific dates, filtering, calculations):
   → Analyze the COMPLETE DATA TABLE
   → Filter, group, and calculate as needed
   
3. **Question type examples**:
   - "What are top 5 products?" → Use SUMMARY (already calculated)
   - "Which product sold most on 2024-11-20?" → Use COMPLETE DATA (filter by date)
   - "Most expensive product?" → Use COMPLETE DATA (find max Price)
   - "Total sales?" → Use SUMMARY (already calculated)
   - "Percentage from California?" → Use SUMMARY + calculate percentage

4. **Important clarifications**:
   - "Most expensive" = highest unit Price (not total sales)
   - "Sold most on [date]" = filter by Date, then group by Product Name
   - "Orders" = count of transactions (rows)
   - "Sales" = sum of Total column

5. **Data columns available**:
   - Date: Order date (YYYY-MM-DD format)
   - Order ID: Unique order identifier
   - Product Name: Name of the product
   - Quantity: Number of units sold
   - Price: Unit price per item
   - Customer State: US state code (e.g., CA, NY)
   - Total: Total amount for this transaction
"""
            
            # Call OpenAI API
            response = self._client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful sales data analyst. You have access to COMPLETE sales data. Answer questions accurately based on the comprehensive data summary provided. When asked about specific dates, products, or metrics, use the complete data summary to give precise answers."},
                    {"role": "user", "content": f"{summary}\n\nQuestion: {question}"}
                ],
                temperature=Config.OPENAI_TEMPERATURE,
                max_tokens=Config.OPENAI_MAX_TOKENS,
                timeout=Config.OPENAI_TIMEOUT
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            error_msg = str(e).lower()
            
            if 'authentication' in error_msg or 'api key' in error_msg or 'api_key' in error_msg:
                return "❌ Invalid API key. Please check your OpenAI API key."
            elif 'rate limit' in error_msg:
                return "⚠️ API rate limit exceeded. Please try again in a moment."
            elif 'timeout' in error_msg:
                return "⏱️ Request timed out. Please try again."
            else:
                return f"❌ Error: {str(e)}"
    
    def validate_api_key(self) -> bool:
        """
        Validate that API key is configured and not empty
        
        Returns:
            bool: True if API key is available and valid
        """
        if not self.api_key:
            return False
        
        # Check if it's a placeholder or empty
        api_key_clean = self.api_key.strip()
        if not api_key_clean or api_key_clean == "your-api-key-here":
            return False
        
        # Check if it looks like a valid OpenAI key (starts with sk-)
        if not api_key_clean.startswith('sk-'):
            return False
        
        return True
