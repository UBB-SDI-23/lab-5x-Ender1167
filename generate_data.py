import random

from faker import Faker

def createPlayers():
    fake = Faker()
    sqls = []
    allClasses = ['Hunter', 'Titan', 'Warlock']

    # generate fake data for players and create INSERT SQL statements
    for j in range(1000000):
        sql_insert = "INSERT INTO destinycharacters_player (name, class1, level, glimmer, shards) "
        for i in range(1000):
            name = fake.name()

            random_class_id = random.randint(0, 2)
            class1 = allClasses[random_class_id]

            level = random.randint(1, 50)
            glimmer = random.randint(0, 1000000)
            shards = random.randint(0, 1000000)
            #sql = "INSERT INTO destinycharacters_player (name, class1, level, glimmer, shards) VALUES ('{}', '{}', {}, {}, {})".format(
            #    name, class1, level, glimmer, shards)
            sql_insert = sql_insert + "VALUES ('{}', '{}', {}, {}, {})".format(name, class1, level, glimmer, shards)
        sqls.append(sql_insert)


    f = open('final_data.sql', 'w')
    # write SQL statements to file in /tmp directory
    for i, sql in enumerate(sqls):
        f.write(sql + "\n")
    f.close()

def main():
    createPlayers()

if __name__ == '__main__':
    main()
