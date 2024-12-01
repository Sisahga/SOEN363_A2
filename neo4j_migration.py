import psycopg2
import py2neo
from py2neo import Graph, Node, Relationship
import pandas as pd

# Postgresql
pg_params = {
    'dbname': 'soen363_movies',
    'user': 'macmee',
    'host': 'localhost',
    'port': '5432'
}

# Neo4j
NEO4J_URI = "neo4j+s://7ab1886e.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "RB8ZDGNHXSKIfRidbf9y-UaVZzxegeINXZb-f0-LsQQ"

def connect_to_postgres():
    try:
        conn = psycopg2.connect(**pg_params)
        print("Connected to PostgreSQL")
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        raise

def connect_to_neo4j():
    try:
        neo_graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        print("Connected to Neo4J")
        return neo_graph
    except Exception as e:
        print(f"Error connecting to Neo4j: {e}")
        raise

def clear_neo4j_database(graph):
    graph.delete_all()


def import_certificates(conn, graph):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM certificate")
    certificates = cursor.fetchall()

    for cert in certificates:
        certificate_node = Node("Certificate",
                                certification=cert[0],
                                meaning=cert[1],
                                order_num=cert[2])
        graph.create(certificate_node)

    cursor.close()
    print(f"Imported {len(certificates)} certificates")


def import_genres(conn, graph):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM genre")
    genres = cursor.fetchall()

    for genre in genres:
        genre_node = Node("Genre",
                          genre_id=genre[0],
                          name=genre[1])
        graph.create(genre_node)

    cursor.close()
    print(f"Imported {len(genres)} genres")


def import_keywords(conn, graph):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM keyword")
    keywords = cursor.fetchall()

    for keyword in keywords:
        keyword_node = Node("Keyword",
                            keyword_id=keyword[0],
                            name=keyword[1])
        graph.create(keyword_node)

    cursor.close()
    print(f"Imported {len(keywords)} keywords")


def import_movies(conn, graph):
    cursor = conn.cursor()

    # Fetch all movies
    cursor.execute("SELECT * FROM movie")
    movies = cursor.fetchall()

    # Columns based on your schema
    columns = [
        'movie_id', 'title', 'plot', 'certificate', 'rating', 'actors',
        'directors', 'release_year', 'runtime', 'akas', 'countries',
        'country_codes', 'languages', 'tmdb_id', 'watchmode_id', 'imdb_id'
    ]

    for movie in movies:
        # Create movie node
        movie_dict = dict(zip(columns, movie))
        movie_node = Node("Movie",
                          movie_id=movie_dict['movie_id'],
                          title=movie_dict['title'],
                          plot=movie_dict['plot'],
                          rating=float(movie_dict['rating']) if movie_dict['rating'] is not None else None,
                          actors=movie_dict['actors'],
                          directors=movie_dict['directors'],
                          release_year=str(movie_dict['release_year']) if movie_dict['release_year'] else None,
                          runtime=movie_dict['runtime'],
                          akas=movie_dict['akas'],
                          countries=movie_dict['countries'],
                          country_codes=movie_dict['country_codes'],
                          languages=movie_dict['languages'],
                          tmdb_id=movie_dict['tmdb_id'],
                          watchmode_id=movie_dict['watchmode_id'],
                          imdb_id=movie_dict['imdb_id'])
        graph.create(movie_node)

        # Create relationship with Certificate
        if movie_dict['certificate']:
            cursor.execute(
                "SELECT * FROM certificate WHERE certification = %s",
                (movie_dict['certificate'],)
            )
            certificate = cursor.fetchone()
            if certificate:
                certificate_node = graph.nodes.match("Certificate", certification=certificate[0]).first()
                if certificate_node:
                    graph.create(Relationship(movie_node, "HAS_CERTIFICATE", certificate_node))

    cursor.close()
    print(f"Imported {len(movies)} movies")


def import_movie_genres(conn, graph):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movie_genre")
    movie_genres = cursor.fetchall()

    for movie_genre in movie_genres:
        movie_id, genre_id = movie_genre

        movie_node = graph.nodes.match("Movie", movie_id=movie_id).first()
        genre_node = graph.nodes.match("Genre", genre_id=genre_id).first()

        if movie_node and genre_node:
            graph.create(Relationship(movie_node, "HAS_GENRE", genre_node))

    cursor.close()
    print(f"Created {len(movie_genres)} movie-genre relationships")


def import_movie_keywords(conn, graph):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movie_keyword")
    movie_keywords = cursor.fetchall()

    for movie_keyword in movie_keywords:
        movie_id, keyword_id = movie_keyword

        movie_node = graph.nodes.match("Movie", movie_id=movie_id).first()
        keyword_node = graph.nodes.match("Keyword", keyword_id=keyword_id).first()

        if movie_node and keyword_node:
            graph.create(Relationship(movie_node, "HAS_KEYWORD", keyword_node))

    cursor.close()
    print(f"Created {len(movie_keywords)} movie-keyword relationships")


pg_conn = connect_to_postgres()
graph = connect_to_neo4j()

try:
    clear_neo4j_database(graph)

    import_certificates(pg_conn, graph)
    import_genres(pg_conn, graph)
    import_keywords(pg_conn, graph)
    import_movies(pg_conn, graph)

    import_movie_genres(pg_conn, graph)
    import_movie_keywords(pg_conn, graph)

    print("Migration completed successfully!")

except Exception as e:
    print(f"Migration failed: {e}")

finally:
    pg_conn.close()