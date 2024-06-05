# Spark video stream analytics

Python implementation of the Spark video stream analytics project. The original project was implemented in Java and can be found [here](https://github.com/baghelamit/video-stream-analytics/tree/master).

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

## Kafka local setup

### Prerequisites

1. Java: Kafka and Zookeeper require Java to run. Make sure you have Java installed:
 ```sh
 sudo apt update
 sudo apt install default-jdk
 java-version
 ```

2. Download Kafka:
 - Download the latest version of Kafka from [Apache Kafka Downloads](https://kafka.apache.org/downloads).
 - Extract the downloaded file:
 ```sh
 tar -xzf kafka_2.13-3.7.0.tgz
 sudo mv kafka_2.13-3.7.0 /opt/kafka
 ```
There is no need to download Zookeeper separately because it comes bundled with Kafka.

### Setting

Add the following lines to your `~/.bashrc` or `~/.zshrc` file to set the environment variables:

```sh
# Zookeeper
export ZOO_HOME="/opt/kafka"
export PATH=$PATH:$ZOO_HOME/bin

# Kafka
export KAFKA_HOME="/opt/kafka"
export PATH=$PATH:$KAFKA_HOME/bin
```

Then, reload the shell configuration file:

```sh
source ~/.bashrc
```

### Start the Services

To start Zookeeper, run the following command from the root directory of repository:

```sh
zookeeper-server-start.sh CONFIG/zookeeper.properties
```

To start Kafka, run the following command from the root directory of repository:

```sh
kafka-server-start.sh CONFIG/server.properties
```
