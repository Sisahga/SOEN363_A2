-- Find total number of movies with and without IMDB id in the database.
SELECT COUNT(CASE WHEN imdb_id IS NOT NULL THEN 1 END) AS has_imdb_id,
       COUNT(CASE WHEN imdb_id IS NULL THEN 1 END)     AS no_imdb_id
FROM movie;

-- Pick an actor. Find all movies by that actor that is released between 2000 and
-- 2020. List TMDB-id, IMDB-id, movie title, release date, and watchmode-id.
-- ACTOR: Tom Hardy
SELECT
    tmdb_id,
    imdb_id,
    title,
    release_year,
    watchmode_id
FROM movie
WHERE
    actors LIKE '%Tom_Hardy%'
    AND release_year BETWEEN '2000-01-01' AND '2020-12-31';

SELECT
    tmdb_id,
    imdb_id,
    title,
    release_year,
    rating
FROM movie
ORDER BY rating DESC
LIMIT 3;

-- Find number of movies that are in more than one language.
-- I couldn't access more than the original movie language, but I can write the query if they were separated by commas
SELECT COUNT(*)
FROM movie
WHERE array_length(string_to_array(languages, ','), 1) > 1;

-- For each language list how many movies are there in the database. Order by highest rank.
-- I only have one language per movie (as explained in question above), so here is my query for this. (I could only
-- get original language.
SELECT languages, COUNT(*) AS movie_count
FROM movie
GROUP BY languages
ORDER BY movie_count DESC;

-- Find top 2 comedies (higher ratings).
SELECT m.title, m.rating
FROM movie m
JOIN movie_genre mg ON m.movie_id = mg.movie_id
JOIN genre g ON mg.genre_id = g.genre_id
WHERE g.name = 'Comedy'
ORDER BY m.rating DESC
LIMIT 2;

-- Write a batch-update query that rounds up all the ratings.
UPDATE movie
SET rating = CEIL(rating);
