"""
Data Processor Module
Handles file loading, validation, column mapping, and data cleaning
"""

import pandas as pd
import streamlit as st
from typing import List, Tuple
from config import Config, UI_TEXT


class FlexibleDataProcessor:
    """
    Flexible data processor with automatic column mapping
    for Shopify export compatibility
    """
    
    def __init__(self):
        self.required_columns = Config.REQUIRED_COLUMNS
        self.column_mappings = Config.COLUMN_MAPPINGS
    
    def load_file(self, uploaded_file) -> pd.DataFrame:
        """
        Load Excel or CSV file
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            pd.DataFrame: Loaded dataframe
            
        Raises:
            ValueError: If file format is not supported
        """
        try:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'xlsx':
                df = pd.read_excel(uploaded_file, engine='openpyxl')
            elif file_extension == 'csv':
                df = pd.read_csv(uploaded_file)
            else:
                raise ValueError(UI_TEXT["error_invalid_format"])
            
            return df
        
        except Exception as e:
            raise ValueError(f"Error loading file: {str(e)}")
    
    def auto_map_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Automatically map column names to standard format
        Supports multiple Shopify column name variants
        
        Args:
            df: Original dataframe
            
        Returns:
            pd.DataFrame: Dataframe with standardized column names
            
        Raises:
            ValueError: If required columns cannot be found
        """
        column_map = {}
        
        # Try to find each required column
        for standard_name, possible_names in self.column_mappings.items():
            found = False
            for col in df.columns:
                if col in possible_names:
                    column_map[col] = standard_name
                    found = True
                    break
            
            if not found:
                # Try case-insensitive match
                for col in df.columns:
                    if col.lower() in [name.lower() for name in possible_names]:
                        column_map[col] = standard_name
                        found = True
                        break
        
        # Rename columns
        df_renamed = df.rename(columns=column_map)
        
        # Check for missing required columns
        missing = set(self.required_columns) - set(df_renamed.columns)
        
        if missing:
            available_cols = ", ".join(df.columns.tolist())
            raise ValueError(
                UI_TEXT["error_missing_columns"].format(columns=", ".join(missing)) +
                f"\n\nAvailable columns: {available_cols}\n\n" +
                "Please download our template for the correct format."
            )
        
        # Return only required columns
        return df_renamed[self.required_columns]
    
    def validate_file(self, df: pd.DataFrame) -> bool:
        """
        Validate that dataframe has all required columns
        
        Args:
            df: Dataframe to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            ValueError: If validation fails
        """
        missing_cols = set(self.required_columns) - set(df.columns)
        
        if missing_cols:
            raise ValueError(
                UI_TEXT["error_missing_columns"].format(
                    columns=", ".join(missing_cols)
                )
            )
        
        return True
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and prepare data for analysis
        - Convert date column to datetime
        - Convert numeric columns to proper types
        - Handle missing values
        
        Args:
            df: Dataframe to clean
            
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        df_clean = df.copy()
        
        # Convert Date column
        df_clean['Date'] = pd.to_datetime(df_clean['Date'], errors='coerce')
        
        # Convert numeric columns
        numeric_columns = ['Quantity', 'Price', 'Total']
        for col in numeric_columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
        # Drop rows with missing critical values
        df_clean = df_clean.dropna(subset=['Date', 'Product Name', 'Total'])
        
        # Fill missing quantities with 1 (assume single item if not specified)
        df_clean['Quantity'] = df_clean['Quantity'].fillna(1)
        
        # Sort by date
        df_clean = df_clean.sort_values('Date')
        
        return df_clean
    
    def validate_data_quality(self, df: pd.DataFrame) -> List[str]:
        """
        Check data quality and return warnings
        
        Args:
            df: Dataframe to check
            
        Returns:
            List[str]: List of warning messages
        """
        warnings = []
        
        # Check for negative quantities
        if (df['Quantity'] < 0).any():
            warnings.append(UI_TEXT["warning_negative_qty"])
        
        # Check for negative totals
        if (df['Total'] < 0).any():
            warnings.append(UI_TEXT["warning_negative_total"])
        
        # Check date range
        if not df.empty:
            date_range = (df['Date'].max() - df['Date'].min()).days
            if date_range > 31:
                warnings.append(
                    UI_TEXT["warning_date_range"].format(days=date_range)
                )
        
        # Check for missing values
        missing_pct = df.isnull().sum() / len(df) * 100
        for col, pct in missing_pct[missing_pct > 0].items():
            if pct > 5:  # Only warn if > 5% missing
                warnings.append(
                    UI_TEXT["warning_missing_values"].format(
                        column=col, percent=pct
                    )
                )
        
        return warnings
    
    def process_file(self, uploaded_file) -> Tuple[pd.DataFrame, List[str]]:
        """
        Complete file processing pipeline
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            Tuple[pd.DataFrame, List[str]]: (processed dataframe, warnings)
        """
        # Load file
        df = self.load_file(uploaded_file)
        
        # Auto-map columns
        df = self.auto_map_columns(df)
        
        # Validate
        self.validate_file(df)
        
        # Clean data
        df = self.clean_data(df)
        
        # Get quality warnings
        warnings = self.validate_data_quality(df)
        
        return df, warnings
