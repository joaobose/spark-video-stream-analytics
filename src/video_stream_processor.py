import base64
import cv2 as cv
import numpy as np

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType, IntegerType, ArrayType, BooleanType
from pyspark.sql.functions import col, from_json, collect_list, struct, udf


from src.vision import check_motion_v1

# Properties
SPARK_MASTER_URL = "local[*]"

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "video-stream-event"
KAFKA_MAX_PARTITION_FETCH_BYTES = 2097152
KAFKA_MAX_POLL_RECORDS = 10

# Create Spark session
spark = (SparkSession
         .builder
         .appName("VideoStreamProcessor")
         .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2")
         .config("spark.driver.memory", "10g")
         .master(SPARK_MASTER_URL)
         .getOrCreate())

# Define schema
schema = StructType([
    StructField("cameraId", StringType(), True),
    StructField("timestamp", LongType(), True),
    StructField("rows", IntegerType(), True),
    StructField("cols", IntegerType(), True),
    StructField("type", StringType(), True),
    StructField("data", StringType(), True)
])


# Read from Kafka
df = (spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
      .option("subscribe", KAFKA_TOPIC)
      .option("kafka.max.partition.fetch.bytes", KAFKA_MAX_PARTITION_FETCH_BYTES)
      .option("kafka.max.poll.records", KAFKA_MAX_POLL_RECORDS)
      .load()
      .selectExpr("CAST(value AS STRING) as message")
      .select(from_json(col("message"), schema).alias("json"))
      .select("json.*"))


# Define processing logic
movement_by_frame_output_schema = ArrayType(
    StructType([
        StructField("timestamp", LongType(), True),
        StructField("has_movement", BooleanType(), True)
    ])
)


def movement_by_frame(values):
    # Sort by timestamp
    sorted_values = sorted(values, key=lambda x: x[0])

    # Process data
    output = []
    prev_frame = None

    for value in sorted_values:
        t, data = value

        # Decode image from .jpg base64 string
        decoded_data = base64.b64decode(data)
        nparr = np.frombuffer(decoded_data, np.uint8)
        frame = cv.imdecode(nparr, cv.IMREAD_COLOR)

        # Check for motion
        if prev_frame is not None:
            has_movement, _, _ = check_motion_v1(prev_frame, frame)
            output.append((t, has_movement))
        else:
            output.append((t, False))

        prev_frame = frame

    return output


movement_by_frame_udf = udf(movement_by_frame, movement_by_frame_output_schema)

# Group by cameraId and map to processing logic
processed_df = df.groupBy("cameraId").agg(
    movement_by_frame_udf(
        collect_list(
            struct(col("timestamp"), col("data"))
        )
    ).alias("movement_by_frame"),
)


# # Process data
query = (processed_df
         .writeStream
         .outputMode("update")
         .format("console")
         .start())

query.awaitTermination()
