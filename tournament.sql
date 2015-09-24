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
    id SERIAL PRIMARY KEY,
    name TEXT
  );

CREATE TABLE IF NOT EXISTS
  tournaments (
    player INTEGER REFERENCES players(id),
    opponent INTEGER REFERENCES players(id),
    winner BOOLEAN,
    CONSTRAINT no_rematch UNIQUE (player, opponent)
  );

CREATE VIEW player_ranking AS
  SELECT
    id,
    name,
    COUNT (CASE WHEN winner THEN 1 ELSE NULL END ) as wins,
    COUNT (player) as matches
  FROM players LEFT JOIN tournaments ON id = player
  GROUP BY id, name
  ORDER BY wins DESC;

CREATE VIEW bye_player AS
  SELECT
    player
  FROM (
    SELECT
      player,
      COUNT (CASE WHEN opponent IS NULL THEN 1 ELSE NULL END ) AS bye
    FROM tournaments GROUP BY player
  ) a
  WHERE bye = 0 LIMIT 1;