import mysql.connector as conn
import mysql.connector.errors as errorcode
from Config.config import PostDB as db
# from Config.config import DB as db
import psycopg2
class SqlUtility:
    def insert_single(query,data):
        config = {
            'user': db.user_name,
            'password': db.password,
            'host': db.host,
            'database': db.database
        }

        # config = {
        #     'user': 'root',
        #     'password': 'Thykoodam6655#',
        #     'host': 'localhost',
        #     'database': 'india_poll',
        #     'raise_on_warnings': True
        # }
        try:
            cnx = psycopg2.connect(**config)
            # cnx = conn.connect(** config)
            cursor = cnx.cursor()
            sql_query = query
            cursor.execute(sql_query,data)
            id = cursor.fetchone()[0]
            cnx.commit()
            return id
        except conn.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()
    def insertMany(query,data):
        config = {
            'user': db.user_name,
            'password': db.password,
            'host': db.host,
            'database': db.database
        }
        try:
            cnx = psycopg2.connect(**config)
            # cnx = conn.connect(** config)
            cursor = cnx.cursor()
            sql_query = query
            cursor.executemany(sql_query,data)
            cnx.commit()
        except conn.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()
    def select_query(query,data):
        config = {
            'user': db.user_name,
            'password': db.password,
            'host': db.host,
            'database': db.database
        }
        try:
            cnx = psycopg2.connect(**config)
            # cnx = conn.connect(**config)
            cursor = cnx.cursor()
            cursor.execute(query,data)
            result = cursor.fetchall()
            return result
            # cnx.commit()
        except conn.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()



