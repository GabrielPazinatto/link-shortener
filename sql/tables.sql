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
  short_url TEXT NOT NULL,

  UNIQUE(short_url)
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

-- INSERT INTO urls (owner_id, url, short_url) VALUES (1, 'http://example.com/unique1', 'http://short.ly/abc123');
-- INSERT INTO urls (owner_id, url, short_url) VALUES (1, 'http://example.com/unique2', 'http://short.ly/def456');
-- INSERT INTO urls (owner_id, url, short_url) VALUES (1, 'http://example.com/unique3', 'http://short.ly/ghi789');
-- INSERT INTO urls (owner_id, url, short_url) VALUES (1, 'http://example.com/unique4', 'http://short.ly/jkl012');
-- INSERT INTO urls (owner_id, url, short_url) VALUES (1, 'http://example.com/unique5', 'http://short.ly/mno345');
-- INSERT INTO urls (owner_id, url, short_url) VALUES (1, 'http://example.com/unique6', 'http://short.ly/pqr678');
-- INSERT INTO urls (owner_id, url, short_url) VALUES (1, 'http://example.com/unique7', 'http://short.ly/stu901');
-- INSERT INTO urls (owner_id, url, short_url) VALUES (1, 'http://example.com/unique8', 'http://short.ly/vwx234');
-- INSERT INTO urls (owner_id, url, short_url) VALUES (1, 'http://example.com/unique9', 'http://short.ly/yz5678');
-- INSERT INTO urls (owner_id, url, short_url) VALUES (1, 'http://example.com/unique10', 'http://short.ly/abc901');