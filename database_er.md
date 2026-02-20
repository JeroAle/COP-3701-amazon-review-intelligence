# Database ER Diagram – E-Commerce System

## Entities

### Strong Entities
- Customer
- Product
- Category
- Order
- Payment
- Review

### Weak Entity
- OrderItem  
  (Depends on Order and cannot exist without it)

### Associative (Bridge) Entities
- ProductCategory (for Product–Category many-to-many)
- OrderItem (also acts as a bridge between Order and Product)

---

## Relationship Types

### One-to-Many (1:N)
- One Customer can place many Orders.
- One Customer can write many Reviews.
- One Product can have many Reviews.
- One Order can contain many OrderItems.

### One-to-One (1:1)
- One Order has one Payment.
- One Payment belongs to one Order.

### Many-to-Many (M:N)
- Products and Categories (resolved using ProductCategory).
- Orders and Products (resolved using OrderItem).

---

## ER Diagram
    CUSTOMER {
        int customer_id PK
        string full_name
        string email NOT_NULL
        string phone OPTIONAL
        date created_at
    }

    PRODUCT {
        int product_id PK
        string product_name NOT_NULL
        decimal price NOT_NULL
        int stock_quantity
    }

    CATEGORY {
        int category_id PK
        string category_name NOT_NULL
    }

    ORDER {
        int order_id PK
        int customer_id FK
        date order_date NOT_NULL
        string status
        decimal total_amount
    }

    PAYMENT {
        int payment_id PK
        int order_id FK UNIQUE
        string payment_method NOT_NULL
        decimal amount NOT_NULL
        datetime payment_date
    }

    REVIEW {
        int review_id PK
        int customer_id FK
        int product_id FK
        int rating NOT_NULL
        string review_text OPTIONAL
        date review_date
    }

    ORDER_ITEM {
        int order_id PK FK
        int product_id PK FK
        int quantity NOT_NULL
        decimal unit_price NOT_NULL
    }

    PRODUCT_CATEGORY {
        int product_id PK FK
        int category_id PK FK
    }
