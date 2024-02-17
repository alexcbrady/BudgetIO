from dotenv import load_dotenv
import os
import pymysql.cursors
from tkinter import *
from tkcalendar import Calendar, DateEntry
import pandas as pd
from datetime import date
import openpyxl
from openpyxl.chart import PieChart, Reference
import time
from openpyxl.styles.borders import Border, Side
from openpyxl.chart.label import DataLabelList

load_dotenv()

#define tk window
windowMain = Tk()
windowMain.title('BudgetIO')
windowMain.geometry('600x400')


#DATE INPUT
dateText = Label(windowMain, text='Enter date of purchase:')
dateText.grid(row=1, column=1)
Bdate = DateEntry(windowMain,date_pattern='yyyy-mm-dd', foreground='white', background='white', width=19)
Bdate.grid(column=2, row=1)

#PRICE INPUT
priceText = Label(windowMain, text="Enter price of item/service:")
priceText.grid(row=2, column=1)
priceVar = StringVar()
price = Entry(windowMain, textvariable=priceVar, background='white', foreground='black')
price.grid(row=2,column=2)

#PLACE OF PURCHASE INPUT
whereText = Label(windowMain, text="Enter place of purchase:")
whereText.grid(row=3, column=1)
whereVar = StringVar()
where = Entry(windowMain, textvariable=whereVar, background='white', foreground='black')
where.grid(row=3, column=2)

#CATEGORY OF PURCHASE INPUT
categoriesText = Label(windowMain, text='Enter category of purchase:')
categoriesText.grid(row=4, column=1)
categories = [
    'Housing',
    'Utilities',
    'Grocery',
    'Phone',
    'Fun',
    'Misc'
    ]
categoryVar = StringVar()
categoryDrop = OptionMenu(windowMain, categoryVar, *categories)
categoryDrop.config(width=19)
categoryDrop.grid(row=4, column=2)

#INSERT DATA BUTTON
insertGo = Button(windowMain,text='Insert', command=(lambda: (insertSQL(Bdate, priceVar.get(), whereVar.get(), categoryVar.get()))))
insertGo.grid(row=4, column=3)


#VIEW-RANGE WINDOW
def newRangeWindow():
    rangeWindow = Toplevel(windowMain)
    rangeWindow.title('Purchase Range')
    rangeWindow.geometry('600x400')

    #START DATE OF SEARCH
    lDateLable = Label(rangeWindow, text="DATE: From:")
    lDate = DateEntry(rangeWindow,date_pattern='yyyy-mm-dd', foreground='white', background='white', width=19)
    lDateLable.grid(column=1, row=1)
    lDate.grid(column=2, row=1)

    #END DATE OF SEARCH
    rDateLabel = Label(rangeWindow, text="To:")
    rDate = DateEntry(rangeWindow,date_pattern='yyyy-mm-dd', foreground='white', background='white', width=19)
    rDateLabel.grid(column=3, row=1)
    rDate.grid(column=4, row=1)

    #START PRICE INPUT
    lPriceVar = StringVar()
    lPriceLable = Label(rangeWindow, text='PRICE: From:')
    lPrice = Entry(rangeWindow, textvariable=lPriceVar, background='white', foreground='black')
    lPriceLable.grid(column=1, row=2)
    lPrice.grid(column=2,row=2)

    #END PRICE INPUT
    rPriceVar = StringVar()
    rPriceLabel = Label(rangeWindow, text='To:')
    rPrice = Entry(rangeWindow, textvariable=rPriceVar, background='white', foreground='black')
    rPriceLabel.grid(column=3, row=2)
    rPrice.grid(column=4, row=2)

    #CATEGORY INPUT
    categoriesText = Label(rangeWindow, text='Enter category of purchase:')
    categoriesText.grid(row=3, column=1)
    categories = [
        'Housing',
        'Utilities',
        'Grocery',
        'Phone',
        'Fun',
        'Misc',
        'Home'
        ]
    categoryVarRange = StringVar()
    categoryDrop = OptionMenu(rangeWindow, categoryVarRange, *categories)
    categoryDrop.config(width=19)
    categoryDrop.grid(row=3, column=2)

    #EXECUTE RANGE SELECTION BUTTON
    executeRange = Button(rangeWindow, text='Execute', command= lambda:selectRangeSQL(lDate, rDate, lPriceVar.get(), rPriceVar.get(), categoryVarRange.get(), csvVar.get()))
    executeRange.grid(row=4, column=4)

    executeWideOpen = Button(rangeWindow, text='Wide Open', command=lambda:SqlWideOpen(csvVar.get()))
    executeWideOpen.grid(row=5,column=4)

    #CSV NAME
    csvVar = StringVar()
    csvLabel = Label(rangeWindow, text='*CSV file name:')
    csvName = Entry(rangeWindow, textvariable=csvVar, background='white', foreground='black')
    csvLabel.grid(column=1, row=4)
    csvName.grid(column=2, row=4)

