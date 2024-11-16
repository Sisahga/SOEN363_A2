import json

import requests

def get_movies(tmdb_urls, header_args):
    responses = []
    for url in tmdb_urls:
        try:
            response = requests.get(url, headers=header_args)
            response.raise_for_status()
            responses += response.json().get("results")
        except requests.exceptions.RequestException as e:
            print(e)

    print("Movies Count: " + str(len(responses)))
    return responses

def get_movie_tmdb_details(tmdb_id, header_args):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
    try:
        response = requests.get(url, headers=header_args)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(e)

    return {}