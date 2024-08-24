from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import tkinter.ttk as ttk
import tkinter as tk
from Database import *
import cv2
import os
import numpy as np
from PIL import Image


def NewStudentForm(master):
    NewStd = Toplevel(master)
    NewStd.geometry("600x465+500+150")
    NewStd.title("New Student")

    def clear_entries():
        TxtNo.delete(0, END)
        TxtName.delete(0, END)
        TxtNameMar.delete(0, END)
        TxtContS.delete(0, END)
        TxtContP.delete(0, END)
        TxtCity.delete(0, END)
        TxtDist.delete(0, END)
        TxtTal.delete(0, END)
        TxtRoomNo.delete(0, END)

        #TxtThumb.delete(0, END)

    def on_start():
        max_no = str(Max_No('gate_pass_account_master', 'std_id', clg_id))
        clear_entries()
        TxtNo.insert(0, max_no)
        TxtName.focus()
        BtnSave['text'] = 'Save'

    def reset():
        NewStd.geometry("600x465+500+150")
        BtnShow['text'] = 'Show'
        BtnShow['command'] = expand

    def show_selected_record(event):
        for selection in List_Data.selection():
            item = List_Data.item(selection)

        clear_entries()
        i1 = item["values"][0]
        print(item["values"])
        ac = str(i1)
        #id, std_id, ac_type, acc_name_mara, ac_name, ac_contact, ac_contact_p, ac_stream, ac_city, ac_taluka,  ac_hostel, ac_room_no, acc_thumb, college_id
        sql = f"SELECT std_id, ac_type, acc_name_mara, ac_name, ac_contact, ac_contact_p, ac_stream, ac_city, ac_taluka, ac_year, ac_div, ac_hostel, ac_room_no, id FROM gate_pass_account_master WHERE std_id = {ac} and college_id = {clg_id}"
        db_cursor.execute(sql)
        data1 = db_cursor.fetchall()

        for i in data1:
            TxtNo.insert(0, str(i[0]))
            TxtGender.set(str(i[1]))
            TxtNameMar.insert(0, str(i[2]))
            TxtName.insert(0, i[3])
            TxtContS.insert(0, str(i[4]))
            TxtContP.insert(0, str(i[5]))

            for j, k in lst_stream.items():
                if j == i[6]:
                    TxtStream.set(str(k))

            TxtCity.insert(0, str(i[7]))

            for l, m in lst_taluka.items():
                if l == i[8]:
                    TxtTal.set(str(m))
                    sql1 = "SELECT gate_pass_district_master.name FROM gate_pass_district_master inner join gate_pass_taluka_master on gate_pass_taluka_master.city_id = gate_pass_district_master.id WHERE gate_pass_taluka_master.taluka_name = %s and gate_pass_taluka_master.college_id = %s"
                    db_cursor.execute(sql1, (m, clg_id))
                    TxtDist.delete(0, END)
                    TxtDist.insert(0, db_cursor.fetchall()[0][0])

            TxtYear.set(str(i[9]))
            TxtDiv.set(str(i[10]))

            for n, o in lst_hostel_name.items():
                if n == i[11]:
                    TxtHost.set(str(o))

            sql2 = "SELECT room_no FROM gate_pass_hostel_room_details WHERE id = %s and college_id = %s"
            db_cursor.execute(sql2, (i[12], clg_id))
            data2 = db_cursor.fetchall()
            n12 = data2[0][0]
            TxtRoomNo.set(n12)

        reset()
        BtnSave['text'] = 'Update'
        mid['text'] = data1[0][-1]

    def expand():
        NewStd.geometry("1050x465+300+150")
        BtnShow['text'] = 'Reset'
        BtnShow['command'] = reset
        List_Data.delete(*List_Data.get_children())

        sql = f"SELECT std_id, ac_name, ac_contact, ac_contact_p, ac_stream, id FROM gate_pass_account_master WHERE college_id = {clg_id}"
        db_cursor.execute(sql)
        data = db_cursor.fetchall()

        codeid = ""
        nm = ""
        mobile = ""
        mobile1 = ""
        stream1 = ""
        m_id = ""
        if db_cursor.rowcount != 0:
            for row in data:
                codeid = row[0]
                nm = row[1]
                mobile = row[2]
                mobile1 = row[3]
                sql1 = f"SELECT name FROM gate_pass_stream_details WHERE id = {row[4]} and college_id = {clg_id}"
                db_cursor.execute(sql1)
                data1 = db_cursor.fetchall()
                stream1 = data1[0][0]
                List_Data.insert("", 'end', text=codeid, values=(
                    codeid, nm, mobile, mobile1, stream1, m_id))

    def Delete_Data():
        n1 = TxtNo.get()
        sql = "DELETE FROM gate_pass_account_master WHERE std_id = %s"
        db_cursor.execute(sql, (n1,))
        db_connection.commit()

        messagebox.showinfo(
            "Information", "Deleted Successfully...", parent=NewStd)
        on_start()

    def Save_Data():
        n1 = TxtNo.get()
        m_id = int(mid['text'])
        n2 = TxtGender.get()
        n3 = TxtName.get()
        n3_1 = TxtNameMar.get()
        n4 = TxtContS.get()
        n5 = TxtContP.get()
        n6_ = TxtStream.get()
        n6 = 0
        for i, j in lst_stream.items():
            if n6_ == j:
                n6 = i

        n7 = TxtCity.get()

        n_8 = TxtTal.get()
        n8 = 0
        for a, b in lst_taluka.items():
            if n_8 == b:
                n8 = a
        #n7 = TxtDiv.get()
        n9 = TxtYear.get()
        n10 = TxtDiv.get()
        n11_ = TxtHost.get()
        n11 = 0

        sql1 = "SELECT hid FROM gate_pass_hostel_master WHERE hname = %s and college_id = %s"
        db_cursor.execute(sql1, (n11_, clg_id))
        data1 = db_cursor.fetchall()
        n11 = data1[0][0]

        n12_ = TxtRoomNo.get()
        n12 = 0
        sql2 = "SELECT gate_pass_hostel_room_details.id FROM gate_pass_hostel_room_details INNER JOIN gate_pass_hostel_master on gate_pass_hostel_master.hid = gate_pass_hostel_room_details.hostel_id WHERE gate_pass_hostel_room_details.room_no = %s and gate_pass_hostel_room_details.hostel_id = %s and gate_pass_hostel_room_details.college_id = %s"
        db_cursor.execute(sql2, (n12_, n11, clg_id))
        data2 = db_cursor.fetchall()
        n12 = data2[0][0]

        #n13 = img_to_blob(TxtThumb.get())
        n14 = clg_id
        if n1 != '' and n2 != '' and n3 != '' and n4 != '' and n5 != '' and n6 != '' and n7 != '' and n8 != '' and n9 != '' and n10 != '' and n11 != '' and n12 != '' and n14 != '':
            if BtnSave['text'] == 'Save':
                #std_id, acc_name_mara, ac_name, ac_contact, ac_contact_p, ac_stream, ac_city, ac_taluka, ac_year, ac_div, ac_hostel, ac_room_no, acc_thumb, college_id
                sql = "INSERT INTO gate_pass_account_master (std_id, ac_type, acc_name_mara, ac_name, ac_contact, ac_contact_p, ac_stream, ac_city, ac_taluka, ac_year, ac_div, ac_hostel, ac_room_no, college_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                db_cursor.execute(sql, (n1, n2, n3_1, n3, n4,
                                  n5, n6, n7, n8, n9, n10, n11, n12, n14))
            if BtnSave['text'] == 'Update':
                sql = "UPDATE gate_pass_account_master SET std_id = %s, ac_type = %s, acc_name_mara = %s, ac_name = %s, ac_contact = %s, ac_contact_p = %s, ac_stream = %s, ac_city = %s, ac_taluka = %s, ac_year = %s,  ac_div = %s, ac_hostel = %s, ac_room_no = %s WHERE id = %s and college_id = %s"
                db_cursor.execute(sql, (n1, n2, n3_1, n3, n4,
                                  n5, n6, n7, n8, n9, n10, n11, n12, m_id, n14))
            db_connection.commit()

            messagebox.showinfo("Information", "Successful...", parent=NewStd)
            BtnSave['text'] = 'Save'
            on_start()
        else:
            messagebox.showerror(
                "Error", "Please fill all fields...", parent=NewStd)

    def lst_str_fun():
        sql1 = f"SELECT id, name FROM gate_pass_stream_details where college_id = {clg_id}"
        db_cursor.execute(sql1,)
        data1 = db_cursor.fetchall()
        for i, j in data1:
            lst_stream[i] = j

    def lst_hostel_name_fun():
        sql1 = f"SELECT hid, hname FROM gate_pass_hostel_master where college_id = {clg_id}"
        db_cursor.execute(sql1,)
        data1 = db_cursor.fetchall()
        for i, j in data1:
            lst_hostel_name[i] = j

    def lst_taluka_name_fun():
        sql1 = f"SELECT id, taluka_name FROM gate_pass_taluka_master where college_id = {clg_id}"
        db_cursor.execute(sql1,)
        data1 = db_cursor.fetchall()
        for i, j in data1:
            lst_taluka[i] = j

    def lst_room_no_fun():
        hid = 1
        sql1 = f"SELECT id, room_no FROM gate_pass_hostel_room_details where hostel_id = {hid} and college_id = {clg_id} order by id"
        db_cursor.execute(sql1,)
        data1 = db_cursor.fetchall()
        for i, j in data1:
            lst_room_no[i] = j

    def getImagesAndLables(path):
        newdir = [os.path.join(path, d) for d in os.listdir(path)]
        imagePath = [
            os.path.join(newdir[i], f)
            for i in range(len(newdir))
            for f in os.listdir(newdir[i])
        ]
        faces = []
        Ids = []
        for imagePath in imagePath:
            pilImage = Image.open(imagePath).convert("L")
            imageNp = np.array(pilImage, "uint8")
            Id = int(os.path.split(imagePath)[-1].split("_")[1])
            faces.append(imageNp)
            Ids.append(Id)
        return faces, Ids

    def Open_Camera(l1, l2, haarcasecade_path, trainimage_path, master, trainimagelabel_path):
        BtnFace['text'] = 'Scanning...'

        if l2 == "":
            messagebox.showerror(
                'Please Enter the your Roll No.', parent=master)
        else:
            try:
                cam = cv2.VideoCapture(0)
                detector = cv2.CascadeClassifier(haarcasecade_path)
                Stream = l1
                Enrollment = l2
                sampleNum = 0
                directory = Enrollment + "_" + Stream
                path = os.path.join(trainimage_path, directory)
                os.mkdir(path)
                while True:
                    ret, img = cam.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = detector.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(
                            img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        sampleNum = sampleNum + 1
                        cv2.imwrite(
                            f"{path}\ "
                            + Stream
                            + "_"
                            + Enrollment
                            + "_"
                            + str(sampleNum)
                            + ".jpg",
                            gray[y: y + h, x: x + w],
                        )
                        cv2.imshow("Frame", img)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                    elif sampleNum > 30:
                        break
                cam.release()
                cv2.destroyAllWindows()
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                faces, Id = getImagesAndLables(trainimage_path)
                recognizer.train(faces, np.array(Id))
                recognizer.save(trainimagelabel_path)

            except:
                pass

    def FaceScan():
        l1 = TxtStream.get()
        l2 = TxtNo.get()
        haarcasecade_path = 'xml1.xml'
        trainimage_path = 'Images\Student'
        trainimagelabel_path = 'TrainImage.yml'
        Open_Camera(l1, l2, haarcasecade_path, trainimage_path,
                    master, trainimagelabel_path)

    clg_id = 1
    m_id = 0
    lst_stream = {}
    lst_hostel_name = {}
    lst_taluka = {}
    lst_room_no = {}

    lst_str_fun()
    lst_hostel_name_fun()
    lst_taluka_name_fun()
    lst_room_no_fun()
    Frm1 = LabelFrame(NewStd, height=445, width=580, bg='#4284f5')
    Frm1.place(x=10, y=10)

    Frm2 = LabelFrame(NewStd, height=445, width=445, bg='#4284f5')
    Frm2.place(x=600, y=10)

    LblHead = Label(Frm1, text="New Student Registration", font=(
        'Arial', 20, 'bold'), bg='#4284f5', fg='white')
    LblHead.place(x=160, y=10)

    LblNo = Label(Frm1, text="No", bg='#4284f5',
                  fg='white', font=('Arial', 15))
    LblNo.place(x=20, y=70)
    TxtNo = Entry(Frm1, font=('Arial', 15), width=5, bd=3, justify='center')
    TxtNo.place(x=145, y=70)

    mid = Label(Frm1, text="10", bg="#4284f5",
                fg="#4284f5", font=('Arial', 15))
    mid.place(x=250, y=70)

    LblName = Label(Frm1, text="Name", bg='#4284f5',
                    fg='white', font=('Arial', 15))
    LblName.place(x=20, y=110)

    TxtName = Entry(Frm1, font=('Arial', 15), width=36, bd=3)
    TxtName.place(x=145, y=110)

    LblName = Label(Frm1, text="naava", bg='#4284f5',
                    fg='white', font=('kf-kiran', 20))
    LblName.place(x=20, y=150)
    TxtNameMar = Entry(Frm1, font=('kf-kiran', 20), width=36, bd=3)
    TxtNameMar.place(x=145, y=150)

    LblContS = Label(Frm1, text="Contact No", bg='#4284f5',
                     fg='white', font=('Arial', 15))
    LblContS.place(x=20, y=190)
    TxtContS = Entry(Frm1, font=('Arial', 15), width=11, bd=3)
    TxtContS.place(x=145, y=190)

    LblContP = Label(Frm1, text="Parent Contact", bg='#4284f5',
                     fg='white', font=('Arial', 15))
    LblContP.place(x=290, y=190)
    TxtContP = Entry(Frm1, font=('Arial', 15), width=10, bd=3)
    TxtContP.place(x=430, y=190)

    LblStream = Label(Frm1, text="Stream", bg='#4284f5',
                      fg='white', font=('Arial', 15))
    LblStream.place(x=20, y=230)
    TxtStream = Combobox(Frm1, font=('Arial', 15), width=11,
                         values=list(lst_stream.values()))
    TxtStream.place(x=145, y=230)
    TxtStream.current(0)

    LblDiv = Label(Frm1, text="Div", bg='#4284f5',
                   fg='white', font=('Arial', 15))
    LblDiv.place(x=295, y=230)
    TxtDiv = Combobox(Frm1, font=('Arial', 15),
                      width=3, values=('A', 'B', 'C'))
    TxtDiv.place(x=330, y=230)
    TxtDiv.current(0)

    LblYear = Label(Frm1, text="Year", bg='#4284f5',
                    fg='white', font=('Arial', 15))
    LblYear.place(x=400, y=230)
    TxtYear = Combobox(Frm1, font=('Arial', 15), width=6,
                       values=('FY', 'SY', 'TY', 'B-Tech'))
    TxtYear.place(x=455, y=230)
    TxtYear.current(0)

    LblHost = Label(Frm1, text="Hostel", bg='#4284f5',
                    fg='white', font=('Arial', 15))
    LblHost.place(x=20, y=270)
    TxtHost = Combobox(Frm1, font=('Arial', 15), width=11,
                       values=list(lst_hostel_name.values()))
    TxtHost.place(x=145, y=270)
    TxtHost.current(0)

    LblRoomNo = Label(Frm1, text="Room No", bg='#4284f5',
                      fg='white', font=('Arial', 15))
    LblRoomNo.place(x=340, y=270)
    TxtRoomNo = Combobox(Frm1, font=('Arial', 15), width=8)
    TxtRoomNo.place(x=430, y=270)

    LblDist = Label(Frm1, text="District", bg='#4284f5',
                    fg='white', font=('Arial', 15))
    LblDist.place(x=360, y=310)
    TxtDist = Entry(Frm1, font=('Arial', 15), width=10, bd=3)
    TxtDist.place(x=430, y=310)

    LblTal = Label(Frm1, text="Taluka", bg='#4284f5',
                   fg='white', font=('Arial', 15))
    LblTal.place(x=20, y=310)
    TxtTal = Combobox(Frm1, font=('Arial', 15), width=11,
                      values=list(lst_taluka.values()))
    TxtTal.place(x=145, y=310)

    LblCity = Label(Frm1, text="City", bg='#4284f5',
                    fg='white', font=('Arial', 15))
    LblCity.place(x=20, y=350)
    TxtCity = Entry(Frm1, font=('Arial', 15), width=10, bd=3)
    TxtCity.place(x=145, y=350)

    TxtGender = Combobox(Frm1, font=('Arial', 15),
                         width=7, values=('Male', 'Female'))
    TxtGender.place(x=280, y=350)
    TxtGender.current(0)

    BtnFace = Button(Frm1, text="Start Face Scan", bg='#3379f2',
                     fg='white', font=('Arial', 13), command=FaceScan)
    BtnFace.place(x=400, y=350)

    BtnNew = Button(Frm1, text="New", font=("Arial", 14),
                    bg="#3379f2", fg='white', width=7)
    BtnNew.place(x=50, y=390)

    BtnSave = Button(Frm1, text="Save", font=("Arial", 14),
                     bg="#3379f2", fg='white', width=7, command=Save_Data)
    BtnSave.place(x=150, y=390)

    BtnDelete = Button(Frm1, text="Delete", font=(
        "Arial", 14), bg="#3379f2", fg='white', width=7, command=Delete_Data)
    BtnDelete.place(x=250, y=390)

    BtnShow = Button(Frm1, text="Show", font=("Arial", 14),
                     bg="#3379f2", fg='white', width=7, command=expand)
    BtnShow.place(x=350, y=390)

    BtnExit = Button(Frm1, text="Exit", font=("Arial", 14),
                     bg="#3379f2", fg='white', width=7)
    BtnExit.place(x=450, y=390)
    TxtName.focus()

    columns = ('#1', '#2', '#3', '#4', '#5')
    List_Data = ttk.Treeview(Frm2, show="headings",
                             height="10", columns=columns)
    List_Data.heading('#1', text='No', anchor='center')
    List_Data.column('#1', width=40, anchor='center', stretch=False)
    List_Data.heading('#2', text='Name', anchor='center')
    List_Data.column('#2', width=85, anchor='w', stretch=True)
    List_Data.heading('#3', text='Contact No', anchor='center')
    List_Data.column('#3', width=50, anchor='w', stretch=True)
    List_Data.heading('#4', text='Parent Contact', anchor='center')
    List_Data.column('#4', width=60, anchor='center', stretch=True)
    List_Data.heading('#5', text='Stream', anchor='center')
    List_Data.column('#5', width=40, anchor='center', stretch=True)
    List_Data.place(x=5, y=5, height=430, width=410)

    vsb = ttk.Scrollbar(Frm2, orient=tk.VERTICAL, command=List_Data.yview)
    vsb.place(x=420, y=5, height=430)
    List_Data.configure(yscroll=vsb.set)

    List_Data.bind("<Double-1>", show_selected_record)
    List_Data.delete(*List_Data.get_children())

    def f1(event):
        TxtNameMar.focus()

    def f2(event):
        TxtContS.focus()

    def f3(event):
        TxtContP.focus()

    def f4(event):
        TxtStream.focus()
        TxtStream.event_generate('<Down>')

    def f5(event):
        TxtDiv.focus()
        TxtDiv.event_generate('<Down>')

    def f6(event):
        TxtYear.focus()
        TxtYear.event_generate('<Down>')

    def f7(event):
        TxtHost.focus()
        TxtHost.event_generate('<Down>')

    def f8(event):
        n1 = TxtHost.get()
        for i, j in lst_hostel_name.items():
            if j == n1:
                sql1 = f"SELECT room_no FROM gate_pass_hostel_room_details WHERE hostel_id = {i} and college_id = {clg_id}"
                db_cursor.execute(sql1,)
                data1 = db_cursor.fetchall()
                if data1 != []:
                    TxtRoomNo['values'] = data1
        TxtRoomNo.focus()
        TxtRoomNo.event_generate('<Down>')

    def f9(event):
        TxtTal.focus()
        TxtTal.event_generate('<Down>')

    def f10(event):
        n1 = TxtTal.get()
        sql1 = f"SELECT gate_pass_district_master.name from gate_pass_district_master INNER JOIN gate_pass_taluka_master on gate_pass_district_master.id = gate_pass_taluka_master.city_id WHERE gate_pass_taluka_master.taluka_name = %s and gate_pass_district_master.college_id = {clg_id}"
        db_cursor.execute(sql1, (n1,))
        data1 = db_cursor.fetchall()
        TxtDist.delete(0, END)
        TxtDist.insert(0, data1[0][0])

        TxtCity.focus()

    def f11(event):
        TxtGender.focus()
        TxtGender.event_generate('<Down>')

    def f12(event):
        BtnFace.focus()

    TxtName.bind('<Return>', f1)
    TxtNameMar.bind('<Return>', f2)
    TxtContS.bind('<Return>', f3)
    TxtContP.bind('<Return>', f4)
    TxtStream.bind('<<ComboboxSelected>>', f5)
    TxtDiv.bind('<<ComboboxSelected>>', f6)
    TxtYear.bind('<<ComboboxSelected>>', f7)
    TxtHost.bind('<<ComboboxSelected>>', f8)
    TxtRoomNo.bind('<<ComboboxSelected>>', f9)
    TxtTal.bind('<<ComboboxSelected>>', f10)
    TxtCity.bind('<Return>', f11)

    on_start()

    NewStd.resizable(False, False)
    NewStd.mainloop()


# NewStudentForm()
