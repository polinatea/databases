import pyodbc
import tkinter as tk
from tkinter import ttk
from tkinter import *
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re

def report3(txtNum):
# Установление соединения с базой данной
    conn = pyodbc.connect(driver = '{SQL Server Native Client 11.0}',server = '192.168.112.103' , database = 'db22205', user = 'User053', password = 'User053#!31')


    cursor = conn.cursor()
 
    report=canvas.Canvas("report3.pdf")
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    report.setFont('FreeSans', 10)
    report.drawString(200, 810, "Выписка по счету")
    report.setStrokeColorRGB(0.2,0.5,0.3)

    report.line(0, 805, 1000, 805)
    report.line(0, 805, 1000, 806) # линия толще

    #txtNum = '40817810570000123456' 
    cursor.execute("""Select tblAccountType.txtAccountTypeName, tblClient.txtClientSurname, tblClient.txtClientName,
                    tblClient.txtClientSecondName, tblAccount.datAccountBegin
                   from tblAccountType, tblClient, tblAccount
                   Where (tblAccount.intAccountTypeId=tblAccountType.intAccountTypeId ) AND
                   (tblAccount.intClientId=tblClient.intClientId) AND
                   (tblAccount.txtAccountNumber = ?)""", txtNum)

    row = cursor.fetchone()   # получение данных записи
    
    x = 20
    y = 780
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    report.setFont('FreeSans', 16)
    report.setFillColorRGB(1,0,0)

    report.drawString(x + 160, y,txtNum)
    y-= 5
    report.setFillColorRGB(0,0,0)
    report.setFont('FreeSans', 10)
    report.drawString(x , y-10, "Тип счета:  " + re.sub(r'\s+', ' ', row[0]))
    report.drawString(x , y-20,"Клиент:  "+ row[1].replace(" ", "")+" "+row[2].replace(" ", "")+" "+row[3].replace(" ", ""))
    report.drawString(x , y-30, "Дата открытия:  "+str(row[4]))
    y-= 60
        
    pdfmetrics.registerFont(TTFont('FreeSans','FreeSans.ttf'))
    report.setFont('FreeSans', 12)


    report.setFillColorRGB(0,0,0)
    report.drawString(x, y, "Список операций: ")
    y=y-15
    pdfmetrics.registerFont(TTFont('FreeSans','FreeSans.ttf'))
    report.setFont('FreeSans', 12)

    report.drawString(x, y, "Дата проведения операции:"+"              " + "Тип операции:" +"                   "+ "Сумма операции:")
    y=y-5   
    report.line(0, y, 1000, y - 3)
    y=y-20
    cursor.execute(""" SELECT tblOperation.datOperation, tblOperationType.txtOperationTypeName, tblOperation.fltValue
                        FROM tblOperation, tblOperationType,tblAccountType,tblAccount
                        WHERE (tblOperation.intOperationTypeId=tblOperationType.intOperationTypeId) AND (tblOperation.intAccountId=tblAccount.intAccountId)
                        AND (tblAccount.intAccountTypeId=tblAccountType.intAccountTypeId) AND (tblAccount.txtAccountNumber=?)
                        order by tblOperation.datOperation desc """,txtNum)
            
    row2=cursor.fetchone()
    print(row2)
    y-=15
    report.setFillColorRGB(0,0,0)
    report.setFont('FreeSans', 12)
    while row2:

        report.drawString(x, y, str(row2[0]).replace(" ", "") +"                                          "+re.sub(r'\s+', ' ', row2[1]) +"                               "+ str(row2[2]) )
        row2=cursor.fetchone()
        y=y-15
        y=y-20
        if y <= 40:
            x = 20
            y = 790
            report.showPage() # новая страница
            pdfmetrics.registerFont(TTFont('FreeSans','FreeSans.ttf'))
            report.setFont('FreeSans', 12)
            report.drawString(200, 810, "Закрытые счета")
            report.setStrokeColorRGB(1,0,0)
            
    y=y-5   
    report.line(0, y, 1000, y - 3)
    y=y-20
    report.save()
    # Закрытие курсора и соединения с базой данной
    print ('privet3')
    cursor.close()
    conn.close()
