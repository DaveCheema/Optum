# Databricks notebook source
#%sh
#ping 10.179.64.4

# COMMAND ----------

#%sh
#nslookup sql-db-server.westus.cloudapp.azure.com

# COMMAND ----------

import pandas as pd
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from pyspark.sql import functions as F
import datetime

# COMMAND ----------

jdbcHostname = "10.179.64.4"
jdbcDatabase = "DCMembersDB"
userName = 'SA'
password = 'Password1234'
jdbcPort = 1433
jdbcUrl = "jdbc:sqlserver://{0}:{1};database={2};user={3};password={4}".format(jdbcHostname, jdbcPort, jdbcDatabase, userName, password)

df = spark.read.jdbc(url=jdbcUrl, table='Members')
display(df)

# COMMAND ----------

#Handle Null values.
df = df.withColumn("HealthCondition", F.when(F.col("HealthCondition").isNull(), "Unknown").otherwise(F.col("HealthCondition")))

#Handle missing values.
df = df.withColumn("HealthCondition", F.when(F.col("HealthCondition") == '', "Not Provided").otherwise(F.col("HealthCondition")))

#Split into 2 separate columns.
df = df.withColumn("Sex_Male", F.when(F.col("Sex") == 'M', 1).otherwise(0))
df = df.withColumn("Sex_Female", F.when(F.col("Sex") == 'F', 1).otherwise(0))

df.show()

# COMMAND ----------

#Perform enrichment.
#Create a Dataframe. In real life, this data will be imported from some external source.

bloodPressureDF = pd.DataFrame({'age': [18, 25, 35, 45, 55, 65],
               'ideal_blood_pressure': [80, 90, 100, 110, 120, 125]})

# COMMAND ----------

inner_join = df.join(bloodPressureDF, int(df.DOB.year) <= int(bloodPressureDF.age))
inner_join.show()

# COMMAND ----------

#dt1 = parse('6/13/1956')
#dt2 = datetime.date.today()
#difference_in_years = relativedelta(dt2, dt1).years
#difference_in_years
#df = df.withColumn("HealthCondition", F.when(F.col("HealthCondition") == '', "Not Provided").otherwise(F.col("HealthCondition")))

#df = df.withColumn("ideal_blood_pressure", F.when(relativedelta(datetime.date.today(), F.col("DOB")) <= 18, 80).otherwise(F.when(relativedelta(datetime.date.today(), #F.col("DOB")) <= 25, 90)otherwise(F.when(relativedelta(datetime.date.today(), F.col("DOB")) <= 35, 100)otherwise(F.when(relativedelta(datetime.date.today(), F.col("DOB")) <= #45, 110)otherwise(F.when(relativedelta(datetime.date.today(), F.col("DOB")) <= 55, 120)otherwise(F.when(relativedelta(datetime.date.today(), F.col("DOB")) <= 65, 125))




# COMMAND ----------

df.printSchema()

# COMMAND ----------

dt = pyspark.sql.types.DateType.Date

# COMMAND ----------

df.count()

len(df.columns), df.columns
df.describe().show()
df.select('Name','DOB', 'Sex', 'HealthCondition').show(3)

# COMMAND ----------

df.show()


# COMMAND ----------

df.groupBy("Sex").count().show()

# COMMAND ----------

renamedColumnsDF = df.withColumnRenamed("DOB", "Date of Birth")
renamedColumnsDF.show()


# COMMAND ----------

#df.select('Sex').distinct().count()

#df.crosstab('Sex', 'HealthCondition').show()

#df.select('Sex','HealthCondition').dropDuplicates().show()

#df.dropna().count() #Drop rows with NULL values

df.fillna(-1).show()

# COMMAND ----------

from dateutil.parser import parse
from pyspark.sql import functions as F

#datetime = parse('1/1/1980')
#df.filter(df.DOB < datetime).show()
#df.groupby('Sex').count().show()
#df.orderBy(df.Sex.asc()).show()
#train.withColumn('Purchase_new', train.Purchase /2.0).select('Purchase','Purchase_new').show(5)
# set fixed value to 'c2' where the condition is met
#df.loc[df['c1'] == 'Value', 'c2'] = 10

# copy value from 'c3' to 'c2' where the condition is NOT met
#df.loc[df['c1'] != 'Value', 'c2'] = df[df['c1'] != 'Value', 'c3']
#df.drop('HealthCondition').columns

df = df.withColumn("Sex_Male", F.when(F.col("Sex") == 'M', (1)).otherwise(0))
df.show()




# COMMAND ----------

ts = df.DOB[2]
ts.printSchema
