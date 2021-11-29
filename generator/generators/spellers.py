from typing import Counter
import faker


class Spellers:
    def __init__(self, connection):
        self.__connection = connection
        self.__faker = faker.Faker("ru_RU")
        self.__last_id = 0
    
    def insert(self, count = 1):
        query = "INSERT INTO spellers (first_name, last_name, address, phone) VALUES(%s, %s, %s, %s) RETURNING speller_id"
        cursor = self.__connection.get_cursor()
        for i in range(count):
            cursor.execute(query, (
                self.__faker.first_name(), 
                self.__faker.last_name(),  
                self.__faker.address().replace("\n", " "),
                self.__faker.phone_number()
            ))
        cursor.execute('SELECT LASTVAL()')
        self.__last_id = cursor.fetchone()[0]
        self.__connection.commit()

    def get_last_id(self):
        return self.__last_id