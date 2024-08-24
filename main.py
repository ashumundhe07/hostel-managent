from tkinter import *
from Database import *
from DashBoard import DashScreen
import tkinter as tk

def check_login():
    n1 = TxtUser.get()
    n2 = TxtPass.get()
    
    if n1 != "" and n2 != "":
        sql1 = "SELECT * FROM gate_pass_college_login_details WHERE login_id = %s and password = %s"
        db_cursor.execute(sql1, (n1, n2))
        data1 = db_cursor.fetchall()
        if data1 != []:
            DashScreen(data1[0][1])


login = tk.Tk()
login.geometry("400x300+550+150")
login.title("Login")
lblHead = LabelFrame(login,height=280,width=380,bg='grey')
lblHead.place(x=10,y=10)

lblHeading = Label(lblHead, text='Login', font=('Times New Roman',30),fg='blue',bg='grey')
lblHeading.place(x=130,y=10)

LblUser = Label(lblHead, text='USERNAME', font=('Times New Roman',15),bg='grey')
LblUser.place(x=20,y=110)
TxtUser = Entry(lblHead, font=('Times New Roman',15),bg='white', bd=2)
TxtUser.place(x=160, y=110)

LblPass = Label(lblHead, text='PASSWORD', font=('Times New Roman',15),bg='grey')
LblPass.place(x=20,y=160)
TxtPass = Entry(lblHead, font=('Times New Roman',15),bg='white', bd=2)
TxtPass.place(x=160, y=160)

BtnLogin = Button(lblHead, text='Login', font=('Times New Roman', 12), width=10, bg='green', fg='white', command=check_login)
BtnLogin.place(x=80, y=210)

BtnExit = Button(lblHead, text='Exit', font=('Times New Roman', 12), width=10, bg='red', fg='white')
BtnExit.place(x=200, y=210)


login.mainloop()