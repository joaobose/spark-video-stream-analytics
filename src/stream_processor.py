import base64
import cv2 as cv
import numpy as np

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, collect_list, struct, udf

from src.utils import load_config
from config.processor.schemas import video_stream_schema, movement_by_frame_output_schema
from src.vision import check_motion_v1

class VideoStreamProcessor:

  def __init__(self, config_path: str) -> None:
    self.config = load_config(config_path)

    self.spark = (SparkSession
      .builder
      .appName("VideoStreamProcessor")
      .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2")
      .config("spark.driver.memory", "10g")
      .master(self.config["spark"]["master_url"])
      .getOrCreate())

  def read_from_kafka(self):
    return (self.spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", self.config["kafka"]["bootstrap_servers"])
      .option("subscribe", self.config["kafka"]["topic"])
      .option("kafka.max.partition.fetch.bytes", self.config["kafka"]["max_batch_size"])
      .option("kafka.max.poll.records", self.config["kafka"]["max_poll_records"])
      .load()
      .selectExpr("CAST(value AS STRING) as message")
      .select(from_json(col("message"), video_stream_schema).alias("json"))
      .select("json.*"))
  
  def movement_by_frame(self, values):
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

  def define_function(self, fun):
    return udf(fun, movement_by_frame_output_schema)
  
  def process_data(self):
    uf_fun = self.define_function(self.movement_by_frame)

    df = self.read_from_kafka()

    processed_df = df.groupBy("cameraId").agg(
      uf_fun(
          collect_list(
              struct(col("timestamp"), col("data"))
          )
      ).alias("movement_by_frame")
    )
    # Process data
    query = (
      processed_df
        .writeStream
        .outputMode("update")
        .format("console")
        .start()
    )

    return query.awaitTermination()
  

if __name__ == "__main__":
  processor = VideoStreamProcessor()
  df = processor.read_from_kafka()
  processor.process_data()