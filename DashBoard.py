from tkinter import *
from PIL import ImageTk, Image
from GatePass import GatePassForm
from GateIn import GateInForm
from NewStudent import NewStudentForm
from NewHostel import HostelAdd
from NewWatchman import WatchmanNew
from Database import *
from report_daily import Daily_Report
from report_weekly import Weekly_Report
from datetime import datetime
import tkinter as tk

def DashScreen(cid):
    def Refresh_Data():
        sql1 = "SELECT count(std_id) FROM gate_pass_account_master WHERE college_id = %s"
        db_cursor.execute(sql1,(clg_id,))
        data1 = db_cursor.fetchall()

        sql2 = "SELECT count(id) FROM gate_pass_master WHERE pass_status = 1 and college_id = %s"
        db_cursor.execute(sql2,(clg_id,))
        data2 = db_cursor.fetchall()

        LblTotalCount['text'] = f"{data2[0][0]} / {data1[0][0]}"

        dt1 = datetime.strftime(datetime.now(),"%Y-%m-%d")

        sql3 = "SELECT count(id) FROM gate_pass_master WHERE date_out = %s and pass_status = 1 and college_id = %s"
        db_cursor.execute(sql3,(dt1, clg_id,))
        data3 = db_cursor.fetchall()

        LblTotalCountToday['text'] = str(data3[0][0])

        #LblTotalCountBoys
        sql4 = "SELECT count(gate_pass_master.id) FROM gate_pass_master INNER JOIN gate_pass_account_master on gate_pass_account_master.std_id = gate_pass_master.std_id WHERE gate_pass_account_master.ac_type = 'Male' and gate_pass_master.pass_status = 1 and gate_pass_master.college_id = %s"
        db_cursor.execute(sql4,(clg_id,))
        data4 = db_cursor.fetchall()
        LblTotalCountBoys['text'] = str(data4[0][0])

        sql5 = "SELECT count(gate_pass_master.id) FROM gate_pass_master inner join gate_pass_account_master on gate_pass_account_master.std_id = gate_pass_master.std_id WHERE gate_pass_account_master.ac_type = 'Female' and gate_pass_master.pass_status = 1 and gate_pass_master.college_id = %s"
        db_cursor.execute(sql5,(clg_id,))
        data5 = db_cursor.fetchall()

        LblTotalCountGirl['text'] = str(data5[0][0])

    def OpenForm(val):
        if val == 1:
            NewStudentForm(dash_screen)
        if val == 2:
            WatchmanNew(dash_screen)
        if val == 3:
            HostelAdd(dash_screen)
        if val == 4:
            HostelAdd(dash_screen)
        if val == 5:
            GatePassForm(dash_screen)
        if val == 6:
            GateInForm(dash_screen)
        if val == 7:
            Daily_Report(dash_screen)
        if val == 8:
            Weekly_Report(dash_screen)
        if val == 11:
            Refresh_Data()

    dash_screen = tk.Tk()
    dash_screen.state("zoomed")
    dash_screen.title("Dashboard")
    clg_id = 1
    Frm1 = Frame(dash_screen, height=150, width=1600, bg='lightgrey')
    Frm1.place(x=0,y=0)
    Frm2 = Frame(dash_screen, height=664, width=1600, bg='white')
    Frm2.place(x=0,y=150)

    image1 = Image.open("./Images/PVPIT.jpg")
    resized_image= image1.resize((1600,624), Image.LANCZOS)

    img = ImageTk.PhotoImage(resized_image)
    label = Label(Frm2, image = img)
    label.pack()

    menubar = Menu(dash_screen)

    NewRegister = Menu(menubar, tearoff=0)
    NewRegister.add_command(label="Student", command = lambda x = 1 : OpenForm(x))
    NewRegister.add_command(label="Watchman", command = lambda x = 2 : OpenForm(x))
    NewRegister.add_command(label="Hostel", command = lambda x = 3 : OpenForm(x))
    NewRegister.add_command(label="miscellaneous", command = lambda x = 4 : OpenForm(x))
    menubar.add_cascade(label="New", menu=NewRegister)

    ReceiptMenu = Menu(menubar, tearoff=0)
    ReceiptMenu.add_command(label="Gate-Pass", command= lambda x = 5 : OpenForm(x))
    ReceiptMenu.add_command(label="Gate-In", command= lambda x = 6 : OpenForm(x))
    menubar.add_cascade(label="Receipt", menu=ReceiptMenu)

    RecordMenu = Menu(menubar, tearoff=0)
    RecordMenu.add_command(label="Daily", command=lambda x = 7 :OpenForm(x))
    RecordMenu.add_command(label="Weekly", command=lambda x = 8 :OpenForm(x))
    RecordMenu.add_command(label="Monthly", command=OpenForm)
    RecordMenu.add_command(label="Yearly", command=OpenForm)
    menubar.add_cascade(label="Report", menu=RecordMenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Refresh", command=lambda x = 11:OpenForm(x))
    helpmenu.add_command(label="About...", command=OpenForm)

    menubar.add_cascade(label="Help", menu=helpmenu)

    dash_screen.config(menu=menubar)

    Frm3 = Frame(Frm1,width=300, height=140, bg='#4284f5')
    Frm3.place(x=5,y=5)

    Frm4 = Frame(Frm1,width=300, height=140, bg='#4284f5')
    Frm4.place(x=315,y=5)

    Frm5 = Frame(Frm1,width=300, height=140, bg='#4284f5',border=5)
    Frm5.place(x=625,y=5)

    Frm6 = Frame(Frm1,width=300, height=140, bg='#4284f5')
    Frm6.place(x=935,y=5)

    Frm7 = Frame(Frm1,width=280, height=140, bg='#4284f5')
    Frm7.place(x=1245,y=5)

    BtnGatePass = Button(Frm3, text='Gate-Pass', font=('Times New Roman',18), bg='#4284f5', fg='white',width=23, command= lambda x = 5 : OpenForm(x))
    BtnGatePass.place(x=0,y=5)
    BtnGateIn = Button(Frm3, text='Gate-In', font=('Times New Roman',18), bg='#4284f5', fg='white',width=23, command= lambda x = 6 : OpenForm(x))
    BtnGateIn.place(x=0,y=70)

    LblTotalCount = Label(Frm4, text='', font=('Times New Roman',30), bg='#4284f5', fg='white')
    LblTotalCount.place(x=70, y=30)
    LblTotalStd = Button(Frm4, text='Total Out Students', font=('Times New Roman',15), bg='#4284f5', fg='white', width=27)
    LblTotalStd.place(x=0,y=95)

    LblTotalCountToday = Label(Frm5, text='0', font=('Times New Roman',30), bg='#4284f5', fg='white')
    LblTotalCountToday.place(x=130, y=30)
    LblTotal = Label(Frm5, text="Today's Out Students", font=('Times New Roman',18), bg='#4284f5', fg='white')
    LblTotal.place(x=50,y=100)

    LblTotalCountBoys = Label(Frm6, text='0', font=('Times New Roman',30), bg='#4284f5', fg='white')
    LblTotalCountBoys.place(x=130, y=30)
    LblTotal = Label(Frm6, text="Total Boys Out", font=('Times New Roman',18), bg='#4284f5', fg='white')
    LblTotal.place(x=80,y=100)

    LblTotalCountGirl = Label(Frm7, text='0', font=('Times New Roman',30), bg='#4284f5', fg='white')
    LblTotalCountGirl.place(x=130, y=30)
    LblTotal = Label(Frm7, text="Total Girls Out", font=('Times New Roman',18), bg='#4284f5', fg='white')
    LblTotal.place(x=80,y=100)
    OpenForm(11)
    dash_screen.mainloop()

DashScreen(1)