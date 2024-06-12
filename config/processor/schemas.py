from pyspark.sql.types import StructType, StructField, StringType, LongType, IntegerType, ArrayType, BooleanType


video_stream_schema = StructType([
  StructField("cameraId", StringType(), True),
  StructField("timestamp", LongType(), True),
  StructField("rows", IntegerType(), True),
  StructField("cols", IntegerType(), True),
  StructField("type", StringType(), True),
  StructField("data", StringType(), True)
])

# Define processing logic
movement_by_frame_output_schema = ArrayType(
  StructType([
    StructField("timestamp", LongType(), True),
    StructField("has_movement", BooleanType(), True)
  ])
)

# Define schema