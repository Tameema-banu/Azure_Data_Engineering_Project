# Databricks notebook source
# MAGIC %md
# MAGIC # Incremental Data Loading Using AutoLoader

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA netflix_catalog.net_schema;

# COMMAND ----------

checkpoint_location ="abfss://silver@datalakeforproject.dfs.core.windows.net/checkpoint"

# COMMAND ----------

df = spark.readStream\
  .format("cloudFiles")\
  .option("cloudFiles.format", "csv")\
  .option("cloudFiles.schemaLocation",checkpoint_location)\
  .load("abfss://raw@datalakeforproject.dfs.core.windows.net")

# COMMAND ----------

display(df)

# COMMAND ----------

df.writeStream\
  .option("checkpointLocation",checkpoint_location)\
  .trigger(processingTime='10 seconds')\
  .start("abfss://bronze@datalakeforproject.dfs.core.windows.net/netflix_titles")

# COMMAND ----------

