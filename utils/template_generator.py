"""
Template Generator Module
Generates blank templates and sample data for users
"""

import pandas as pd
import numpy as np
from io import BytesIO
from datetime import datetime, timedelta
import random


class TemplateGenerator:
    """
    Generate Excel templates and sample data
    """
    
    @staticmethod
    def generate_blank_template() -> BytesIO:
        """
        Generate blank Excel template with correct columns
        
        Returns:
            BytesIO: Excel file in memory
        """
        template_df = pd.DataFrame(columns=[
            'Date', 'Order ID', 'Product Name', 
            'Quantity', 'Price', 'Customer State', 'Total'
        ])
        
        output = BytesIO()
        template_df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        return output
    
    @staticmethod
    def generate_sample_data(num_rows: int = 50) -> BytesIO:
        """
        Generate sample sales data for testing
        
        Args:
            num_rows: Number of sample rows to generate
            
        Returns:
            BytesIO: Excel file with sample data
        """
        # Sample products (skincare items)
        products = [
            'Hydrating Serum',
            'Night Cream',
            'Face Wash',
            'Moisturizer',
            'Eye Cream',
            'Toner',
            'Sunscreen SPF 50',
            'Vitamin C Serum',
            'Retinol Cream',
            'Clay Mask'
        ]
        
        # Sample states
        states = ['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']
        
        # Generate data
        data = []
        base_date = datetime.now() - timedelta(days=7)
        order_id_start = 1000
        
        for i in range(num_rows):
            # Random date within last 7 days
            date = base_date + timedelta(days=random.randint(0, 6))
            
            # Random product
            product = random.choice(products)
            
            # Random quantity (1-5)
            quantity = random.randint(1, 5)
            
            # Random price based on product type
            if 'Serum' in product:
                price = round(random.uniform(25.99, 49.99), 2)
            elif 'Cream' in product:
                price = round(random.uniform(29.99, 59.99), 2)
            else:
                price = round(random.uniform(19.99, 39.99), 2)
            
            # Calculate total
            total = round(quantity * price, 2)
            
            # Random state
            state = random.choice(states)
            
            data.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Order ID': order_id_start + i,
                'Product Name': product,
                'Quantity': quantity,
                'Price': price,
                'Customer State': state,
                'Total': total
            })
        
        # Create dataframe
        sample_df = pd.DataFrame(data)
        
        # Sort by date
        sample_df = sample_df.sort_values('Date')
        
        # Export to Excel
        output = BytesIO()
        sample_df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        return output
