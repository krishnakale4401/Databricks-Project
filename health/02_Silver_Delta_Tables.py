# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import (StructType, StructField, StringType, IntegerType, TimestampType, FloatType, DateType)

from delta.tables import DeltaTable

import re
source_path = '/Volumes/main/ecommerce/managed_volumes/lakehouse_vol/bronze/'
destination_path = '/Volumes/main/ecommerce/managed_volumes/lakehouse_vol/silver/'

dbutils.fs.ls(source_path)
for i in dbutils.fs.ls(source_path):
    print(i.name)
    nm=i.name
    print(nm)
    dataframe = spark.read.parquet(source_path+i.name)


    first_row_list = list(dataframe.first())
    print(first_row_list)
    d = dataframe.columns
    print(d)
    l = []

    print("================================== SHOW FIRST ROW DATA ==================================")

    for i in first_row_list:
        if i is None:
            continue

        if isinstance(i, int) or isinstance(i, str) and re.fullmatch(r"[+-]?\d+",i):
            l.append('Integer')
            print(i)

        elif isinstance(i, float) or isinstance(i, str) and re.fullmatch(r"[+-]?\d+\.\d+",i):
            l.append('Float')
            print(i)

        elif isinstance(i, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}",i):
            l.append('Date')
            print(i)

        elif isinstance(i, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(\.\d+)?",i):
            l.append('Timestamp')
            print(i)

        else:
            l.append('String')
            print(i)
    print("================================= SHOW DATATYPE COLUMNS =================================")
    print(l)


    for i, t in zip(l, d):
        if i == 'Integer':
            dataframe = dataframe.withColumn(t, dataframe[t].cast(IntegerType()))
        elif i == 'Float':
            dataframe = dataframe.withColumn(t, dataframe[t].cast(FloatType()))
        elif i == 'Date':
            dataframe = dataframe.withColumn(t, dataframe[t].cast(DateType()))
        elif i == 'Timestamp':
            dataframe = dataframe.withColumn(t, dataframe[t].cast(TimestampType()))
        elif i == 'String':
            dataframe = dataframe.withColumn(t, dataframe[t].cast(StringType()))

    print("====================================== SHOW SCHEMA ======================================")
    dataframe.printSchema()
    c = dataframe.count()
    print(c)
    d = dataframe.distinct().count()
    print(d)
    print(d - c)
    NA = dataframe.fillna(0) 
    nm=nm.replace('.parquet','').replace('/','')
    print(nm)
    
    print("=================================== SHOW DATAFRAME ===================================")
    dataframe.show()

    dataframe.write.mode("overwrite").saveAsTable(f"main.ecommerce.src_{nm}")




# COMMAND ----------

