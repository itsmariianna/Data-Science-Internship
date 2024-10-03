import sqlite3

conn = sqlite3.connect('mydatabase.db')

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS streets (
    id INTEGER PRIMARY KEY,
    name TEXT,
    length REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS houses (
    id INTEGER PRIMARY KEY,
    street_id INTEGER,
    tenants INTEGER,
    floors INTEGER,
    FOREIGN KEY (street_id) REFERENCES streets(id)
)
""")

cursor.execute('DELETE FROM houses')
cursor.execute('DELETE FROM streets')


# Streets
streets_data = [
    (1, 'Wisteria Lane', 3.5),
    (2, 'Willow Way', 2.8),
    (3, 'Cherry Blossom Lane', 5.0),
    (4, 'Laurel Path', 1.5),
    (5, 'Maple Avenue', 4.0),
    (6, 'Cypress Court', 2.0),
    (7, 'Main Street', 6.2)
]

# Houses
houses_data = [
    (1, 1, 150, 10),
    (2, 1, 200, 22),
    (3, 2, 50, 13),
    (4, 3, 300, 14),
    (5, 3, 100, 12),
    (6, 4, 200, 21),
    (7, 5, 580, 32),
    (8, 5, 20, 1),
    (9, 6, 30, 12),
    (10, 7, 620, 30),
    (11, 2, 580, 21),
    (12, 4, 60, 12),
    (13, 6, 40, 10),
    (14, 5, 70, 20),
    (15, 3, 90, 16),
    (16, 3, 50, 14)
]

# Inserting
cursor.executemany('INSERT INTO streets (id, name, length) VALUES (?, ?, ?)', streets_data)
cursor.executemany('INSERT INTO houses (id, street_id, tenants, floors) VALUES (?, ?, ?, ?)', houses_data)


conn.commit()


# Function of getting the three longest streets with fewer than 500 residents
def find_longest_streets(conn):
    query = '''
    SELECT s.id, s.name, s.length
    FROM streets s
    JOIN (
        SELECT h.street_id, SUM(h.tenants) AS total_tenants
        FROM houses h
        GROUP BY h.street_id
    ) AS grouped_houses ON s.id = grouped_houses.street_id
    WHERE grouped_houses.total_tenants < 500
    ORDER BY s.length DESC
    LIMIT 3
    '''

    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    
    return results


# Usage

longest_streets = find_longest_streets(conn)
for street in longest_streets:
    print(f'Street ID: {street[0]}, Name: {street[1]}, Length: {street[2]} km')

conn.close()

