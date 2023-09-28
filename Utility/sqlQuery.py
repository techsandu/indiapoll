from Config.config import PostDB as db
# from Config.config import DB as db
import psycopg2
from common_classes import MyCustomException as ex
class SqlUtility:
    def insert_single(query,data):
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
            cursor.execute(sql_query,data)
            id = cursor.fetchone()[0]
            cnx.commit()
            return id
        except(Exception, psycopg2.Error) as err:
            print("Error", err)
            raise ex(err)
        # else:
        #     cnx.close()
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
        except(Exception, psycopg2.Error) as err:
            print("Error", err)
            raise ex(err)
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
        except(Exception, psycopg2.Error) as err:
            print("Error", err)
            raise ex(err)
        else:
            cnx.close()



