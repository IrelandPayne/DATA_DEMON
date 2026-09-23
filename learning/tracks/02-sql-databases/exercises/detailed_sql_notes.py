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

#----
#more helpful notes from sebastianraschka
#creating a new SQLite db 

import sqlite3

sqlite_file = 'my_first_db.sqlite'    # name of the sqlite database file
table_name1 = 'my_table_1'  # name of the table to be created
table_name2 = 'my_table_2'  # name of the table to be created
new_field = 'my_1st_column' # name of the column
field_type = 'INTEGER'  # column data type

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Creating a new SQLite table with 1 column
c.execute('CREATE TABLE {tn} ({nf} {ft})'\
        .format(tn=table_name1, nf=new_field, ft=field_type))

# Creating a second table with 1 column and set it as PRIMARY KEY
# note that PRIMARY KEY column must consist of unique values!
c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
        .format(tn=table_name2, nf=new_field, ft=field_type))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()

# --- 
#adding new columns in the db 
import sqlite3

sqlite_file = 'my_first_db.sqlite'    # name of the sqlite database file
table_name = 'my_table_2'   # name of the table to be created
id_column = 'my_1st_column' # name of the PRIMARY KEY column
new_column1 = 'my_2nd_column'  # name of the new column
new_column2 = 'my_3nd_column'  # name of the new column
column_type = 'TEXT' # E.g., INTEGER, TEXT, NULL, REAL, BLOB
default_val = 'Hello World' # a default value for the new column rows

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# A) Adding a new column without a row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=new_column1, ct=column_type))

# B) Adding a new column with a default row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct} DEFAULT '{df}'"\
        .format(tn=table_name, cn=new_column2, ct=column_type, df=default_val))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()

# --- 
#inserting and updating rows 
import sqlite3

sqlite_file = 'my_first_db.sqlite'
table_name = 'my_table_2'
id_column = 'my_1st_column'
column_name = 'my_2nd_column'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# A) Inserts an ID with a specific value in a second column
try:
    c.execute("INSERT INTO {tn} ({idf}, {cn}) VALUES (123456, 'test')".\
        format(tn=table_name, idf=id_column, cn=column_name))
except sqlite3.IntegrityError:
    print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))

# B) Tries to insert an ID (if it does not exist yet)
# with a specific value in a second column
c.execute("INSERT OR IGNORE INTO {tn} ({idf}, {cn}) VALUES (123456, 'test')".\
        format(tn=table_name, idf=id_column, cn=column_name))

# C) Updates the newly inserted or pre-existing entry            
c.execute("UPDATE {tn} SET {cn}=('Hi World') WHERE {idf}=(123456)".\
        format(tn=table_name, cn=column_name, idf=id_column))

conn.commit()
conn.close()

#---
#selecting entries 
import sqlite3

sqlite_file = 'my_first_db.sqlite'    # name of the sqlite database file
table_name = 'my_table_2'   # name of the table to be queried
id_column = 'my_1st_column'
some_id = 123456
column_2 = 'my_2nd_column'
column_3 = 'my_3rd_column'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# 1) Contents of all columns for row that match a certain value in 1 column
c.execute('SELECT * FROM {tn} WHERE {cn}="Hi World"'.\
        format(tn=table_name, cn=column_2))
all_rows = c.fetchall()
print('1):', all_rows)

# 2) Value of a particular column for rows that match a certain value in column_1
c.execute('SELECT ({coi}) FROM {tn} WHERE {cn}="Hi World"'.\
        format(coi=column_2, tn=table_name, cn=column_2))
all_rows = c.fetchall()
print('2):', all_rows)

# 3) Value of 2 particular columns for rows that match a certain value in 1 column
c.execute('SELECT {coi1},{coi2} FROM {tn} WHERE {coi1}="Hi World"'.\
        format(coi1=column_2, coi2=column_3, tn=table_name, cn=column_2))
all_rows = c.fetchall()
print('3):', all_rows)

# 4) Selecting only up to 10 rows that match a certain value in 1 column
c.execute('SELECT * FROM {tn} WHERE {cn}="Hi World" LIMIT 10'.\
        format(tn=table_name, cn=column_2))
