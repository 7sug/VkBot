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
    connection = create_connection("vk_bot", "postgres", "redonu28", "127.0.0.1", "5432")
    cur = connection.cursor()
    cur.execute(
        """INSERT INTO USERS (ID,MONEY,USER_NAME,HEALTH,CLAN,POWER,PEER_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (id, money, user_name, health, clan, power, peer_id)
    )
    connection.commit()


def check_uniq_user(user_id):
    a = 0
    query = """ SELECT PEER_ID FROM USERS """
    connection = create_connection("vk_bot", "postgres", "redonu28", "127.0.0.1", "5432")
    cur = connection.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        if user_id in row:
            a += 1
            break
        else:
            a = 0
    return a


def show_profile(peer_id):
    query = """SELECT USER_NAME, MONEY, HEALTH, CLAN, POWER FROM USERS WHERE PEER_ID='%s'""" % peer_id
    connection = create_connection("vk_bot", "postgres", "redonu28", "127.0.0.1", "5432")
    cur = connection.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        money = row[1]
        name = row[0]
        health = row[2]
        clan = row[3]
        power = row[4]
        return money, name, health, clan, power


