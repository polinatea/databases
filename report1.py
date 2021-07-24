import pyodbc
import tkinter as tk
from tkinter import ttk
from tkinter import *
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re

def report1():
# Установление соединения с базой данной
    conn = pyodbc.connect(driver = '{SQL Server Native Client 11.0}',server = '192.168.112.103' , database = 'db22205', user = 'User053', password = 'User053#!31')


    cursor = conn.cursor()
 
    report=canvas.Canvas("report1.pdf")
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    report.setFont('FreeSans', 16)
    report.drawString(200, 810, "Счета")
    report.setStrokeColorRGB(0.2,0.5,0.3)

    report.line(0, 805, 1000, 805)
    report.line(0, 805, 1000, 806) # линия толще



    cursor.execute("""Select DISTINCT tblClient.intClientId, tblClient.txtClientSurname,tblClient.txtClientName,tblClient.txtClientSecondName, tblClient.datBirthday, tblClient.txtClientAddress
                from tblClient""")

    list_data = []
    row = cursor.fetchone()   # получение данных записи 
    while row:
        list_data.append(row[1]+row[2]+row[3]+str(row[4])+"           "+row[5])  
        row = cursor.fetchone()   # получение данных одной записи
    
    x = 20
    y = 790

    pdfmetrics.registerFont(TTFont('FreeSans','FreeSans.ttf'))
    report.setFont('FreeSans', 12)
    
    for i in list_data:    
        i1 = re.sub(r'\s+', ' ', i)
        i1 = i1.split(' ')
    # surn = i1[0]
    # name = i1[1]
    # patr = i1[2]
    
        count_str = 0
        if y <= 100:
            x = 20
            y = 790
            report.showPage() # новая страница
            pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
            report.setFont('FreeSans', 12)
            report.drawString(200, 810, "Счета")
            report.setStrokeColorRGB(0.2,0.5,0.3)
            report.line(0, 805, 1000, 805)
            report.line(0, 805, 1000, 806) # линия толще
    
        pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
        report.setFont('FreeSans', 6)
        report.setFillColorRGB(1,0,0)
        report.drawString(50, y, i)
        y = y - 20
        report.setFillColorRGB(0,0,0)
        report.setFont('FreeSans', 7)
        report.drawString(x, y, "Номер счета"+"                             " + "Наименование типа счета" +"                         "+ "Дата открытия счета" +"                          "+ "Сумма на счете")
##        cursor.execute(""" SELECT tblAccount.txtAccountNumber, tblAccountType.txtAccountTypeName, tblAccount.datAccountBegin, tblAccount.fltAccountSum
##                       FROM tblAccount, tblAccountType
##                       WHERE (tblAccount.intAccountTypeId = tblAccountType.intAccountTypeId) and (tblAccount.intClientId=?)""",row[0])

        cursor.execute(""" SELECT tblAccount.txtAccountNumber, tblAccountType.txtAccountTypeName, tblAccount.datAccountBegin, tblAccount.fltAccountSum
                   FROM tblAccount, tblAccountType,tblClient
                   WHERE (tblAccount.intAccountTypeId = tblAccountType.intAccountTypeId) and (tblAccount.intClientId=tblClient.intClientId) and (tblClient.txtClientSurname=?)
                   and(tblClient.txtClientName=?) and(tblClient.txtClientSecondName=?)""",i1[0],i1[1],i1[2])        
        row1 = cursor.fetchone()
        y -= 15
    
        while row1:
            count_str += 1
            a =str(row1[2])
            b=str(row1[3])
            report.drawString(x, y, row1[0] +"          "+ re.sub(r'\s+', ' ', row1[1]) +"                                     "+a.replace(" ","") +"                                                       "+b.replace(' ', ''))
            row1 = cursor.fetchone()
            y = y - 15
        y = y -5
        report.drawString(x, y, "Кол-во счетов: ")
        report.drawString(x + 100, y, str(count_str))
        y = y - 5
        report.setStrokeColorRGB(0.2,0.5,0.3)
    
        y = y - 15

        cursor.execute(""" SELECT sum (fltAccountSum) FROM  tblAccount, tblClient WHERE (tblAccount.intClientId=tblClient.intClientId) and (tblClient.txtClientSurname=?)
                   and(tblClient.txtClientName=?) and(tblClient.txtClientSecondName=?)""",i1[0],i1[1],i1[2] )
        row2=cursor.fetchone()
        report.drawString(x, y, "Общая сумма: ")
        report.drawString(x + 100, y-3, str(row2[0]))
        y = y - 25
        report.line(0, y, 1000, y - 3)
        y=y-20
    report.save()
    # Закрытие курсора и соединения с базой данной
    print ('privet')
    cursor.close()
    conn.close()
