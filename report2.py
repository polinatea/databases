import pyodbc
import tkinter as tk
from tkinter import ttk
from tkinter import *
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re

def report2():
# Установление соединения с базой данной
    conn = pyodbc.connect(driver = '{SQL Server Native Client 11.0}',server = '192.168.112.103' , database = 'db22205', user = 'User053', password = 'User053#!31')


    cursor = conn.cursor()
 
    report=canvas.Canvas("report2.pdf")
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    report.setFont('FreeSans', 16)
    report.drawString(200, 810, "Закрытые счета")
    report.setStrokeColorRGB(0.2,0.5,0.3)

    report.line(0, 805, 1000, 805)
    report.line(0, 805, 1000, 806) # линия толще

    cursor.execute("""Select DISTINCT tblAccountType.txtAccountTypeName FROM tblAccountType""")
    list_data = []
    row = cursor.fetchone()   # получение данных записи
    
    while row:
        list_data.append(row[0])
        row = cursor.fetchone()   # получение данных одной записи
    
    x = 20
    y = 790
    
    pdfmetrics.registerFont(TTFont('FreeSans','FreeSans.ttf'))
    report.setFont('FreeSans', 12)
    
    for i in list_data:    

     #surn = i1[0]
    # name = i1[1]
    # patr = i1[2]
    
        count_str = 0
        count_oper=0
        if y <= 100:
            x = 20
            y = 790
            report.showPage() # новая страница
            pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
            report.setFont('FreeSans', 16)
            report.drawString(200, 810, "Закрытые счета")
            report.setStrokeColorRGB(0.2,0.5,0.3)
            report.setFont('FreeSans', 12)
            report.line(0, 805, 1000, 805)
            report.line(0, 805, 1000, 806) # линия толще
    
        pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
        report.setFont('FreeSans', 6)
        report.setFillColorRGB(1,0,0)
        report.drawString(50, y, i)
        y = y - 20
        report.setFillColorRGB(0,0,0)
        report.setFont('FreeSans', 7)
        report.drawString(x, y, "Номер счета"+"                             " + "Дата открытия" +"                         "+ "Дата закрытия" +"                          "+ "ФИО"+"                                                      "+ "Адрес")

        cursor.execute(""" SELECT tblAccount.txtAccountNumber, tblAccount.datAccountBegin,tblAccount.datAccountEnd, tblClient.txtClientSurname,
                    tblClient.txtClientName, tblClient.txtClientSecondName,tblClient.txtClientAddress,tblAccount.intAccountId
                   FROM tblAccount, tblAccountType,tblClient
                   WHERE (tblAccount.intAccountTypeId = tblAccountType.intAccountTypeId) and (tblAccount.intClientId=tblClient.intClientId)
                   and(tblAccountType.txtAccountTypeName=?)""",i)
        list_data1=[]
        row1 = cursor.fetchone()
        y -= 15
    
        while row1:
            count_str += 1
#        report.drawString(x, y, row1[0] +"          "+ row1[1] +"                                     "+ row[2] +"                                                       "+row[3])
            report.drawString(x, y, row1[0] +"            "+ str(row1[1]) +"                                  "+ str(row1[2]) +"          "+row1[3].replace(" ","")+ " " + row1[4].replace(" ","")+ " " +row1[5].replace(" ","")+ "                   " +row1[6])


        
            row1 = cursor.fetchone()
            y = y - 15
            if y <= 40:
                x = 20
                y = 790
                report.showPage() # новая страница
                pdfmetrics.registerFont(TTFont('FreeSans','FreeSans.ttf'))
                report.setFont('FreeSans', 16)
                report.drawString(200, 810, "Закрытые счета")
                report.setFont('FreeSans', 12)
                y = y - 5
                report.line(0, y, 1000, y - 3)
                y=y-20
                report.setStrokeColorRGB(1,0,0)
                report.setFont('FreeSans', 6)
        y=y-5
        report.setFont('FreeSans', 6)
        report.drawString(x, y, "Кол-во счетов: ")
        report.drawString(x + 100, y, str(count_str))
        y = y - 5
        report.setStrokeColorRGB(0.2,0.5,0.3)
        y=y-15
##        list_data1.append(row1[0])
##        print(list_data1)
##        for j in list_data1:
##            print(j)
        report.drawString(x, y, "Дата проведения операции"+"         " + "Тип операции" +"                                          "+ "Сумма операции")
        cursor.execute(""" SELECT tblOperation.datOperation, tblOperationType.txtOperationTypeName, tblOperation.fltValue
                        FROM tblOperation, tblOperationType,tblAccountType,tblAccount
                        WHERE (tblOperation.intOperationTypeId=tblOperationType.intOperationTypeId) AND (tblOperation.intAccountId=tblAccount.intAccountId)
                        AND (tblAccount.intAccountTypeId=tblAccountType.intAccountTypeId) AND (tblAccountType.txtAccountTypeName=?)""",i)
            
        row2=cursor.fetchone()
        y-=15
        while row2:
            count_oper+=1
                #print(str(row2[0]))
               # print(str(row2[1]))
                #print(str(row2[2]))
            report.setFont('FreeSans', 6)
            report.drawString(x, y, str(row2[0]).replace(" ", "") +"                                          "+ row2[1] +"   "+ str(row2[2]) )
            row2=cursor.fetchone()
            y=y-15
            if y <= 40:
                x = 20
                y = 790
                report.showPage() # новая страница
                pdfmetrics.registerFont(TTFont('FreeSans','FreeSans.ttf'))
                report.setFont('FreeSans', 16)
                report.drawString(200, 810, "Закрытые счета")
                y = y - 5
                report.line(0, y, 1000, y - 3)
                y=y-20

        report.setFont('FreeSans', 6)         
        y=y-5
        report.drawString(x, y, "Кол-во операций: ")
        report.drawString(x + 100, y, str(count_oper))
        y = y - 5
        report.line(0, y, 1000, y - 3)
        y=y-20
    report.save()
# Закрытие курсора и соединения с базой данной
    print ('privet2')
    cursor.close()
    conn.close()
