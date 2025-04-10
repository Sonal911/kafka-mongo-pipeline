import unittest
from unittest.mock import MagicMock
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from consumer.consumer import process_message, check_and_emit_expired_windows
from collections import defaultdict

class TestStreamProcessor(unittest.TestCase):

    def test_process_message(self):
        window_data = defaultdict(list)
        data = {
            "sensorId": "sensor-123",
            "value": 45.2,
            "timestamp": 1741032960000  # This is an aligned timestamp (e.g., 12:56:00)
        }

        process_message(data, window_data)

        window_start = (data["timestamp"] // 60000) * 60000
        self.assertIn(("sensor-123", window_start), window_data)
        self.assertEqual(window_data[("sensor-123", window_start)], [45.2])

    def test_check_and_emit_expired_windows(self):
        window_data = defaultdict(list)
        producer = MagicMock()
        output_topic = "sensor-output"

        sensor_id = "sensor-123"
        window_start = 1741032900000
        window_end = window_start + 60000

        # Add some values to window
        window_data[(sensor_id, window_start)] = [10, 20, 30]

        current_time = window_end + 6000  # After grace period

        emitted = check_and_emit_expired_windows(window_data, current_time, producer, output_topic)

        expected = [{
            "sensorId": sensor_id,
            "windowStart": window_start,
            "windowEnd": window_end,
            "averageValue": 20.0
        }]

        producer.send.assert_called_once_with(output_topic, expected[0])
        self.assertEqual(emitted, expected)
        self.assertNotIn((sensor_id, window_start), window_data)

if __name__ == "__main__":
    unittest.main()
