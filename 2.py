import mysql.connector

db_connection = mysql.connector.connect(host="119.18.54.81", user="agitsgag_pvpit_stud_feedback", password="Rq0o6rTE6IqN")
db_cursor = db_connection.cursor(buffered=True)
db_cursor.execute("use agitsgag_pvpit_stud_feedback")