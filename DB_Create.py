#!/usr/bin/env python3
import sqlite3
from VAR import *
###############################

sqliteConnection = sqlite3.connect(f'{GUILD}.db')

cursor = sqliteConnection.cursor()

sqlite_Create_query1 = (f'''CREATE TABLE IF NOT EXISTS scholar (
id INTEGER PRIMARY KEY,
Account TEXT NOT NULL UNIQUE,
D_ID TEXT NOT NULL UNIQUE,
Wallet TEXT NOT NULL UNIQUE )''')

cursor.execute(sqlite_Create_query1)

sqlite_Create_query2 =(f'''PRAGMA auto_vacuum = FULL;''')

sqliteConnection.commit()

cursor.execute(sqlite_Create_query2)

cursor.close()
