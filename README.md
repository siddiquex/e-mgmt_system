# E-commerce Management service - FastAPI

## Description

This service provides a RESTful API for managing an e-commerce management system. It includes endpoints for products, inventory, and sales.

## Setup Instructions

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/siddiquex/e-mgmt_system
    cd e-mgmt_system
    ```

2.  **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the app using Docker Compose (Recommended):**

    - Ensure you have Docker and Docker Compose installed.
    - Run the following command in the project root:

      ```bash
      docker-compose up -d
      ```

    - This will start a MySQL database in a Docker container and run your FastAPI application(on http://localhost:8000), connected to the database.

5.  **Access the API:**

    - The API will be available at `http://localhost:8000`.
    - You can also view the API documentation at `http://localhost:8000/docs`.

## Endpoints

### Products

- `POST /products/`: Create a new product.
- `GET /products/`: Retrieve all products.
- `GET /products/{product_id}`: Retrieve a specific product by ID.
- `PATCH /products/{product_id}`: Update a product.
- `DELETE /products/{product_id}`: Delete a product.

### Inventory

- `GET /inventory/low_stock/`: Retrieve products with low stock.
- `GET /inventory/`: Retrieve current inventory status for all products.
- `GET /inventory/{product_id}`: Retrieves the inventory status for a specific product ID
- `PATCH /inventory/{product_id}`: Update inventory levels for a specific product.

### Sales

- `POST /sales/`: Create a new sale.
- `GET /sales/`: Retrieve all sales.
- `GET /sales/{sale_id}`: Retrieve a specific sale by ID.
- `PATCH /sales/{sale_id}`: Update a sale.
- `DELETE /sales/{sale_id}`: Delete a sale.
- `GET /sales/daily_revenue/`: Calculate daily revenue.
- `GET /sales/weekly_revenue/`: Calculate weekly revenue.
- `GET /sales/monthly_revenue/`: Calculate monthly revenue.
- `GET /sales/annual_revenue/`: Calculate annual revenue.

## Notes regarding Database Setup

- The application, by default, connects to the database specified in the docker-compose.yml
- If you are running the database outside docker, remember to change the database connection string in `docker-compose.yml`

## Database Doc

**Database Schema**
The database schemas consists of three tables:

- **products**
- **inventory**
- **sales**

## Table: products

Stores information about individual products.

### Columns

| Column      | Data Type    | Description                                     |
| :---------- | :----------- | :---------------------------------------------- |
| product_id  | INT          | Primary key, unique identifier for the product. |
| name        | VARCHAR(255) | Name of the product.                            |
| description | VARCHAR(500) | Description of the product.                     |
| price       | FLOAT        | Price of the product.                           |
| created_at  | DATETIME     | Timestamp when the product was created.         |
| updated_at  | DATETIME     | Timestamp when the product was last updated.    |

## Table: inventory

Stores information about the current stock level for each product.

### Columns

| Column       | Data Type | Description                                                             |
| :----------- | :-------- | :---------------------------------------------------------------------- |
| inventory_id | INT       | Primary key, unique identifier for the inventory record.                |
| product_id   | INT       | Foreign key referencing `products.product_id`, unique for each product. |
| in_stock     | INT       | Number of units of the product currently in stock.                      |
| last_updated | DATETIME  | Timestamp when the inventory was last updated.                          |

### Relationships

- One-to-one relationship with the `products` table via the `product_id` column.

## Table: sales

Stores information about sales transactions.

### Columns

| Column     | Data Type | Description                                              |
| :--------- | :-------- | :------------------------------------------------------- |
| sale_id    | INT       | Primary key, unique identifier for the sale transaction. |
| product_id | INT       | Foreign key referencing `products.product_id`.           |
| quantity   | INT       | Quantity of the product sold in this transaction.        |
| sale_price | FLOAT     | The price at which the product was sold.                 |
| sale_date  | DATETIME  | Timestamp when the sale occurred.                        |

### Relationships

- One-to-many relationship with the `products` table via the `product_id` column.
