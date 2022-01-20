import names
from swnamer import NameGenerator
from faker import Faker


import dbConnection

fake = Faker()
#for _ in range(100):
#    name1 = fake.unique.name()
#    print(name1)

conn = dbConnection.getDBConnection()

generator = NameGenerator(lowercase=False, use_species=True, use_planets=False, separator=' ')
cur = conn.cursor()
cur.execute("SELECT DISTINCT name from users") # where team_id <> 21")
records = cur.fetchall()
for row in records:
    nickname = fake.unique.name() #names.get_full_name()
    swnickname = generator.generate()
    cur.execute("UPDATE users SET nickname = ? where name = ?", (nickname, row[0]))
conn.commit()
conn.close()
#for i in range(10):
#    print(names.get_full_name())