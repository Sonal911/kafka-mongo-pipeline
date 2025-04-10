import unittest
from unittest.mock import MagicMock
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from consumer.consumer_to_mongo import consume_and_insert

class TestKafkaToMongo(unittest.TestCase):

    def test_consume_and_insert(self):
        # Mock Kafka consumer
        mock_consumer = [
            MagicMock(value={"sensorId": "sensor-001", "averageValue": 55.5}),
            MagicMock(value={"sensorId": "sensor-002", "averageValue": 42.1}),
        ]

        # Mock MongoDB collection
        mock_collection = MagicMock()

        # Call the function with a limit (so it doesn't loop forever)
        consume_and_insert(mock_consumer, mock_collection, limit=2)

        # Assert insert_one was called with expected data
        expected_calls = [
            ({"sensorId": "sensor-001", "averageValue": 55.5},),
            ({"sensorId": "sensor-002", "averageValue": 42.1},)
        ]

        actual_calls = [call.args for call in mock_collection.insert_one.call_args_list]
        self.assertEqual(actual_calls, expected_calls)

        self.assertEqual(mock_collection.insert_one.call_count, 2)

if __name__ == "__main__":
    unittest.main()
