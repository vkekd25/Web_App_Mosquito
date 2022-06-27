import os
import sqlite3


DB_FILENAME = "mosquito_db.sqlite3"
DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)
conn = sqlite3.connect(DB_FILEPATH)
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS mosquito;''')
cur.execute("""CREATE TABLE mosquito(
                Id PRIMARY KEY,
                날짜 VARCHAR(128),
                모기지수 FLOAT,
                '강수량(mm)' FLOAT,
                '평균기온(C)' FLOAT,
                '최저기온(C)' FLOAT,
                '최대기온(C)' FLOAT
                );
            """)
conn.commit()

import csv
f = open('/Users/byungwookkang/Section3/sc3_project/mosquito.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)


cur.executemany("""INSERT INTO mosquito(Id, 날짜, 모기지수, '강수량(mm)', '평균기온(C)', '최저기온(C)', '최대기온(C)')
                    VALUES(?,?,?,?,?,?,?);""", list(rdr)[1:])
conn.commit()

