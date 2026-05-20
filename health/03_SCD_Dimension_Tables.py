# Databricks notebook source
# MAGIC %sql
# MAGIC select count(*) from main.ecommerce.src_olist_customers_dataset;

# COMMAND ----------

# MAGIC %sql
# MAGIC create  table if not exists main.ecommerce.dim_customer
# MAGIC (
# MAGIC customer_sk   BIGINT GENERATED ALWAYS AS IDENTITY,
# MAGIC customer_id STRING,
# MAGIC customer_unique_id STRING,
# MAGIC customer_zip_code_prefix integer,
# MAGIC customer_city STRING,
# MAGIC customer_state STRING,
# MAGIC effective_start_date DATE,
# MAGIC effective_end_date DATE,
# MAGIC is_Active boolean
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW scd2_source AS
# MAGIC SELECT
# MAGIC     tgt.customer_id AS merge_customer_id,
# MAGIC     src.customer_id,
# MAGIC     src.customer_unique_id,
# MAGIC     src.customer_zip_code_prefix,
# MAGIC     src.customer_city,
# MAGIC     src.customer_state,
# MAGIC     false AS is_new
# MAGIC FROM main.ecommerce.dim_customer tgt
# MAGIC JOIN main.ecommerce.src_olist_customers_dataset src
# MAGIC     ON tgt.customer_id = src.customer_id
# MAGIC     AND tgt.is_Active = true
# MAGIC WHERE tgt.customer_unique_id <> src.customer_unique_id
# MAGIC     OR tgt.customer_city <> src.customer_city
# MAGIC     OR tgt.customer_state <> src.customer_state
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     src.customer_id AS merge_customer_id,
# MAGIC     src.customer_id,
# MAGIC     src.customer_unique_id,
# MAGIC     src.customer_zip_code_prefix,
# MAGIC     src.customer_city,
# MAGIC     src.customer_state,
# MAGIC     true AS is_new
# MAGIC FROM main.ecommerce.src_olist_customers_dataset src
# MAGIC LEFT JOIN main.ecommerce.dim_customer tgt
# MAGIC     ON src.customer_id = tgt.customer_id
# MAGIC     AND tgt.is_Active = true
# MAGIC WHERE tgt.customer_id IS NULL
# MAGIC     OR tgt.customer_unique_id <> src.customer_unique_id
# MAGIC     OR tgt.customer_zip_code_prefix <> src.customer_zip_code_prefix
# MAGIC     OR tgt.customer_city <> src.customer_city
# MAGIC     OR tgt.customer_state <> src.customer_state
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO main.ecommerce.dim_customer tgt
# MAGIC USING scd2_source src
# MAGIC ON tgt.customer_id = src.customer_id
# MAGIC AND tgt.is_Active = true
# MAGIC
# MAGIC
# MAGIC WHEN MATCHED AND src.is_new = false THEN
# MAGIC UPDATE SET
# MAGIC   tgt.effective_end_date = current_date(),
# MAGIC   tgt.is_Active = false
# MAGIC
# MAGIC
# MAGIC WHEN NOT MATCHED AND src.is_new = true
# MAGIC THEN INSERT (
# MAGIC   customer_id,
# MAGIC   customer_unique_id,
# MAGIC   customer_zip_code_prefix,
# MAGIC   customer_city,
# MAGIC   customer_state,
# MAGIC   effective_start_date,
# MAGIC   effective_end_date,
# MAGIC   is_Active
# MAGIC )
# MAGIC VALUES (
# MAGIC   src.customer_id,
# MAGIC   src.customer_unique_id,
# MAGIC   src.customer_zip_code_prefix,
# MAGIC   src.customer_city,
# MAGIC   src.customer_state,
# MAGIC   current_date(),
# MAGIC   DATE '9999-12-31',
# MAGIC   true
# MAGIC );
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from main.ecommerce.dim_customer where customer_id = '17ddf5dd5d51696bb3d7c6291687be6f';

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from main.ecommerce.dim_customer;

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from main.ecommerce.src_olist_products_dataset;

# COMMAND ----------

