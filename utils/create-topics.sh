#!/bin/bash

while IFS= read -r topic || [[ -n "$topic" ]]; do
  echo "Creating topic: $topic"
  kafka-topics --create \
    --bootstrap-server broker:29092 \
    --replication-factor 1 \
    --partitions 1 \
    --topic "$topic" \
    --if-not-exists || true
done < /utils/bootstrap_topics.txt

