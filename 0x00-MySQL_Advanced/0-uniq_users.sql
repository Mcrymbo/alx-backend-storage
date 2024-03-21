-- SQL script that creates a table called user --
CREATE TABLE IF NOT EXISTS users (
	id INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255));	
