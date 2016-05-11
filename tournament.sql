-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.


DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament
    CREATE table player ( name TEXT NOT NULL,
                          id SERIAL primary key
                        );


    CREATE table round  (   rid SERIAL primary key,
                            Winner integer references Player(id) ON DELETE CASCADE,
                            Loser integer REFERENCES Player(id) ON DELETE CASCADE,
                            Rounds integer
                         );

    CREATE VIEW Win AS
    SELECT player.id AS pid,  player.name AS pname, COUNT(round.winner) AS Win
    FROM Player LEFT JOIN round
    ON Player.id = round.winner
    GROUP BY Player.id, player.name;


    CREATE VIEW loss AS
    SELECT Player.id AS pid, player.name as pname, COUNT(round.loser) AS loss
    FROM Player LEFT JOIN round
    ON Player.id = round.loser
    GROUP BY player.id, player.name;

    create view matches as
    select rid, Player.name as winnername, Player.name as losername
    from round join Player
    on round.Winner=Player.id or Player.id = round.loser
    group by rid, player.name

