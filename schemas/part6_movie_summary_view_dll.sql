CREATE VIEW movie_summary AS
SELECT
    m.tmdb_id AS "TMDB Key",
    m.imdb_id AS "IMDB Key",
    m.title AS "Title",
    m.plot AS "Description/Plot",
    m.certificate AS "Content Rating",
    m.runtime AS "Runtime",
    (SELECT COUNT(*)
     FROM movie_keyword mk
     WHERE mk.movie_id = m.movie_id) AS "Number of Keywords"
FROM
    movie m;