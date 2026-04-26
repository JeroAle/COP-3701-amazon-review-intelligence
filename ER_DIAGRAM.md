# Database ER Diagram (Final Normalized Relational Schema / BCNF)

## Entities / Relations

### Strong Entities
- Customer
- Product
- Category
- Order
- Payment
- Review

### Bridge / Associative Entities
- OrderItem (resolves Order–Product M:N and represents line items)
- ProductCategory (resolves Product–Category M:N)

> Note: OrderItem is existence-dependent on Order (line items cannot exist without an Order).

---

## Relationship Types (Revised ER Summary)

### One-to-Many (1:N)
- One Customer can place many Orders.
- One Customer can write many Reviews.
- One Product can have many Reviews.
- One Order can contain many OrderItems.

### One-to-One (1:1)
- One Order has one Payment.
- One Payment belongs to one Order.
  - Implemented by `PAYMENT.order_id` as a UNIQUE foreign key.

### Many-to-Many (M:N)
- Products and Categories (resolved using ProductCategory).
- Orders and Products (resolved using OrderItem).

---

## Final Normalized Relational Schema (BCNF)

### CUSTOMER
- PK: `customer_id`
- Attributes: `full_name`, `email` (NOT NULL), `phone` (optional), `created_at`

### PRODUCT
- PK: `product_id`
- Attributes: `product_name` (NOT NULL), `price` (NOT NULL), `stock_quantity`

### CATEGORY
- PK: `category_id`
- Attributes: `category_name` (NOT NULL)

### ORDER
- PK: `order_id`
- FK: `customer_id` → CUSTOMER(`customer_id`)
- Attributes: `order_date` (NOT NULL), `status`, `total_amount`

### PAYMENT
- PK: `payment_id`
- FK (UNIQUE): `order_id` → ORDER(`order_id`)
- Attributes: `payment_method` (NOT NULL), `amount` (NOT NULL), `payment_date`

### REVIEW
- PK: `review_id`
- FK: `customer_id` → CUSTOMER(`customer_id`)
- FK: `product_id` → PRODUCT(`product_id`)
- Attributes: `rating` (NOT NULL), `review_text` (optional), `review_date`

### ORDER_ITEM
- PK: (`order_id`, `product_id`)
- FK: `order_id` → ORDER(`order_id`)
- FK: `product_id` → PRODUCT(`product_id`)
- Attributes: `quantity` (NOT NULL), `unit_price` (NOT NULL)

### PRODUCT_CATEGORY
- PK: (`product_id`, `category_id`)
- FK: `product_id` → PRODUCT(`product_id`)
- FK: `category_id` → CATEGORY(`category_id`)

---

## ER Diagram (Text Form)

    CUSTOMER {
        int customer_id PK
        string full_name NOT_NULL
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
        int customer_id FK  // → CUSTOMER.customer_id
        date order_date NOT_NULL
        string status
        decimal total_amount
    }

    PAYMENT {
        int payment_id PK
        int order_id FK UNIQUE  // → ORDER.order_id (enforces 1:1)
        string payment_method NOT_NULL
        decimal amount NOT_NULL
        datetime payment_date
    }

    REVIEW {
        int review_id PK
        int customer_id FK  // → CUSTOMER.customer_id
        int product_id FK   // → PRODUCT.product_id
        int rating NOT_NULL
        string review_text OPTIONAL
        date review_date
    }

    ORDER_ITEM {
        int order_id PK FK   // → ORDER.order_id
        int product_id PK FK // → PRODUCT.product_id
        int quantity NOT_NULL
        decimal unit_price NOT_NULL
    }

    PRODUCT_CATEGORY {
        int product_id PK FK   // → PRODUCT.product_id
        int category_id PK FK  // → CATEGORY.category_id
    }

---

## Normalization Note (BCNF)

All relations satisfy BCNF because every non-trivial functional dependency has a determinant that is a superkey (e.g., entity IDs or full composite keys in bridge tables).
