# Realtime Data Pipeline – Kafka × Flink × PostgreSQL

Ziel des Projekts ist der Aufbau einer containerisierten **Echtzeit-Datenpipeline**, die Rohdaten aus einer CSV-Datei liest, über Apache Kafka (Redpanda) streamt, in **Flink** verarbeitet und aggregierte Ergebnisse in **PostgreSQL** speichert.  
Das System ist vollständig lokal mit **Docker Compose** lauffähig.


##  Systemarchitektur

sample.csv → Producer → Kafka (Redpanda) → Flink-Job → PostgreSQL → Adminer


Producer	Python-Service, der 1 Mio Datensätze aus sample.csv liest, pseudonymisiert und an das Kafka-Topic telemetry.v0 sendet

Redpanda	Kafka-kompatibler Streaming-Broker für lokale Umgebungen

Kafka-UI	Weboberfläche zur Topic-Überwachung (http://localhost:8080)

Flink-Job	Python-basierter Microservice, konsumiert Kafka-Events, schreibt Rohdaten in telemetry.raw_events und 1-Minuten-Aggregationen in telemetry.agg_1min

PostgreSQL	Persistente Datenhaltung

Adminer	SQL-UI unter http://localhost:9090

# Startanleitung

Docker Desktop (Windows / macOS / Linux)
Git

# Schritte
git clone https://github.com/tklages1992/RealtimePipeline.git
cd RealtimePipeline
docker compose up -d


# Nach dem Start:

Kafka UI	http://localhost:8080 Monitoring / Topics
Adminer	http://localhost:9090 Datenbank-UI
Flink JobManager	http://localhost:8083 Flink Dashboard
PostgreSQL	localhost:5432 (User: app / Pass: app / DB: telemetry)	

# Um alle Container zu stoppen:
docker compose down

# Kafka Topic

Name: telemetry.v0
Messages: > 1 000 000
Schema: {"sensor_id": int, "value": float, "event_time": timestamp}


# Kriterium	              Umsetzung
Reliability	            Health-Checks, automatische Start-Delays für Kafka & Postgres
Scalability	            Entkopplung über Kafka-Topics, modulare Microservices
Maintainability	        Einheitliche Docker-Compose-Struktur, klarer Code
Data Security	          Pseudonymisierte IDs, lokale Ausführung
Data Governance	        Versionierte Konfiguration & dokumentierte Architektur


# Reflexion

Aufbau und Stabilisierung der Container-Kommunikation über interne Netzwerke (redpanda:29092)
Debugging von Docker-CMD/ENTRYPOINT und UTF-8-BOM-Problemen unter Windows
Testlauf mit 1 000 000 CSV-Zeilen erfolgreich – ca. 150 000 persistierte Datensätze, 156 000 Aggregationen
Stabile, reproduzierbare Umgebung für zukünftige Erweiterungen geschaffen
