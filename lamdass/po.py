from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, date_format


def main():
    # 1. Pokreni Spark lokalno
    spark = (
        SparkSession.builder
        .appName("WeatherDataProcessing")
        .getOrCreate()
    )

    # 2. Putanja do lokalnog fajla (PROMENI ime ako treba)
    input_path = "C:\\Users\\Lenovo\\PyCharmMiscProject\\levi9-hack9-weather-firehose-2-2022-04-01-00-20-43-275c851c-6d00-3e8a-b95a-387a70ea9ae0"

    # 3. Učitaj CSV sa headerom
    df_raw = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(input_path)
    )

    # (optional) - proveri šemu jednom
    print("=== RAW SCHEMA ===")
    df_raw.printSchema()

    # Očekujemo kolone: name, time_date, weather_temp, weather_windSpeed, itd.

    # 4. Transformacije:
    #    - time_date -> ISO 8601 string
    #    - weather_windSpeed (m/s) -> wind_speed_kmh (km/h)
    df_clean = (
        df_raw
        .withColumn(
            "datetime_iso",
            date_format(
                to_timestamp(col("time_date")),  # "2022-04-01 00:50:43"
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

    print("=== TRANSFORMED SAMPLE ===")
    df_clean.show(10, truncate=False)

    # 5. Snimi lokalno kao CSV sa ; delimiterom
    output_path = "file:///C:/spark_demo/output/weather2_csv"

    (
        df_clean
        .coalesce(1)  # sve u jedan fajl (zgodno za testiranje)
        .write
        .mode("overwrite")
        .option("header", "true")
        .option("delimiter", ";")
        .csv(output_path)
    )

    print("✅ DONE – CSV je snimljen u:", output_path)

    spark.stop()


if __name__ == "__main__":
    main()
