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

    @staticmethod
    def generate_ecommerce_data(num_rows: int = 300) -> pd.DataFrame:
        """生成电商场景数据（服装、电子、家居）"""
        products = {
            'Wireless Headphones': (79.99, 149.99),
            'Smart Watch': (199.99, 399.99),
            'Laptop Stand': (29.99, 59.99),
            'USB-C Cable': (9.99, 24.99),
            'Webcam HD': (49.99, 89.99),
            'Mechanical Keyboard': (89.99, 179.99),
            'Desk Lamp': (34.99, 69.99),
            'Phone Case': (14.99, 29.99),
            'Bluetooth Speaker': (59.99, 129.99),
            'Monitor': (199.99, 449.99)
        }

        states = ['CA', 'NY', 'TX', 'FL', 'IL']
        start_date = datetime.now() - timedelta(days=14)

        data = []
        for i in range(num_rows):
            product = random.choice(list(products.keys()))
            price_range = products[product]
            price = round(random.uniform(*price_range), 2)
            quantity = random.randint(1, 3)  # 电商一般少量购买

            day_offset = random.randint(0, 14)  # 0-14共15天，确保>=14天
            order_date = start_date + timedelta(days=day_offset)

            # 周末订单更多（70%概率）
            if order_date.weekday() >= 5 and random.random() < 0.3:
                continue

            data.append({
                'Date': order_date.strftime('%Y-%m-%d'),
                'Order ID': f'EC{2000+i}',
                'Product Name': product,
                'Quantity': quantity,
                'Price': price,
                'Customer State': random.choice(states),
                'Total': round(price * quantity, 2)
            })

        return pd.DataFrame(data).sort_values('Date')

    @staticmethod
    def generate_restaurant_data(num_rows: int = 350) -> pd.DataFrame:
        """生成餐饮场景数据（主食、饮料、甜点）"""
        products = {
            'Burger Combo': (8.99, 12.99),
            'Pizza Large': (14.99, 22.99),
            'Pasta Bowl': (11.99, 16.99),
            'Caesar Salad': (7.99, 10.99),
            'Steak Dinner': (19.99, 34.99),
            'Fried Chicken': (9.99, 13.99),
            'Soft Drink': (2.49, 3.99),
            'Coffee Latte': (3.99, 5.99),
            'Dessert Cake': (5.99, 8.99),
            'Ice Cream': (4.99, 6.99)
        }

        states = ['CA', 'NY', 'TX', 'FL', 'IL', 'PA']
        start_date = datetime.now() - timedelta(days=14)

        data = []
        for i in range(num_rows):
            product = random.choice(list(products.keys()))
            price_range = products[product]
            price = round(random.uniform(*price_range), 2)
            quantity = random.randint(1, 4)  # 餐饮可能多份

            day_offset = random.randint(0, 14)  # 0-14共15天，确保>=14天
            order_date = start_date + timedelta(days=day_offset)

            # 周末订单更多（60%概率增加）
            if order_date.weekday() >= 5:
                if random.random() < 0.6:
                    quantity += random.randint(0, 2)

            data.append({
                'Date': order_date.strftime('%Y-%m-%d'),
                'Order ID': f'R{3000+i}',
                'Product Name': product,
                'Quantity': quantity,
                'Price': price,
                'Customer State': random.choice(states),
                'Total': round(price * quantity, 2)
            })

        return pd.DataFrame(data).sort_values('Date')

    @staticmethod
    def generate_retail_data(num_rows: int = 250) -> pd.DataFrame:
        """生成零售场景数据（快消品）"""
        products = {
            'Shampoo 500ml': (12.99, 18.99),
            'Body Wash': (9.99, 14.99),
            'Toothpaste Twin Pack': (6.99, 9.99),
            'Laundry Detergent': (15.99, 24.99),
            'Tissues Box': (4.99, 7.99),
            'Paper Towels': (8.99, 12.99),
            'Dish Soap': (5.99, 8.99),
            'Hand Soap': (4.49, 6.99),
            'Trash Bags': (11.99, 16.99),
            'Air Freshener': (6.99, 10.99)
        }

        states = ['CA', 'NY', 'TX', 'FL', 'IL', 'OH', 'PA']
        start_date = datetime.now() - timedelta(days=14)

        data = []
        for i in range(num_rows):
            product = random.choice(list(products.keys()))
            price_range = products[product]
            price = round(random.uniform(*price_range), 2)
            quantity = random.randint(1, 5)  # 零售可能批量购买

            day_offset = random.randint(0, 14)  # 0-14共15天，确保>=14天
            order_date = start_date + timedelta(days=day_offset)

            data.append({
                'Date': order_date.strftime('%Y-%m-%d'),
                'Order ID': f'RT{4000+i}',
                'Product Name': product,
                'Quantity': quantity,
                'Price': price,
                'Customer State': random.choice(states),
                'Total': round(price * quantity, 2)
            })

        return pd.DataFrame(data).sort_values('Date')
