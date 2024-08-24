import mysql.connector

db_connection = mysql.connector.connect(host="localhost", user="root", password="omicron")
db_cursor = db_connection.cursor(buffered=True)
db_cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_f") 
db_cursor.execute("use inventory_f")

def Max_No(tb_name, col_name, cid):
    id_no = 0
    query = f"SELECT {col_name} FROM {tb_name} where college_id = {cid}"
    db_cursor.execute(query)
    db_cursor.rowcount
    if db_cursor.rowcount == 0:
        id_no = 1 
    else:
        rows = db_cursor.fetchall()  
        for row in rows:  
            id_no = row[0]
            id_no = id_no + 1
    return id_no