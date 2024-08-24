from tkinter import *
import tkinter.ttk as ttk

def Miscell_Form():
    Frm_Miscellaneous_Master = Tk()
    
    var_options = StringVar()
    
    Frm1 = ttk.LabelFrame(Frm_Miscellaneous_Master, height=230, width=150)
    Frm1.place(x=10, y=50)
    Frm2 = ttk.LabelFrame(Frm_Miscellaneous_Master, height=230, width=350)
    Frm2.place(x=170, y=50)
    Frm3 = ttk.LabelFrame(Frm_Miscellaneous_Master, height=150, width=510)
    Frm3.place(x=10, y=280)

    LblMiscellaneousmaster = Label(Frm_Miscellaneous_Master, text = 'gaaMvaacaI maaihtaI', font = ('KF-Kiran', 30), fg = 'Red')
    LblMiscellaneousmaster.place(x = 200, y = 4)

    CheckState = Radiobutton(Frm1, text='rajya',font = ('KF-Kiran', 15), variable = var_options, value = 'State', state = 'disabled')
    CheckState.place(x=10, y=0)
    CheckDistrict = Radiobutton(Frm1, text='ijalaa',font = ('KF-Kiran', 15), variable = var_options, value = 'District', state = 'disabled')
    CheckDistrict.place(x=10, y=30)
    CheckTaluka = Radiobutton(Frm1, text='taalaukxa',font = ('KF-Kiran', 15), variable = var_options, value = 'Taluka', state = 'disabled')
    CheckTaluka.place(x=10, y=60)
    CheckVillage = Radiobutton(Frm1, text='gaaMva/Sahr',font = ('KF-Kiran', 15), variable = var_options, value = 'Village', state = 'disabled')
    CheckVillage.place(x=10, y=90)

    LblCode = Label(Frm2, text = 'kxaoD', font = ('KF-Kiran', 15))
    LblCode.place(x = 30, y = 10)
    LblName = Label(Frm2, text = 'naaMva', font = ('KF-Kiran', 15))
    LblName.place(x = 34, y = 40)
    TxtCode = Entry(Frm2, width=10, font = ('Arial', 15),state='disabled')
    TxtCode.place(x=70, y=10)
    TxtName = Entry(Frm2, width=28, font = ('KF-Kiran', 15),state='disabled')
    TxtName.place(x=70, y=40)
    LblMarname = Label(Frm2, text = 'marazI naaMva', font = ('KF-Kiran', 15),state='disabled')
    LblMarname.place(x = 0, y = 70)
    TxtMarname = Entry(Frm2, width=28, font = ('KF-Kiran', 15),state='disabled')
    TxtMarname.place(x=70, y=70)

    LblState = Label(Frm2, text = 'rajya', font = ('KF-Kiran', 15))
    LblState.place(x = 26, y = 100)
    LblDistrict = Label(Frm2, text = 'ijalha', font = ('KF-Kiran', 15))
    LblDistrict.place(x = 23, y = 130)
    LblTaluka = Label(Frm2, text = 'taalaukxa', font = ('KF-Kiran', 15))
    LblTaluka.place(x = 16, y = 160)

    ComboState = ttk.Combobox(Frm2, width=26, font = ('KF-Kiran', 15), values = list(list_state.values()), state = 'disabled')
    ComboState.place(x=70, y=100)
    ComboDistrict = ttk.Combobox(Frm2, width=26, font = ('KF-Kiran', 15), state = 'disabled')
    ComboDistrict.place(x=70, y=130)
    ComboTaluka = ttk.Combobox(Frm2, width=26, font = ('KF-Kiran', 15), state = 'disabled')
    ComboTaluka.place(x=70, y=160)

    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('KF-Kiran', 17)) # Modify the font of the body
    style.configure("mystyle.Treeview.Heading", highlightthickness=0, bd=0, font=('KF-Kiran', 17)) # Modify the font of the body

    columns = ("#1", "#2",)
    TreeViewOptions = ttk.Treeview(Frm3, show="headings", height="10", columns=columns, style="mystyle.Treeview")

    TreeViewOptions.heading('#1', text='kxaoD', anchor='center')
    TreeViewOptions.column('#1', width=60, anchor='center', stretch=False)
    TreeViewOptions.heading('#2', text='naaMva', anchor='center')
    TreeViewOptions.column('#2', width=10, anchor='center', stretch=True) 

    vsb= ttk.Scrollbar(Frm3, orient=tk.VERTICAL,command=TreeViewOptions.yview)  
    vsb.place(x=485, y=0, height=120)
    TreeViewOptions.configure(yscroll=vsb.set)

    TreeViewOptions.place(x=10,y=0,height=120,width=475)
    style1.configure("Treeview.Heading", font=("kf-kiran", 10))
    TreeViewOptions.bind("<Double-1>", show_selected_record)

    BtnNew = Button(Frm_Miscellaneous_Master, text='naivana',width=10, font = ('KF-Kiran', 14), command = New_Entry, bg = 'skyblue', fg = 'white')
    BtnNew.place(x=50, y=440)
    BtnSave = Button(Frm_Miscellaneous_Master, text='saova',width=10, font = ('KF-Kiran', 14), state = 'disabled', command =lambda flag = 1: save_miss(flag), bg = 'green', fg = 'white')
    BtnSave.place(x=160, y=440)
    BtnDelete = Button(Frm_Miscellaneous_Master, text='kxaZNao',width=10, font = ('KF-Kiran', 14), command = delete_miss, bg = 'brown', fg = 'white')
    BtnDelete.place(x=270, y=440)
    BtnExit = Button(Frm_Miscellaneous_Master, text='baahor',width=10, font = ('KF-Kiran', 14), command=Frm_Miscellaneous_Master.destroy, bg = 'red', fg = 'white')
    BtnExit.place(x=380, y=440)
    BtnHelp = Button(Frm2, text='madta',font = ('kf-kiran',13), command = Show_Help)
    BtnHelp.place(x=280,y=2)

    state_list()
    TxtName.bind('<Return>',f1)
    
    ComboState.bind("<<ComboboxSelected>>", State_Id)
    ComboDistrict.bind("<<ComboboxSelected>>",Dist_Id)

    Frm_Miscellaneous_Master.resizable(False, False)
    Frm_Miscellaneous_Master.mainloop()
    
Miscell_Form()