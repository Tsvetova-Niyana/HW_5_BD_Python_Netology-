"""
Необходимо разработать структуру БД для хранения информации и несколько функций на Python для управления данными.

Функция, создающая структуру БД (таблицы).
Функция, позволяющая добавить нового клиента.
Функция, позволяющая добавить телефон для существующего клиента.
Функция, позволяющая изменить данные о клиенте.
Функция, позволяющая удалить телефон для существующего клиента.
Функция, позволяющая удалить существующего клиента.
Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
"""


def create_table(conn):
    """
    Функция, создающая структуру БД (таблицы).

    Требуется хранить персональную информацию о клиентах:

    имя,
    фамилия,
    email,
    телефон.

    Сложность в том, что телефон у клиента может быть не один, а два, три и даже больше. А может и вообще не быть
    телефона, например, он не захотел его оставлять.
    """
    with conn.cursor() as cur:
        # удаление таблиц
        cur.execute("""
        DROP TABLE phone_clients;
        DROP TABLE info_client;        
        """)

        # создание таблиц
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS info_client(
                        id_client SERIAL PRIMARY KEY,
                        name_client VARCHAR(50) NOT NULL,
                        surname_client VARCHAR(50) NOT NULL,
                        email VARCHAR(20) UNIQUE
                    );
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS phone_clients(
                        id_pc SERIAL PRIMARY KEY,
                        id_client INTEGER NOT NULL REFERENCES info_client(id_client),
                        phone VARCHAR(12)
                    );
                    """)
        conn.commit()


def add_client(conn, name_client, surname_client, email):
    """
    Функция, позволяющая добавить нового клиента.
    """
    with conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO info_client(name_client, surname_client, email)
                    VALUES (%s, %s, %s);
                    """, (name_client, surname_client, email,))
        conn.commit()


def add_phone(conn, id_client, phone):
    """
    Функция, позволяющая добавить телефон для существующего клиента.
    """
    with conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO phone_clients (id_client, phone)
                    VALUES(%s, %s);
                    """, (id_client, phone,))
        conn.commit()


def update_info_client(conn, id_client, name_client=None, surname_client=None, email=None, phone=None, id_pc=None):
    """
    Функция, позволяющая изменить данные о клиенте.
    """
    with conn.cursor() as cur:
        if name_client:
            cur.execute("""
                        UPDATE info_client
                        SET name_client = %s
                        WHERE id_client = %s;
                        """, (name_client, id_client,))

        if surname_client:
            cur.execute("""
                        UPDATE info_client
                        SET surname_client = %s
                        WHERE id_client = %s;
                        """, (surname_client, id_client,))

        if email:
            cur.execute("""
                        UPDATE info_client
                        SET email = %s
                        WHERE id_client = %s;
                        """, (email, id_client,))

        if phone and id_pc:
            cur.execute("""
                        UPDATE phone_clients
                        SET phone = %s
                        WHERE id_pc = %s
                                AND id_client = %s;
                        """, (phone, id_pc, id_client))
            conn.commit()


def delete_phone(conn, id):
    """
    Функция, позволяющая удалить телефон для существующего клиента.
    """
    with conn.cursor() as cur:
        cur.execute("""
                    DELETE FROM phone_clients
                    WHERE id_pc = %s;
                    """, (id,))
        conn.commit()


def delete_client(conn, id_client):
    """
    Функция, позволяющая удалить существующего клиента.
    """
    with conn.cursor() as cur:
        cur.execute("""
                    DELETE FROM info_client
                    WHERE id_client = %s;
                    """, (id_client,))
        conn.commit()


def select_info_client(conn):
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT ic.* FROM info_client ic
                    ORDER BY ic.id_client;
                    """)
        print(cur.fetchall())


def select_info_client_with_phone(conn):
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT ic.*, pc.phone FROM info_client ic
                    LEFT JOIN phone_clients pc ON ic.id_client = pc.id_client
                    ORDER BY ic.id_client;
                    """)
        print(cur.fetchall())


def search_client_by_info(conn, name_client=None, surname_client=None, email=None, phone=None):
    """
    Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
    """
    with conn.cursor() as cur:
        if name_client:
            cur.execute("""
                        SELECT ic.*, pc.phone FROM info_client ic
                        LEFT JOIN phone_clients pc ON ic.id_client = pc.id_client
                        WHERE ic.name_client = %s;
                        """, (name_client,))

        if surname_client:
            cur.execute("""
                        SELECT ic.*, pc.phone FROM info_client ic
                        LEFT JOIN phone_clients pc ON ic.id_client = pc.id_client
                        WHERE ic.surname_client = %s;
                        """, (surname_client,))

        if email:
            cur.execute("""
                        SELECT ic.*, pc.phone FROM info_client ic
                        LEFT JOIN phone_clients pc ON ic.id_client = pc.id_client
                        WHERE ic.email = %s;
                        """, (email,))

        if phone:
            cur.execute("""
                        SELECT ic.*, pc.phone FROM info_client ic
                        LEFT JOIN phone_clients pc ON ic.id_client = pc.id_client
                        WHERE pc.phone = %s;
                        """, (phone,))

        print(cur.fetchall())
