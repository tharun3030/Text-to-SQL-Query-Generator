import os
import sqlite3
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Step 1: Configure Google Gemini API Key
genai.configure(api_key="AIzaSyCkPT1dszp6QjiCJ72_wchI12jBPhJYrrY")


# Step 2: Define the database schema and sample data creation function
def create_schema():
    connection = sqlite3.connect("sales_management.db")
    cursor = connection.cursor()

    # Clear existing data
    cursor.execute("DROP TABLE IF EXISTS Sales")
    cursor.execute("DROP TABLE IF EXISTS Orders")
    cursor.execute("DROP TABLE IF EXISTS Customers")
    cursor.execute("DROP TABLE IF EXISTS Products")

    # Create Products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        category TEXT
    )
    ''')

    # Create Customers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        customer_id INTEGER PRIMARY KEY,
        customer_name TEXT NOT NULL,
        segment TEXT
    )
    ''')

    # Create Orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id INTEGER,
        order_date DATE,
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    )
    ''')

    # Create Sales table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sales (
        sale_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        sale_amount DECIMAL(10, 2),
        sale_date DATE,
        FOREIGN KEY (order_id) REFERENCES Orders(order_id)
    )
    ''')

    # Insert sample data into Products table
    cursor.execute("INSERT INTO Products (product_name, category) VALUES ('Laptop', 'Electronics')")
    cursor.execute("INSERT INTO Products (product_name, category) VALUES ('Desk', 'Furniture')")
    cursor.execute("INSERT INTO Products (product_name, category) VALUES ('Chair', 'Furniture')")

    # Insert sample data into Customers table
    cursor.execute("INSERT INTO Customers (customer_name, segment) VALUES ('Alice', 'Retail')")
    cursor.execute("INSERT INTO Customers (customer_name, segment) VALUES ('Bob', 'Corporate')")
    cursor.execute("INSERT INTO Customers (customer_name, segment) VALUES ('Charlie', 'Retail')")

    # Insert sample data into Orders table
    cursor.execute("INSERT INTO Orders (customer_id, product_id, order_date) VALUES (1, 1, '2024-01-10')")
    cursor.execute("INSERT INTO Orders (customer_id, product_id, order_date) VALUES (2, 2, '2024-02-15')")
    cursor.execute("INSERT INTO Orders (customer_id, product_id, order_date) VALUES (1, 3, '2024-03-20')")

    # Insert sample data into Sales table
    cursor.execute("INSERT INTO Sales (order_id, sale_amount, sale_date) VALUES (1, 1000.00, '2024-01-11')")
    cursor.execute("INSERT INTO Sales (order_id, sale_amount, sale_date) VALUES (2, 300.00, '2024-02-16')")
    cursor.execute("INSERT INTO Sales (order_id, sale_amount, sale_date) VALUES (3, 150.00, '2024-03-21')")

    # Commit changes and close connection
    connection.commit()
    connection.close()


# Step 3: Define the function to get SQL query from natural language
def get_sql_query(question, prompt):
    model = genai.GenerativeModel('gemini-pro')  # Use Gemini model for conversion
    full_prompt = prompt + "\nQuestion: " + question
    response = model.generate_content([full_prompt])
    sql_query = response.text.strip()  # Strip whitespace to clean the response
    # Remove any markdown formatting or SQL prefixes if present
    sql_query = sql_query.replace("```sql", "").replace("```", "").replace("SQL:", "").strip()
    return sql_query


# Step 4: Function to execute the SQL query and fetch results
def execute_sql_query(sql_query, db_name="sales_management.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        conn.commit()
    except Exception as e:
        results = f"Error executing query: {e}"
    finally:
        conn.close()

    return results


# Step 5: Streamlit App Setup
create_schema()  # Create schema and insert sample data

st.set_page_config(page_title="Sales Data Query App")
st.header("Query Sales Data in Natural Language")

# User input
user_question = st.text_input("Ask a question about sales:", key="input")
submit = st.button("Get SQL Query and Results")

# Define the LLM prompt
prompt = """
You are an expert in converting English questions to SQL queries.
We have a database schema with the following tables:
- Products (product_id, product_name, category)
- Customers (customer_id, customer_name, segment)
- Orders (order_id, customer_id, product_id, order_date)
- Sales (sale_id, order_id, sale_amount, sale_date)

Here are some examples of English questions and their corresponding SQL queries:
1. Question: "Show me all the products in the Electronics category."
   SQL: SELECT * FROM Products WHERE category = 'Electronics';

2. Question: "What are the total sales amounts by customer segment?"
   SQL: SELECT Customers.segment, SUM(Sales.sale_amount) 
        FROM Sales 
        JOIN Orders ON Sales.order_id = Orders.order_id 
        JOIN Customers ON Orders.customer_id = Customers.customer_id 
        GROUP BY Customers.segment;

3. Question: "How many orders were placed in January 2024?"
   SQL: SELECT COUNT(*) FROM Orders WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31';

Translate the following question to SQL based on the above schema:
"""

# If the user clicks submit
if submit:
    if user_question:
        # Get the SQL query from the LLM
        sql_query = get_sql_query(user_question, prompt)
        st.subheader("Generated SQL Query:")
        st.code(sql_query)

        # Execute the SQL query
        results = execute_sql_query(sql_query)
        st.subheader("Query Results:")
        if isinstance(results, str):  # Check if results is an error message
            st.error(results)
        else:
            # Format and display results
            st.write("Results:")
            for row in results:
                st.write(row)
    else:
        st.warning("Please ask a question.")
