import pyodbc
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkcalendar import Calendar, DateEntry
import re
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from report1 import report1
from report2 import report2
from report3 import report3
# Установление соединения с базой данной
conn = pyodbc.connect(driver = '{SQL Server Native Client 11.0}',server = '192.168.112.103' , database = 'db22205', user = 'User053', password = 'User053#!31')

print ('privet')
cursor = conn.cursor()
MainRoot= tk.Tk() 
getNum=0
###########################################################
############# ПЕРЕМЕННЫЕ ДЛЯ 9 ЛАБОРАТОРНОЙ ##################
summa=StringVar()
getType=StringVar()
getData=StringVar()
getAccNum=0
#############################################3################
############################################################    
def main1():
    root = tk.Toplevel(MainRoot)                            # Основное окно
    root.title("Счета")
    root.geometry("1100x300")
    tree = ttk.Treeview(root)
    label1 = tk.Label(root,text="Информация о счетах клиентов")
    label1.place(relx = 0.1, rely = 0.05)

    tree["columns"] = ("one", "two", "three","four")
    tree.column("one", width=400, anchor=tk.CENTER)
    tree.column("two", width=200,anchor=tk.CENTER)
    tree.column("three", width=200,anchor=tk.CENTER)
    tree.column("four", width=200,anchor=tk.CENTER)

    tree.heading("one", text="ФИО", anchor=tk.CENTER)
    tree.heading("two", text="Наименование типа счета",anchor=tk.CENTER)
    tree.heading("three", text="Дата открытия счета",anchor=tk.CENTER)
    tree.heading("four", text="Номер счета",anchor=tk.CENTER)

    scroll = tk.Scrollbar(command=tree.yview)  # Линейка прокрутки для списка
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    #tree.place()
    tree.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)



# переменные
    iati_msg = StringVar()
    ici_msg = StringVar()
    dab_msg= StringVar()
    dae_msg= StringVar()
    tan_msg= StringVar()
    fas_msg= StringVar()









# Заполнение списка деталей из базы данных
# выполнение команды SQL
    cursor.execute("Select tblClient.txtClientSurname, tblClient.txtClientName, tblClient.txtClientSecondName, txtAccountTypeName, datAccountBegin, txtAccountNumber From tblClient,tblAccount,tblAccountType Where (tblAccount.intClientId=tblClient.intClientId)AND(tblAccount.intAccountTypeId=tblAccountType.intAccountTypeId)")
    row = cursor.fetchone()   # получение данных одной записи
    i = 0


    while row: 
        # добавление элемента (номер детали и ее цвет) в список
        #lbox.insert(i, "{:<5}".format(str(row[0])) + '| ' + "{:5}".format(str(row[1]))+ "{:5}".format(str(row[2]))+ "{:5}".format(str(row[3]))+ "{:5}".format(str(row[4]))+ "{:5}".format(str(row[5])))
        row[0]=row[0].replace(" ", "")
        row[1]=row[1].replace(" ", "")
        row[2]=row[2].replace(" ", "")
        tree.insert('', 'end', values=(row[0]+"   "+row[1]+"   "+row[2], row[3], row[4],row[5]))
        tree['show']='headings'
        row = cursor.fetchone()   # получение данных одной записи



    def add_new_account():
        cursor.execute('Insert into tblAccount(intAccountTypeId,intClientId,datAccountBegin,datAccountEnd,txtAccountNumber, fltAccountSum)\
    values(?,?,?,?,?,?)', iati_msg.get(),ici_msg.get(),dab_msg.get(),dae_msg.get(),tan_msg.get(),fas_msg.get())
        conn.commit()                
 
    def updateTable():
        cursor.execute("Select tblClient.txtClientSurname, tblClient.txtClientName, tblClient.txtClientSecondName, txtAccountTypeName, datAccountBegin, txtAccountNumber From tblClient,tblAccount,tblAccountType Where (tblAccount.intClientId=tblClient.intClientId)AND(tblAccount.intAccountTypeId=tblAccountType.intAccountTypeId)")
        row = cursor.fetchone()   # получение данных одной записи
        i = 0

   
        while row: 
            row[0]=row[0].replace(" ", "")
            row[1]=row[1].replace(" ", "")
            row[2]=row[2].replace(" ", "")
            tree.insert('', 'end', values=(row[0]+"   "+row[1]+"   "+row[2], row[3], row[4],row[5]))
            tree['show']='headings'
            row = cursor.fetchone()
    
    
    def new_account():
        newAccount = tk.Toplevel(root)
        newAccount.geometry("500x300")
        newAccount.title("Новый счет")
    
        intAccountTypeId=Label(newAccount, text="Тип счета: ")
        intAccountTypeId.place(relx=0.1, rely=.1)

        iati_msg_entry = Entry(newAccount, textvariable=iati_msg)
        iati_msg_entry.place(relx=.31, rely=.1, width="250")

        intClientId=Label(newAccount, text="Клиент: ")
        intClientId.place(relx=.1, rely=.2)

        ici_msg_entry = Entry(newAccount, textvariable=ici_msg)
        ici_msg_entry.place(relx=.31, rely=.2, width="250")

        datAccountBegin=Label(newAccount, text="Дата открытия счета: ")
        datAccountBegin.place(relx=.05, rely=.3)

        dab_msg_entry = Entry(newAccount, textvariable=dab_msg)
        dab_msg_entry.place(relx=.31, rely=.3, width="250")

        datAccountEnd=Label(newAccount, text="Дата закрытия счета: ")
        datAccountEnd.place(relx=.05, rely=.4)

        dae_msg_entry = Entry(newAccount, textvariable=dae_msg)
        dae_msg_entry.place(relx=.31, rely=.4, width="250")

        txtAccountNumber=Label(newAccount, text="Номер счета: ")
        txtAccountNumber.place(relx=.1, rely=.5)

        tan_msg_entry = Entry(newAccount, textvariable=tan_msg)
        tan_msg_entry.place(relx=.31, rely=.5, width="250")

        fltAccountSum=Label(newAccount, text="Сумма на счете: ")
        fltAccountSum.place(relx=.1, rely=.6)

        fas_msg_entry = Entry(newAccount, textvariable=fas_msg)
        fas_msg_entry.place(relx=.31, rely=.6, width="250")

        new_account_btn=Button(newAccount, text="OK", width=10,command=add_new_account)
        new_account_btn.pack()
        new_account_btn.place(relx=.7, rely=.8)

        update_btn=Button(newAccount, text="Обновить", width=10,command=updateTable)
        update_btn.pack()
        update_btn.place(relx=.5, rely=.8)    
    
    btn=tk.Button(root, text="Добавить", width=20,  command=new_account)
    btn.pack()
    btn.place(relx=.8, rely=.9)




