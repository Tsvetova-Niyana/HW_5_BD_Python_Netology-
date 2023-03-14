import psycopg2
from function import *

if __name__ == '__main__':
    with psycopg2.connect(database="netology", user="postgres", password="123") as conn:
        # создание таблиц
        create_table(conn)

        # добавление клиентов
        add_client(conn, "Василий", "Пупкин", "pupkin@bk.ru")
        add_client(conn, "Иван", "Сидоров", "sidorov@bk.ru")
        add_client(conn, "Иван", "Иванов", "ivanov@list.ru")
        add_client(conn, "Семен", "Иванов", "ivanovS@list.ru")
        add_client(conn, "Андрей", "Семенов", "aSemenoff@mail.ru")

        # проверка информации о добавленных клиентах
        print("Клиенты в базе (без телефонов):")
        select_info_client(conn)
        print()

        # добавление телефонов клиентов
        add_phone(conn, 1, "89991234567")
        add_phone(conn, 2, "83331234567")
        add_phone(conn, 1, "87771234567")
        add_phone(conn, 4, "89371234567")
        add_phone(conn, 5, "85551234567")

        # проверка информации о добавленных клиентах
        print("Клиенты в базе (инфо с телефонами):")
        select_info_client_with_phone(conn)
        print()

        # обновление информации о клиенте с id = 1 (изменяем имя клиента и его номер телефона на позиции 3
        # в справочнике телефонов)
        update_info_client(conn, 1, "Виталий", None, None, "89776655555", 3)

        # обновление информации о клиенте с id = 2 (изменяем email клиента)
        update_info_client(conn, 2, None, None, "sidorov@list.ru")

        # обновление информации о клиенте с id = 1 (изменяем номер телефона клиента на позиции 3
        # в справочнике телефонов)
        update_info_client(conn, 1, None, None, None, "89116655555", 1)

        # проверка информации о клиентах после обновления информации
        print("Информация о клиентах после обновления:")
        select_info_client_with_phone(conn)
        print()

        # удаление номера телефона с id = 2
        delete_phone(conn, 2)

        print("Информация о клиентах после удаления телефона:")
        select_info_client_with_phone(conn)
        print()

        # удаление клиента с id = 2
        delete_client(conn, 2)

        print("Информация после удаления клиента:")
        select_info_client_with_phone(conn)
        print()

        # поиск клиента по имени
        print("Поиск клиента по имени:")
        search_client_by_info(conn, "Виталий")
        print()

        print("Поиск клиента по фамилии:")
        search_client_by_info(conn, None, "Иванов")
        print()

        print("Поиск клиента по email:")
        search_client_by_info(conn, None, None, "aSemenoff@mail.ru")
        print()

        print("Поиск клиента по телефону:")
        search_client_by_info(conn, None, None, None, "89116655555")

    conn.close()
