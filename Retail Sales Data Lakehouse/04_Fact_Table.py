# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE main.ecommerce.fact_sales AS
# MAGIC SELECT
# MAGIC     o.order_id,
# MAGIC     oi.order_item_id,
# MAGIC     o.customer_id,
# MAGIC     oi.product_id,
# MAGIC
# MAGIC     o.order_purchase_timestamp,
# MAGIC     DATE(o.order_purchase_timestamp) AS order_date,
# MAGIC
# MAGIC     oi.price,
# MAGIC     oi.freight_value,
# MAGIC     (oi.price + oi.freight_value) AS revenue,
# MAGIC
# MAGIC     c.customer_state,
# MAGIC     p.product_category_name
# MAGIC
# MAGIC FROM main.ecommerce.src_olist_orders_dataset o
# MAGIC INNER JOIN main.ecommerce.src_olist_order_items_dataset oi
# MAGIC     ON o.order_id = oi.order_id
# MAGIC LEFT JOIN main.ecommerce.src_olist_customers_dataset c
# MAGIC     ON o.customer_id = c.customer_id
# MAGIC LEFT JOIN main.ecommerce.src_olist_products_dataset p
# MAGIC     ON oi.product_id = p.product_id;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE main.ecommerce.fact_sales

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM main.ecommerce.src_olist_orders_dataset;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM main.ecommerce.fact_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from main.ecommerce.fact_sales;

# COMMAND ----------

