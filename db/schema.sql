-- Script to create the database schema.

DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS shipments;
DROP TABLE IF EXISTS inventory;

CREATE TABLE items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  description TEXT,
  price REAL
);

CREATE TABLE shipments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_id INTEGER,
  quantity INTEGER,
  time_created TEXT,
  FOREIGN KEY(item_id) REFERENCES items(id)
);

CREATE TABLE inventory (
  item_id INTEGER,
  quantity INTEGER,
  FOREIGN KEY(item_id) REFERENCES items(id)
);