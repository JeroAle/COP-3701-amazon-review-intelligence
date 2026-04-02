import pandas as pd
import os
import random
import re
from datetime import datetime, timedelta

df = pd.read_csv("amazon.csv")
df.columns = df.columns.str.strip()
os.makedirs("data", exist_ok=True)

def clean_price(v):
    s = str(v).replace("₹", "").replace(",", "").strip()
    try:
        return round(float(s), 2)
    except:
        return 0.0

def clean_rating(v):
    try:
        x = float(v)
        x = max(1, min(5, round(x)))
        return int(x)
    except:
        return 3

def slug_name(name):
    s = str(name).strip().lower()
    s = re.sub(r"[^a-z0-9]+", ".", s).strip(".")
    return s[:40] or "customer"

start = datetime(2023, 1, 1)

categories = df[["category"]].dropna().drop_duplicates().reset_index(drop=True)
categories["category_id"] = range(1, len(categories) + 1)
categories = categories[["category_id", "category"]]
categories.columns = ["category_id", "category_name"]
category_map = dict(zip(categories["category_name"], categories["category_id"]))

products = df[["product_id", "product_name", "discounted_price"]].dropna(subset=["product_id", "product_name"]).drop_duplicates(subset=["product_id"]).copy()
products["price"] = products["discounted_price"].apply(clean_price)
products["stock_quantity"] = [random.randint(20, 250) for _ in range(len(products))]
products = products[["product_id", "product_name", "price", "stock_quantity"]]

customers = df[["user_id", "user_name"]].dropna(subset=["user_id", "user_name"]).drop_duplicates(subset=["user_id"]).copy()
customers["email"] = [f"{slug_name(n)}{i}@example.com" for i, n in enumerate(customers["user_name"], start=1)]
customers["phone"] = [f"555{random.randint(1000000, 9999999)}" for _ in range(len(customers))]
customers["created_at"] = [(start + timedelta(days=random.randint(0, 730))).date().isoformat() for _ in range(len(customers))]
customers = customers[["user_id", "user_name", "email", "phone", "created_at"]]
customers.columns = ["customer_id", "full_name", "email", "phone", "created_at"]

reviews = df[["review_id", "user_id", "product_id", "rating", "review_content"]].dropna(subset=["review_id", "user_id", "product_id"]).drop_duplicates(subset=["review_id"]).copy()
reviews["rating"] = reviews["rating"].apply(clean_rating)
reviews["review_date"] = [(start + timedelta(days=random.randint(0, 730))).date().isoformat() for _ in range(len(reviews))]
reviews = reviews[["review_id", "user_id", "product_id", "rating", "review_content", "review_date"]]
reviews.columns = ["review_id", "customer_id", "product_id", "rating", "review_text", "review_date"]

product_category = df[["product_id", "category"]].dropna(subset=["product_id", "category"]).drop_duplicates().copy()
product_category["category_id"] = product_category["category"].map(category_map)
product_category = product_category[["product_id", "category_id"]].drop_duplicates()

customer_ids = customers["customer_id"].tolist()
product_ids = products["product_id"].tolist()
price_map = dict(zip(products["product_id"], products["price"]))

orders = []
order_items = []
payments = []

for order_id in range(1, 251):
    customer_id = random.choice(customer_ids)
    order_date = (start + timedelta(days=random.randint(0, 730))).date().isoformat()
    status = random.choice(["Pending", "Shipped", "Delivered", "Cancelled"])
    chosen_products = random.sample(product_ids, random.randint(1, 3))
    total = 0

    for product_id in chosen_products:
        quantity = random.randint(1, 3)
        unit_price = float(price_map[product_id])
        total += quantity * unit_price
        order_items.append([order_id, product_id, quantity, round(unit_price, 2)])

    total = round(total, 2)
    orders.append([order_id, customer_id, order_date, status, total])
    payment_date = (start + timedelta(days=random.randint(0, 730), seconds=random.randint(0, 86399))).strftime("%Y-%m-%d %H:%M:%S")
    payments.append([order_id, order_id, random.choice(["Credit Card", "Debit Card", "UPI", "PayPal"]), total, payment_date])

categories.to_csv("data/categories.csv", index=False)
products.to_csv("data/products.csv", index=False)
customers.to_csv("data/customers.csv", index=False)
reviews.to_csv("data/reviews.csv", index=False)
product_category.to_csv("data/product_category.csv", index=False)
pd.DataFrame(orders, columns=["order_id", "customer_id", "order_date", "status", "total_amount"]).to_csv("data/orders.csv", index=False)
pd.DataFrame(order_items, columns=["order_id", "product_id", "quantity", "unit_price"]).to_csv("data/order_items.csv", index=False)
pd.DataFrame(payments, columns=["payment_id", "order_id", "payment_method", "amount", "payment_date"]).to_csv("data/payments.csv", index=False)

print("Done. CSV files are in the data folder.")
