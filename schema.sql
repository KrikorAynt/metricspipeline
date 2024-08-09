CREATE EXTENSION IF NOT EXISTS "uuid-ossp";  -- Enable the extension for UUID generation

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE sessions (
    session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    device TEXT,
    app_version TEXT
);

CREATE TABLE metrics (
    metric_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES sessions(session_id),
    timestamp TIMESTAMP NOT NULL,
    metric_type VARCHAR(50) NOT NULL,
    value FLOAT NOT NULL
);

-- Indexes for performance
CREATE INDEX idx_timestamp ON metrics (timestamp);
CREATE INDEX idx_session_metric ON metrics (session_id, metric_type);
