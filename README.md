# Enterprise E-Commerce Data Engineering Platform

An end-to-end data engineering platform designed to ingest, process, transform, orchestrate, store, and visualize e-commerce data using modern data engineering technologies.

## Project Overview

This project simulates a real-world e-commerce data platform.

It will collect data from multiple sources, process both batch and streaming data, transform the data into analytics-ready datasets, store it in a data warehouse, and provide business insights through Power BI.

The project is being built incrementally to demonstrate the complete data engineering lifecycle, from data ingestion to analytics.

## Technology Stack

- Python
- SQL
- PostgreSQL
- Pandas
- Apache Spark
- Apache Kafka
- dbt
- Apache Airflow
- AWS
- Docker
- Power BI

## Project Status

🚧 Currently under development.

This project is being built as a 45-day data engineering learning and portfolio project.

## Data Model

The platform uses five core entities:

### 1. Customers

| Column | Type |
|---|---|
| customer_id | Integer |
| first_name | String |
| last_name | String |
| email | String |
| country | String |
| created_at | Timestamp |

### 2. Products

| Column | Type |
|---|---|
| product_id | Integer |
| product_name | String |
| category | String |
| price | Decimal |
| stock_quantity | Integer |
| created_at | Timestamp |

### 3. Orders

| Column | Type |
|---|---|
| order_id | Integer |
| customer_id | Integer |
| order_date | Timestamp |
| order_status | String |
| total_amount | Decimal |

### 4. Order Items

| Column | Type |
|---|---|
| order_item_id | Integer |
| order_id | Integer |
| product_id | Integer |
| quantity | Integer |
| unit_price | Decimal |

### 5. Payments

| Column | Type |
|---|---|
| payment_id | Integer |
| order_id | Integer |
| payment_method | String |
| payment_status | String |
| payment_date | Timestamp |
| amount | Decimal |

### Relationships

- `orders.customer_id` → `customers.customer_id`
- `order_items.order_id` → `orders.order_id`
- `order_items.product_id` → `products.product_id`
- `payments.order_id` → `orders.order_id`