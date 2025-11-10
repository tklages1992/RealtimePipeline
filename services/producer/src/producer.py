import os, json, hashlib
import pandas as pd
from kafka import KafkaProducer
from dateutil import parser

BROKERS = os.getenv("KAFKA_BROKERS", "redpanda:9092")
TOPIC   = os.getenv("TOPIC", "telemetry.v0")
CSV     = os.getenv("CSV_PATH", "/data/sample.csv")

def pseudonymize(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:16]

def main():
    print(f"📦 Starte Producer: {CSV} -> {TOPIC} @ {BROKERS}")
    df = pd.read_csv(CSV)

    producer = KafkaProducer(
        bootstrap_servers=BROKERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    expected_cols = {"Time_GMT", "Phone", "Rating"}
    if not expected_cols.issubset(df.columns):
        print("❗ CSV enthält nicht die erwarteten Spalten:", df.columns.tolist())
        return

    for _, row in df.iterrows():
        try:
            event = {
                "event_time": parser.parse(str(row["Time_GMT"])).isoformat(),
                "sensor_id": pseudonymize(str(row["Phone"])),
                "value": float(row["Rating"]),
                "meta": {"src": "csv", "ver": 1}
            }
            producer.send(TOPIC, event)
        except Exception as e:
            print("⚠️ Fehler bei Zeile:", e)
            continue

    producer.flush()
    print("✅ Alle Events erfolgreich gesendet.")

if __name__ == "__main__":
    main()
