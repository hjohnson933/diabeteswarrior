-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS scan;
DROP TABLE IF EXISTS health;
DROP TABLE IF EXISTS meal;
DROP TABLE IF EXISTS food;
DROP TABLE IF EXISTS bgl;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE scan (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  msg INTEGER,
  glucose INTEGER,
  trend INTEGER,
  lower_limit INTEGER,
  upper_limit INTEGER,
  bolus_u INTEGER,
  bolus INTEGER,
  basal_u INTEGER,
  basal INTEGER,
  carbohydrate INTEGER,
  food INTEGER,
  notes text,
  exercises INTEGER,
  medication INTEGER,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE health (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  po_pulse INTEGER,
  po_ox INTEGER,
  wgt REAL,
  fat REAL,
  bp_pulse INTEGER,
  bp_systolic INTEGER,
  bp_diastolic INTEGER,
  bp_ihb INTEGER,
  bp_hypertension INTEGER,
  temperature REAL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE meal (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  calories INTEGER,
  fat INTEGER,
  cholesterol INTEGER,
  sodium INTEGER,
  carbohydrate INTEGER,
  protein INTEGER,
  servings TEXT,
  indices TEXT,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE food (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  domain TEXT,
  portion TEXT,
  title TEXT,
  unit TEXT,
  calories INTEGER,
  fat INTEGER,
  cholesterol INTEGER,
  sodium INTEGER,
  carbohydrate INTEGER,
  protein INTEGER,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE bgl (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  chart_min INTEGER,
  chart_max INTEGER,
  limit_min INTEGER,
  limit_max INTEGER,
  target_min INTEGER,
  target_max  INTEGER,
  my_min INTEGER,
  my_max INTEGER,
  meal_ideal INTEGER,
  meal_good INTEGER,
  meal_bad INTEGER,
  FOREIGN KEY (author_id) REFERENCES user (id)
);