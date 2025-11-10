# Realtime Data Backend (Kafka → Flink → PostgreSQL)

Lokale Microservice-Architektur (Docker):
- Producer liest data/sample.csv und sendet Events an Kafka
- Flink verarbeitet Events (Event-Time, Watermarks, 1-Minuten-Fenster)
- PostgreSQL speichert Roh- und Aggregatdaten

## Ordner
- data/                 (lokale Daten, **nicht** in Git)
- db/init/              (SQL-Skripte für DB-Init)
- docker/               (Compose/Configs)
- services/producer/    (CSV→Kafka Producer)
- services/flink_job/   (Streaming Job)

## Getting started
- Voraussetzungen: Docker Desktop, Git
