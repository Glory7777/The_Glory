#https://qt3b1s62da6s.tistory.com/547 참조사이트
#https://thesool.com/front/find/M000000082/list.do 크롤링?

import pandas as pd
import sqlite3

# Read csv file.
df = pd.read_csv("../API/전통주_API_DATA.csv")

# Connect to (create) database.
database = "db.sqlite3"
conn = sqlite3.connect(database)
dtype={


    "size": "CharField",
    "perecent": "IntegerField",
    "name":"CharField",
    "company" : "CharField",
    "mtrl" : "CharField"
}

df.to_sql(name='traditional_liq', con=conn, if_exists='replace', dtype=dtype, index=True, index_label="id")

# Remove duplicates from 'traditional_liq' based on 'id'
query = """
DELETE FROM traditional_liq 
WHERE id NOT IN (
    SELECT MIN(id) 
    FROM traditional_liq 
    GROUP BY 규격, 도수, 전통주명, 제조사, 주원료
)
"""
conn.execute(query)

# Drop the temporary table
conn.execute('DROP TABLE IF EXISTS temporary_table')

conn.close()

