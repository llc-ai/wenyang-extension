import sqlite3

conn = sqlite3.connect('wenyang.db')
c = conn.cursor()

sql_table_wenyang = """
    create table if not exists wenyang (
        period TEXT,
        content TEXT,
        race TEXT,
        isAI TEXT,
        pic TEXT
    )
"""
sql_table_type = "create table if not exists types (typeName TEXT, typeValue TEXT)"

sql_insert_wenyang = "insert into wenyang values (?,?,?,?,?)"

c.execute(sql_table_wenyang)
c.execute(sql_table_type)

conn.close()

def insertWenyang(rows):
        connect = sqlite3.connect('wenyang.db')
        cc = connect.cursor()
        cc.executemany(sql_insert_wenyang, rows)
        connect.commit()
        connect.close()

def query(period, content, race, isAI):
        connect = sqlite3.connect('wenyang.db')
        cc = connect.cursor()
        cc.execute(f"""
            select pic from wenyang where period = '{period}' and content = '{content}' and isAI = '{isAI}'
        """)
        result = cc.fetchall()
        connect.close()
        return result

def queryType(type):
        connect = sqlite3.connect('wenyang.db')
        cc = connect.cursor()
        cc.execute(f"""
                    select distinct({type}) from wenyang
                """)
        result = cc.fetchall()
        connect.close()

        return [x[0] for x in result]
def img_save_dir():
        return "../data"

def test():
        connect = sqlite3.connect('wenyang.db')
        cc = connect.cursor()
        cc.execute(f"""
            select * from wenyang
        """)
        result = cc.fetchall()
        connect.close()
        return result

r = test()
print(r)

