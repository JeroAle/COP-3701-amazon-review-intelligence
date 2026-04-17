import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# automatically set the session state to "home"
if "page" not in st.session_state:
    st.session_state.page = "home"
    
### --- HELPER FUNCTIONS --- ###
# login info for MariaDB
def connect_db():
    return mysql.connector.connect (
        host="localhost",
        user="root",
        password="rinter44",
        database="amazon_review_intelligence"
    )

# to run a SELECT query
def run_select_query(query, params=None):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return pd.DataFrame(rows, columns=columns)

# add a back button on the bottom right of the page
def add_back_button():
    with st._bottom:
        col1, col2 = st.columns([8, 1])
        with col2:
            if st.button("Back"):
                st.session_state.page = "home"
                st.rerun()

# get all the customer info (including total # of orders and money spent)
def get_all_customers():
    query = """
        SELECT
            c.customer_id,
            c.full_name,
            c.email,
            c.phone,
            c.created_at,
            COUNT(o.order_id) AS number_of_orders,
            COALESCE(SUM(o.total_amount), 0) AS total_spent
        FROM Customer c
        LEFT JOIN Orders o
            ON c.customer_id = o.customer_id
        GROUP BY
            c.customer_id,
            c.full_name,
            c.email,
            c.phone,
            c.created_at
        ORDER BY c.customer_id
    """
    df = run_select_query(query)
    df.columns = [
        "Customer ID",
        "Full Name",
        "Email",
        "Phone",
        "Date Created",
        "Number of Orders",
        "Total Spent"
    ]
    return df

# get all the products and their info (include total sold and category)
def get_all_products():
    query = """
        SELECT 
            p.product_id,
            p.product_name,
            p.price,
            p.stock_quantity,
            c.category_name,
            COALESCE(s.total_sold, 0) AS total_sold
        FROM Product p
        LEFT JOIN Product_Category pc
            ON p.product_id = pc.product_id
        LEFT JOIN Category c
            ON pc.category_id = c.category_id
        LEFT JOIN (
            SELECT product_id, SUM(quantity) AS total_sold
            FROM Order_Item
            GROUP BY product_id
        ) s
            ON p.product_id = s.product_id
        ORDER BY p.product_id
    """
    df = run_select_query(query)
    df.columns = [
        "Product ID",
        "Product Name",
        "Price",
        "Stock Quantity",
        "Category",
        "Total Sold"
    ]
    return df
    
# get all orders
def get_all_orders():
    query = """
        SELECT
            order_id,
            customer_id,
            order_date,
            status,
            total_amount
        FROM Orders
        ORDER BY order_date DESC
    """
    df = run_select_query(query)
    df.columns = [
        "Order ID",
        "Customer ID",
        "Order Date",
        "Status",
        "Total Amount"
    ]
    return df

# get all info to compare number of sales to price
def get_product_sales_vs_price():
    query = """
        SELECT
            p.product_name,
            p.price,
            COALESCE(SUM(oi.quantity), 0) AS total_sold
        FROM Product p
        LEFT JOIN Order_Item oi
            ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.product_name, p.price
        ORDER BY p.price
    """
    return run_select_query(query)

# create graph to show number of sales vs. price
def show_price_vs_sales_chart():
    df = get_product_sales_vs_price()

    if df.empty:
        st.write("No product sales data available.")
        return

    x = df["total_sold"].astype(float)
    y = df["price"].astype(float)

    fig, ax = plt.subplots()
    ax.scatter(x, y)


    ax.set_xlabel("Total Sold", fontweight="bold")
    ax.set_ylabel("Price", fontweight="bold")
    ax.set_title("Price vs Total Items Sold", fontweight="bold")

    st.pyplot(fig)

# get all info to show the top 10 categories in terms of number of sales
def get_top_10_categories_by_sales():
    query = """
        SELECT
            c.category_name,
            COALESCE(SUM(oi.quantity), 0) AS total_bought
        FROM Category c
        LEFT JOIN Product_Category pc
            ON c.category_id = pc.category_id
        LEFT JOIN Order_Item oi
            ON pc.product_id = oi.product_id
        GROUP BY c.category_id, c.category_name
        ORDER BY total_bought DESC
        LIMIT 10
    """
    return run_select_query(query)
    
# make graph to show top ten categories vs. amount sold
def show_top_10_categories_chart():
    df = get_top_10_categories_by_sales()

    if df.empty:
        st.write("No category sales data available.")
        return

    fig, ax = plt.subplots()
    ax.bar(df["category_name"], df["total_bought"])

    ax.set_xlabel("Category", fontweight="bold", fontsize=12)
    ax.set_ylabel("Total Amount Sold", fontweight="bold", fontsize=12)
    ax.set_title("Top 10 Categories by Amount Sold", fontweight="bold", fontsize=14)

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    st.pyplot(fig)

def get_order_status_counts():
    query = """
        SELECT
            status,
            COUNT(order_id) AS total_orders
        FROM Orders
        GROUP BY status
        ORDER BY total_orders DESC
    """
    df = run_select_query(query)
    df.columns = ["Status", "Total Orders"]
    df["Status"] = df["Status"].str.title()
    return df

def show_order_status_pie_chart():
    df = get_order_status_counts()

    if df.empty:
        st.write("No order status data available.")
        return

    fig, ax = plt.subplots()

    ax.pie(
        df["Total Orders"],
        labels=df["Status"],
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Order Status Distribution", fontweight="bold", fontsize=14)
    ax.axis("equal")

    st.pyplot(fig)





### --- HOME PAGE --- ###
if st.session_state.page == "home":
    # title and subtitle
    st.title("Amazon Review Intelligence")
    st.write("Choose a path:")

    # customers and products buttons to view that info
    
    if st.button("Customers", use_container_width=True):
        st.session_state.page = "customers"
        st.rerun()
    if st.button("Products", use_container_width=True):
        st.session_state.page = "products"
        st.rerun()
    if st.button("Orders", use_container_width=True):
        st.session_state.page = "orders"
        st.rerun()




### --- CUSTOMERS PAGE --- ###
elif st.session_state.page == "customers":
    # title of page
    st.title("Customers")
    
    # back button on the bottom right
    add_back_button()
    
    # print all the customers to the page
    customers_df = get_all_customers()
    st.dataframe(customers_df, use_container_width=True, hide_index=True)





### --- PRODUCTS PAGE --- ###
elif st.session_state.page == "products":
    # title of page
    st.title("Products")
    
    # back button on the bottom right
    add_back_button()
    
    # drop down for chart choice
    st.subheader("Product Sales Analysis")
    chart_choice = st.selectbox(
        "Choose a chart:",
        [
            "Price vs Total Sold",
            "Top 10 Categories by Amount Bought"
        ]
    )
    if chart_choice == "Price vs Total Sold":
        show_price_vs_sales_chart()

    elif chart_choice == "Top 10 Categories by Amount Bought":
        show_top_10_categories_chart()
    
    # print all products to the page
    st.subheader("Product List")
    products_df = get_all_products()
    st.dataframe(products_df, use_container_width=True, hide_index=True)
    
    
    
    
    
### --- ORDERS PAGE --- ###
elif st.session_state.page == "orders":
    # title of page
    st.title("Orders")
    
    # back button on the bottom right
    add_back_button()
    
    # add a summary of number of orders in each status with pie chart
    show_order_status_pie_chart()
    
    # print all orders to the page
    st.subheader("Order List")
    orders_df = get_all_orders()
    st.dataframe(orders_df, use_container_width=True, hide_index=True)
