Easy package for your Amazon Review Intelligence project.

Files included:
- create_db.sql
- preprocess.py
- dataload.py
- data/*.csv already generated from amazon.csv

Row counts:
- Category: 211
- Product: 1351
- Customer: 1194
- Review: 1194
- Product_Category: 1351
- Orders: 250
- Payment: 250
- Order_Item: 494

How to use:
1. Run create_db.sql in MariaDB
2. Install Python packages:
   pip install pandas mariadb
3. Put your MariaDB root password into dataload.py
4. Run:
   python dataload.py
