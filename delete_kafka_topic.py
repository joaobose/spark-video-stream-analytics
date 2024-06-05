from confluent_kafka.admin import AdminClient, NewTopic

def delete_kafka_topic(config, topic_name):
    """
    Deletes a Kafka topic if it exists.
    
    Args:
    - config (dict): Configuration dictionary for the Kafka admin client.
    - topic_name (str): Name of the topic to delete.
    """
    admin_client = AdminClient(config)
    
    fs = admin_client.delete_topics([topic_name], operation_timeout=30)
    
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print(f"Topic {topic} deleted")
        except Exception as e:
            print(f"Failed to delete topic {topic}: {e}")

if __name__ == '__main__':
    kafka_config = {
        'bootstrap.servers': 'localhost:9092'
    }

    topic_name = 'video-stream-event'
    delete_kafka_topic(kafka_config, topic_name)
