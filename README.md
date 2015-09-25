<h1>Swiss Tournament Pair Matching</h1>

## Synopsis

This Python module provides the swiss tournament pair matching solutions to your application. Simply import this module, and you are good to go!

## Requirements

- Python 2.7 or newer
- Your own Python application

## Installation

1. Install the Python 2.7 or newer
2. Import tournament.py in your Python app.
3. For the usage, please refer to the API reference below.

## API Reference

`tournament.deleteMatches()`

Remove all the match records from the database.

`tournament.deletePlayers()`

Remove all the players records from the database.

`tornament.registerPlayer(name)`

Adds a player to the tournament database.
  
- name: the player's full name (need not be unique).

`tournament.playerStandings()`

Returns a list of the players and their win records, sorted by wins.

`tournament.reportMatch(winner, loser, [draw])`

Records the outcome of a sigle match between two players.

- winner:  the id number of the player who won
- loser:  the id number of the player who lost
- draw (Optional): if the game result was draw, set True

`tournament.swissPairings()`

Returns a list of pairs of players for the next round of a match.

## Contacts

Please send any bug reports or feedbacks to

Email: no_junk_email@gmail.com
