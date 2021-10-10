import psycopg2

import monsters


def create_connection(database, user, password, host, port):
    con = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return con


def insert_user(id, money, user_name, health, clan, power, peer_id, exp, lvl):
    connection = create_connection("database", "user", "your_pass", "host", "port")
    cur = connection.cursor()
    cur.execute(
        """INSERT INTO USERS (ID,MONEY,USER_NAME,HEALTH,CLAN,POWER,PEER_ID, EXP, LVL)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (id, money, user_name, health, clan, power, peer_id, exp, lvl)
    )
    connection.commit()
    connection.close()


def check_uniq_user(user_id):
    a = 0
    query = """ SELECT PEER_ID FROM USERS """
    connection = create_connection("database", "user", "your_pass", "host", "port")
    cur = connection.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        if user_id in row:
            a += 1
            break
        else:
            a = 0
    connection.close()
    return a


def show_profile(user_id):
    query = """SELECT HEALTH, USER_NAME, POWER, CLAN, MONEY, LVL FROM USERS WHERE PEER_ID = '%s'""" % user_id
    connection = create_connection("database", "user", "your_pass", "host", "port")
    cur = connection.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        health = row[0]
        user_name = row[1]
        power = row[2]
        clan = row[3]
        money = row[4]
        exp = row[5]
        return money, user_name, health, clan, power, exp


def shop_show_items(bd_name):
    query = """SELECT ITEM_NAME, ITEM_POWER, ITEM_HEALTH, ITEM_COAST FROM %s""" % bd_name
    connection = create_connection("database", "user", "your_pass", "host", "port")
    cur = connection.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    items_array = []
    for row in rows:
        items_array.append(row[0])
    return items_array


def monster_fight_queries(user_id, bd_name):
    monster_data = []
    user_data = []
    monster_query = """SELECT NAME, POWER, HEALTH, REWARD, EARN_EXP FROM %s ORDER BY RANDOM() LIMIT 1""" % bd_name
    user_query = """SELECT POWER, HEALTH, MONEY, EXP FROM USERS WHERE PEER_ID = '%s'""" % user_id
    connection = create_connection("database", "user", "your_pass", "host", "port")
    first_cur = connection.cursor()
    first_cur.execute(monster_query)
    monster_rows = first_cur.fetchall()
    for row in monster_rows:
        monster_data.append(row[0])
        monster_data.append(row[1])
        monster_data.append(row[2])
        monster_data.append(row[3])
        monster_data.append(row[4])
    second_cur = connection.cursor()
    second_cur.execute(user_query)
    user_rows = second_cur.fetchall()
    for row in user_rows:
        user_data.append(row[0])
        user_data.append(row[1])
        user_data.append(row[2])
        user_data.append(row[3])
    connection.close()
    return monster_data, user_data


def insert_reward(user_id, money, exp):
    query = """UPDATE USERS SET MONEY = '%s' WHERE PEER_ID = '%s'""" % (money, user_id)
    query_exp = """UPDATE USERS SET exp = '%s' WHERE PEER_ID = '%s'""" % (exp, user_id)
    connection = create_connection("database", "user", "your_pass", "host", "port")
    cur = connection.cursor()
    cur.execute(query)
    cur.execute(query_exp)
    connection.commit()
    connection.close()


def check_inv(user_id, item_name):
    user_items = []
    connection = create_connection("database", "user", "your_pass", "host", "port")
    cur = connection.cursor()
    cur.execute("""SELECT NAME FROM INVENTORY WHERE USER_ID = '%s'""" % user_id)
    rows = cur.fetchall()
    for row in rows:
        for i in row:
            user_items.append(i)
    for i in user_items:
        if i == item_name:
            return True
    return False


def show_inventory(user_id):
    user_items = []
    connection = create_connection("database", "user", "your_pass", "host", "port")
    cur = connection.cursor()
    cur.execute("""SELECT NAME FROM INVENTORY WHERE USER_ID = '%s'""" % user_id)
    rows = cur.fetchall()
    for row in rows:
        for i in row:
            user_items.append(i)
    return user_items


def buy_items(user_id, item_name, bd_name):
    item_data = []
    user_inventory = []
    item_query = """SELECT ITEM_POWER, ITEM_HEALTH, ITEM_COAST FROM %s WHERE ITEM_NAME = '%s'""" % (bd_name, item_name)
    connection = create_connection("database", "user", "your_pass", "host", "port")
    first_cur = connection.cursor()
    first_cur.execute(item_query)
    rows = first_cur.fetchall()
    for row in rows:
        item_data.append(row[0])
        item_data.append(row[1])
        item_data.append(row[2])
    user_money_query = """SELECT MONEY FROM USERS WHERE PEER_ID = '%s'""" % user_id
    third_cur = connection.cursor()
    third_cur.execute(user_money_query)
    get_user_current_money = third_cur.fetchall()
    tuple_user_current_money = get_user_current_money[0]
    user_current_money = tuple_user_current_money[0]
    print(item_data)
    if (user_current_money >= item_data[2]) and (check_inv(user_id, item_name) is False):
        user_inventory.append(item_name)
        user_query = """UPDATE USERS SET MONEY = MONEY -'%s', POWER = POWER + '%s', HEALTH = HEALTH + '%s' 
        WHERE PEER_ID = '%s'""" \
                     % (item_data[2], item_data[0], item_data[1],  user_id)
        second_cur = connection.cursor()
        second_cur.execute(user_query)
        third_cur.execute("""INSERT INTO INVENTORY (NAME, USER_ID) VALUES(%s, %s)""", (item_name, user_id))
        connection.commit()
        connection.close()
        return f"Предмет {item_name} успешно куплен! Характеристики обновлены: \n " \
               f"Урон: +{item_data[0]} \n" \
               f"Здоровье: +{item_data[1]} \n" \
               f"Деньги: -{item_data[2]} !!!"
    elif check_inv(user_id, item_name) is True:
        return f"У вас уже есть этот предмет"
    else:
        return f"Недостаточно денег! Стоимость предмета - {item_data[2]} монет."


def check_exp(user_id):
    lvl = 0
    exp = 0
    exp_patterns = [100, 200, 400, 500, 1000, 2000, 4000, 8000, 16000, 32000]
    query = """SELECT EXP FROM USERS WHERE PEER_ID = '%s'""" % user_id
    connection = create_connection("database", "user", "your_pass", "host", "port")
    cur = connection.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        exp = row[0]
    for i in exp_patterns:
        if exp >= i:
            lvl += 1
    print(lvl)
    return lvl


def lvl_up(user_id):
    current_lvl = 0
    lvl = check_exp(user_id)
    connection = create_connection("database", "user", "your_pass", "host", "port")
    cur = connection.cursor()
    lvl_query = """SELECT LVL FROM USERS WHERE PEER_ID = '%s'""" % user_id
    cur.execute(lvl_query)
    rows = cur.fetchall()
    for row in rows:
        current_lvl = row[0]
    patterns = {'1': 10, '2': 20, '3': 40, '4': 80, '5': 160, '6': 320, '7': 500, '8': 1000, '9': 2000, '10': 5000}
    keys = list(patterns.keys())
    print(current_lvl)
    for i in keys:
        if (i == str(lvl)) and (current_lvl != lvl):
            data = patterns.get(i)
            query = """UPDATE USERS SET LVL = '%s', POWER = POWER + '%s', HEALTH = HEALTH + '%s' WHERE PEER_ID = '%s'""" \
                    % (lvl, data, data, user_id)
            cur.execute(query)
            connection.commit()
            connection.close()
            return f"Ты получил уровень {lvl}! \n Сила: +{data} \n Здоровье: +{data}"
    return f"Убивай больше монстров, чтоб получить новый уровень!"


def key(user_id, key_name):
    user_items = []
    connection = create_connection("database", "user", "your_pass", "host", "port")
    cur = connection.cursor()
    cur.execute("""SELECT NAME FROM INVENTORY WHERE USER_ID = '%s'""" % user_id)
    rows = cur.fetchall()
    for row in rows:
        for i in row:
            user_items.append(i)
    for i in user_items:
        if i == key_name:
            return True
    return False


def boss_fight_queries(user_id, bd_name, boss_name):
    monster_data = []
    user_data = []
    monster_query = """SELECT NAME, POWER, HEALTH, REWARD, EARN_EXP FROM %s WHERE NAME = '%s'""" % (bd_name, boss_name)
    user_query = """SELECT POWER, HEALTH, MONEY, EXP FROM USERS WHERE PEER_ID = '%s'""" % user_id
    connection = create_connection("database", "user", "your_pass", "host", "port")
    first_cur = connection.cursor()
    first_cur.execute(monster_query)
    monster_rows = first_cur.fetchall()
    for row in monster_rows:
        monster_data.append(row[0])
        monster_data.append(row[1])
        monster_data.append(row[2])
        monster_data.append(row[3])
        monster_data.append(row[4])
    second_cur = connection.cursor()
    second_cur.execute(user_query)
    user_rows = second_cur.fetchall()
    for row in user_rows:
        user_data.append(row[0])
        user_data.append(row[1])
        user_data.append(row[2])
        user_data.append(row[3])
    connection.close()
    return monster_data, user_data







