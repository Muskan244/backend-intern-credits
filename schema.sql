-- Users & Credits

CREATE TABLE IF NOT EXISTS users (
  user_id     SERIAL PRIMARY KEY,
  email       TEXT NOT NULL UNIQUE,
  name        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS credits (
  user_id      INTEGER PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
  credits      INTEGER NOT NULL DEFAULT 0 CHECK (credits >= 0),
  last_updated TIMESTAMPTZ NOT NULL DEFAULT NOW()
);