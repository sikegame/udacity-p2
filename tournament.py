#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

# Set default match identification
DEFAULT_TOURNAMENT_ID = 0

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches(t_id=None):
    """Remove all the match records from the database."""
    # Initialize tournament id
    if(t_id):
        tournament_id = t_id
    else:
        tournament_id = DEFAULT_TOURNAMENT_ID
    # Delete the selected match data
    db = connect()
    c = db.cursor()
    c.execute('DELETE FROM tournaments WHERE id = %s',
              (tournament_id,))
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute('DELETE FROM players')
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute('SELECT COUNT(*) FROM players')
    result = c.fetchone()[0]
    db.close()
    return result


def registerPlayer(name, t_id=None):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    db = connect()
    c = db.cursor()
    # Insert name into the player table and get the player id
    c.execute('INSERT INTO players (name) VALUES (%s) RETURNING id',
              (name,))
    # Initialize the tournament table with the player id
    c.execute('INSERT INTO tournaments VALUES (%s, %s, 0, 0)',
              (DEFAULT_TOURNAMENT_ID, c.fetchone()[0],))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute('SELECT player_id, player_name, wins, matches FROM ranking')
    result = c.fetchall()
    db.close()
    return result

def reportMatch(winner, loser, draw=False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute('UPDATE tournaments SET wins = '
              '(SELECT wins FROM tournaments WHERE player = %s) + 1, '
              'matches = '
              '(SELECT matches FROM tournaments WHERE player = %s) + 1 '
              'WHERE player = %s;'
              'UPDATE tournaments SET matches = '
              '(SELECT matches FROM tournaments WHERE player = %s) + 1 '
              'WHERE  player = %s;',
              (winner, winner, winner, loser, loser, ))
    db.commit()
    db.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
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

    pairs = []
    temp_pair = ()

    db = connect()
    c = db.cursor()
    # Get player_id and player_name list sorted by wins
    c.execute('SELECT player_id, player_name FROM ranking')
    result = c.fetchall()
    db.close()

    # Match pairs from top to bottom
    for i in result:
        temp_pair += (i[0], i[1])
        if len(temp_pair) == 4:
            pairs.append(temp_pair)  # Append to pairs array
            temp_pair = ()  # Reset temp_pair tuple
    return pairs
