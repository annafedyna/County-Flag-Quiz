from pg8000 import Connection
import csv 
import os 
from dotenv import load_dotenv

load_dotenv()

def connect_to_db():
    try:
        conn = Connection(
            host=os.environ.get("DB_HOST_DW"),
            port=os.environ.get("DB_PORT_DW"),
            database=os.environ.get("DB_DW"),
            user=os.environ.get("DB_USER_DW"),
            password=os.environ.get("DB_PASSWORD_DW"),
        )
        return conn
    except Exception as e:
        raise e
    
def insert_capitals(conn):
    try:
        cur = conn.cursor()
        with open("data/capitals.csv", 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)  
            header = next(reader, None) 
            if header != ["id", "country", "capital"]:
                print("Warning: CSV header does not match expected format.")
                return

            for row in reader:
                if len(row) == 3:
                    try:
                        id_val = int(row[0].strip())
                        country_val = row[1].strip()
                        capital_val = row[2].strip()

                        query = "INSERT INTO capitals (id, country, capital) VALUES (%s, %s, %s)"
                        cur.execute(query, (id_val, country_val.replace("'", "''"), capital_val.replace("'", "''")))
                    except ValueError:
                        print(f"Warning: Skipping row due to invalid data: {row}")
                    except Exception as e:
                        print(f"Error inserting row {row}: {e}")
                        conn.rollback() 
                        continue 
            conn.commit()
        cur.close()
    except Exception as e:
        raise e
    
def insert_flags(conn):
    try:
        cur = conn.cursor()
        with open('data/flags.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            header = next(reader, None) 
            if header != ["id", "name", "flag"]:
                print("Warning: CSV header does not match expected format.")
                return
            for row in reader:
                if len(row) == 3:
                    try:
                        id_val = int(row[0].strip())
                        name_val = row[1].strip()
                        flag_val = row[2].strip()

                        query = f"INSERT INTO flags (id,name,flag) VALUES ({id_val}, '{name_val}', '{flag_val}')"
                        cur.execute(query)
                    except ValueError:
                        print(f"Warning: Skipping row due to invalid data: {row}")
                    except Exception as e:
                        print(f"Error inserting row {row}: {e}")
                        conn.rollback() 
                        continue 
            conn.commit()
        cur.close()
    except Exception as e:
        raise e
    
conn = connect_to_db()
insert_capitals(conn)
insert_flags(conn)