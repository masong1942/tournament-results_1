#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    '''
	Return a database connection and a cursor.
	
    If the database does not exist, letting the exception
    go uncaught - the message it contains is usefull:
	   database "tournaments" does not exist"
	'''
    conn = psycopg2.connect("dbname = tournament") 
    return conn, conn.cursor()
	       


def deleteMatches():
    """Remove all the match records from the database."""
    conn,cur = connect()
    cur.execute('delete from matches')
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn,cur = connect()
    cur.execute('delete from players;')
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn,cur = connect()
    cur.execute('select count(*) from players;')
    result = cur.fetchall()
    conn.close()
    return result[0][0]


def registerPlayer(arg_name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    
    conn,cur = connect()
	#using a tuple trick to sanitize the string
    cur.execute( "insert into players(name) values(%s)", (arg_name,) )
    conn.commit()
    conn.close()

def listPlayers():
    conn,cur = connect()
    cur.execute("select * from players;")
    return cur.fetchall()
    conn.close()
	
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
	
    conn,cur = connect()
    query = '''
	 select players.id, players.name, 
            sum(case when players.id = matches.winner then 1 else 0 end) as wins,
	        sum(case when players.id = matches.winner or players.id = matches.loser then 1 else 0 end) as matches
      from players left join matches 
        on players.id = matches.winner or players.id = matches.loser
	  group by players.id
	  order by wins desc;
    '''
    cur.execute(query)
    results = cur.fetchall()
    conn.close()
    return results

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner: the id number of the player who won
       loser: the id number of the player who lost
    """
    conn,cur = connect()
    cmd = "insert into matches(winner, loser) values ({},{});".format(winner,loser)
    cur.execute(cmd)
    conn.commit()
    conn.close()
    
 
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
    conn,cur = connect()
    ranks = playerStandings()
    new_pairs_list = [(ranks[i][0],ranks[i][1],ranks[i+1][0],ranks[i+1][1])
       for i in xrange(0,len(ranks),2)]
       
    return new_pairs_list
	


