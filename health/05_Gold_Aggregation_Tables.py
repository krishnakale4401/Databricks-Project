# Databricks notebook source
# MAGIC %sql
# MAGIC SELECT
# MAGIC     customer_state,   
# MAGIC     SUM(revenue) AS total_sales
# MAGIC FROM main.ecommerce.fact_sales
# MAGIC GROUP BY customer_state
# MAGIC ORDER BY total_sales DESC;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     CASE
# MAGIC         WHEN customer_state IN ('SP','RR','AP','TO','MG','ES') THEN 'West'
# MAGIC         WHEN customer_state IN ('PR','SC','RS', 'MT','MS') THEN 'South'
# MAGIC         WHEN customer_state IN ('BA','PE','CE','RN','PB','AL','SE','PI','MA','RJ') THEN 'East'
# MAGIC         WHEN customer_state IN ('AM','PA','AC','RO','RR','AP','TO','MG','DF','GO') THEN 'North'
# MAGIC         ELSE 'Other'
# MAGIC     END AS region,
# MAGIC     SUM(revenue) AS total_sales
# MAGIC FROM main.ecommerce.fact_sales
# MAGIC GROUP BY region
# MAGIC ORDER BY total_sales DESC;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC select product_category_name,
# MAGIC sum(revenue) as Revenue
# MAGIC from main.ecommerce.fact_sales
# MAGIC group by product_category_name
# MAGIC order by Revenue desc
# MAGIC limit 20;

# COMMAND ----------

# MAGIC %sql
# MAGIC select order_date, 
# MAGIC sum(revenue) as Deily_Revenue
# MAGIC from main.ecommerce.fact_sales
# MAGIC group by order_date
# MAGIC order by order_date;

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC month(order_date) as month,
# MAGIC sum(revenue) as monthly_sales_trands
# MAGIC from main.ecommerce.fact_sales
# MAGIC group by  month
# MAGIC order by month;

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) as Row_Count from main.ecommerce.fact_sales;
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from main.ecommerce.fact_sales
# MAGIC where customer_id is null;

# COMMAND ----------

