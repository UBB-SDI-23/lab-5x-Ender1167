import datetime
import random

from passlib.hash import pbkdf2_sha256
from faker import Faker

import base64
import hashlib
import secrets

ALGORITHM = "pbkdf2_sha256"


def hash_password(password, salt=None, iterations=260000):
    if salt is None:
        salt = secrets.token_hex(16)
    assert salt and isinstance(salt, str) and "$" not in salt
    assert isinstance(password, str)
    pw_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations
    )
    b64_hash = base64.b64encode(pw_hash).decode("ascii").strip()
    return "{}${}${}${}".format(ALGORITHM, iterations, salt, b64_hash)

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
    fake = Faker()
    plain_password = "temporarypassword1"
    hashed_password = hash_password(plain_password)

    first_name_generic = "John"
    last_name_generic = "Doe"
    email_generic = "johndoe@gmail.com"
    is_superuser_generic = False
    is_staff_generic = False
    is_active_generic = True

    dummy_user = "temp"
    dummy_id = 0

    # generate fake data for players and create INSERT SQL statements
    for j in range(10):
        sql_insert = "INSERT INTO auth_user (password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES"
        for i in range(1000):
            #username = fake.user_name()
            username = dummy_user + str(dummy_id)
            dummy_id = dummy_id + 1
            print(username)
            sql_insert = sql_insert + " ('{}', {}, '{}', '{}', '{}', '{}', {}, {}, TIMESTAMP '2011-05-16 15:36:38'), ".format(hashed_password, is_superuser_generic, username, first_name_generic, last_name_generic, email_generic, is_staff_generic, is_active_generic)

        insert_size = len(sql_insert)
        sql_insert_modified = sql_insert[:insert_size - 2]
        sql_insert_modified = sql_insert_modified + ";"

        sqls.append(sql_insert_modified)

    f = open('data_users.sql', 'w')
    for i, sql in enumerate(sqls):
        #print(sql)
        f.write(sql + "\n")
    f.close()

def createUserProfile():
    sqls = []
    fake = Faker()
    genders = ["Male", "Female"]
    marital_status = ["Married", "Not married"]
    start = 13780
    counter = start

    end = 10305
    for j in range(4):
        sql_insert = "INSERT INTO destinycharacters_userprofile (bio, location, age, gender, marital_status, user_id) VALUES"
        for i in range(1000):

            user_bio = ""
            for k in range(2):
                user_bio = user_bio + fake.sentence(nb_words=10, variable_nb_words=False)

            user_location = fake.city()
            user_age = random.randint(1, 60)

            gender_id = random.randint(0, len(genders) - 1)
            selected_gender = genders[gender_id]

            marital_status_id = random.randint(0, len(marital_status) - 1)
            selected_status = marital_status[marital_status_id]

            selected_user_id = counter
            selected_isActive = True
            counter = counter - 1

            sql_insert = sql_insert + " ('{}', '{}', {}, '{}', '{}', {}), ".format(user_bio, user_location, user_age, selected_gender, selected_status, selected_user_id)

        insert_size = len(sql_insert)
        sql_insert_modified = sql_insert[:insert_size - 2]
        sql_insert_modified = sql_insert_modified + ";"

        sqls.append(sql_insert_modified)

    f = open('data_profiles.sql', 'w')
    for i, sql in enumerate(sqls):
        #print(sql)
        f.write(sql + "\n")
    f.close()



def main():
    #createPlayers()
    #createWeapons()
    #createLocations()
    #createLocationWeapons()
    #createUser()
    createUserProfile()

if __name__ == '__main__':
    main()
