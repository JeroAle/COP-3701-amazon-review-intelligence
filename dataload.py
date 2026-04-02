import pandas as pd
import mariadb

conn = mariadb.connect(
    host="localhost",
    user="root",
    password="rinter44",
    database="amazon_review_intelligence"
)
cur = conn.cursor()

load_order = [
    ("Category", "data/categories.csv"),
    ("Product", "data/products.csv"),
    ("Customer", "data/customers.csv"),
    ("Orders", "data/orders.csv"),
    ("Payment", "data/payments.csv"),
    ("Review", "data/reviews.csv"),
    ("Order_Item", "data/order_items.csv"),
    ("Product_Category", "data/product_category.csv"),
]

for table_name, file_name in load_order:
    df = pd.read_csv(file_name)
    cols = list(df.columns)
    placeholders = ", ".join(["?"] * len(cols))
    sql = f"INSERT IGNORE INTO {table_name} ({', '.join(cols)}) VALUES ({placeholders})"

    for row in df.itertuples(index=False, name=None):
        cur.execute(sql, row)

    conn.commit()
    print(f"Loaded {len(df)} rows into {table_name}")

cur.close()
conn.close()
print("All data loaded.")
