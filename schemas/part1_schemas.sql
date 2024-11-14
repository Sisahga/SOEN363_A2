CREATE TABLE genre (
    genre_id INTEGER UNIQUE NOT NULL PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE certificate (
    certification VARCHAR(5) UNIQUE NOT NULL PRIMARY KEY,
    meaning VARCHAR(100),
    order_num INTEGER
);

CREATE TABLE keyword (
    keyword_id INTEGER UNIQUE NOT NULL PRIMARY KEY,
    name VARCHAR(20)
);

CREATE TABLE movie (
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    plot VARCHAR(512),
    certificate VARCHAR(5),
    rating NUMERIC(3, 1),
    actors VARCHAR(512),
    directors VARCHAR(255),
    release_year DATE,
    akas VARCHAR(255),
    country VARCHAR(50),
    country_code VARCHAR(3),
    languages VARCHAR(100),
    tmdb_id INTEGER UNIQUE,
    watchmode_id INTEGER UNIQUE,
    imdb_id VARCHAR(12) UNIQUE,
    FOREIGN KEY (certificate) REFERENCES certificate(certification)
);

CREATE TABLE movie_genre (
    movie_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id) ON DELETE CASCADE
);

CREATE TABLE movie_certificate (
    movie_id INTEGER NOT NULL,
    certification VARCHAR(5) NOT NULL,
    PRIMARY KEY (movie_id, certification),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (certification) REFERENCES certificate(certification) ON DELETE CASCADE
);

CREATE TABLE movie_keyword (
    movie_id INTEGER NOT NULL,
    keyword_id INTEGER NOT NULL,
    PRIMARY KEY (movie_id, keyword_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
    FOREIGN KEY (keyword_id) REFERENCES keyword(keyword_id)
)