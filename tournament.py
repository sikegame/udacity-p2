#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from contextlib import contextmanager


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


@contextmanager
def get_cursor():
    """Decorates frequently used database cursor code."""
    db = connect()
    c = db.cursor()
    try:
        yield c
    except:
        raise
    else:
        db.commit()
    finally:
        db.close()


def deleteMatches():
    """Remove all the match records from the database."""
    with get_cursor() as c:
        c.execute('DELETE FROM tournaments')


def deletePlayers():
    """Remove all the player records from the database."""
    with get_cursor() as c:
        c.execute('DELETE FROM players')


def countPlayers():
    """Returns the number of players currently registered."""
    with get_cursor() as c:
        c.execute('SELECT COUNT (*) FROM players')
        result = c.fetchone()[0]
    return result


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    with get_cursor() as c:
        c.execute('INSERT INTO players (name) VALUES (%s)',
                  (name, ))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    with get_cursor() as c:
        c.execute('SELECT id, name, wins, matches FROM player_ranking')
        result = c.fetchall()
    return result


def reportMatch(winner, loser, draw=False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      draw (Optional): if the game result was draw, set True
    """
    with get_cursor() as c:
        c.execute('INSERT INTO tournaments VALUES '
                  '(%s, %s, %s), '
                  '(%s, %s, %s)',
                  (winner, loser, not draw,  # Insert the winner info
                   loser, winner, False, ))  # Insert the loser into


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    This modified version of code takes both an even and odd number of players and each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    with get_cursor() as c:
        if countPlayers() % 2 == 0:
            # Get player_id and player_name list sorted by wins
            c.execute('SELECT id, name FROM player_ranking')
        else:
            # Set a bye player if countPlayers() returns odd number
            # and remove the bye player from pair matching selection
            c.execute('SELECT id, name FROM player_ranking'
                      'WHERE id != %s', (setByePlayer(), ))
        result = c.fetchall()
    return matchingPairs(result)


def matchingPairs(players):
    """ Takes a list of available players sorted by wins and
    returns a list of paired players.
    """
    pairs = []
    temp = ()
    # Match pairs from top to bottom
    for p in players:
        temp += (p[0], p[1])
        if len(temp) == 4:
            pairs.append(temp)  # Append to pairs array
            temp = ()  # Reset temp tuple
    return pairs


def setByePlayer():
    """ Sets a bye player and returns the current bye player id."""
    with get_cursor() as c:
        c.execute('INSERT INTO tournaments (player, winner) '
                  'VALUES ((SELECT * FROM bye_player), TRUE ) '
                  'RETURNING player')
        result = c.fetchone()[0]
    return result
