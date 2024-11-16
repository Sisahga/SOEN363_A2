import psycopg2, os

def connect_and_initialize(dbparams):
    working_dir = os.getcwd()
    sql_file_path = os.path.join(working_dir, 'schemas', 'part1_schemas.sql')

    try:
        conn = psycopg2.connect(**dbparams)
        print("Connection successful")

        cur = conn.cursor()
        # Reads sql init file to initialize the DB.
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()
            try:
                cur.execute(sql_script)
                conn.commit()
                print("Database initialized successfully!")
            except Exception as e:
                print(f"Error executing SQL script: {e}")
                conn.rollback()  # Rollback in case of error

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error connecting to the database: {e}")