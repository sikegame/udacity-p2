-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

CREATE TABLE IF NOT EXISTS
  players (id SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE IF NOT EXISTS
  tournaments (
    id INTEGER, player SERIAL REFERENCES players(id),
    wins INTEGER, matches INTEGER
  );

INSERT INTO players (name) VALUES ('Shinsuke Ikegame');
INSERT INTO players (name) VALUES ('Teppei Aoyama');