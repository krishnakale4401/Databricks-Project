# Databricks notebook source
source_path = '/Volumes/main/ecommerce/managed_volumes/lakehouse_vol/Raw_DS/'
destination = '/Volumes/main/ecommerce/managed_volumes/lakehouse_vol/bronze/'

dbutils.fs.ls(source_path)
for i in dbutils.fs.ls(source_path):
  #print(i.path)
  df = spark.read.csv(i.path,header=True)
  #display(df)
  df.write.mode("overwrite").parquet(f'{destination}/{i.name[0:len(i.name)-4:1]}.parquet')

# COMMAND ----------

