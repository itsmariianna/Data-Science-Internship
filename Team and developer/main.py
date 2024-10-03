import sqlite3

conn = sqlite3.connect('teams.db')
cursor = conn.cursor()

#Creating table
cursor.execute('''
CREATE TABLE IF NOT EXISTS team_tasks (
    team TEXT NOT NULL,
    developer TEXT NOT NULL,
    task_count INTEGER NOT NULL
)
''')

# Creatig Teams
cursor.execute("INSERT INTO team_tasks (team, developer, task_count) VALUES ('Team A', 'Bob', 5)")
cursor.execute("INSERT INTO team_tasks (team, developer, task_count) VALUES ('Team A', 'Ann', 3)")
cursor.execute("INSERT INTO team_tasks (team, developer, task_count) VALUES ('Team B', 'Kevin', 4)")
cursor.execute("INSERT INTO team_tasks (team, developer, task_count) VALUES ('Team B', 'James', 2)")
cursor.execute("INSERT INTO team_tasks (team, developer, task_count) VALUES ('Team C', 'Nancy', 6)")
cursor.execute("INSERT INTO team_tasks (team, developer, task_count) VALUES ('Team C', 'Joe', 1)")
cursor.execute("INSERT INTO team_tasks (team, developer, task_count) VALUES ('Team D', 'Michael', 7)")
cursor.execute("INSERT INTO team_tasks (team, developer, task_count) VALUES ('Team D', 'Mary', 5)")

conn.commit()

query = '''
WITH RankedDevelopers AS (
    SELECT 
        team,
        developer,
        task_count,
        ROW_NUMBER() OVER (PARTITION BY team ORDER BY task_count) AS rn
    FROM 
        team_tasks
)
SELECT 
    team,
    developer,
    task_count
FROM 
    RankedDevelopers
WHERE 
    rn = 1;
'''

cursor.execute(query)
results = cursor.fetchall()

for row in results:
    print(f"Team: {row[0]}, Developer: {row[1]}, Task Count: {row[2]}")

conn.close()

