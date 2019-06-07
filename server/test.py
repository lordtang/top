import pymysql

db = pymysql.connect('localhost','ayuan','MyNewPassWord5!','test')
cursor = db.cursor()

sql_create_table = """CREATE TABLE %s (City VARCHAR(40) NOT NULL,Count TINYINT)"""

def create_table(tableName):
    cursor.execute(sql_create_table%(tableName))

create_table('CAR')