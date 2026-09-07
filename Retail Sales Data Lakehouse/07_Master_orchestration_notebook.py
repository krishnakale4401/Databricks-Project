# Databricks notebook source
notebook = [
    '/Workspace/Users/kalek9184@gmail.com/Databricks_Project/Notebook/01_Bronze_Parquet_Datasets',
    '/Workspace/Users/kalek9184@gmail.com/Databricks_Project/Notebook/02_Silver_Delta_Tables',
    '/Workspace/Users/kalek9184@gmail.com/Databricks_Project/Notebook/03_SCD_Dimension_Tables',
    '/Workspace/Users/kalek9184@gmail.com/Databricks_Project/Notebook/04_Fact_Table',
    '/Workspace/Users/kalek9184@gmail.com/Databricks_Project/Notebook/05_Gold_Aggregation_Tables',
    '/Workspace/Users/kalek9184@gmail.com/Databricks_Project/Notebook/06_Time_travel__rollback_demonstration'
]
for nb in notebook:
    print(nb)
    try:
        dbutils.notebook.run(nb, 300,)
        print('Pipeline completed successfully')
    except Exception as e:
        print(f"Pipeline failed at {nb}")
        raise e
