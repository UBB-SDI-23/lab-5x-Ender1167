import random

from faker import Faker

def createPlayers():
    fake = Faker()
    sqls = []
    allClasses = ['Hunter', 'Titan', 'Warlock']

    # generate fake data for players and create INSERT SQL statements
    for j in range(1000):
        sql_insert = "INSERT INTO destinycharacters_player (name, class1, level, glimmer, shards) VALUES"
        for i in range(1000):
            name = fake.name()

            random_class_id = random.randint(0, 2)
            class1 = allClasses[random_class_id]

            level = random.randint(1, 50)
            glimmer = random.randint(0, 250000)
            shards = random.randint(0, 1000000)
            #sql = "INSERT INTO destinycharacters_player (name, class1, level, glimmer, shards) VALUES ('{}', '{}', {}, {}, {})".format(
            #    name, class1, level, glimmer, shards)
            sql_insert = sql_insert + " ('{}', '{}', {}, {}, {}), ".format(name, class1, level, glimmer, shards)
        insert_size = len(sql_insert)
        sql_insert_modified = sql_insert[:insert_size - 2]
        sql_insert_modified = sql_insert_modified + ";"

        sqls.append(sql_insert_modified)


    f = open('data_player.sql', 'w')
    # write SQL statements to file in /tmp directory
    for i, sql in enumerate(sqls):
        f.write(sql + "\n")
    f.close()


def createWeapons():
    fake = Faker()
    sqls = []
    allElements = ['Kinetic', 'Solar', 'Arc', 'Void', 'Strand', 'Strand']
    allTypes = ['Hand cannon', 'Auto rifles', 'Shotgun', 'Fusion Rifle', 'Linear Fusion Rifle', 'Bow', 'Sniper Rifle',
                'Scout Rifle', 'Submachine gun', 'Pulse Rifle', 'Rocket Launcher']
    allSlots = ['Kinetic', 'Energy', 'Heavy']


    # generate fake data for players and create INSERT SQL statements
    for j in range(1000):
        sql_insert = "INSERT INTO destinycharacters_weapon (weapon_name, weapon_slot, weapon_element, weapon_type, weapon_damage, player_weapon_id, weapon_description) VALUES"
        for i in range(1000):
            weapon_name = fake.word()

            random_slot = random.randint(0, len(allSlots)-1)
            random_element = random.randint(0, len(allElements)-1)
            random_type = random.randint(0, len(allTypes)-1)
            weapon_damage = random.randint(0, 450)
            player_weapon = random.randint(1, 1000000)

            weapon_description = ""
            for k in range(10):
                weapon_description = weapon_description + fake.sentence(nb_words=10, variable_nb_words=False)

            weapon_slot = allSlots[random_slot]
            weapon_element = allElements[random_element]
            weapon_type = allTypes[random_type]

            #sql = "INSERT INTO destinycharacters_player (name, class1, level, glimmer, shards) VALUES ('{}', '{}', {}, {}, {})".format(
            #    name, class1, level, glimmer, shards)
            sql_insert = sql_insert + " ('{}', '{}', '{}', '{}', {}, {}, '{}'), ".format(weapon_name, weapon_slot, weapon_element, weapon_type, weapon_damage, player_weapon, weapon_description)
        insert_size = len(sql_insert)
        sql_insert_modified = sql_insert[:insert_size - 2]
        sql_insert_modified = sql_insert_modified + ";"

        sqls.append(sql_insert_modified)


    f = open('data_weapons.sql', 'w')
    # write SQL statements to file in /tmp directory
    for i, sql in enumerate(sqls):
        f.write(sql + "\n")
    f.close()

def createLocations():
    fake = Faker()
    sqls = []
    allEnemies = ['Fallen', 'Scorn', 'Cabal', 'Vex', 'Taken']


    # generate fake data for players and create INSERT SQL statements
    for j in range(10000):
        sql_insert = "INSERT INTO destinycharacters_location (location_name, enemy_type, min_level, nr_public_events, nr_lost_sectors) VALUES"
        for i in range(1000):
            location_name = fake.city()

            random_enemy = random.randint(0, len(allEnemies)-1)
            enemy_type = allEnemies[random_enemy]
            min_level = random.randint(1, 50)
            nr_public_events = random.randint(0, 10)
            nr_lost_sectors = random.randint(3, 7)


            #sql = "INSERT INTO destinycharacters_player (name, class1, level, glimmer, shards) VALUES ('{}', '{}', {}, {}, {})".format(
            #    name, class1, level, glimmer, shards)
            sql_insert = sql_insert + " ('{}', '{}', {}, {}, {}), ".format(location_name, enemy_type, min_level, nr_public_events, nr_lost_sectors)
        insert_size = len(sql_insert)
        sql_insert_modified = sql_insert[:insert_size - 2]
        sql_insert_modified = sql_insert_modified + ";"

        sqls.append(sql_insert_modified)


    f = open('data_locations.sql', 'w')
    # write SQL statements to file in /tmp directory
    for i, sql in enumerate(sqls):
        f.write(sql + "\n")
    f.close()

def createLocationWeapons():

    sqls = []

    # generate fake data for players and create INSERT SQL statements
    for j in range(10000):
        sql_insert = "INSERT INTO destinycharacters_location_weapon (drop_rate, wep_id, loc_id) VALUES"
        for i in range(1000):

            drop_rate = random.randint(1, 100)
            wep = random.randint(1, 1000000)
            loc = random.randint(1, 1000000)


            #sql = "INSERT INTO destinycharacters_player (name, class1, level, glimmer, shards) VALUES ('{}', '{}', {}, {}, {})".format(
            #    name, class1, level, glimmer, shards)
            sql_insert = sql_insert + " ({}, {}, {}), ".format(drop_rate, wep, loc)
        insert_size = len(sql_insert)
        sql_insert_modified = sql_insert[:insert_size - 2]
        sql_insert_modified = sql_insert_modified + ";"

        sqls.append(sql_insert_modified)


    f = open('data_location_weapons.sql', 'w')
    # write SQL statements to file in /tmp directory
    for i, sql in enumerate(sqls):
        f.write(sql + "\n")
    f.close()

def createUser():
    sqls = []

    # generate fake data for players and create INSERT SQL statements
    for j in range(10000):
        sql_insert = "INSERT INTO destinycharacters_user_profile (drop_rate, wep_id, loc_id) VALUES"
def main():
    #createPlayers()
    createWeapons()
    #createLocations()
    #createLocationWeapons()
    createUser()

if __name__ == '__main__':
    main()
