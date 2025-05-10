# Databricks notebook source
# MAGIC %md
# MAGIC # Silver Data Transformations

# COMMAND ----------

from pyspark.sql.functions import*
from pyspark.sql.types import*

# COMMAND ----------

df = spark.read.format("delta")\
    .option("header",True)\
    .option("inferSchema",True)\
    .load("abfss://bronze@datalakeforproject.dfs.core.windows.net/netflix_titles")

# COMMAND ----------

df.display()

# COMMAND ----------

df = df.fillna({"duration_minutes":0,"duration_seasons":1})

# COMMAND ----------

df.display()

# COMMAND ----------

df =df.withColumn("duration_minutes",df["duration_minutes"].cast(IntegerType()))\
    .withColumn("duration_seasons",df["duration_seasons"].cast(IntegerType()))

# COMMAND ----------

df.display()

# COMMAND ----------

df = df.withColumn("shorttitle",split(col('title'),':')[0])

# COMMAND ----------

df.display()

# COMMAND ----------

df = df.withColumn("rating",split(col('rating'),'-')[0])
df.display()

# COMMAND ----------

df = df.withColumn("type_flag",when(col("type")=="Movie",1)\
                        .when(col("type")=="TV Show",2)\
                        .otherwise(0))
df.display()


# COMMAND ----------

from pyspark.sql.window import Window

# COMMAND ----------

df=df.withColumn("duration_ranking",dense_rank().over(Window.orderBy(col("duration_minutes").desc())))

# COMMAND ----------

df.display()

# COMMAND ----------

df_viz = df.groupBy("type").agg(count('*').alias("total_count"))
df_viz.display()

# COMMAND ----------

df.write.format("delta")\
    .mode("overwrite")\
    .option("path","abfss://silver@datalakeforproject.dfs.core.windows.net/netflix_titles")\
    .save()

# COMMAND ----------