ten_rows = c.fetchall()
print('4):', ten_rows)

# 5) Check if a certain ID exists and print its column contents
c.execute("SELECT * FROM {tn} WHERE {idf}={my_id}".\
        format(tn=table_name, cn=column_2, idf=id_column, my_id=some_id))
id_exists = c.fetchone()
if id_exists:
    print('5): {}'.format(id_exists))
else:
    print('5): {} does not exist'.format(some_id))

# Closing the connection to the database file
conn.close()

#--- 
# date and time ops 
import sqlite3

sqlite_file = 'my_first_db.sqlite'    # name of the sqlite database file
table_name = 'my_table_3'   # name of the table to be created
id_field = 'id' # name of the ID column
date_col = 'date' # name of the date column
time_col = 'time'# name of the time column
date_time_col = 'date_time' # name of the date & time column
field_type = 'TEXT'  # column data type

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Creating a new SQLite table with 1 column
c.execute('CREATE TABLE {tn} ({fn} {ft} PRIMARY KEY)'\
        .format(tn=table_name, fn=id_field, ft=field_type))

# A) Adding a new column to save date insert a row with the current date
# in the following format: YYYY-MM-DD
# e.g., 2014-03-06
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}'"\
         .format(tn=table_name, cn=date_col))
# insert a new row with the current date and time, e.g., 2014-03-06
c.execute("INSERT INTO {tn} ({idf}, {cn}) VALUES('some_id1', DATE('now'))"\
         .format(tn=table_name, idf=id_field, cn=date_col))

# B) Adding a new column to save date and time and update with the current time
# in the following format: HH:MM:SS
# e.g., 16:26:37
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}'"\
         .format(tn=table_name, cn=time_col))
# update row for the new current date and time column, e.g., 2014-03-06 16:26:37
c.execute("UPDATE {tn} SET {cn}=TIME('now') WHERE {idf}='some_id1'"\
         .format(tn=table_name, idf=id_field, cn=time_col))

# C) Adding a new column to save date and time and update with current date-time
# in the following format: YYYY-MM-DD HH:MM:SS
# e.g., 2014-03-06 16:26:37
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}'"\
         .format(tn=table_name, cn=date_time_col))
# update row for the new current date and time column, e.g., 2014-03-06 16:26:37
c.execute("UPDATE {tn} SET {cn}=(CURRENT_TIMESTAMP) WHERE {idf}='some_id1'"\
         .format(tn=table_name, idf=id_field, cn=date_time_col))

# The database should now look like this:
# id         date           time        date_time
# "some_id1" "2014-03-06"   "16:42:30"  "2014-03-06 16:42:30"

# 4) Retrieve all IDs of entries between 2 date_times
c.execute("SELECT {idf} FROM {tn} WHERE {cn} BETWEEN '2013-03-06 10:10:10' AND '2015-03-06 10:10:10'".\
    format(idf=id_field, tn=table_name, cn=date_time_col))
all_date_times = c.fetchall()
print('4) all entries between ~2013 - 2015:', all_date_times)

# 5) Retrieve all IDs of entries between that are older than 1 day and 12 hrs
c.execute("SELECT {idf} FROM {tn} WHERE DATE('now') - {dc} >= 1 AND DATE('now') - {tc} >= 12".\
    format(idf=id_field, tn=table_name, dc=date_col, tc=time_col))
all_1day12hrs_entries = c.fetchall()
print('5) entries older than 1 day:', all_1day12hrs_entries)

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()

#--- 
#retrieving column names 
import sqlite3

sqlite_file = 'my_first_db.sqlite'
table_name = 'my_table_3'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Retrieve column information
# Every column will be represented by a tuple with the following attributes:
# (id, name, type, notnull, default_value, primary_key)
c.execute('PRAGMA TABLE_INFO({})'.format(table_name))

# collect names in a list
names = [tup[1] for tup in c.fetchall()]
print(names)
# e.g., ['id', 'date', 'time', 'date_time']

# Closing the connection to the database file
conn.close()