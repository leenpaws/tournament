#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#



import psycopg2 #gives out list of tuples


class TournamentDB():
    def __init__(self):
        """Connect to the PostgreSQL database.  Returns a database connection."""
        self.Tdb = psycopg2.connect("dbname=tournament")
        self.c = self.Tdb.cursor()
        self.round = 0


    def result(self):
        '''Obtains result of running method'''
        self.result = self.c.fetchall()
        print self.result
        return self.result

    def closeDB(self):
        self.Tdb.commit()
        self.Tdb.close()

    def deleteMatches(self):
        """Remove all the match records from the database."""

        self.c.execute("delete  from round")



    def deletePlayers(self):
        """Remove all the player records from the database."""

        self.c.execute("delete  from Player")



    def countPlayers(self):
        """Returns the number of players currently registered."""
        self.c.execute("select count(id) from Player")
        result = self.c.fetchone()[0]
        print result
        return result

    def registerPlayer(self, name):

        """Adds a player to the tournament database.
        c.execute("INSERT INTO posts (content) VALUES (%s)", (content,))
         c.execute("update posts set content = 'cheese' where content like '%spam%'")
        The database assigns a unique serial id number for the player.  (This
         should be handled by your SQL database schema, not in your Python code.)

        Args:
      name: the player's full name (need not be unique).
    """
        self.c.execute("INSERT INTO Player (name) VALUES (%s)", (name,))
        self.Tdb.commit()
        self.c.execute("select * from player order by id asc")
        self.Tdb.commit()

        # self.c.execute("Insert Rounds into round Values (1))", ())

        #      self.c.execute("update Player")
        #     self.c.execute("update round")
        # result = self.c.fetchall()

        # return result

    def playerStandings(self):
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


        self.c.execute("select Win.pid, Win.pname, Win.Win, "
                       "((Win.Win) + (loss.loss)) as Matches "
                       "from Win join loss on Win.pid=Loss.pid "
                       "group by Win.pid, Win.pname, Win.Win, loss.loss "
                       "order by Win.Win desc")

        result = self.c.fetchall()
        print result
        return result





    def reportMatch(self, Winner, Loser):

        """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
        self.c.execute("INSERT INTO round(Winner, Loser) VALUES (%s, %s)", (Winner, Loser,))
        self.Tdb.commit()

    def validpair(self):
        self.c.execute("select winner, loser from round")

        result = self.c.fetchall()
        print result
        return result



    @property
    def swissPairings(self):

        # Returns a list of temp_pairs of players for the next round of a match.

        """Assuming that there are an even number of players registered, each player
        appears exactly once in the pairings.  Each player is paired with another
        player with an equal or nearly-equal win record, that is, a player adjacent
        to him or her in the standings.

        Returns:
          A list of tuples, each of which contains (id1, name1, id2, name2)
            id1: the first player's unique id
            name1: the first player's name
            id2: the second player's unique id
            name2: the second player's name"""
        self.round = self.round + 1
        testpair = self.validpair()
        possiblepair = []

        standings = self.playerStandings()

        self.output_pairs = []
        #look up race condition
        temp_pairs = []
        for j in range(0, len(testpair)):
            p1test=testpair[j]
            p1place=testpair[0]
            p2place=testpair[1]

            if p1place > p2place :
                possiblepair.append((p2place, p1place))
            else:
                possiblepair.append((p1place, p2place))


        while len(standings) > 0:
            player1 = standings.pop(0)
            player1_id = player1[0]
            player1_name = player1[1]
            for player in standings :

              


                for i in range(1, len(standings)):
                    player2_id = player2[0]
                    player2_name = player2[1]
                    #tuple=immutable object that can't be changed, pop takes something out
                    pairing_tuple = (player1_id, player1_name, player2_id, player2_name)

            self.output_pairs.append(pairing_tuple)
        return self.output_pairs

        def get_previous_pairings(self):
            """Retrieves a set of player pairings from previous matches.

            A pairing indicates that the players have already played each
            other.  Each player pairing is sorted by player id.

            Returns:
                A set of tuples where each tuple consists of two player
                ids (in in ascending order) indicating that the players
                have already played each other.
            """

            # get pairings from database
            query = '''
                SELECT
                    r.winner AS player1_id,
                    r.loser AS player2_id,
                FROM round AS r
            '''
            self.c.execute(query)
            results = self.c.fetchall()

            # sort each pairing by player id
            pairings = set()
            for pairing in results:
                pairings.add(sorted(pairing))

            return pairings

        @property
        def swissPairings(self):
            """Assuming that there are an even number of players registered, each player
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

            self.round += 1
            standings = self.playerStandings()
            previous_pairings = self.get_previous_pairings()
            next_match_pairings = []

            # loop until there are no unmatched players left
            while len(standings) > 0:

                # find a valid pairing for the next match
                player1 = standings.pop(0)
                for potential_player2 in standings:

                    # pair two players (that may or may not have played each other)
                    if player1[0] < potential_player2[0]:
                        possible_pairing = (player1[0], potential_player2[0])
                    else:
                        possible_pairing = (potential_player2[0], player1[0])

                    # if they haven't played each other, stop looking
                    if possible_pairing not in previous_pairings:
                        player2 = potential_player2
                        break

                # next match = player1 id, player1 name, player2 id, player2 name
                pairing = (player1[0], player1[1], player2[0], player2[1])
                next_match_pairings.append(pairing)

            return next_match_pairings









            #for statement using the player standings tuple and enumerating it
        #rank = the playerid so no need to create an extra field
        #using names because who cares if duplicates if you're just going through listtestpair = self.c.execute("select Winner, Loser from round")


        #
        # for row in standings:
        #
        #     # checks to see if there are only 2 players
        #     #if len(standings) % 2 == 0:
        #      #   self.output_pairs.append((standings[0], standings[1]))
        #       #  break
        #         #    temp_pairs.append(player[0])
        #         #    temp_pairs.append(player[1])
        #         #    output_pairs.append(tuple(temp_pairs))
        #         # here's where pairs are made
        #         # else:
        #
        #         # create list from matches table
        #
        #
        #         # test to see if the pair is valid by seeing if the pair exists in the matches database
        #
        #
        #
        #
        #         #   if(testpairs.count(tuple(temp_pairs)) == 0):
        #     #else:
        #        temp_pairs.append(standings[0])
        #        temp_pairs.append(standings[1])
        #        self.output_pairs.append({standings[0], standings[1]})
        #        temp_pairs = []
        #
        # print self.output_pairs
        # return self.output_pairs
        #



