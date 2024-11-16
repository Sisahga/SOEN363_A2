from movie_fetcher import *
# from populate import *
from connect_init import *
from populate import *

# TMDB headers
tmdb_headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3MzE5ZDc5MGEwMjkwNDFlOGZjMTgwNmIxNjYwNDBkNCIsIm5iZiI6MTczMTYxNTgyMC40NjI3NDE2LCJzdWIiOiI2NzM2NWFkNDE0M2U0MzlkYjRjNjcxMjAiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.9cfmhBiooj84EtsbB53wm0E_50v11WeoCSKZVDAjtnk"
}
# TMDB URLs
tmdb_urls = ["https://api.themoviedb.org/3/movie/popular?language=en-US&page=1",
             "https://api.themoviedb.org/3/movie/popular?language=en-US&page=2",
             "https://api.themoviedb.org/3/movie/popular?language=en-US&page=3"]
db_params = {
    'dbname': 'soen363_movies',
    'user': 'macmee',
    'host': 'localhost',
    'port': '5432'
}

# connect_and_initialize(db_params)
# init_genres()
# init_certificates()

movies = get_movies(tmdb_urls, tmdb_headers)
insert_movies_tmdb(movies)