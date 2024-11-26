import psycopg
from psycopg2 import pool
import json
import uuid
import pandas as pd
from readCsv import ParseCSV

connectionString = 'postgresql://trideDB_owner:uGHc5xoYmwh0@ep-icy-pine-a5sjpt9l.us-east-2.aws.neon.tech/trideDB?sslmode=require'

templateBody = {
    "id": "b40e85b2-1328-4919-bc99-8c245c76979c",
    "username": "admin",
    "email": "soyeladmin@gmail.com",
    "firstName": "admin",
    "lastName": "elQueAdministra",
    "creationDate": 1731436654,
    "isActive": True,
    "password": "$2b$10$aASo.012Iujk0MkWAqdZROaXxB0bR6.mGPplDt9.R0sOIa4DnNmcG"
}

connection_pool = pool.SimpleConnectionPool(1, 10, connectionString)

if connection_pool:
    print("Connection pool created successfully")

def seedPredictions():
    ParseCSV('./data/timeModel2.csv')
    seedUsers(templateBody)
    try:
        with open('./data/parsed.json', 'r') as file:
            data = json.load(file)
        
        conn = connection_pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS predictions")
                cur.execute("""
                    CREATE TABLE predictions(
                        id text PRIMARY KEY,
                        RUTA text,
                        BARRIO text,
                        HORARIO text,
                        CLIMA text,
                        TIEMPO_REAL text,
                        TIEMPO_ESPERADO text,
                        TIEMPO_PERDIDO text,
                        userid uuid,
                        FOREIGN KEY ("userid") REFERENCES "user"(id) ON DELETE CASCADE
                    )
                """)
                
                for record in data:
                    cur.execute("""
                        INSERT INTO predictions(id, RUTA, BARRIO, HORARIO, CLIMA, TIEMPO_REAL, TIEMPO_ESPERADO, TIEMPO_PERDIDO, userid)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        str(uuid.uuid4()), 
                        record['RUTA'], 
                        record['BARRIO'], 
                        record['HORARIO'], 
                        record['CLIMA'], 
                        record['TIEMPO_REAL'], 
                        record['TIEMPO_ESPERADO'], 
                        record['TIEMPO_PERDIDO'],
                        templateBody['id']
                    ))
                
                conn.commit()
            return "Success: predictions seed executed"
        except Exception as e:
            print(f"Error al insertar datos: {e}")
            return f"Error: {e}"
        finally:
            connection_pool.putconn(conn)

    except Exception as e:        
        print(f"Error al procesar archivo: {e}")
        return f"Error: {e}"

def seedUsers(body):
    conn = connection_pool.getconn()
    try:
        with conn.cursor() as cur:                 
            cur.execute("""
                INSERT INTO "user"
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                templateBody['id'],
                body['username'],
                body['email'],
                body['firstName'],
                body['lastName'],
                body['creationDate'],
                body['isActive'],
                body['password']
            ))
            conn.commit()
            return "User inserted successfully"
    except Exception as e:
        print(f"Error al insertar usuario: {e}")
        return f"Error: {e}"
    finally:
        connection_pool.putconn(conn)

def getPredictions():
    print('Predictions')
    conn = connection_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT ruta, barrio, horario, clima, tiempo_real, tiempo_esperado, tiempo_perdido FROM predictions")        
            records = [list(record) for record in cur.fetchall()]
                            
            df = pd.DataFrame(records, columns=['RUTA', 'BARRIO', 'HORARIO', 'CLIMA', 'TIEMPO_REAL', 'TIEMPO_ESPERADO', 'TIEMPO_PERDIDO'])
            print(df)
                            
            df.to_csv('./data/timeModel2.csv', index=True)
            return df
    except Exception as e:
        print(f"Error al obtener registros: {e}")
        return f"Error: {e}"
    finally:
        connection_pool.putconn(conn)
    
def insertPrediction(body):
    conn = connection_pool.getconn()
    try: 
        with conn.cursor() as cur:
            cur.execute("""
                    INSERT INTO predictions(id, RUTA, BARRIO, HORARIO, CLIMA, TIEMPO_REAL, TIEMPO_ESPERADO, TIEMPO_PERDIDO, userid)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    str(uuid.uuid4()), 
                    body['RUTA'], 
                    body['BARRIO'], 
                    body['HORARIO'], 
                    body['CLIMA'], 
                    body['TIEMPO_REAL'], 
                    body['TIEMPO_ESPERADO'], 
                    body['TIEMPO_PERDIDO'],
                    body['id']
                ))
            conn.commit()
        return "Success register created"
    except Exception as e:
        print(f"Error register not created: {e}")
        return f"Error: {e}"
    finally:
        connection_pool.putconn(conn)
