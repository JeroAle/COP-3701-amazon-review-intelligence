import pandas as pd
import mariadb

conn = mariadb.connect(
    host="localhost",
    user="root",
    password="Rinter44",
    database="amazon_review_intelligence"
)
cur = conn.cursor()

load_order = [
    ("category", "data/categories.csv"),
    ("product", "data/products.csv"),
    ("customer", "data/customers.csv"),
    ("orders", "data/orders.csv"),
    ("payment", "data/payments.csv"),
    ("review", "data/reviews.csv"),
    ("order_item", "data/order_items.csv"),
    ("product_category", "data/product_category.csv"),
]

for table_name, file_name in load_order:
    df = pd.read_csv(file_name)
    cols = list(df.columns)
    placeholders = ", ".join(["%s"] * len(cols))
    sql = f"INSERT IGNORE INTO {table_name} ({', '.join(cols)}) VALUES ({placeholders})"

    for row in df.itertuples(index=False, name=None):
        cur.execute(sql, row)

    conn.commit()
    print(f"Loaded {len(df)} rows into {table_name}")

cur.close()
conn.close()
print("All data loaded.")
