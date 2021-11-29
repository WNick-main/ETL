import psycopg2
import os

class Connector:
    def __init__(self, host, 
        database=os.environ['DB_NAME'], 
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']):
        self.__connection = psycopg2.connect(
            host=host, 
            database=database, 
            user=user, 
            password=password
        )
    def get_cursor(self):
        return self.__connection.cursor()
    
    def commit(self):
        return self.__connection.commit()

    def execute_batch(self, commands: list):
        cursor = self.get_cursor()
        for command in commands:
            cursor.execute(command)
        self.commit()
    
    def execute_single(self, command, args):
        if args:
            self.get_cursor().execute(command, args)
        else:
            self.get_cursor().execute(command)
        self.commit()