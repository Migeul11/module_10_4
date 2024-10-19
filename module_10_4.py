from queue import Queue
from random import randint
from threading import Thread
from time import sleep


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(3, 10))


class Cafe:
    def __init__(self, *tables):
        self.tables = []
        self.queue = Queue()
        self.occupied_tables_qty = 0
        for table in tables:
            self.tables.append(table)

    def guest_arrival(self, *guests):
        table_index = 0
        tables_qty = len(self.tables)
        for guest in guests:
            guest_gets_free_table = False

            while table_index < tables_qty and not guest_gets_free_table:
                if self.tables[table_index].guest is None:
                    guest_gets_free_table = True
                    self.tables[table_index].guest = guest
                    self.occupied_tables_qty += 1
                    guest.start()
                    print(f"{guest.name} сел(-а) за стол номер {self.tables[table_index].number}")
                table_index += 1

            if not guest_gets_free_table:
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or self.occupied_tables_qty > 0:
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None
                    self.occupied_tables_qty -= 1

                if table.guest is None and not self.queue.empty():
                    table.guest = self.queue.get()
                    self.occupied_tables_qty += 1
                    table.guest.start()
                    print(f"{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()