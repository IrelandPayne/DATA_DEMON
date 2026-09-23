#sql/db notes 

import sqlite3

conn = sqlite3.connect(':memory:')
conn

#connecting a db to a file
conn2 = sqlite3.connect('test.sqlite')
conn2

#connecting to an object 
#the object manages the db connection 
#need a cursor to manage state
#cursor sends queries and contains results 
conn = sqlite3.connect('biblio.sqlite')
cursor = conn.cursor()

#setting up a db, use create
cq = '''CREATE TABLE books (
    title TEXT, author TEXT, date INTEGER
    )'''
cursor.execute(cq)

#creating entries
iq = '''INSERT INTO books VALUES (
        '2001: A Space Odyssy',
        'Arthur C. Clarke',
        '1951'
        )'''
cursor.execute(iq)

#scaling up
#can be impractical at scale, larger num of records can be created with executemany()
data = [
    ("I, Robot", "Isacc Asimov", 1950),
    ("Mona's Eyes", "Brady Shell", 2025)
]

#map data tuples onto a query using the ? placeholder 
imq = '''INSERT INTO books VALUES (?,?,?)'''
cursor.executemany(imq, data)

#read <- to view data in the db, use READ
#fetchall() can be used to get all results as a list 
sq = '''SELECT title FROM books'''
books = cursor.execute(sq).fetchall()
print(books)
#result:
[('2001: A Space Odyssy',), ('I, Robot',), ('Mona\'s Eyes',)]

#verify updates
vq = '''SELECT * 
            FROM books
            WHERE title = "Mona\'s Eyes" '''
cursor.execute(vq)
print(cursor.fetchall())
#reuslt:
[('Mona\s Eyes', 'Brady Shell', 2025)]

#delete info
dq = '''DELETE
            FROM books 
            WHERE author = "Brady Shell" '''
cursor.execute(dq)

#all of the above occurs in-memory 
#to presist, changes must be committed, which saves them 
#you should commit frequently in practice 
conn.commit()
conn.close()

#selecting normalized data 
#have to use SQLs JOIN syntax
#specify fields to match on, like linking foreign keys to pks
jq = '''SELECT authors.name, books.title, books.year
        FROM books JOIN authors
        ON books.author_id = author.id'''
books = cursor.execute(join_query, filter).fetchall()