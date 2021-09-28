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


def insert_user(id, money, user_name, health, clan, power, peer_id):
    connection = create_connection("vk_bot", "postgres", "password", "127.0.0.1", "port")
    cur = connection.cursor()
    cur.execute(
        """INSERT INTO USERS (ID,MONEY,USER_NAME,HEALTH,CLAN,POWER,PEER_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (id, money, user_name, health, clan, power, peer_id)
    )
    connection.commit()


def check_uniq_user(peer_id):
    query = """ SELECT PEER_ID FROM USERS """
    connection = create_connection("vk_bot", "postgres", "redonu28", "127.0.0.1", "5432")
    cur = connection.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    for i in rows:
        if peer_id in i:
            return False
        else:
            return True
