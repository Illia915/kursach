#Add this param in adf
catalog_name = dbutils.widgets.get("catalog-name")
dbutils.widgets.text("volume_schema_name", "spuds_data")
volume_schema_name = dbutils.widgets.get("volume_schema_name")
input_file_path = dbutils.widgets.get("input_file_path")
print(input_file_path)

from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("H1", StringType(), True),
    StructField("Consortium", IntegerType(), True),
    StructField("Currency", StringType(), True),
    StructField("Channel", StringType(), True),
    StructField("MerchantId", StringType(), True),
    StructField("MIDName", StringType(), True),
    StructField("Type", StringType(), True),
    StructField("ExternalRequestCode", StringType(), True),
    StructField("TransactionCount", IntegerType(), True),
    StructField("Amount", StringType(), True),
])

df_raw = spark.read.option("header", "false").schema(schema).csv(input_file_path)
display(df_raw)

# Get the first row's second column value
settlementDate = df_raw.head(1)[0][1]  # First row (index 0), second column (index 1)

# Get the new header from the second row
header_row = df_raw.head(2)[1]  # index 1 because index 0 is old header
new_columns = [str(c) for c in header_row]

# Remove first two rows (old header + new header row)
from pyspark.sql.functions import monotonically_increasing_id, col

df_final = (df_raw
    .withColumn("_idx", monotonically_increasing_id())
    .filter(col("_idx") >= 2)
    .drop("_idx"))

# Add settlementDate as a new column
from pyspark.sql.functions import lit
df_final = df_final.withColumn("SettlementDate", lit(settlementDate))

# Get current column names
cols = df_final.columns

# Rename 2nd and 8th columns
cols[1] = "Consortium"      # index 1 = second column
cols[8] = "TransactionCount"    # index 7 = eighth column

# Apply new column names
df_renamed = df_final.toDF(*cols)
display(df_renamed)