#####################################################################################################
#----------------------------------- 9 ЛАБОРАТОРНАЯ -----------------------------------------------#
    def add_operation():
        print("----------")
        print(getType.get()) #Выводится правильно
        print(getAccNum) # Почему то выводится 0 (значение не переприсваивается)
        print(summa.get()) # выводится правильно
        print(getData) #Вообще не выводится
        cursor.execute('select intOperationTypeId  from tblOperationType  Where txtOperationTypeName =?', getType.get())
        row1 = cursor.fetchone()
        print (row1[0])
        currOperType=row1[0]
        cursor.execute('select intAccountId  from tblAccount  Where txtAccountNumber =?', getAccNum)
        row2=cursor.fetchone()
        currAccNum=row2[0]
        print(currAccNum)
        cursor.execute('Insert into tblOperation(intOperationTypeId,intAccountId,fltValue,datOperation)\
        values(?,?,?,?)',currOperType,currAccNum,summa.get(),getData)
        conn.commit()       
    

    def new_operation(one,two,three):
        newOperation = tk.Toplevel(root)
        newOperation.geometry("500x400")
        newOperation.title("Новая операция")
    
        fio=Label(newOperation, text="ФИО клиента: ")
        fio.place(relx=0.177, rely=.1)

        fio_entry = Entry(newOperation)
        fio_entry.place(relx=.35, rely=.1, width="250")
        fio_entry.insert(0,one)
        fio_entry.configure(state='disabled')
    
        accNumber=Label(newOperation, text="Номер счета: ")
        accNumber.place(relx=.18, rely=.2)

        accNumber_entry = Entry(newOperation)
        accNumber_entry.place(relx=.35, rely=.2, width="250")
        accNumber_entry.insert(0,two)
        accNumber_entry.configure(state='disabled')
    
        #ЗДЕСЬ ПОЛУЧАЮ НОМЕР СЧЕТА В ПЕРЕМЕННУЮ getAccNum(но он почему то там не сохраняется)
        global getAccNum
        getAccNum=two
        print ("gg=", getAccNum)
        accName=Label(newOperation, text="Наименование типа счета: ")
        accName.place(relx=.037, rely=.3)

        accName_entry = Entry(newOperation)
        accName_entry.place(relx=.35, rely=.3, width="250")
        accName_entry.insert(0,three)
        accName_entry.configure(state='disabled')

        operType=Label(newOperation, text="Тип операции: ")
        operType.place(relx=.17, rely=.4)
    
        #РАСКРЫВАЮЩИЙСЯ СПИСОК
        def combo_input():
            cursor.execute("SELECT txtOperationTypeName FROM tblOperationType")
            data=[]
            for row2 in cursor.fetchall():
                data.append(row2[0])
            return data        
    
        def ifComboSel(event):
            print("тип вывелся")
            getType=combo.get()
           # getType=getType.replace(" ", "")
            print (getType) #проверка выведения типа
        combo = ttk.Combobox(newOperation, textvariable=getType)
        combo.place(relx=.35, rely=.4, width="250")
        combo.bind("<<ComboboxSelected>>", ifComboSel)
        combo['values'] = combo_input()
    
        #КАЛЕНДАРЬ    
        operDate=Label(newOperation, text="Дата проведения операции: ")
        operDate.place(relx=.027, rely=.5)


        def print_sel(event):
            print("дата вывелась")
            global getData
            getData=cal.get_date() 
            print(getData)#здесь дата выводится правильно
        
        cal = DateEntry(newOperation, width=12, background='darkblue',foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        cal.pack(padx=15, pady=5)
        cal.place(relx=.35, rely=.5) 
        cal.bind("<<DateEntrySelected>>", print_sel)

        def upd(accN):
            cursor.execute("SELECT tblOperation.datOperation, tblOperationType.txtOperationTypeName,\
            tblOperation.fltValue FROM tblOperation, tblOperationType, tblAccount Where (tblAccount.txtAccountNumber=?)\
            AND (tblOperation.intOperationTypeId=tblOperationType.intOperationTypeId) AND (tblOperation.intAccountId=tblAccount.intAccountId)", accN)

            row1 = cursor.fetchone()
            i = 0
            while row1:        
                tree1.insert('', 'end', values=(row1[0], row1[1],row1[2]))
                #tree1['show']='headings'
                row1 = cursor.fetchone()

        #МАСКА СУММЫ
        operSum=Label(newOperation, text="Сумма: ")
        operSum.place(relx=.25, rely=.6)

        operSum_entry = Entry(newOperation, textvariable=summa)
        operSum_entry.place(relx=.35, rely=.6, width="250")

        def entry_mask_check(text, valid, entry):
            ip = re.findall("^\d{0,10}\.\d{0,2}$",text.get())
            if len(ip) != 1:
                text.set(valid[0])
            if ip:
                valid[0] = ip[0]
                #jump next on 3 didgits
                cursor_position = entry.index("insert")
                index = ip[0][:cursor_position].rfind(u".")
           # if cursor_position - index == 4:
              #  entry.icursor(cursor_position+1)
        operSum_last_valid=[u"."]
        summa.trace("w", lambda *args: entry_mask_check(summa, operSum_last_valid,operSum_entry))
        summa.set("")
        operSum_entry.focus()

    #ВЫЗОВ ФУНКЦИИ ДОБАВЛЕНИЯ НОВОЙ ОПЕРАЦИИ
        b=Button(newOperation, text="OK", width=10, command=add_operation)
        b.pack()
        b.place(relx=.7, rely=.8)  

        upd=Button(newOperation, text="Обновить", width=10, command=upd(getAccNum))
        upd.pack()
        upd.place(relx=.4, rely=.8)

#---------------------------------------------------------------------------------------------------#    
####################################################################################################


    
#-----------------------------------8 ЛАБА-----------------------------------------
    def double_click(event):
        account = tk.Toplevel(root)
        account.geometry("700x500")
        account.title("Счет")

        accountInformation=Label(account, text="Информация о счете")
        accountInformation.place(relx=0.05, rely=.05)

        stroka=tree.selection()[0]
        values=tree.item(stroka, option="value")
    
        client=Label(account, text="Клиент: ")
        client.place(relx=0.1, rely=.12)
        client_value=Label(account, text=values[0])
        client_value.place(relx=0.25, rely=.12)


        accountType=Label(account, text="Тип счета: ")
        accountType.place(relx=0.1, rely=.16)
        accountType_value=Label(account, text=values[1])
        accountType_value.place(relx=0.25, rely=.16)


        accountBegin=Label(account, text="Дата открытия: ")
        accountBegin.place(relx=0.1, rely=.2)
        accountBegin_value=Label(account, text=values[2])
        accountBegin_value.place(relx=0.25, rely=.2)

        accountNumber=Label(account, text="Номер счета: ")
        accountNumber.place(relx=0.1, rely=.24)
        accountNumber_value=Label(account, text=values[3])
        accountNumber_value.place(relx=0.25, rely=.24)

        tree1 = ttk.Treeview(account)
        tree1["columns"] = ("one1", "two1", "three1")
        tree1.column("one1", width=185, anchor=tk.CENTER)
        tree1.column("two1", width=185,anchor=tk.CENTER)
        tree1.column("three1", width=185,anchor=tk.CENTER)

        tree1.heading("one1", text="Дата проведения операции", anchor=tk.CENTER)
        tree1.heading("two1", text="Наименование типа операции",anchor=tk.CENTER)
        tree1.heading("three1", text="Сумма",anchor=tk.CENTER)
        tree1['show']='headings'
        tree1.pack()
        tree1.place(relx=.1, rely=.3)    
        accNum=values[3]
        print(accNum)
    
        cursor.execute("SELECT tblOperation.datOperation, tblOperationType.txtOperationTypeName,\
tblOperation.fltValue FROM tblOperation, tblOperationType, tblAccount Where (tblAccount.txtAccountNumber=?)\
AND (tblOperation.intOperationTypeId=tblOperationType.intOperationTypeId) AND (tblOperation.intAccountId=tblAccount.intAccountId)", accNum)

        row1 = cursor.fetchone()
        i = 0
        while row1:        
            tree1.insert('', 'end', values=(row1[0], row1[1],row1[2]))
            #tree1['show']='headings'
            row1 = cursor.fetchone()

        btn2=Button(account, text="Новая операция", width=20,command=lambda:new_operation(values[0], values[3], values[1]))
        btn2.pack()
        btn2.place(relx=.65, rely=.8)
        
    tree.bind('<Double-Button-1>', double_click)
#---------------------------------------------------------------------------------------------------


    

def main():
  
    MainRoot.title("Банковские операции")
    MainRoot.geometry("300x400")
    accounts = tk.Button(MainRoot, text="Счета", width = 14, height = 2, font=("Comic Sans MS", 8), border="4", command = main1)
    accounts.place(relx = 0.50, rely = 0.1, anchor = tk.CENTER)

    reportAccounts = tk.Button(MainRoot, text="Отчет по счетам", width = 14, height = 2, font=("Comic Sans MS", 8), border="4", command = report1)
    reportAccounts.place(relx = 0.50, rely = 0.3, anchor = tk.CENTER)

    reportClosedAccounts = tk.Button(MainRoot, text="Отчет по закрытым счетам", width = 20, height = 2, font=("Comic Sans MS", 8), border="4", command = report2)
    reportClosedAccounts.place(relx = 0.50, rely = 0.5, anchor = tk.CENTER)
    lab=Label(MainRoot, text="Выберите номер счета: ")
    lab.place(relx=0.1, rely=.65)
    global getNum
        #РАСКРЫВАЮЩИЙСЯ СПИСОК
    def combo_input():
        cursor.execute("SELECT txtAccountNumber FROM tblAccount")
        data=[]
        for row2 in cursor.fetchall():
            data.append(row2[0])
        return data        
    
    def ifComboSel(event):
        print("тип вывелся")
        global getNum
        getNum=combo.get()
           # getType=getType.replace(" ", "")
        print (getNum) #проверка выведения типа
    combo = ttk.Combobox(MainRoot, textvariable=getNum)
    combo.place(relx=.1, rely=.7, width="250")
    combo.bind("<<ComboboxSelected>>", ifComboSel)
    combo['values'] = combo_input()


    reportStatement = tk.Button(MainRoot, text="Выписка по счету", width = 14, height = 2, font=("Comic Sans MS", 8), border="4", command = lambda: report3(getNum))
    reportStatement.place(relx = 0.50, rely = 0.9, anchor = tk.CENTER)
        

# Передача управления пользователю
    MainRoot.mainloop()

# Закрытие курсора и соединения с базой данной
    cursor.close()
    conn.close()

if __name__=="__main__":
    main()

