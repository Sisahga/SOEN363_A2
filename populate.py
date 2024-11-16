import json
from urllib.error import HTTPError

import requests, psycopg2
from connect_init import *

# TODO: Get keywords from TMDB
db_params = {
    'dbname': 'soen363_movies',
    'user': 'macmee',
    'host': 'localhost',
    'port': '5432'
}
# TMDB headers
tmdb_headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3MzE5ZDc5MGEwMjkwNDFlOGZjMTgwNmIxNjYwNDBkNCIsIm5iZiI6MTczMTYxNTgyMC40NjI3NDE2LCJzdWIiOiI2NzM2NWFkNDE0M2U0MzlkYjRjNjcxMjAiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.9cfmhBiooj84EtsbB53wm0E_50v11WeoCSKZVDAjtnk"
}
watchmode_api_key = "Ll3YP4slW4ReSiV3UEw3NzUSdmJquAcwhcQt4wxm"


# === PART 5 ===
# Inserts list of movies into 'movie'
def insert_movies_tmdb(movies: list[dict[str, str]]):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # === GATHERING DATA
    for movie in movies:
        print("Current movie: " + json.dumps(movie, indent=4))
        tmdb_id = movie['id']
        title = movie['title']
        genres = movie['genre_ids']
        plot = movie['overview']
        rating = movie['vote_average']
        release_year = movie['release_date']
        # Prepare countries
        # countries_arr = movie['production_countries']
        # countries = ""  # Use to insert in DB
        # country_codes = ""
        # count = 0
        # for country in countries_arr:
        #     if count != len(countries_arr) - 1:
        #         countries += country['name'] + ","
        #         country_codes += country['iso_3166_1'] + ","
        #     else:
        #         countries += country['name']
        #         country_codes += country['iso_3166_1']
        #     count += 1

        # languages_arr = movie['spoken_languages']
        # languages = ""
        # count = 0
        # for language in languages_arr:
        #     if count != len(languages_arr) - 1:
        #         languages += language['name'] + ","
        #     else:
        #         languages += language['name']
        #     count += 1
        language = movie['original_language']

        # Get other details from tmdb and watchmode
        # Watchmode request
        w_url = f"https://api.watchmode.com/v1/title/movie-{tmdb_id}/details/?apiKey={watchmode_api_key}"
        w_response = requests.get(w_url)
        w_json = w_response.json()
        print(json.dumps(w_json, indent=4))
        if w_response.status_code == 400:
            watchmode_id = None
            certification = None
            imdb_id = None
            runtime = None

        else:
            watchmode_id = w_json['id']
            certification = w_json['us_rating']
            imdb_id = w_json['imdb_id']
            runtime = w_json['runtime_minutes']

        # TMDB Credits
        tmdb_credits_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/credits?language=en-US"
        credits_res = requests.get(tmdb_credits_url, headers=tmdb_headers)
        actors_json = credits_res.json().get('cast')
        crew_json = credits_res.json().get('crew')

        # Handle actors
        actors = ""
        count = 0
        for actor in actors_json:
            if count != len(actors_json) - 1:
                actors += actor['name'] + ","
            else:
                actors += actor['name']
        # Handle directors
        directors = ""
        for crew_member in crew_json:
            if crew_member['job'] != 'Director':
                continue
            else:
                if count != len(crew_json) - 1:
                    directors += crew_member['name'] + ","
                else:
                    directors += crew_member['name']

        # TMDB keywords
        tmdb_keywords_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/keywords"
        keywords_res = requests.get(tmdb_keywords_url, headers=tmdb_headers)
        keywords = keywords_res.json().get('keywords')
        # === END OF GATHERING DATA ===

        # === INSERTIONS ===

        # INSERT MAIN MOVIE DATA
        cur.execute("""
        INSERT INTO movie (title, plot, certificate, rating, actors, directors, release_year, runtime, languages, tmdb_id, watchmode_id, imdb_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING movie_id
        """, (
            title, plot, certification, rating, actors, directors, release_year, runtime, language,
            tmdb_id, watchmode_id, imdb_id
        ))
        this_movie_id = cur.fetchone()[0]
        print("Commited " + str(this_movie_id))

        # INSERT GENRE
        for genre_id in genres:
            cur.execute("""
            INSERT INTO movie_genre (movie_id, genre_id)
            VALUES (%s, %s)""", (
                this_movie_id, genre_id
            ))

        # INSERT KEYWORDS
        for keyword in keywords:
            cur.execute("SELECT COUNT(*) FROM keyword WHERE keyword_id = %s", (keyword['id'],))
            exists = cur.fetchone()[0] > 0

            if not exists:
                cur.execute("""
                INSERT INTO keyword (keyword_id, name)
                VALUES (%s, %s)""", (
                    keyword['id'], keyword['name']
                ))

            cur.execute("""
                        INSERT INTO movie_keyword (movie_id, keyword_id)
                        VALUES(%s, %s)""", (
                this_movie_id, keyword['id']
            ))
    # === END OF INSERTIONS ===

    # Commit all transactions
    conn.commit()

    cur.close()
    conn.close()

# Initializes genres in the DB
def init_genres():
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    url = "https://api.themoviedb.org/3/genre/movie/list"
    response = requests.get(url, headers=tmdb_headers)
    genres = response.json().get('genres')

    for genre in genres:
        genre_id = genre['id']
        name = genre['name']

        cur.execute("""
        INSERT INTO genre (genre_id, name)
        VALUES (%s, %s)
        """, (
            genre_id, name
        ))
    conn.commit()
    cur.close()
    conn.close()

    print("Successfully initialized the genres table")

# Initializes certifications in the DB
def init_certificates():
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    url = "https://api.themoviedb.org/3/certification/movie/list"
    response = requests.get(url, headers=tmdb_headers)
    us_certificates = response.json().get('certifications')['US']
    for certificate in us_certificates:
        certification = certificate['certification']
        meaning = certificate['meaning']

        cur.execute("""
        INSERT INTO certificate (certification, meaning)
        VALUES (%s, %s)""", (
            certification, meaning
        ))

    conn.commit()
    cur.close()
    conn.close()

    print("Successfully initialized the certificates table")
