# kafka-mongo-pipeline
A real-time data pipeline that consumes sensor data from Kafka, aggregates it, and stores the output in MongoDB. Includes CI/CD with GitHub Actions and unit testing support.

Once we clone the repo, we will run unit test.  

**CI/CD Test Stage:**  
GitHub Actions will automatically run tests on every push.  
To run locally:

python -m unittest discover tests
![image](https://github.com/user-attachments/assets/3bd3cd3b-8318-42bd-90a4-0bf806383f13)

**Start the pipeline:**  
Run all services via Docker Compose:

docker-compose up –build
![image](https://github.com/user-attachments/assets/6593b573-f03c-4c75-ae72-ddafd8c063eb)

- **broker** – Kafka broker for message handling.  
- **mongodb** – Stores aggregated sensor data.  
- **akhq** – Web UI to monitor Kafka topics.  
- **topic-creator** – Creates Kafka topics at startup.  
- **sensor-producer** – Sends random sensor data to Kafka topic.  
- **sensor-consumer** – Aggregates and forwards sensor data to Kafka topic.  
- **kafka_mongo_consumer** – Inserts Kafka messages into MongoDB.

Once everything is up and running, 

![image](https://github.com/user-attachments/assets/1f574c3d-b1fc-4baf-9ec1-6dadd276bb8f)


**topic-creator:**  
Will create topics and close

![image](https://github.com/user-attachments/assets/03e0711b-e4a8-4412-9dad-3e5b9acc8310)

**sensor-producer:**  
Producer pushes sensor messages to sensor-input

![image](https://github.com/user-attachments/assets/5a564e3b-ea5d-4810-8563-48c727d6f0d5)

**sensor-consumer:**  
Consumer reads from sensor-input, aggregates, and sends data to sensor-output.

![image](https://github.com/user-attachments/assets/8c5898ee-ae81-432f-90d5-46d4c1d8f323)

**kafka_mongo_consumer:**  
kafka_mongo_consumer will send the results in aggregated_output collection to Mongo DB.

![image](https://github.com/user-attachments/assets/eba9c3f5-8bc6-4999-93df-fa166376bc9b)

MongoDB stores the final results in aggregated_output collection

**Check MongoDB Output:**

Open bash:

docker exec -it mongodb mongo -u admin -p adminpassword --authenticationDatabase admin

![image](https://github.com/user-attachments/assets/ba71b2cd-9214-47cd-bade-71273ad262d0)

use sensor_data  
db.aggregated_output.find().pretty()

![image](https://github.com/user-attachments/assets/2b815f87-3d1b-4c7b-880f-e942014fd422)


We can now see records in Mongodb.














