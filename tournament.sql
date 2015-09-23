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
  players (
    p_id SERIAL PRIMARY KEY,
    p_name TEXT
  );

CREATE TABLE IF NOT EXISTS
  tournaments (
    player INTEGER REFERENCES players(p_id),
    opponent INTEGER REFERENCES players(p_id),
    winner BOOLEAN
  );

CREATE VIEW ranking AS
  SELECT
    p_id as player_id,
    p_name as player_name,
    COUNT (CASE WHEN winner THEN 1 ELSE NULL END) as wins,
    COUNT (player) as matches
  FROM players LEFT JOIN tournaments ON p_id = player
  GROUP BY p_id, p_name
  ORDER BY wins DESC;