import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv("D:/Trustwise/docker/login.env") #enter the entire path if running this code on windows.

#postgres login data
conn = psycopg2.connect(
    host=os.getenv("HOST"),
    port=os.getenv("PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)


def create_table():
    create_query = """CREATE TABLE IF NOT EXISTS output (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    string TEXT,
    vectara REAL,
    toxicity REAL
    );"""
    cursor = conn.cursor()
    cursor.execute(create_query)
    conn.commit()
    cursor.close()

#DB input action
def insert_data(string, toxic_out, vectara_out):
    create_table()
    try:
        cursor = conn.cursor()    
        cursor.execute("INSERT INTO output(string, vectara, toxicity) VALUES (%s, %s, %s)", (string, vectara_out[0], toxic_out))
        conn.commit()
        cursor.close()
    except psycopg2.Error as err:
        return {"error" : f"Error occured while executing query : {err}"}

#DB table or graph call
def create_table_graph():
    create_table()
    try:
        df = pd.read_sql("SELECT string, vectara, toxicity FROM output ", conn)  
        json_data = df.to_dict(orient='records')
        return json_data
    except psycopg2.Error as err:
        return {"error" : f"Error occured while executing query : {err}"}
