# Spark video stream analytics

Python implementation of the Spark video stream analytics project. The original project was implemented in Java and can be found [here](https://github.com/baghelamit/video-stream-analytics/tree/master).

# Setup

## Python environment setup

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

## Pyspark and Java

Currently, the project is utilizing the pyspark library in its version 3.5.1

Spark runs on Java 8/11/17, Scala 2.12/2.13, Python 3.8+, and R 3.5+. Java 8 prior to version 8u371 support is deprecated as of Spark 3.5.0.

So, in order to run the project without issues, make sure you have Java 8/11/17 installed on your machine.

# Execution

Before running the code, make sure to source the environment:

```bash
source venv/bin/activate
```

## Motion detection demo

To run the motion detection demo, run the following command:

```bash
python src/motion-demo.py
```

## Video stream collector

To run the video stream collector, run the following command:

```bash
python src/video-stream-collector.py --config CONFIG
```

Where config is the path to the configuration file. Multiple example configuration files can be found in the [`config/collector`](./config/collector) directory.
