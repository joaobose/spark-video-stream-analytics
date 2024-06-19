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
    # Configuration is loaded from a yaml file
    self.config = load_config(config_path)

    # Create spark session with SQL support
    self.spark = (SparkSession
      .builder
      .appName("VideoStreamProcessor")
      .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2")
      .config("spark.driver.memory", "10g")
      .master(self.config["spark"]["master_url"])
      .getOrCreate())

  def read_from_kafka(self):
    """Reads video stream data from Kafka.

    Configuration for Kafka is loaded from the configuration file.

    The data that is returns follows a schema defined in configuration and 
    follows the structure:
    - cameraId: String
    - timestamp: Long
    - rows: Integer
    - cols: Integer
    - type: String
    - data: String
    """
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
    """Processes video stream data to detect motion by frame.

    The function receives a list of values, where each value is a tuple
    containing a timestamp and a base64 encoded image. The function will
    decode the image, and check for motion between frames.

    For checking the motion, it is being used currently the function 
    check_motion_v1, that replicates the original logic from the
    original article.

    The output will be a list of tuples, where each tuple contains a timestamp
    and a boolean indicating if there was motion in the frame.

    The output schema is defined in the configuration file.
    """
  
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

      # Apply custom motion detection function in between frames
      if prev_frame is not None:
        has_movement, _, _ = check_motion_v1(prev_frame, frame)
        output.append((t, has_movement))
      else:
        output.append((t, False))

      prev_frame = frame

    return output
  
  def process_data(self):
    """Processes video stream data to detect motion by frame.

    The function reads video stream data from Kafka, processes it to detect
    motion by frame, and writes the results to the console.

    The output schema is defined in the configuration file.
    """
    uf_fun = udf(self.movement_by_frame, movement_by_frame_output_schema)

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
  processor = VideoStreamProcessor("../config/processor/variables.yaml")
  processor.process_data()