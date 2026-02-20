# COP 3710 - Database Project  
## Amazon Product Review & Sales Intelligence Database

## Application Domain

This project designs a relational database for an e-commerce system using Amazon-style product, sales, and review data. The database will be implemented in **MariaDB**.

The system stores and organizes information about products, categories, customers, orders (sales history), and customer reviews/ratings in a normalized structure.

## Goals
- Design and implement a normalized schema in MariaDB.
- Store product details, customer accounts, order records, and review data.
- Support SQL queries for analyzing sales trends, product performance, and customer feedback.

### Project Goals
- Design and implement a normalized database for e-commerce data.
- Store product details and customer review information.
- Analyze ratings and review activity.
- Support queries for sales trends and product performance.

### Intended Users
- Business analysts  
- Store managers  
- Database administrators  

### Data Sources
- Amazon Sales Dataset (Kaggle):  
  https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset  
- Additional sample data created for testing.

### Scope
The database will include information about:
- Products and categories  
- Customers  
- Reviews and ratings  
- Orders and sales history

## Notes / Challenging Aspects
- The model includes multiple relationship types (1:1, 1:N, M:N).
- Many-to-many relationships are implemented using bridge entities.
