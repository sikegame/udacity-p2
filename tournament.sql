-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE IF NOT EXISTS
  players (id SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE IF NOT EXISTS
  tournaments (
    id INTEGER, player SERIAL REFERENCES players(id),
    wins INTEGER, matches INTEGER, bye BOOLEAN
  );

CREATE VIEW ranking AS
  SELECT a.id as player_id, name as player_name, wins, matches, bye
  FROM players a LEFT JOIN tournaments b ON a.id = player
  ORDER BY wins DESC;