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

## Motion detection demo

To run the motion detection demo, first source the environment:

```bash
source venv/bin/activate
```

Then run the following command:

```bash
python src/motion-demo.py
```

## Kafka local installation instructions
The following instructions will allow you to install Kafka on your Ubuntu system (and other Debian based systems)

1. Apache Kafka is a Java-based software, so you must have Java installed on your system. You can install it by running the following command

```bash
sudo sh -c 'apt install default-jdk && apt install default-jre'
```

2. Download the latest version of Apache Kafka from https://kafka.apache.org/downloads in binary downloads. Alternatively you can run a wget command (we will assume version `2.13-3.7.0`).

```bash
wget https://downloads.apache.org/kafka/3.7.0/kafka_2.12-3.7.0.tgz
```

3. Download and extract the contents to a directory of your choice, for example `~/kafka_2.13-3.7.0`

```bash
tar xzf kafka_2.13-3.7.0.tgz
mv kafka_2.13-3.7.0 ~
```

4. Open a Shell and navigate to the Apache Kafka root directory. We will assume that the Kafka download is expanded to the `~/kafka_2.13-3.7.0` directory.

Since Apache Kafka depends on Zookeeper for cluster management, you must start Zookeeper before starting Kafka. You don't need to install Zookeeper explicitly, as it comes included with Apache Kafka. From Apache Kafka root, run the following command to start it

```bash
~/kafka_2.13-3.7.0/bin/zookeeper-server-start.sh ~/kafka_2.13-3.7.0/config/zookeeper.properties
```

Then to start Apache Kafka open another shell window and run the following command from Apache Kafka root to start Apache Kafka

```bash
~/kafka_2.13-3.7.0/bin/kafka-server-start.sh ~/kafka_2.13-3.7.0/config/server.properties
```

Be sure to keep both shell windows open; otherwise it will close Kafka or Zookeeper. Ready! Kafka has already started.
