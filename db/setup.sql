CREATE TABLE devices (
	id SERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	name TEXT NOT NULL
);

CREATE TABLE measurements (
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	device_id INTEGER REFERENCES devices (id),
	reading REAL NOT NULL
);

CREATE INDEX idx_measurements_device_created_at ON measurements (device_id, created_at);
