CREATE TABLE comments (
	id SERIAL PRIMARY KEY, 
	userid INTEGER,
	threadid INTEGER,
	time TIMESTAMP,
	content TEXT,
	username TEXT
);

CREATE TABLE users (
	id SERIAL PRIMARY KEY, 
	username TEXT,
	password TEXT,
	admin INTEGER
);

CREATE TABLE follows (
	id SERIAL PRIMARY KEY, 
	userid INTEGER,
	threadid INTEGER
);

CREATE TABLE messages (
	id SERIAL PRIMARY KEY, 
	content TEXT
);

CREATE TABLE subjectarea (
	id SERIAL PRIMARY KEY, 
	subjectarea TEXT,
	shortname TEXT
);

CREATE TABLE threads (
	id SERIAL PRIMARY KEY, 
	userid INTEGER,
	subjectarea INTEGER,
	title TEXT,
	content TEXT
);

CREATE TABLE follows (
	id SERIAL PRIMARY KEY,
	userid INTEGER,
	threadid INTEGER
