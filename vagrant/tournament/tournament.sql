DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament

CREATE TABLE player  (
    id serial PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE match  (
    id serial PRIMARY KEY,
    loser INT REFERENCES player(id) ON DELETE CASCADE,
    winner INT REFERENCES player(id) ON DELETE CASCADE,
    CHECK (loser <> winner)
);

CREATE VIEW rank as
	SELECT total_wins.wins_player_id as id, total_wins.name, total_wins.wins, total_matchs.matches FROM
	(SELECT player.id as wins_player_id, player.name, count(match.winner) as wins
	FROM player LEFT JOIN match
    ON player.id = match.winner
  	GROUP BY player.id) total_wins
	LEFT JOIN
  	(SELECT player.id as matchs_player_id, count(match.id) as matches
	FROM player LEFT JOIN match
    ON player.id = match.winner OR player.id = match.loser
  	GROUP BY player.id) total_matchs
  	ON total_wins.wins_player_id = total_matchs.matchs_player_id
  	ORDER BY wins DESC;