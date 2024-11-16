CREATE TABLE IF NOT EXISTS genre (
    genre_id INTEGER UNIQUE NOT NULL PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS certificate (
    certification VARCHAR(5) UNIQUE NOT NULL PRIMARY KEY,
    meaning VARCHAR(1000),
    order_num INTEGER
);

CREATE TABLE IF NOT EXISTS keyword (
    keyword_id INTEGER UNIQUE NOT NULL PRIMARY KEY,
    name VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS movie (
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    plot VARCHAR(1500),
    certificate VARCHAR(5),
    rating NUMERIC(3, 1),
    actors VARCHAR(2000),
    directors VARCHAR(255),
    release_year DATE,
    runtime INTEGER,
    akas VARCHAR(255),
    countries VARCHAR(255),
    country_codes VARCHAR(30),
    languages VARCHAR(100),
    tmdb_id INTEGER UNIQUE,
    watchmode_id INTEGER UNIQUE,
    imdb_id VARCHAR(12) UNIQUE,
    FOREIGN KEY (certificate) REFERENCES certificate(certification)
);

CREATE TABLE IF NOT EXISTS movie_genre (
    movie_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS movie_keyword (
    movie_id INTEGER NOT NULL,
    keyword_id INTEGER NOT NULL,
    PRIMARY KEY (movie_id, keyword_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE ,
    FOREIGN KEY (keyword_id) REFERENCES keyword(keyword_id) ON DELETE CASCADE
)