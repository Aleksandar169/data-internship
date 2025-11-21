from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, date_format


def main():

    spark = (
        SparkSession.builder
        .appName("WeatherDataProcessing")
        .getOrCreate()
    )

    input_path = "C:\\Users\\Lenovo\\PyCharmMiscProject\\levi9-hack9-weather-firehose-2-2022-04-01-00-20-43-275c851c-6d00-3e8a-b95a-387a70ea9ae0"

    df_raw = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(input_path)
    )

    print("=== RAW SCHEMA ===")
    df_raw.printSchema()

    df_clean = (
        df_raw
        .withColumn(
            "datetime_iso",
            date_format(
                to_timestamp(col("time_date")),
                "yyyy-MM-dd'T'HH:mm:ss"
            )
        )
        .withColumn(
            "wind_speed_kmh",
            col("weather_windSpeed") * 3.6
        )
        .select(
            col("name"),
            col("datetime_iso"),
            col("weather_temperature").alias("temperature"),
            col("wind_speed_kmh")
        )
    )

    output_path = "file:///C:/spark_demo/output/weather2_csv"

    (
        df_clean
        .coalesce(1)
        .write
        .mode("overwrite")
        .option("header", "true")
        .option("delimiter", ";")
        .csv(output_path)
    )

    print("CSV je snimljen u:", output_path)

    spark.stop()


if __name__ == "__main__":
    main()
