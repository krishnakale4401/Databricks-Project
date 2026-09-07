# Databricks notebook source
# MAGIC %sql
# MAGIC DESCRIBE HISTORY main.ecommerce.fact_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM main.ecommerce.fact_sales VERSION AS OF 0;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM main.ecommerce.fact_sales TIMESTAMP AS OF '2026-01-04T10:15:00';

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE main.ecommerce.fact_sales SET price = 0;

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM main.ecommerce.fact_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM main.ecommerce.fact_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC RESTORE TABLE main.ecommerce.fact_sales TO VERSION AS OF 1;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC RESTORE TABLE main.ecommerce.fact_sales
# MAGIC TO TIMESTAMP AS OF '2026-01-04T10:15:00';
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM main.ecommerce.fact_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY main.ecommerce.fact_sales;

# COMMAND ----------

