from tkinter import *
from datetime import datetime
from tkcalendar import DateEntry
import tkinter.ttk as ttk
import tkinter as tk
from Database import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from sms_send import Send_SMS

def GateInForm(master):
    GeteIn_Form = Toplevel(master)
    GeteIn_Form.geometry("1200x440+190+130")

    gatepass = IntVar()

    def on_start():
        clear_entries()
        sql = "SELECT gate_pass_no, std_id, date_out, reason FROM gate_pass_master WHERE pass_status = 1 and college_id = %s"
        db_cursor.execute(sql, (clg_id,))
        data = db_cursor.fetchall()
        gid = ""
        nm = ""
        mobile = ""
        dt = ""
        reason = ""
        List_Data.delete(*List_Data.get_children())
        if db_cursor.rowcount != 0:
            for row in data:
                gid = row[0]

                sql2 = "SELECT ac_name, ac_contact FROM gate_pass_account_master WHERE std_id = %s and college_id = %s"
                db_cursor.execute(sql2, (row[1], clg_id))
                data2 = db_cursor.fetchall()
                nm = data2[0][0]
                mobile = data2[0][1]

                dt = datetime.strftime(row[2], "%d/%m/%Y")
                reason = row[3]
                List_Data.insert("", 'end', text=gid, values=(gid, nm, mobile, dt, reason))

        sql2 = "SELECT mid, watchman_name FROM gate_pass_watchman_details WHERE college_id = %s"
        db_cursor.execute(sql2,(clg_id,))
        data2 = db_cursor.fetchall()

        for i,j in data2:
            lst_watchman[i] = j

        TxtWatchman['values'] = list(lst_watchman.values())

    def ChangeText(val):
        if val == 'G':
            LblSearchBy1['text'] = 'Gatepass No'
        if val == 'N':
            LblSearchBy1['text'] = 'Name'

    def clear_entries():
        TxtReason.delete(0, END)
        TxtContactS.delete(0, END)
        TxtName.delete(0, END)
        TxtReason.delete(0, END)
        TxtSearchBy.delete(0,END)
        TxtOutTime["text"] = ""

    def show_selected_record(event):
        for selection in List_Data.selection():
            item = List_Data.item(selection)

        clear_entries()
        i1 = item["values"]
        TxtSearchBy.insert(0,i1[0])
        TxtName.insert(0,i1[1])
        TxtContactS.insert(0,str(i1[2]))
        TxtOutTime["text"] = i1[3]
        TxtReason.insert(0,i1[4])
        TxtWatchman.focus()
        TxtWatchman.event_generate('<Down>')

    def Save_Data():
        dt1 = datetime.strftime(datetime.now(),"%Y-%m-%d")
        dt2 = datetime.strftime(datetime.now(),"%I:%M %p")

        n1 = TxtSearchBy.get()
        n2_ = TxtWatchman.get()
        n2 = 0
        for i,j in lst_watchman.items():
            if n2_ == j:
                n2 = i
        if n1 != "":
            sql1 = "UPDATE gate_pass_master SET date_in = %s, time_in = %s, w_id_in = %s, pass_status = 0 WHERE gate_pass_no = %s and college_id = %s"
            db_cursor.execute(sql1, (dt1, dt2, n2, n1, clg_id))
            db_connection.commit()
            
            
            
            messagebox.showinfo("Success", "Successful...",parent=GeteIn_Form)
            on_start()



    clg_id = 1
    lst_watchman = {}
    
    Frm1 = LabelFrame(GeteIn_Form, height=420, width=680, bg='#518aed')
    Frm1.place(x=10, y=10)

    LblHead = Label(Frm1, text="Gate In Form", bg='#518aed', fg='white', font=('Times New Roman',35))
    LblHead.place(x=180,y=10)

    LblDate = Label(Frm1, text="Date",font=('Times New Roman',15), bg='#518aed', fg='white')
    LblDate.place(x=450,y=70)
    TxtDate = DateEntry(Frm1, width=12, background='darkblue', foreground='white', borderwidth=2, locale='en_US', date_pattern='dd-mm-yyyy', font = ('Times New Roman',15))
    TxtDate.place(x=510,y=70)

    Frm2 = LabelFrame(Frm1, height=50, width=550, bg='#518aed')
    Frm2.place(x=50,y=120)

    Frm3 = LabelFrame(Frm1, height=220, width=630, bg='#518aed')
    Frm3.place(x=20,y=180)

    LblSearchBy = Label(Frm2, text="Search By", font=('Times New Roman',20), bg='#518aed', fg='white')
    LblSearchBy.place(x=10, y=5)

    BtnGatePass = Radiobutton(Frm2, variable=gatepass, value='G',text='Gatepass No', font=('Times New Roman',20), bg='#518aed', fg='white', command=lambda x = 'G':ChangeText(x))
    BtnGatePass.place(x=200,y=1)
    BtnName = Radiobutton(Frm2, variable=gatepass, value='N', text='Name', font=('Times New Roman',20), bg='#518aed', fg='white', command=lambda x = 'N':ChangeText(x))
    BtnName.place(x=400,y=1)
    BtnGatePass.select()

    LblSearchBy1 = Label(Frm3, text="Gatepass No", font=('Times New Roman',17), bg='#518aed', fg='white')
    LblSearchBy1.place(x=5, y=5)
    TxtSearchBy = Entry(Frm3, width=20, font=('Times New Roman',17))
    TxtSearchBy.place(x=140,y=5)

    BtnSearch = Button(Frm3, text='Search', width=8, font=('Times New Roman',14), bg='brown', fg='white')
    BtnSearch.place(x=370,y=5)

    TxtDateSearch = DateEntry(Frm3, width=12, background='darkblue', foreground='white', borderwidth=2, locale='en_US', date_pattern='dd-mm-yyyy', font = ('Times New Roman',15))
    TxtDateSearch.place(x=470,y=5)

    LblName = Label(Frm3, text="Name", font=('Times New Roman',17), bg='#518aed', fg='white')
    LblName.place(x=20, y=45)
    TxtName = Entry(Frm3, width=25, font=('Times New Roman',17))
    TxtName.place(x=150,y=45)

    LblContactS = Label(Frm3, text="Contact No", font=('Times New Roman',17), bg='#518aed', fg='white')
    LblContactS.place(x=20, y=85)
    TxtContactS = Entry(Frm3, width=11, font=('Times New Roman',17))
    TxtContactS.place(x=150,y=85)

    LblCity = Label(Frm3, text="Reason", font=('Times New Roman',17), bg='#518aed', fg='white')
    LblCity.place(x=300, y=85)
    TxtReason = Entry(Frm3, width=21, font=('Times New Roman',17))
    TxtReason.place(x=380,y=85)

    LblWatchman = Label(Frm3, text="Watchman", font=('Times New Roman',17), bg='#518aed', fg='white')
    LblWatchman.place(x=20, y=125)
    TxtWatchman = Combobox(Frm3, width=10, font=('Times New Roman',17))
    TxtWatchman.place(x=150,y=125)

    LblOutTime = Label(Frm3, text="Out Date :", font=('Times New Roman',17), bg='#518aed', fg='white')
    LblOutTime.place(x=310, y=125)
    TxtOutTime = Label(Frm3, text='', font=('Times New Roman',17), bg='#518aed', fg='white')
    TxtOutTime.place(x=420,y=125)

    BtnSave = Button(Frm3, text="Save", font=('Times New Roman',15), bg='#518aed',  fg='white', width=10, command=Save_Data)
    BtnSave.place(x=40,y=165)

    BtnReset = Button(Frm3, text="Reset", font=('Times New Roman',15), bg='#518aed', fg='white', width=10)
    BtnReset.place(x=180,y=165)

    BtnExit = Button(Frm3, text="Exit", font=('Times New Roman',15), bg='#518aed', fg='white', width=10)
    BtnExit.place(x=320,y=165)

    columns = ('#1', '#2', '#3', "#4")
    List_Data = ttk.Treeview(GeteIn_Form,show="headings",height="10", columns=columns)
    List_Data.heading('#1', text='GatePass No', anchor='center')
    List_Data.column('#1', width=80, anchor='center', stretch=False)
    List_Data.heading('#2', text='Name', anchor='center')
    List_Data.column('#2', width=150, anchor='w', stretch=True)
    List_Data.heading('#3', text='Contact No', anchor='center')
    List_Data.column('#3', width=80, anchor='center', stretch=True)
    List_Data.heading('#4', text='Date Out', anchor='center')
    List_Data.column('#4', width=80, anchor='center', stretch=True)
    List_Data.place(x=710, y=10, height=420, width=450)  

    vsb= ttk.Scrollbar(GeteIn_Form, orient=tk.VERTICAL,command=List_Data.yview)  
    vsb.place(x=1160, y=10, height=420)
    List_Data.configure(yscroll=vsb.set)

    List_Data.delete(*List_Data.get_children())

    List_Data.bind("<Double-1>", show_selected_record)
    on_start()

    GeteIn_Form.mainloop()

#GateInForm()