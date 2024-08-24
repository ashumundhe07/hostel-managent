from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from Database import *
import tkinter as tk

def WatchmanNew(master):
    watchman_Registration = Toplevel(master)
    watchman_Registration.geometry("600x300+450+190")
    
    def on_start():
        TxtNo.delete(0, END)
        TxtHostelName.delete(0, END)
        
        n1 = Max_No('gate_pass_watchman_details', 'mid', clg_id)
        TxtNo.insert(0, n1)

        List_Data.delete(*List_Data.get_children())
        sql1 = "SELECT mid, watchman_name, id, contact_no FROM gate_pass_watchman_details WHERE college_id = %s"
        db_cursor.execute(sql1, (clg_id,))
        data1 = db_cursor.fetchall()
        n1 = ""
        n2 = ""
        n3 = ""
        n4 = ""
        for i in data1:
            n1 = str(i[0])
            n2 = i[1]
            n3 = str(i[2])
            List_Data.insert("", 'end', text=n1, values=(n1, n2, n3, i[3]))

        TxtHostelName.focus()
    
    def Save_Data():
        n1 = TxtNo.get()
        n2 = TxtHostelName.get()
        n3 = LblMid['text']
        n4 = TxtContact.get()
        if n1 != '' and n2 != '' and BtnSave['text'] == 'Save':
            sql = "INSERT INTO gate_pass_watchman_details(mid, watchman_name, contact_no, college_id) values(%s, %s, %s)"
            db_cursor.execute(sql, (n1, n2, n4, clg_id))
            db_connection.commit()
            messagebox.showinfo("information","Successful...",parent=watchman_Registration)
        
        elif n1 != '' and n2 != '' and BtnSave['text'] == 'Update':
            sql = "UPDATE gate_pass_watchman_details SET mid = %s, watchman_name = %s, contact_no = %s WHERE id = %s and college_id = %s"
            db_cursor.execute(sql, (n1, n2, n4, n3, clg_id))
            db_connection.commit()
            messagebox.showinfo("information","Successful...",parent=watchman_Registration)
            BtnSave['text'] = 'Save'
        else:
            messagebox.showerror("Error","Please fill all fields...",parent=watchman_Registration)
        
        on_start()
        
    def reset():
        watchman_Registration.geometry("600x300+450+190")
        BtnShow['text'] = 'Show'
        BtnShow['command'] = expand

    def expand():
        watchman_Registration.geometry("1000x300+300+190")
        BtnShow['text'] = 'Reset'
        BtnShow['command'] = reset

    def clear_entries():
        TxtNo.delete(0,END)
        TxtHostelName.delete(0,END)
        TxtContact.delete(0, END)

    def show_selected_record(event):
        for selection in List_Data.selection():
            item = List_Data.item(selection)

        clear_entries()
        i1 = item["values"]
        TxtNo.insert(0,i1[0])
        TxtHostelName.insert(0,i1[1])
        TxtContact.insert(0, i1[3])
        LblMid['text'] = i1[2]

        BtnSave['text'] = 'Update'
        reset()

    clg_id = 1

    Frm1 = LabelFrame(watchman_Registration, height=285, width=580, bg='#518aed')
    Frm1.place(x=10, y=10)

    LblHead = Label(Frm1, text='Watchman Registration', font=('Arial',25), bg='#518aed', fg='white')
    LblHead.place(x=150,y=10)
    
    LblNo = Label(Frm1, text='No', font=('Arial',17), bg='#518aed', fg='white',)
    LblNo.place(x=60,y=70)
    TxtNo = Entry(Frm1, width=4, font=('Arial',17), justify='center')
    TxtNo.place(x=205,y=70)

    LblMid = Label(Frm1, text='', bg='#518aed', fg = '#518aed')
    LblMid.place(x=300, y=70)


    LblHostelName = Label(Frm1, text='Name', font=('Arial',17), bg='#518aed', fg='white',)
    LblHostelName.place(x=60,y=110)
    TxtHostelName = Entry(Frm1, width=25, font=('Arial',17))
    TxtHostelName.place(x=205,y=110)
    
    LblContact = Label(Frm1, text='Contact No', font=('Arial',17), bg='#518aed', fg='white',)
    LblContact.place(x=60,y=150)
    TxtContact = Entry(Frm1, width=25, font=('Arial',17))
    TxtContact.place(x=205,y=150)

    BtnSave = Button(Frm1, text="Save", bg='#518aed', fg='white',width=8, font=('Arial',17), command=Save_Data)
    BtnSave.place(x=30,y=210)
    BtnShow = Button(Frm1, text="Show", bg='#518aed', fg='white',width=8, font=('Arial',17), command=expand)
    BtnShow.place(x=160,y=210)
    BtnDelete = Button(Frm1, text="Delete", bg='#518aed', fg='white',width=8, font=('Arial',17))
    BtnDelete.place(x=290,y=210)
    BtnExit = Button(Frm1, text="Exit", bg='#518aed', fg='white',width=8, font=('Arial',17))
    BtnExit.place(x=420,y=210)
    
    columns = ('#1', '#2')
    List_Data = ttk.Treeview(watchman_Registration,show="headings",height="10", columns=columns)
    List_Data.heading('#1', text='No', anchor='center')
    List_Data.column('#1', width=80, anchor='center', stretch=False)
    List_Data.heading('#2', text='Name', anchor='center')
    List_Data.column('#2', width=150, anchor='w', stretch=True)
    List_Data.place(x=610, y=10, height=280, width=370)  

    vsb= ttk.Scrollbar(watchman_Registration, orient=tk.VERTICAL,command=List_Data.yview)  
    vsb.place(x=990, y=10, height=280)
    List_Data.configure(yscroll=vsb.set)

    List_Data.delete(*List_Data.get_children())

    List_Data.bind("<Double-1>", show_selected_record)    
    on_start()

    watchman_Registration.mainloop()

#WatchmanNew()