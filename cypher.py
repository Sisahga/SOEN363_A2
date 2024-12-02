from neo4j import GraphDatabase

class Neo4jHandler:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            return session.run(query, parameters).data()

# Connect to Neo4j
neo4j_handler = Neo4jHandler("neo4j+s://7ab1886e.databases.neo4j.io", "neo4j", "RB8ZDGNHXSKIfRidbf9y-UaVZzxegeINXZb-f0-LsQQ")

# Queries
queries = {
    "A": """
        MATCH (m:Movie)
        WHERE $actorName IN split(m.actors, ",")
        RETURN m.title, m.release_year
    """,
    "B": """
        MATCH (m:Movie)
        RETURN 
            count(m.watchmode_id) AS MoviesWithWatchMode,
            count(m) - count(m.watchmode_id) AS MoviesWithoutWatchMode""",
    "C": """
        MATCH (m:Movie)
        WHERE toInteger(substring(m.release_year, 0, 4)) > $year AND m.rating >= $rating
        RETURN m.title, m.rating, substring(m.release_year, 0, 4) AS release_year;
    """,
    "D": """
        MATCH (m:Movie)
        WHERE any(c IN $countries WHERE c IN SPLIT(m.countries, ","))
        RETURN m.title, m.countries
    """,
    "E": """
        MATCH (m:Movie)-[:HAS_KEYWORD]->(k:Keyword)
        RETURN m.title, count(k) AS KeywordCount
        ORDER BY KeywordCount DESC
        LIMIT 2
    """,
    "F": """
        MATCH (m:Movie)
        WHERE $language IN m.languages
        RETURN m.title, m.rating
        ORDER BY m.rating DESC
        LIMIT 5
    """,
    "G": """
        CREATE FULLTEXT INDEX moviePlots FOR (n:Movie) ON EACH [n.plot];
    """,
    "H": """
        CALL db.index.fulltext.queryNodes("moviePlots", "storm")
        YIELD node, score
        RETURN node.title AS title, node.plot AS plot, score
        ORDER BY score DESC;
    """
}

# Execute Queries
def execute_query(label, parameters=None):
    print(f"Running query {label}:")
    result = neo4j_handler.run_query(queries[label], parameters)
    for record in result:
        print(record)
    print("\n")

# Sample Parameters
parameters = {
    "A": {"actorName": "Ryan Reynolds"},
    "C": {"year": 2023, "rating": 5.0},
    "D": {"countries": ["USA", "Canada"]},
    "F": {"language": "en"},
    "H": {"searchText": "dreams"}
}

# Run Queries
execute_query("A", parameters["A"])
execute_query("B")
execute_query("C", parameters["C"])
execute_query("D", parameters["D"])
execute_query("E")
execute_query("F", parameters["F"])
# execute_query("G") # Uncomment to create fulltext index on plot - only run once
execute_query("H", parameters["H"])

# Close Connection
neo4j_handler.close()