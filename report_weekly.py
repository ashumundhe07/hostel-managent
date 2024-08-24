from tkinter import *
from tkcalendar import DateEntry
from datetime import *
from Database import *
from fpdf import *
import os
def Weekly_Report(master):
    def Show_Report():
        dt1 = datetime.strftime(TxtDate1.get_date(),'%Y-%m-%d')
        dt2 = datetime.strftime(TxtDate2.get_date(),'%Y-%m-%d')
        
        head1 = 'Padmabhooshan Vasantraodada Patil Institute of Technology, Budhgaon'
        pdf = FPDF(format = 'A4')
        pdf.add_page()
        pdf.add_font("KF-Kiran", style='B', fname = "./Fonts/TNR.ttf", uni = True)
        pdf.set_font("KF-Kiran", size = 18,style='B')
        pdf.cell(10)
        pdf.cell(500, 5, txt=str(head1), align='L')

        pdf.ln(6)
        
        head2 = 'Weekly Gate-Pass Report'
        pdf.add_font("KF-Kiran", style='B', fname = "./Fonts/TNR.ttf", uni = True)
        pdf.set_font("KF-Kiran", size = 15,style='B')
        pdf.cell(70)
        pdf.cell(500, 5, txt=str(head2), align='L')
        
        pdf.ln(6)
        
        head3 = str(TxtDate1.get_date())
        head5 = str(TxtDate2.get_date())
        
        pdf.add_font("KF-Kiran", style='B', fname = "./Fonts/TNR.ttf", uni = True)
        pdf.set_font("KF-Kiran", size = 14,style='B')
        pdf.cell(80)
        pdf.cell(500, 5, txt="Date: From "+head3+" To "+head5, align='L')
        
        pdf.dashed_line(0, 29, 250, 29, dash_length=1, space_length=1)
        pdf.ln(7)
        head4 = "No                               Name of Student                                        Contact                                      Reason                               Pass Status" 
        pdf.add_font("KF-Kiran", style='B', fname = "./Fonts/TNR.ttf", uni = True)
        pdf.set_font("KF-Kiran", size = 10,style='B')
        pdf.cell(500, 5, txt=head4, align='L')
        pdf.ln(5)
        
        pdf.dashed_line(0, 35, 250, 35, dash_length=1, space_length=1)
        sql1 = f"SELECT gate_pass_account_master.ac_name, gate_pass_account_master.ac_contact, gate_pass_master.reason, gate_pass_master.pass_status FROM gate_pass_master INNER JOIN gate_pass_account_master on gate_pass_account_master.std_id = gate_pass_master.std_id WHERE gate_pass_master.date_out between %s and %s"
        db_cursor.execute(sql1,(dt1, dt2))
        data1 = db_cursor.fetchall()
        cnt = 1
        pdf.ln(6)
        if db_cursor.rowcount > 0:
            for i in data1:
                pdf.cell(15, txt=str(cnt), align='L')
                pdf.cell(70, txt=i[0], align='L')
                pdf.cell(40, txt=i[1], align='L')
                pdf.cell(40, txt=i[2], align='L')
                if i[3] == 1:
                    pdf.cell(80, txt="Active", align='L')
                else:
                    pdf.cell(80, txt="Not-Active", align='L')
                    
                pdf.ln(6)
                cnt += 1
            pdf.cell(250, txt="-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

            pdf.output("D:\Ishan\HostelManagement\Reports\Weekly_Report.pdf",'F')
    
            os.startfile("D:\Ishan\HostelManagement\Reports\Weekly_Report.pdf")

    DailyReport = Toplevel()
    DailyReport.geometry("400x200+550+300")

    Frm1 = LabelFrame(DailyReport, height=180, width=380)
    Frm1.place(x=10, y=10)

    Lblhead = Label(Frm1, text="Weekly Report", font=('Times New Roman', 20), fg='red')
    Lblhead.place(x=110, y=5)

    LblDate1 = Label(Frm1, text='From', font=('Times New Roman', 18))
    LblDate1.place(x=80, y=40)
    TxtDate1 = DateEntry(Frm1, font=('Times New Roman', 18), date_pattern = 'dd/mm/yyyy', width=10)
    TxtDate1.place(x=190, y=40)

    LblDate2 = Label(Frm1, text='To', font=('Times New Roman', 18))
    LblDate2.place(x=80, y=90)
    TxtDate2 = DateEntry(Frm1, font=('Times New Roman', 18), date_pattern = 'dd/mm/yyyy', width=10)
    TxtDate2.place(x=190, y=90)
    
    BtnShow = Button(Frm1, text="Show", fg='white', bg='green', font=('Times New Roman', 12), width=10, command=Show_Report)
    BtnShow.place(x=140, y=130)

    DailyReport.mainloop()
    
#Weekly_Report()