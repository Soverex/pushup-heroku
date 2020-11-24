import psycopg2
from flask import session
import os

def updateData():
    user  = session['profile']['email']
    try:
        connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        cursor = connection.cursor()
        cursor.execute(f"select sum(pushup) from \"pushup\" where user_email = '{user}' and DATE(datetime) >= CURRENT_DATE AND DATE(datetime) < CURRENT_DATE + INTERVAL '1 DAY'")
        result = cursor.fetchone()[0]
        print(result)
        session['pushup_day'] = result
        cursor.execute(f"select sum(pushup) from \"pushup\" where user_email = '{user}'")
        result2 = cursor.fetchone()[0]
        print(result2)
        session['pushup_all'] = result2
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
        session['pushup_day'] = 0
        session['pushup_all'] = 0
    finally:
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

def addpushup(user):
    try:
        connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO \"pushup\" (user_email, datetime, pushup) VALUES ('{user}', current_timestamp, 1);")
        connection.commit()
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

def getpushup_data(user):
    try:
        connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        cursor = connection.cursor()
        cursor.execute(f"select sum(pushup) from \"pushup\" where user_email = '{user}' and DATE(datetime) >= CURRENT_DATE AND DATE(datetime) < CURRENT_DATE + INTERVAL '1 DAY'")
        result = cursor.fetchone()[0]
        return result
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
        return 0
    finally:
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")