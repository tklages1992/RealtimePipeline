CREATE SCHEMA IF NOT EXISTS telemetry;

-- Rohdaten (alle Original-Events)
CREATE TABLE IF NOT EXISTS telemetry.raw_events (
  event_time  TIMESTAMPTZ NOT NULL,
  sensor_id   TEXT NOT NULL,
  value       DOUBLE PRECISION NOT NULL,
  payload     JSONB,
  PRIMARY KEY (event_time, sensor_id)
);

-- 1-Minuten-Aggregationen
CREATE TABLE IF NOT EXISTS telemetry.agg_1min (
  window_start TIMESTAMPTZ NOT NULL,
  window_end   TIMESTAMPTZ NOT NULL,
  sensor_id    TEXT NOT NULL,
  cnt          BIGINT NOT NULL,
  avg_value    DOUBLE PRECISION NOT NULL,
  min_value    DOUBLE PRECISION NOT NULL,
  max_value    DOUBLE PRECISION NOT NULL,
  PRIMARY KEY (window_start, sensor_id)
);

-- Performance-Indizes
CREATE INDEX IF NOT EXISTS ix_raw_events_time ON telemetry.raw_events (event_time);
CREATE INDEX IF NOT EXISTS ix_agg_1min_sensor_time ON telemetry.agg_1min (sensor_id, window_start);
