#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
	"""Connect to the PostgreSQL database.  Returns a database connection."""
	return psycopg2.connect("dbname=tournament")

def execute(has_commit, query, *params):
	"""Connects to the PostgreSQL database, executes the query
		and returns the rows, if any.
	"""
	db = connect()
	c = db.cursor()

	if params:
		c.execute(query, params)
	else:
		c.execute(query)

	rows = []
	if has_commit:
		db.commit()
	else:
		rows = c.fetchall()

	db.close()

	return rows

def deleteMatches():
	"""Remove all the match records from the database."""
	execute(True, "DELETE FROM match")

def deletePlayers():
	"""Remove all the player records from the database."""
	execute(True, "DELETE FROM player")


def countPlayers():
	"""Returns the number of players currently registered."""
	row = execute(False, "SELECT count(*) FROM player")
	return int(row[0][0])


def registerPlayer(name):
	"""Adds a player to the tournament database.

	The database assigns a unique serial id number for the player.  (This
	should be handled by your SQL database schema, not in your Python code.)

	Args:
	  name: the player's full name (need not be unique).
	"""
	parameter = (name,)
	execute(True, "INSERT INTO player (name) VALUES (%s)", parameter)

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
	return execute(False, "SELECT * FROM rank")

def reportMatch(winner, loser):
	"""Records the outcome of a single match between two players.

	Args:
	  winner:  the id number of the player who won
	  loser:  the id number of the player who lost
	"""
	execute(True, "INSERT INTO match (winner,loser) VALUES (%d,%d)" % (int(winner),int(loser)))

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
	rows = execute(False, "SELECT id, name FROM rank")
	pairs = []
	for i in xrange(len(rows)-1,0,-2):
		pairs.append((rows[i][0], rows[i][1], rows[i-1][0], rows[i-1][1]))

	return pairs