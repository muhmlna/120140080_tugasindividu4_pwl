import sqlite3

conn = sqlite3.connect('dota2.db')
cursor = conn.cursor()

# Membuat tabel Dota 2 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS dota2 (
        id INTEGER PRIMARY KEY,
        hero_name TEXT,
        role TEXT
    )
''')

#  data dummy
dummy_data = [
    (1, 'Axe', 'Tank'),
    (2, 'Crystal Maiden', 'Support'),
    (3, 'Drow Ranger', 'Carry'),
    (4, 'Invoker', 'Mid'),
    (5, 'Mirana', 'Support'),
    (6, 'Phantom Assassin', 'Carry'),
    (7, 'Earthshaker', 'Support'),
    (8, 'Juggernaut', 'Carry'),
    (9, 'Pudge', 'Tank'),
    (10, 'Templar Assassin', 'Mid')
]

# Memasukkan data dummy ke dalam tabel
cursor.executemany('INSERT INTO dota2 (id, hero_name, role) VALUES (?, ?, ?)', dummy_data)

# Commit perubahan ke dalam basis data
conn.commit()

# Menutup koneksi ke basis data
conn.close()
