import json
import time
import os
from kafka import KafkaConsumer, KafkaProducer
from collections import defaultdict


def process_message(data, window_data):
    sensor_id = data["sensorId"]
    value = data["value"]
    timestamp = data["timestamp"]

    window_start = (timestamp // 60000) * 60000
    window_data[(sensor_id, window_start)].append(value)

def check_and_emit_expired_windows(window_data, current_time, producer, output_topic):
    emitted = []
    for key in list(window_data.keys()):
        sensor_id, window_start = key
        window_end = window_start + 60000

        if current_time > window_end + 5000:
            values = window_data[key]
            avg = round(sum(values) / len(values), 2)
            result = {
                "sensorId": sensor_id,
                "windowStart": window_start,
                "windowEnd": window_end,
                "averageValue": avg
            }
            producer.send(output_topic, result)
            print(f"Published: {result}")
            emitted.append(result)
            del window_data[key]
    return emitted

def main():
    bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS", "localhost:9092")
    topic_name = "sensor-input"

    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=bootstrap_servers,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="sensor-consumer-group"
    )

    producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    # Store readings per (sensorId, windowStart)
    window_data = defaultdict(list)

    print("Starting stream...")

    try:
        while True:
            messages = consumer.poll(timeout_ms=1000)

            current_time = int(time.time() * 1000)

            for _, msgs in messages.items():
                for msg in msgs:
                    data = msg.value
                    process_message(data, window_data)
            # Check for expired windows (older than 65s)
            emitted = check_and_emit_expired_windows(window_data, current_time, producer, "sensor-output")

    except KeyboardInterrupt:
        print("Stopped.")

if __name__ == "__main__":
    main()
