#!/bin/bash
echo "? warte auf Kafka?"
until nc -z redpanda 29092; do sleep 2; done
echo "? Kafka erreichbar"

echo "? warte auf Postgres?"
until nc -z postgres 5432; do sleep 2; done
echo "? Postgres erreichbar"

python src/flink_job.py