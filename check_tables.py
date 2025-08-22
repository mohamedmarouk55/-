#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('management_system.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print('الجداول الموجودة في قاعدة البيانات:')
for table in tables:
    print(f'  - {table[0]}')

conn.close()