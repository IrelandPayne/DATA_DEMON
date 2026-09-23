# Detailed SQL Notes

#creating a db table 
import sqlite3

conn = sqlite3.connect('music.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Track')
cur.execute('CREATE TABLE Track (title TEXT, plays INTEGER)')

conn.close()

#inserting 2 new rows of data into the table 
import sqlite3

conn = sqlite3.connect('music.sqlite')
cur = conn.cursor()

cur.execute('INSERT INTO Track (title, plays) VALUES (?, ?)',
    ('Thunderstruck', 20))
cur.execute('INSERT INTO Track (title, plays) VALUES (?, ?)',
    ('My Way', 15))
conn.commit()

#using SELECT command to retrieve rows we just inserted
print('Track:')
cur.execute('SELECT title, plays FROM Track')
for row in cur: #each row is python tuple
     print(row)

#execute command to DELETE rows, must use WHERE
cur.execute('DELETE FROM Track WHERE plays < 100')
conn.commit()

cur.close()

#output is as follows: 

#Track:
#('Thunderstruck', 20)
#('My Way', 15)

#another example: 

import sqlite3

conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

handle = open('tracks.csv')

for line in handle:
    line = line.strip()
    pieces = line.split(',')
    if len(pieces) != 6 : continue

    name = pieces[0]
    artist = pieces[1]
    album = pieces[2]
    count = pieces[3]
    rating = pieces[4]
    length = pieces[5]

    print(name, artist, album, count, rating, length)

#repeating INSERT OR IGNORE followed by SELECT to get the appropriate artist_id for use in later INSERT statements 
    cur.execute('''INSERT OR IGNORE INTO Artist (name)
        VALUES ( ? )''', ( artist, ) )
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    artist_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id)
        VALUES ( ?, ? )''', ( album, artist_id ) )
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, len, rating, count)
        VALUES ( ?, ?, ?, ?, ? )''',
        ( name, album_id, length, rating, count ) )

    conn.commit()
    
# now following the SQLite tutorial 

#to create a connection to the database tutorial.db in the current working directory, or create it if it dosent exist: 
import sqlite3
con = sqlite3.connect("tutorial.db")

#the returned object con represents the connection on the on-disl db 

#to execute/fetch SQL queries, need a db cursor.
#call con.cursor() to create the Cursor: 

cur = con.cursor()

#now that conneciton is established, can create table called movie 

cur.execute("CREATE TABLE move(title, year, score)")

#verifying the table has been created by quering sqlite_master table built-in to SQLite
res = cur.execute("SELECT name FROM sqlite_master")
res.featchone()
#returns ('movie',)

#we see that the table has been created! query returns a tuple 

# add two rows of data suppled as SQL literals by executing an INSERT statement
cur.execute("""
            INSERT INTO movie VALUES
            ('Monty Python and the Holy Grail', 1975, 8.2),
            ('And Now for Something Completely Different', 1971, 7.5)
            """)
#connect object to commit the transaction
con.commit()

#check if data was inserted correctly 
res = cur.execute("SELECT score FROM movie")
res.featchall()
#returns list of tuples 
#output: [(8.2, ), (7.5, )]

#insert 3 more rows: 
data = [
    ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
    ("Monty Python's The Meaning of Life", 1983, 7.5),
    ("Monty Python's Life of Brian", 1979, 8.0),
]
#using ? as placeholders used to bind "data" to the query
#always use placeholders for string formatting to bind python to SQL
#to avoid SQL injection attacks 
cur.executemany("INSERT INTO movie VALUES(?,?,?)", data)
con.commit() 

#verify new rows: 
for row in cur.execute("SELECT year, title FROM movie ORDER BY year"):
    print(row)
#output: 
#(1971, 'And Now for Something Completely Different')
#(1975, 'Monty Python and the Holy Grail')
#(1979, "Monty Python's Life of Brian")
#(1982, 'Monty Python Live at the Hollywood Bowl')
#(1983, "Monty Python's The Meaning of Life")

#verify the db has been written to the disk by calling 
con.close()

#to close the existing connection
#then open a new one 
new_con = sqlite3.connect("tutorial.db")
new_cur = new_con.cursor()

#the query the db: 
res = new_cur.execute("SELECT title, year FROM movie ORDER BY score DESC")
title, year = res.fetchone()
print(f'The highest scoring Monty Python movie is {title!r}, released in {year}')