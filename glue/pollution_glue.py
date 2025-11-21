import sys
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.context import SparkContext
from pyspark.sql.functions import to_date, col, input_file_name

args = getResolvedOptions(
    sys.argv,
    ["JOB_NAME", "SOURCE_PATH", "TARGET_PATH"]
)

source_base = args["SOURCE_PATH"].rstrip("/")
target_path = args["TARGET_PATH"].rstrip("/")

input_path = f"{source_base}/*/*"

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args["JOB_NAME"], args)

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(input_path)
)

df = df.withColumn("_input_file", input_file_name())

df = df.withColumn(
    "date",
    to_date(col("time_date"), "yyyy-MM-dd HH:mm:ss")
)

dyf = DynamicFrame.fromDF(df, glueContext, "pollution_dyf")

glueContext.write_dynamic_frame.from_options(
    frame=dyf,
    connection_type="s3",
    format="csv",
    connection_options={
        "path": target_path,
        "partitionKeys": ["date"]
    },
    format_options={
        "withHeader": True
    }
)

job.commit()
