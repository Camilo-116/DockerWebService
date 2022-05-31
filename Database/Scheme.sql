DROP DATABASE IF EXISTS asistenciaEC;

CREATE DATABASE If NOT EXISTS asistenciaEC;
USE asistenciaEC;

CREATE TABLE S_table (
	hash_ VARCHAR(50) NOT NULL,
	id INTEGER NOT NULL,
	timeS DATE NOT NULL,
	-- Primary Key
	PRIMARY KEY (hash_, id),
	-- Unique key
	UNIQUE(hash_)
);

CREATE TABLE A_table (
	id INTEGER NOT NULL,
	hash_ VARCHAR(50) NOT NULL,
	timeS DATE NOT NULL,
	response VARCHAR(10) NOT NULL,
	-- Primary Key
	PRIMARY KEY (id, hash_),
	-- Unique key
	UNIQUE(hash_)
);