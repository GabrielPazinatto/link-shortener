--drop table if exists urls;
--drop table if exists users;

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(20) NOT NULL,
  password TEXT NOT NULL,

  UNIQUE(username)
);

CREATE TABLE IF NOT EXISTS urls (
  id INTEGER  PRIMARY KEY AUTOINCREMENT,
  owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  url TEXT NOT NULL,
  short_url TEXT NOT NULL
);

-- INSERT INTO users (username, password) VALUES ('user1', 'password1');
-- INSERT INTO users (username, password) VALUES ('user2', 'password2');
-- INSERT INTO users (username, password) VALUES ('user3', 'password3');
-- INSERT INTO users (username, password) VALUES ('user4', 'password4');
-- INSERT INTO users (username, password) VALUES ('user5', 'password5');
-- INSERT INTO users (username, password) VALUES ('user6', 'password6');
-- INSERT INTO users (username, password) VALUES ('user7', 'password7');
-- INSERT INTO users (username, password) VALUES ('user8', 'password8');
-- INSERT INTO users (username, password) VALUES ('user9', 'password9');
-- INSERT INTO users (username, password) VALUES ('user10', 'password10');