import random

class Spells:
    def __init__(self, conn, spellers):
        self.__connection = conn
        self.__spellers = spellers
    
    def insert(self, count=10):
        elements = ["Air", "Poison", "Fire", "Earth", "Light", "Ice", "Water"]
        query  = "INSERT INTO spells(speller_id, element, attack, healing, magic_defence) VALUES(%s, %s, %s, %s, %s)"
        for _ in range(count):
            self.__connection.execute_single(query, (
                random.randint(0,self.__spellers.get_last_id()),
                elements[random.randint(0,len(elements)-1)],
                random.randint(-100,100),
                random.randint(-100,100),
                random.randint(-100,100)
            ))