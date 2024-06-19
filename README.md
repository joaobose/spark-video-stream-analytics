# Spark video stream analytics

Python implementation of the Spark video stream analytics project. The original project was implemented in Java and can be found [here](https://github.com/baghelamit/video-stream-analytics/tree/master).

## Setup

### Python environment setup

First, make sure you have a Python environment set up. You can use the following command to create a new environment:

```bash
python3 -m venv ./venv
```

Then source the enviroment with the following command:

```bash
source venv/bin/activate
```

Finally, install the required packages with the following command:

```bash
python3 -m pip install -r requirements.txt
```

Make sure to deactivate the environment when you are done with the following command:

```bash
deactivate
```

Whenever you want to work on the project, make sure to source the environment before running the code.

### Pyspark and Java

Currently, the project is utilizing the pyspark library in its version 3.5.1

Spark runs on Java 8/11/17, Scala 2.12/2.13, Python 3.8+, and R 3.5+. Java 8 prior to version 8u371 support is deprecated as of Spark 3.5.0.

So, in order to run the project without issues, make sure you have Java 8/11/17 installed on your machine.

## Installation of Spark

Even though the project is using the pyspark library, it is necessary to have the Spark service installed and running on your machine when launching thr project.

Before installing Spark, make sure you have Java 8/11/17 installed on your machine and the variable `JAVA_HOME` is correctly set in your environment variables.

Now, the following steps will guide you through the installation of Spark:

1. Download the latest version of Spark from the [official website](https://spark.apache.org/downloads.html).
1. Extract the downloaded file to a directory of your choice.
1. Set the `SPARK_HOME` variable in your environment variables to the directory where you extracted the Spark files.
1. Test the installation by running the following command:

```bash
# launch Scala Based Spark
spark-shell

# launch PySpark
pyspark
```

If you see the Spark shell, then the installation was successful.

## Kafka and Zookeper

Even tho the project `kafka-python` library to interact with Kafka, it is necessary to have Kafka and Zookeeper services running on your machine. In order to achieve that, those environments were configured to work through a **Docker** container.

So, having docker installed and working on your machine is a requirement to run the project.

Now, the following steps will guide you through the installation of the container with Kafka and Zookeeper:
1. Run the following command to build the container:

```bash
make BUILDSERVER
```

1. Run the following command to start the container:

```bash
make RUNSERVER
```

When you finish working with the project, make sure to stop the container with the following command:

```bash
make STOPSERVER
```

## Execution

Before running the code, make sure to source the environment:

```bash
source venv/bin/activate
```

or if you are using Windows:

```bash
.\venv\Scripts\activate
```

### Services setup

Before running either the video stream collector or the video stream processor, we need to run some services to ensure the project executes correctly. These services are: Zookeeper, Kafka, and Spark.

Currently, Kafka and Zookeper are running on a Docker container. To start the container, run the following command:

```bash
make RUNSERVER
```

### Motion detection demo

To run the motion detection demo, run the following command:

```bash
python src/motion-demo.py
```

### Video Stream Collector

To run the video stream collector, run the following command:

```bash
python src/video-stream-collector.py --config {{ CONFIG_FILE }}
```

Where `CONFIG_FILE` is the path to the configuration file. Multiple example configuration files can be found in the [`config/collector`](./config/collector) directory.

All of the configuration files can be used to test the video stream collector.

### Video Stream Processor

To run the video stream processor, we need to have the Spark service running. Once the service is running, run the following command:

```bash
pyspark < src/video_stream_processor.py
```
