# Text-to-SQL-Query-Generator

This is a **Streamlit-based application** that allows users to interact with a sales management database using **natural language queries**. The app translates user queries into **SQL** and retrieves relevant data from a **SQLite database**. It leverages **Google's Gemini Language Model** to convert English questions into SQL queries.

# Features

- **Natural Language Interface**: Ask questions in plain English to retrieve sales data.
- **SQL Query Generation**: The app automatically generates SQL queries based on user input.
- **Database Interaction**: Execute queries on a pre-defined SQLite database that includes products, customers, orders, and sales.
- **Sample Data**: The app comes with pre-populated sample data for quick testing.
- **Results Display**: SQL query results are displayed directly in the app.

# Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Sample Prompts](#sample-prompts)
- [Acknowledgments](#acknowledgments)

# Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/sales-data-query-app.git
   cd sales-data-query-app
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Google Gemini API key**:
   Set the `GOOGLE_API_KEY` environment variable with your Google API key:
   ```bash
   export GOOGLE_API_KEY="your_api_key"
   ```

4. **Run the application**:
   ```bash
   streamlit run sales_query_app.py
   ```

# Usage

1. Once the application is running, you'll be able to ask natural language questions like:
   - "What are the total sales amounts by customer segment?"
   - "Show me all products in the Furniture category."

2. The application will:
   - Convert your question into an SQL query.
   - Execute the query on the SQLite database.
   - Display the results directly in the application.

# Sales Management Schema

The database consists of the following tables:

- **Products**:
  - `product_id`: Unique identifier for each product.
  - `product_name`: Name of the product.
  - `category`: Product category (e.g., Electronics, Furniture).

- **Customers**:
  - `customer_id`: Unique identifier for each customer.
  - `customer_name`: Name of the customer.
  - `segment`: Segment (e.g., Retail, Corporate).

- **Orders**:
  - `order_id`: Unique identifier for each order.
  - `customer_id`: Reference to the customer who placed the order.
  - `product_id`: Reference to the product being ordered.
  - `order_date`: The date the order was placed.

- **Sales**:
  - `sale_id`: Unique identifier for each sale.
  - `order_id`: Reference to the associated order.
  - `sale_amount`: Total sale amount.
  - `sale_date`: The date the sale was made.

# Sample Prompts

Here are some example queries you can try in the app:

- "List all the products."
- "How many orders were placed in February 2024?"
- "What are the total sales for Electronics?"
- "Show me all orders placed by Alice."
- "What are the top 3 best-selling products?"

For more examples, see the [Sample Prompts](#sample-prompts) section.

# Acknowledgments

- This project uses **Streamlit** for the user interface.
- The natural language to SQL conversion is powered by **Google Gemini**.
- **SQLite** is used for database management.

