import names
from swnamer import NameGenerator


import dbConnection

conn = dbConnection.getDBConnection()

generator = NameGenerator(lowercase=False, use_species=True, use_planets=False, separator=' ')
cur = conn.cursor()
cur.execute("SELECT DISTINCT name from users where team_id <> 21")
records = cur.fetchall()
for row in records:
    nickname = names.get_full_name()
    swnickname = generator.generate()
    cur.execute("UPDATE users SET nickname = ? where name = ?", (swnickname, row[0]))
conn.commit()
conn.close()
for i in range(10):
    print(names.get_full_name())