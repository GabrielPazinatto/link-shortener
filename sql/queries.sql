-- Select all urls belonging to an user
SELECT url, short_url FROM urls WHERE owner_id = $1;

-- Select the full url from the short url
SELECT url FROM urls WHERE short_url = $1;

-- Insert a new url
INSERT TABLE urls (owner_id, url, short_url) VALUES ($1, $2, $3);

-- Delete a url
DELETE FROM urls WHERE short_url = $1;

-- Create a new user
INSERT INTO users (username, password) VALUES ($1, $2);

-- Delete a user
DELETE FROM users WHERE users.id = $1;