def newDeleteWindow():
    deleteWindow = Toplevel(windowMain)
    deleteWindow.title('Delete Entry')
    deleteWindow.geometry('600x400')

    #DATE TO DELETE
    dateText = Label(deleteWindow, text='Enter date of purchase:')
    dateText.grid(row=1, column=1)
    Bdate = DateEntry(deleteWindow,date_pattern='yyyy-mm-dd', foreground='white', background='white', width=19)
    Bdate.grid(column=2, row=1)

    #PRICE TO DELETE
    priceText = Label(deleteWindow, text="Enter price of item/service:")
    priceText.grid(row=2, column=1)
    priceVar = StringVar()
    price = Entry(deleteWindow, textvariable=priceVar, background='white', foreground='black')
    price.grid(row=2,column=2)

    #PLACE OF PURCHASE TO DELETE
    whereText = Label(deleteWindow, text="Enter place of purchase:")
    whereText.grid(row=3, column=1)
    whereVar = StringVar()
    where = Entry(deleteWindow, textvariable=whereVar, background='white', foreground='black')
    where.grid(row=3, column=2)

    #CATEGORY OF PURCHASE TO DELETE
    categoriesText = Label(deleteWindow, text='Enter category of purchase:')
    categoriesText.grid(row=4, column=1)
    categories = [
        'Housing',
        'Utilities',
        'Grocery',
        'Phone',
        'Fun',
        'Misc'
        ]
    categoryVar = StringVar()
    categoryDrop = OptionMenu(deleteWindow, categoryVar, *categories)
    categoryDrop.config(width=19)
    categoryDrop.grid(row=4, column=2)

    #DELETE DATA BUTTON
    deleteGo = Button(deleteWindow,text='Delete', command = lambda: verifyDeleteWindow(deleteWindow, Bdate.get_date(), priceVar, whereVar, categoryVar))
    deleteGo.grid(row=6, column=3)


def verifyDeleteWindow(topWindow, when : Calendar, price : StringVar, where : StringVar, category : StringVar):
    verifyDelete = Toplevel(topWindow)
    verifyDelete.title('Verify Deletion')
    verifyDelete.geometry('350x150')

    verifyQuestion = Label(verifyDelete,text=f'Do you wish to delete this entry of ${price.get()} spent at {where.get()} on {when}?', justify='center', wraplength=260)
    verifyQuestion.grid(row=1,column=1)

    yesButton = Button(verifyDelete,text='YES', command=lambda: (sqlDelete(when, price.get(), where.get(), category.get())), justify='left')
    yesButton.grid(row=2, column=1)

    noButton = Button(verifyDelete,text='NO', command= lambda : verifyDelete.destroy(), justify='left')
    noButton.grid(row=2, column=2)



    

#MENU BAR TKINTER
mainMenu = Menu(windowMain)
findMenu = Menu(mainMenu)
optionMenu = Menu(mainMenu)
mainMenu.add_cascade(label='Find', menu=findMenu)
findMenu.add_command(label='Range', command=newRangeWindow)
mainMenu.add_cascade(label='Options', menu=optionMenu)
optionMenu.add_separator()
optionMenu.add_command(label='DELETE', command=newDeleteWindow)




windowMain.config(menu=mainMenu)


#--------SQL METHODS----------#

#INSERTS PURCHASES INTO DB -------METHOD--------
def insertSQL(bdate : Calendar, amount , Where , Category):
    cxn = pymysql.connect(host= os.getenv('HOST'), user= 'root', password=os.getenv('PASSWORD'), database='budget',cursorclass=pymysql.cursors.DictCursor )
    with cxn:
        with cxn.cursor() as cursor:
            cursor.execute(f"INSERT INTO expenses VALUES ('{bdate.get_date()}', {amount}, '{Where}', '{Category}')")
            result = cursor.fetchone()
            print(result)
        cxn.commit()