# MAGIC %sql
# MAGIC create  table if not exists main.ecommerce.dim_products
# MAGIC (
# MAGIC customer_sk   BIGINT GENERATED ALWAYS AS IDENTITY,
# MAGIC product_id STRING,
# MAGIC product_category_name STRING,
# MAGIC product_name_lenght integer,
# MAGIC product_description_lenght integer,
# MAGIC product_photos_qty integer,
# MAGIC product_weight_g integer,
# MAGIC product_length_cm integer,
# MAGIC product_height_cm integer,
# MAGIC product_width_cm integer,
# MAGIC effective_start_date DATE,
# MAGIC effective_end_date DATE,
# MAGIC is_Active boolean
# MAGIC )
# MAGIC USING DELTA;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW scd2_products_source AS
# MAGIC
# MAGIC -- Existing product but attributes changed (old record is expire)
# MAGIC SELECT
# MAGIC     tgt.product_id AS merge_product_id,
# MAGIC     src.product_id,
# MAGIC     src.product_category_name,
# MAGIC     src.product_name_lenght,
# MAGIC     src.product_description_lenght,
# MAGIC     src.product_photos_qty,
# MAGIC     src.product_weight_g,
# MAGIC     src.product_length_cm,
# MAGIC     src.product_height_cm,
# MAGIC     src.product_width_cm,
# MAGIC     false AS is_new
# MAGIC FROM main.ecommerce.dim_products tgt
# MAGIC JOIN main.ecommerce.src_olist_products_dataset src
# MAGIC     ON tgt.product_id = src.product_id
# MAGIC     AND tgt.is_Active = true
# MAGIC WHERE
# MAGIC     tgt.product_category_name <> src.product_category_name
# MAGIC  OR tgt.product_name_lenght <> src.product_name_lenght
# MAGIC  OR tgt.product_description_lenght <> src.product_description_lenght
# MAGIC  OR tgt.product_photos_qty <> src.product_photos_qty
# MAGIC  OR tgt.product_weight_g <> src.product_weight_g
# MAGIC  OR tgt.product_length_cm <> src.product_length_cm
# MAGIC  OR tgt.product_height_cm <> src.product_height_cm
# MAGIC  OR tgt.product_width_cm <> src.product_width_cm
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC -- New product OR changed product isnew active record then insert
# MAGIC SELECT
# MAGIC     src.product_id AS merge_product_id,
# MAGIC     src.product_id,
# MAGIC     src.product_category_name,
# MAGIC     src.product_name_lenght,
# MAGIC     src.product_description_lenght,
# MAGIC     src.product_photos_qty,
# MAGIC     src.product_weight_g,
# MAGIC     src.product_length_cm,
# MAGIC     src.product_height_cm,
# MAGIC     src.product_width_cm,
# MAGIC     true AS is_new
# MAGIC FROM main.ecommerce.src_olist_products_dataset src
# MAGIC LEFT JOIN main.ecommerce.dim_products tgt
# MAGIC     ON src.product_id = tgt.product_id
# MAGIC     AND tgt.is_Active = true
# MAGIC WHERE tgt.product_id IS NULL
# MAGIC    OR tgt.product_category_name <> src.product_category_name
# MAGIC    OR tgt.product_name_lenght <> src.product_name_lenght
# MAGIC    OR tgt.product_description_lenght <> src.product_description_lenght
# MAGIC    OR tgt.product_photos_qty <> src.product_photos_qty
# MAGIC    OR tgt.product_weight_g <> src.product_weight_g
# MAGIC    OR tgt.product_length_cm <> src.product_length_cm
# MAGIC    OR tgt.product_height_cm <> src.product_height_cm
# MAGIC    OR tgt.product_width_cm <> src.product_width_cm;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO main.ecommerce.dim_products tgt
# MAGIC USING scd2_products_source src
# MAGIC ON tgt.product_id = src.merge_product_id
# MAGIC AND tgt.is_Active = true
# MAGIC
# MAGIC -- 1️⃣ Expire old active record
# MAGIC WHEN MATCHED AND src.is_new = false THEN
# MAGIC UPDATE SET
# MAGIC   tgt.effective_end_date = current_date(),
# MAGIC   tgt.is_Active = false
# MAGIC
# MAGIC -- 2️⃣ Insert new active record
# MAGIC WHEN NOT MATCHED AND src.is_new = true
# MAGIC THEN INSERT (
# MAGIC   product_id,
# MAGIC   product_category_name,
# MAGIC   product_name_lenght,
# MAGIC   product_description_lenght,
# MAGIC   product_photos_qty,
# MAGIC   product_weight_g,
# MAGIC   product_length_cm,
# MAGIC   product_height_cm,
# MAGIC   product_width_cm,
# MAGIC   effective_start_date,
# MAGIC   effective_end_date,
# MAGIC   is_Active
# MAGIC )
# MAGIC VALUES (
# MAGIC   src.product_id,
# MAGIC   src.product_category_name,
# MAGIC   src.product_name_lenght,
# MAGIC   src.product_description_lenght,
# MAGIC   src.product_photos_qty,
# MAGIC   src.product_weight_g,
# MAGIC   src.product_length_cm,
# MAGIC   src.product_height_cm,
# MAGIC   src.product_width_cm,
# MAGIC   current_date(),
# MAGIC   DATE '9999-12-31',
# MAGIC   true
# MAGIC );
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from main.ecommerce.dim_products;

# COMMAND ----------

