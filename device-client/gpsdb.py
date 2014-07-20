#!/usr/bin/python 
# gpsdb.py - create gps database

import sys 
import MySQLdb 

host = "localhost"
user = "root"
passwd = "123456"
dbname = "animal"

# connect to the MySQL server 
try: 
    conn = MySQLdb.connect (host, user, passwd, db)
 
except MySQLdb.Error, e: 
    print "Error %d: %s" % (e.args[0], e.args[1]) 
    sys.exit (1) 
# create the animal table and populate it 

try:  
   cursor = conn.cursor () 
   # hapus table jika ada
   cursor.execute ("DROP TABLE IF EXISTS animal") 
   
   # buat table dengan nama animal
   cursor.execute (""" 
   CREATE TABLE animal 
   ( 
    name CHAR(40), 
    category CHAR(40) 
    ) 
    """) 
    # isi record 
    
    cursor.execute (""" 
    INSERT INTO animal (name, category) 
    VALUES 
    ('snake', 'reptile'), 
    ('frog', 'amphibian'), 
    ('tuna', 'fish'), 
    ('racoon', 'mammal') 
    """) 
    
    print "%d rows were inserted" % cursor.rowcount 
    # perform a fetch loop using fetchone() 


    cursor.execute ("SELECT name, category FROM animal") 
    while (1): 
        row = cursor.fetchone () 
        if row == None: 
            break 
        print "%s, %s" % (row[0], row[1]) 
        print "%d rows were returned" % cursor.rowcount 
 
    # perform a fetch loop using fetchall() 
    cursor.execute ("SELECT name, category FROM animal") 
    rows = cursor.fetchall () 
    for row in rows: 
        print "%s, %s" % (row[0], row[1]) 
        print "%d rows were returned" % cursor.rowcount 
# issue a query that includes data values literally in 
# the query string, then do same thing using placeholders 
    cursor.execute (""" 
    UPDATE animal SET name = 'turtle' 
    WHERE name = 'snake' 
    """) 
    print "%d rows were updated" % cursor.rowcount 
    cur_name = "snake" 
    new_name = "turtle" 
    cursor.execute (""" 
    UPDATE animal SET name = %s 
    WHERE name = %s 
    """, (new_name, cur_name)) 
    print "%d rows were updated" % cursor.rowcount 
 
# create a dictionary cursor so that column values 
# can be accessed by name rather than by position 

    cursor.close () 
    cursor = conn.cursor (MySQLdb.cursors.DictCursor) 
    cursor.execute ("SELECT name, category FROM animal") 
    result_set = cursor.fetchall () 
    for row in result_set: 
        print "%s, %s" % (row["name"], row["category"]) 
        print "%d rows were returned" % cursor.rowcount 
    cursor.close () 
except MySQLdb.Error, e: 
    print "Error %d: %s" % (e.args[0], e.args[1]) 
    sys.exit (1) 
    conn.close () 
    sys.exit (0)
    
    

