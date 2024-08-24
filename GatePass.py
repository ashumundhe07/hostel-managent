from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkcalendar import DateEntry
import tkinter.ttk as ttk
import tkinter as tk
from datetime import datetime
from Database import *
from sms_send import Send_SMS
import pandas as pd
import cv2
import time

def GatePassForm(master):
    GatePass_Form = Toplevel(master)
    GatePass_Form.geometry("700x450+400+130")
    GatePass_Form.title("Gate Pass Receipt")

    def Save_Data():
        n1 = int(LblGatePass2['text'])
        n2 = TxtNo.get()
        n3_ = TxtWatchman.get()
        n3 = 0
        for i,j in lst_watchman.items():
            if n3_ == j:
                n3 = i

        n4 = TxtReason.get()
        #dt1 = datetime.strftime(datetime.now(),"%Y-%m-%d %I:%M %p")
        dt1 = datetime.strftime(datetime.now(),"%Y-%m-%d")
        dt2 = datetime.strftime(datetime.now(),"%I:%M %p")

        msg1 = TxtName.get()
        msg2 = ""
        try:
            msg2 = msg1.split()[1]
        except:
            pass
        msg3 = TxtContactP.get()
        pst = 1
        if n1 != '' and n3_ != '' and BtnSave['text'] == 'Save':
            sql3 = "INSERT INTO gate_pass_master(gate_pass_no, std_id, w_id_out, reason, date_out, time_out, pass_status, college_id) values (%s, %s, %s, %s, %s, %s, %s, %s)"
            db_cursor.execute(sql3, (n1, n2, n3, n4, dt1, dt2, pst, clg_id))
            db_connection.commit()
            db_connection.close
            Send_SMS(msg3, msg1, msg2)

            messagebox.showinfo("Information","Successful...",parent=GatePass_Form)
            clear_form()
            
        else:
            messagebox.showerror("Error","Error...",parent=GatePass_Form)
        '''    
        if n1 != '' and n3 != '' and BtnSave['text'] == 'Update':
            sql3 = "UPDATE gate_pass_master = std_no, watchman, reason, date_out_word, gate_pass_no) values (%d, %d, %d, %d, %d)"
            db_cursor.execute(sql3, (n1, n2, n3, dt1, n4))
            db_connection.commit()

            messagebox.showinfo("Information","Successful...",parent=GatePass_Form)
        '''

    def reset():
        GatePass_Form.geometry("700x450+400+130")
        BtnShow['text'] = 'Show'
        BtnShow['command'] = expand

    def expand():
        GatePass_Form.geometry("700x680+400+80")
        BtnShow['text'] = 'Reset'
        BtnShow['command'] = reset
        dt1 = str(datetime.strftime(datetime.now(),"%Y-%m-%d"))
        
        sql = "SELECT gate_pass_no, std_id, reason FROM gate_pass_master WHERE pass_status = 1 and date_out = %s and college_id = %s"
        db_cursor.execute(sql, (dt1, clg_id))
        data = db_cursor.fetchall()
        codeid = ""
        nm = ""
        mobile = ""
        reason = ""
        List_Data.delete(*List_Data.get_children())
        if db_cursor.rowcount != 0:
            for row in data:
                codeid = row[0]
                
                sql2 = "SELECT ac_name, ac_contact FROM gate_pass_account_master WHERE std_id = %s"
                db_cursor.execute(sql2, (row[1],))
                data2 = db_cursor.fetchall()
                nm = data2[0][0]
                mobile = data2[0][1]
                reason = row[2]
                
                List_Data.insert("", 'end', text=codeid, values=(codeid, nm, mobile, reason))    

    def clear_form():
        TxtNo.delete(0, END)
        TxtName.delete(0, END)
        TxtContactS.delete(0, END)
        TxtContactP.delete(0, END)
        TxtCity.delete(0, END)
        TxtReason.delete(0, END)
        
        n1 = Max_No('gate_pass_master', 'gate_pass_no', clg_id)
        LblGatePass2['text'] = f"{n1}"
    
    def on_start():
        clear_form()
        sql2 = "SELECT id, watchman_name FROM gate_pass_watchman_details WHERE college_id = %s"
        db_cursor.execute(sql2,(clg_id,))
        data2 = db_cursor.fetchall()

        for i,j in data2:
            lst_watchman[i] = j

        TxtWatchman['values'] = list(lst_watchman.values())

    def search_data():
        n1 = TxtNo.get()
        sql1 = "SELECT ac_name, ac_contact, ac_contact_p, ac_city FROM gate_pass_account_master WHERE std_id = %s and college_id = %s"
        db_cursor.execute(sql1,(n1, clg_id))
        data1 = db_cursor.fetchall()
        if db_cursor.rowcount != 0:
            TxtName.delete(0, END)
            TxtCity.delete(0, END)
            TxtContactP.delete(0, END)
            TxtContactS.delete(0, END)
            TxtReason.delete(0, END)
            
            TxtName.insert(0, data1[0][0])
            TxtContactS.insert(0, data1[0][1])
            TxtContactP.insert(0, data1[0][2])
            TxtCity.insert(0, data1[0][3])
            
            
            TxtWatchman.focus()
            TxtWatchman.event_generate('<Down>')
        else:
            messagebox.showerror("Error", "Record not found...!!!",parent=GatePass_Form)

    def FaceScan():
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            recognizer.read('TrainImage.yml')
            
        except:
            messagebox.showerror("","Model not found,please train model",parent=master)
        
        facecasCade = cv2.CascadeClassifier('xml1.xml')
        df = pd.read_csv('StudentDetails/studentdetails.csv')
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ["Roll", "Name"]
        attendance = pd.DataFrame(columns=col_names)
        future = time.time() + 20
        
        while True:
            ___, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = facecasCade.detectMultiScale(gray, 1.2, 5)
            for (x, y, w, h) in faces:
                global Id
                Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                if conf < 70:
                    try:
                        TxtNo.delete(0, END)
                        TxtNo.insert(0, str(Id))
                        search_data()
                        aa = df.loc[df["Roll"] == Id]["Name"].values
                        tt = str(Id) + "-" + aa
                        attendance.loc[len(attendance)] = [
                                Id,
                                aa,
                            ]
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                        cv2.putText(
                            im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4
                        )
                    except:
                        messagebox.showerror("", "Student Not Found",parent=master)
                        
                    finally:
                        break
            if time.time() > future:
                break
            
            attendance = attendance.drop_duplicates(
                        ["Roll"], keep="first"
                    )
            key = cv2.waitKey(30) & 0xFF
            if key == 27:
                break
            
            cam.release()
            cv2.destroyAllWindows()
        
    
    clg_id = 1
    lst_watchman = {}

    Frm1 = LabelFrame(GatePass_Form, height=430, width=680, bg='#518aed')
    Frm1.place(x=10, y=10)

    Frm2 = LabelFrame(Frm1, height=50, width=550, bg='#518aed')
    Frm2.place(x=60, y=360)

    Frm3 = LabelFrame(GatePass_Form, height=220, width=680, bg='#518aed')
    Frm3.place(x=10, y=450)

    LblHead = Label(Frm1, text="Gate Pass Form", bg='#518aed', fg='white', font=('Times New Roman',35))
    LblHead.place(x=180,y=10)

    LblDate = Label(Frm1, text="Date",font=('Times New Roman',15), bg='#518aed', fg='white')
    LblDate.place(x=450,y=70)
    TxtDate = DateEntry(Frm1,width=12, background='darkblue', foreground='white', borderwidth=2, locale='en_US', date_pattern='dd-mm-yyyy', font = ('Times New Roman',15))
    TxtDate.place(x=510,y=70)

    LblNo = Label(Frm1, text="No", font=('Times New Roman',20), bg='#518aed', fg='white')
    LblNo.place(x=20, y=120)
    TxtNo = Entry(Frm1, width=5, font=('Times New Roman',20), justify='center',bd=3)
    TxtNo.place(x=150,y=120)
    TxtNo.focus()
    
    LblGatePass1 = Label(Frm1, text='Gatepass No: ', font=('Times New Roman',20), bg='#518aed', fg='white')
    LblGatePass1.place(x=240,y=120)
    LblGatePass2 = Label(Frm1, text='', font=('Times New Roman',20), bg='#518aed', fg='white')
    LblGatePass2.place(x=390,y=120)
    
    BtnFace = Button(Frm1, text="Start Face Scan", bg='#3379f2', fg='white', font=('Arial', 13), command=FaceScan)
    BtnFace.place(x=480, y=120)
    
    LblName = Label(Frm1, text="Name", font=('Times New Roman',20), bg='#518aed', fg='white')
    LblName.place(x=20, y=165)
    TxtName = Entry(Frm1, width=25, font=('Times New Roman',20),bd=3)
    TxtName.place(x=150,y=165)

    LblContactS = Label(Frm1, text="Contact No", font=('Times New Roman',20), bg='#518aed', fg='white')
    LblContactS.place(x=20, y=210)
    TxtContactS = Entry(Frm1, width=10, font=('Times New Roman',20),bd=3)
    TxtContactS.place(x=150,y=210)

    LblContactP = Label(Frm1, text="Parent Contact", font=('Times New Roman',20), bg='#518aed', fg='white')
    LblContactP.place(x=310, y=210)
    TxtContactP = Entry(Frm1, width=11, font=('Times New Roman',20),bd=3)
    TxtContactP.place(x=480,y=210)

    LblCity = Label(Frm1, text="City", font=('Times New Roman',20), bg='#518aed', fg='white')
    LblCity.place(x=20, y=255)
    TxtCity = Entry(Frm1, width=10, font=('Times New Roman',20),bd=3)
    TxtCity.place(x=150,y=255)

    LblWatchman = Label(Frm1, text="Watchman", font=('Times New Roman',20), bg='#518aed', fg='white')
    LblWatchman.place(x=310, y=255)
    TxtWatchman = Combobox(Frm1, width=10, font=('Times New Roman',20))
    TxtWatchman.place(x=480,y=255)
    
    LblReason = Label(Frm1, text="Reason", font=('Times New Roman',20), bg='#518aed', fg='white')
    LblReason.place(x=20,y=300)
    TxtReason = Entry(Frm1, width=30, font=('Times New Roman',20), fg='black',bd=3)
    TxtReason.place(x=150,y=300)

    BtnSave = Button(Frm2, text="Save", font=('Times New Roman',15), bg='#387ef5', fg='white', width=10, command=Save_Data)
    BtnSave.place(x=10,y=2)

    BtnReset = Button(Frm2, text="Reset", font=('Times New Roman',15), bg='#387ef5', fg='white', width=10)
    BtnReset.place(x=140,y=2)

    BtnShow = Button(Frm2, text="Show", font=('Times New Roman',15), bg='#387ef5', fg='white', width=10, command=expand)
    BtnShow.place(x=280,y=2)

    BtnExit = Button(Frm2, text="Exit", font=('Times New Roman',15), bg='#387ef5', fg='white', width=10)
    BtnExit.place(x=410,y=2)

    columns = ('#1', '#2', '#3', '#4', '#5')
    List_Data = ttk.Treeview(Frm3,show="headings",height="10", columns=columns)
    List_Data.heading('#1', text='GatePass No', anchor='center')
    List_Data.column('#1', width=80, anchor='center', stretch=False)
    List_Data.heading('#2', text='Name', anchor='center')
    List_Data.column('#2', width=150, anchor='w', stretch=True)
    List_Data.heading('#3', text='Contact No', anchor='center')
    List_Data.column('#3', width=80, anchor='w', stretch=True)
    List_Data.heading('#4', text='Reason', anchor='center')
    List_Data.column('#4', width=325, anchor='center', stretch=True)
    List_Data.place(x=5, y=5, height=210, width=645)  

    vsb= ttk.Scrollbar(Frm3, orient=tk.VERTICAL,command=List_Data.yview)  
    vsb.place(x=655, y=5, height=210)
    List_Data.configure(yscroll=vsb.set)

    List_Data.delete(*List_Data.get_children())

    on_start()

    def f1(event):
        search_data()
    
    def f2(event):
        TxtReason.focus()
    
    def f3(event):
        BtnSave.focus()

    TxtNo.bind("<Return>", f1)
    TxtWatchman.bind("<<ComboboxSelected>>", f2)
    TxtReason.bind("<Return>", f3)

    GatePass_Form.resizable(False, False)
    GatePass_Form.mainloop()
    
#GatePassForm()