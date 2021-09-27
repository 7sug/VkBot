import psycopg2


def create_connection(database, user, password, host, port):
    con = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return con


def insert_user(id, money, user_name, health):
    connection = create_connection("vk_bot", "postgres", "redonu28", "127.0.0.1", "5432")
    cur = connection.cursor()
    cur.execute(
        """INSERT INTO USERS (ID,MONEY,USER_NAME,HEALTH) VALUES (%s, %s, %s, %s)""", (id, money, user_name, health)
    )
    connection.commit()
