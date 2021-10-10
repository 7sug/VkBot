import database


def fight(user_id, bd_name):
    all_the_data = database.monster_fight_queries(user_id, bd_name)
    print(all_the_data)
    monster_data = all_the_data[0]
    user_data = all_the_data[1]
    monster_name = monster_data[0]
    monster_power = monster_data[1]
    monster_health = monster_data[2]
    monster_reward = monster_data[3]
    monster_exp = monster_data[4]
    user_power = user_data[0]
    user_health = user_data[1]
    user_money = user_data[2]
    user_exp = user_data[3]
    health_data = []
    health_data.append({'Здоровье монстра ' + monster_name: monster_health})
    health_data.append({'Ваше здоровье': user_health})
    while (monster_health > 0) and (user_health > 0):
        monster_health -= user_power
        monster_turn = {'Здоровье монстра ' + monster_name: monster_health}
        user_health -= monster_power
        user_turn = {'Ваше здоровье': user_health}
        health_data.append(monster_turn)
        health_data.append(user_turn)
    if user_health > monster_health:
        user_money += monster_reward
        user_exp += monster_exp
        database.insert_reward(user_id, user_money, user_exp)
        lvl_data = database.lvl_up(user_id)
        health_data.append('Вы победили! Награда получена: ' + str(monster_reward) + ' монет, '
                           + str(monster_exp) + ' очков опыта!')
        health_data.append(lvl_data)
    else:
        health_data.append('Вы проиграли! Уползаем с позором...')
    return health_data


def boss_fight(user_id, bd_name, boss_name, key_name):
    if database.key(user_id, key_name) is True:
        all_the_data = database.boss_fight_queries(user_id, bd_name, boss_name)
        print(all_the_data)
        monster_data = all_the_data[0]
        user_data = all_the_data[1]
        monster_name = monster_data[0]
        monster_power = monster_data[1]
        monster_health = monster_data[2]
        monster_reward = monster_data[3]
        monster_exp = monster_data[4]
        user_power = user_data[0]
        user_health = user_data[1]
        user_money = user_data[2]
        user_exp = user_data[3]
        health_data = []
        health_data.append({'Здоровье монстра ' + monster_name: monster_health})
        health_data.append({'Ваше здоровье': user_health})
        while (monster_health > 0) and (user_health > 0):
            monster_health -= user_power
            monster_turn = {'Здоровье монстра ' + monster_name: monster_health}
            user_health -= monster_power
            user_turn = {'Ваше здоровье': user_health}
            health_data.append(monster_turn)
            health_data.append(user_turn)
        if user_health > monster_health:
            user_money += monster_reward
            user_exp += monster_exp
            database.insert_reward(user_id, user_money, user_exp)
            lvl_data = database.lvl_up(user_id)
            health_data.append('Вы победили! Награда получена: ' + str(monster_reward) + ' монет, '
                               + str(monster_exp) + ' очков опыта!')
            health_data.append(lvl_data)
        else:
            health_data.append('Вы проиграли! Уползаем с позором...')
        print(health_data)
        return health_data
    else:
        key_warning = []
        key_warning.append('Тебе необходим ' + key_name)
        return key_warning