#SEARCHES SQL DB VIA RANGE -----METHOD--------
def selectRangeSQL(ldate : Calendar, rdate : Calendar, lprice, rprice, category, xlName):
    cxn = pymysql.connect(host= os.getenv('HOST'), user= 'root', password=os.getenv('PASSWORD'), database='budget',cursorclass=pymysql.cursors.DictCursor )
    with cxn:
        with cxn.cursor() as cursor:

            #RANGE BY DATE, CATEGORY, AND PRICE
            if (ldate != '' and rdate != '') and lprice != '' and rprice !='' and category != '':
                query = f"SELECT Bdate, price, location, category FROM budget.expenses WHERE bdate BETWEEN '{ldate.get_date()}' AND '{rdate.get_date()}' AND category = '{category}' AND price BETWEEN {lprice} AND {rprice}"
                df = pd.read_sql(query, cxn)
                
            #RANGE BY DATE AND CATEGORY
            if (ldate != '' and rdate != '') and lprice == '' and rprice == '' and category != '':
                query = f"SELECT Bdate, price, location, category FROM budget.expenses WHERE bdate BETWEEN '{ldate.get_date()}' AND '{rdate.get_date()}' AND category = '{category}';"
                df = pd.read_sql(query, cxn)

            #RANGE BY DATE AND PRICE
            if (ldate != '' and rdate != '') and lprice != '' and rprice != '' and category == '':
                query = f"SELECT Bdate, price, location, category FROM budget.expenses WHERE bdate BETWEEN '{ldate.get_date()}' AND '{rdate.get_date()}' AND price BETWEEN {lprice} AND {rprice};"
                df = pd.read_sql(query, cxn)

            #RANGE ONLY BY DATE
            if (ldate != '' and rdate != '') and lprice == '' and rprice == '' and category == '':
                query = f"SELECT Bdate, price, location, category FROM budget.expenses WHERE bdate BETWEEN '{ldate.get_date()}' AND '{rdate.get_date()}';"
                df = pd.read_sql(query, cxn)
    
        cxn.commit()
    df.to_excel(f"{os.getenv('BUDGETIO_OUTPUT_PATH')}{xlName} {ldate.get_date()} {rdate.get_date()}.xlsx")

    #CREATING PIE CHART IN EXCEL
    workbook = openpyxl.load_workbook(f"{os.getenv('BUDGETIO_OUTPUT_PATH')}{xlName} {ldate.get_date()} {rdate.get_date()}.xlsx")
    sheet = workbook.active
    chart = PieChart()
    labels = Reference(sheet, min_col=5, max_col=5, min_row=2, max_row=len(df.index)+1)
    data = Reference(sheet, min_col=3, max_col=3, min_row=2, max_row=len(df.index)+1)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(labels)
    chart.title = 'Categorical Spending'
    sheet.add_chart(chart, 'G2')

    #FORMATTING DATE COLUMN
    dateCol = sheet.column_dimensions['B']
    dateCol.number_format = 'YYYY MM DD'

    #ADDING SUMMATION CELL TO PRICE COLUMN
    sheet[f'C{len(df.index)+2}'] = f'=SUM(C2:C{len(df.index)+1})'
    sheet[f'A{len(df.index)+2}'] = 'SUM'
    #BORDER FOR SUMMATION CELL
    thickBorder = Border(top = Side(style = 'thick'))
    sheet.cell(row = len(df.index)+2, column = 3).border = thickBorder

    workbook.save(f"{os.getenv('BUDGETIO_OUTPUT_PATH')}{xlName} {ldate.get_date()} {rdate.get_date()}.xlsx")

#FOR RANGE PAGE - WIDE OPEN ----- METHOD ----------
def SqlWideOpen(xlName):
    cxn = pymysql.connect(host= os.getenv('HOST'), user= 'root', password= os.getenv('PASSWORD'), database='budget',cursorclass=pymysql.cursors.DictCursor )
    with cxn:
        with cxn.cursor() as cursor:
            query = "SELECT * FROM Budget.expenses;"
            df = pd.read_sql(query, cxn)
        cxn.commit()
    df.to_excel(f"{os.getenv('BUDGETIO_OUTPUT_PATH')}{xlName} {date.today()}.xlsx")
    
    
    #CREATING PIE CHART IN EXCEL
    workbook = openpyxl.load_workbook(f"{os.getenv('BUDGETIO_OUTPUT_PATH')}{xlName} {date.today()}.xlsx")
    sheet = workbook.active
    chart = PieChart()
    labels = Reference(sheet, min_col=5, max_col=5, min_row=2, max_row=len(df.index)+1)
    data = Reference(sheet, min_col=3, max_col=3, min_row=2, max_row=len(df.index)+1)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(labels)
    chart.title = 'Categorical Spending'
    sheet.add_chart(chart, 'G2')
    
    
    #FORMATTING DATE COLUMN
    dateCol = sheet.column_dimensions['B']
    dateCol.number_format = 'YYYY MM DD'

    #ADDING SUMMATION CELL TO PRICE COLUMN
    sheet[f'C{len(df.index)+2}'] = f'=SUM(C2:C{len(df.index)+1})'
    sheet[f'A{len(df.index)+2}'] = 'SUM'
    #BORDER FOR SUMMATION CELL
    thickBorder = Border(top = Side(style = 'thick'))
    sheet.cell(row = len(df.index)+2, column = 3).border = thickBorder

    workbook.save(f"{os.getenv('BUDGETIO_OUTPUT_PATH')}{xlName} {date.today()}.xlsx")
    
def sqlDelete(bdate : Calendar, amount , Where , Category):
    cxn = pymysql.connect(host= os.getenv('HOST'), user= 'root', password=os.getenv('PASSWORD'), database='budget',cursorclass=pymysql.cursors.DictCursor )
    with cxn:
        with cxn.cursor() as cursor:
            cursor.execute(f"DELETE FROM expenses WHERE bdate = '{bdate}' AND price = {amount} AND location = '{Where}' AND category ='{Category}'")
            result = cursor.fetchone()
            print(result)
        cxn.commit()







windowMain.mainloop()