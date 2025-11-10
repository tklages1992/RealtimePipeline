import os, json, time
from kafka import KafkaConsumer
import psycopg2
from datetime import datetime
from dateutil import parser

# --- Umgebungsvariablen ---
brokers = os.getenv("KAFKA_BROKERS", "redpanda:9092")
topic   = os.getenv("TOPIC", "telemetry.v0")
pg_host = os.getenv("PGHOST", "postgres")
pg_db   = os.getenv("PGDATABASE", "telemetry")
pg_user = os.getenv("PGUSER", "app")
pg_pw   = os.getenv("PGPASSWORD", "app")

print(f"?? Aggregator startet (Kafka: {brokers}, Topic: {topic}, Postgres: {pg_host})")

# --- PostgreSQL Verbindung ---
conn = psycopg2.connect(host=pg_host, dbname=pg_db, user=pg_user, password=pg_pw)
conn.autocommit = True
cur = conn.cursor()

# --- Kafka Consumer ---
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=brokers,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="flink-group-agg",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

window = {}   # { (sensor_id, minute): [werte] }

def flush_window():
    for (sid, minute), vals in list(window.items()):
        if not vals: 
            continue
        w_start = minute
        w_end   = minute + 60
        cnt     = len(vals)
        avg     = sum(vals) / cnt
        mn      = min(vals)
        mx      = max(vals)
        cur.execute("""
            INSERT INTO telemetry.agg_1min (window_start, window_end, sensor_id, cnt, avg_value, min_value, max_value)
            VALUES (to_timestamp(%s), to_timestamp(%s), %s, %s, %s, %s, %s)
            ON CONFLICT (window_start, sensor_id)
            DO UPDATE SET cnt = EXCLUDED.cnt,
                          avg_value = EXCLUDED.avg_value,
                          min_value = EXCLUDED.min_value,
                          max_value = EXCLUDED.max_value;
        """, (w_start, w_end, sid, cnt, avg, mn, mx))
        window.pop((sid, minute), None)

for msg in consumer:
    evt = msg.value
    try:
        ts = parser.parse(evt["event_time"]).timestamp()
        sid = evt["sensor_id"]
        val = float(evt["value"])
        # --- raw_events speichern ---
        cur.execute("""
            INSERT INTO telemetry.raw_events (event_time, sensor_id, value, payload)
            VALUES (to_timestamp(%s), %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (ts, sid, val, json.dumps(evt)))
        # --- in Fenster sammeln ---
        minute_bucket = int(ts // 60) * 60
        window.setdefault((sid, minute_bucket), []).append(val)
    except Exception as e:
        print("?? Fehler:", e)

    # alle 10 Sekunden aggregieren
    if int(time.time()) % 10 == 0:
        flush_window()