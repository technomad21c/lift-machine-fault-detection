import mysql.connector
from mysql.connector import errorcode

class SensorDB():
    def __init__(self):
        self.connection = None
        self.cur = None
        self.encoding = 'UTF-8'

    def connect(self, server, database, username, password):
        try:
            self.connection  = mysql.connector.connect(
                user=username, password=password, host=server, database=database)
            self.cur = self.connection.cursor()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def read(self, query_select):
        results = []
        self.cur.execute(query_select)
        results = self.cur.fetchall()

        return results

    def update(self, query_update):
        self.cur.execute(query_update)
        self.connection.commit()

    def close(self):
        if self.cur:
            self.cur.close()
        if self.connection:
            self.connection.close()