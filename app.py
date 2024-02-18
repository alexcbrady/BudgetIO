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
from sqlalchemy import create_engine

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
insertGo = Button(windowMain,text='Insert', command=(lambda: (insertExpenseSQL(Bdate, priceVar.get(), whereVar.get(), categoryVar.get()))))
insertGo.grid(row=4, column=3)


#INSERT INCOME WINDOW
def newIncomeWindow():
    incomeWindow = Toplevel(windowMain)
    incomeWindow.title('Income')
    incomeWindow.geometry('600x400')

    #DATE OF INCOME
    incomeDateLabel = Label(incomeWindow, text='Enter date of income:')
    incomeDateLabel.grid(row=1, column=1)

    incomeDateEntry = DateEntry(incomeWindow, date_pattern='yyyy-mm-dd', width=19)
    incomeDateEntry.grid(row=1, column=2)

    #CHECKING AMOUNT
    checkingLabel = Label(incomeWindow, text='Enter checking amount:')
    checkingLabel.grid(row=2, column=1)

    checkingVar = StringVar()
    checkingEntry = Entry(incomeWindow, textvariable=checkingVar, background='white', foreground='black')
    checkingEntry.grid(row=2, column=2)

    #SAVINGS AMOUNT
    savingsLabel = Label(incomeWindow, text='Enter savings amount:')
    savingsLabel.grid(row=3, column=1)

    savingsVar = StringVar()
    savingsEntry = Entry(incomeWindow, textvariable=savingsVar, background='white', foreground='black')
    savingsEntry.grid(row=3,column=2)

    #RETIREMENT AMOUNT
    retirementLabel = Label(incomeWindow, text='Enter retirement amount:')
    retirementLabel.grid(row=4, column=1)

    retirementVar = StringVar()
    retirementEntry = Entry(incomeWindow, textvariable=retirementVar, background='white', foreground='black')
    retirementEntry.grid(row=4, column=2)

    #SOURCE OF INCOME
    sourceLabel = Label(incomeWindow, text='Enter source of income:')
    sourceLabel.grid(row=5, column=1)

    sources = [
    'Qorvo',
    'Other'
    ]
    sourceVar = StringVar()
    sourceDrop = OptionMenu(incomeWindow, sourceVar, *sources)
    sourceDrop.config(width=19)
    sourceDrop.grid(row=5, column=2)

    insertIncomeButton = Button(incomeWindow, text='Insert', command= lambda: insertIncomeSQL(incomeDateEntry, checkingVar.get(), savingsVar.get(), retirementVar.get(), sourceVar.get()))
    insertIncomeButton.grid(row=5,column=3)

#VIEW-RANGE WINDOW
def newExpenseViewWindow():
    rangeWindow = Toplevel(windowMain)
    rangeWindow.title('Expense Export')
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
    executeRange = Button(rangeWindow, text='Execute', command= lambda:viewExpenseRangeSQL(lDate, rDate, lPriceVar.get(), rPriceVar.get(), categoryVarRange.get(), csvVar.get()))
    executeRange.grid(row=4, column=4)

    executeWideOpen = Button(rangeWindow, text='Wide Open', command=lambda:expenseSQLWideOpen(csvVar.get()))
    executeWideOpen.grid(row=5,column=4)

    #CSV NAME
    csvVar = StringVar()
    csvLabel = Label(rangeWindow, text='*File name:')
    csvName = Entry(rangeWindow, textvariable=csvVar, background='white', foreground='black')
    csvLabel.grid(column=1, row=4)
    csvName.grid(column=2, row=4)

def newViewIncomeWindow():
    viewIncomeWindow = Toplevel(windowMain)
    viewIncomeWindow.title('Income Export')
    viewIncomeWindow.geometry('300x100')

    csvLabel = Label(viewIncomeWindow, text='*File name:')
    csvLabel.grid(row=1, column=1)

    csvVar = StringVar()
    csvEntry = Entry(viewIncomeWindow, textvariable=csvVar, background='white', foreground='black')
    csvEntry.grid(row=1, column=2)

    executeIncomeExportButton = Button(viewIncomeWindow, text='Execute', command= lambda: viewSQLIncome(csvVar.get()))
    executeIncomeExportButton.grid(row=3,column=2)

def newDeleteIncomeWindow():
    deleteIncomeWindow = Toplevel(windowMain)
    deleteIncomeWindow.title('Delete Income Entry')
    deleteIncomeWindow.geometry('600x400')

    #DATE TO DELETE
    dateText = Label(deleteIncomeWindow, text='Enter date of income')
    dateText.grid(row=1, column=1)
    Bdate = DateEntry(deleteIncomeWindow,date_pattern='yyyy-mm-dd', foreground='white', background='white', width=19)
    Bdate.grid(column=2, row=1)

    #CHECKING AMOUNT TO DELETE
    checkingLabel = Label(deleteIncomeWindow, text="Enter checking amount:")
    checkingLabel.grid(row=2, column=1)
    checkingVar = StringVar()
    checking = Entry(deleteIncomeWindow, textvariable=checkingVar, background='white', foreground='black')
    checking.grid(row=2,column=2)

    #SAVINGS AMOUNT TO DELETE
    savingsLabel = Label(deleteIncomeWindow, text="Enter savings amount:")
    savingsLabel.grid(row=3, column=1)
    savingsVar = StringVar()
    savings = Entry(deleteIncomeWindow, textvariable=savingsVar, background='white', foreground='black')
    savings.grid(row=3,column=2)

    #RETIREMENT AMOUNT TO DELETE
    retirementLabel = Label(deleteIncomeWindow, text="Enter retirement amount:")
    retirementLabel.grid(row=4, column=1)
    retirementVar = StringVar()
    retirement = Entry(deleteIncomeWindow, textvariable=retirementVar, background='white', foreground='black')
    retirement.grid(row=4,column=2)

    #SOURCE TO DELETE
    sourceLabel = Label(deleteIncomeWindow, text='Enter source of income:')
    sourceLabel.grid(row=5, column=1)

    sources = [
    'Qorvo',
    'Other'
    ]
    sourceVar = StringVar()
    sourceDrop = OptionMenu(deleteIncomeWindow, sourceVar, *sources)
    sourceDrop.config(width=19)
    sourceDrop.grid(row=5, column=2)

    #DELETE INCOME BUTTON
    deleteIncomeButton = Button(deleteIncomeWindow, text='Delete', command=lambda: newVerifyDeleteIncomeWindow(deleteIncomeWindow, Bdate, checkingVar, savingsVar, retirementVar, sourceVar))
    deleteIncomeButton.grid(row=5, column=3)

def newVerifyDeleteIncomeWindow(window, date : Calendar, checking, savings, retirement, source):
    verifyDeleteIncomeWindow = Toplevel(window)
    verifyDeleteIncomeWindow.title('Verify Deletion')
    verifyDeleteIncomeWindow.geometry('350x150')

    total = int(checking.get()) + int(savings.get()) + int(retirement.get())
    verifyQuestion = Label(verifyDeleteIncomeWindow,text=f"Do you wish to delete income entry of {total} reported on {date.get_date()}?")
    verifyQuestion.grid(row=1,column=1)

    yesButton = Button(verifyDeleteIncomeWindow,text='YES', command=lambda: sqlIncomeDelete(date, checking, savings, retirement, source))
    yesButton.grid(row=2, column=1)

    noButton = Button(verifyDeleteIncomeWindow,text='NO', command= lambda : verifyDeleteIncomeWindow.destroy(), justify='left')
    noButton.grid(row=2, column=2)  

def newDeleteExpenseWindow():
    deleteExpenseWindow = Toplevel(windowMain)
    deleteExpenseWindow.title('Delete Expense Entry')
    deleteExpenseWindow.geometry('600x400')

    #DATE TO DELETE
    dateText = Label(deleteExpenseWindow, text='Enter date of purchase:')
    dateText.grid(row=1, column=1)
    Bdate = DateEntry(deleteExpenseWindow,date_pattern='yyyy-mm-dd', foreground='white', background='white', width=19)
    Bdate.grid(column=2, row=1)

    #PRICE TO DELETE
    priceText = Label(deleteExpenseWindow, text="Enter price of item/service:")
    priceText.grid(row=2, column=1)
    priceVar = StringVar()
    price = Entry(deleteExpenseWindow, textvariable=priceVar, background='white', foreground='black')
    price.grid(row=2,column=2)

    #PLACE OF PURCHASE TO DELETE
    whereText = Label(deleteExpenseWindow, text="Enter place of purchase:")
    whereText.grid(row=3, column=1)
    whereVar = StringVar()
    where = Entry(deleteExpenseWindow, textvariable=whereVar, background='white', foreground='black')
    where.grid(row=3, column=2)

    #CATEGORY OF PURCHASE TO DELETE
    categoriesText = Label(deleteExpenseWindow, text='Enter category of purchase:')
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
    categoryDrop = OptionMenu(deleteExpenseWindow, categoryVar, *categories)
    categoryDrop.config(width=19)
    categoryDrop.grid(row=4, column=2)

    #DELETE DATA BUTTON
    deleteGo = Button(deleteExpenseWindow,text='Delete', command = lambda: newVerifyDeleteExpenseWindow(deleteExpenseWindow, Bdate.get_date(), priceVar, whereVar, categoryVar))
    deleteGo.grid(row=6, column=3)

def newVerifyDeleteExpenseWindow(topWindow, when : Calendar, price : StringVar, where : StringVar, category : StringVar):
    verifyDeleteExpenseWindow = Toplevel(topWindow)
    verifyDeleteExpenseWindow.title('Verify Deletion')
    verifyDeleteExpenseWindow.geometry('350x150')

    verifyQuestion = Label(verifyDeleteExpenseWindow,text=f'Do you wish to delete this entry of ${price.get()} spent at {where.get()} on {when}?', justify='center', wraplength=260)
    verifyQuestion.grid(row=1,column=1)

    yesButton = Button(verifyDeleteExpenseWindow,text='YES', command=lambda: (sqlExpenseDelete(when, price.get(), where.get(), category.get())), justify='left')
    yesButton.grid(row=2, column=1)

    noButton = Button(verifyDeleteExpenseWindow,text='NO', command= lambda : verifyDeleteExpenseWindow.destroy(), justify='left')
    noButton.grid(row=2, column=2)


#INCOME EXPENSE REPORT WINDOW
def newExpenseToIncomeWindow():
    expenseToIncomeWindow = Toplevel(windowMain)   
    expenseToIncomeWindow.title('Expense To Income Report')
    expenseToIncomeWindow.geometry('600x400')

    #FROM   
    lDateLable = Label(expenseToIncomeWindow, text='From:')
    lDateLable.grid(row=1, column=1)

    lDate = DateEntry(expenseToIncomeWindow, date_pattern='yyyy-mm-dd')
    lDate.grid(row=1, column=2)

    #TO
    rDateLabel = Label(expenseToIncomeWindow, text='To:')
    rDateLabel.grid(row=1, column=3)

    rDate = DateEntry(expenseToIncomeWindow, date_pattern='yyyy-mm-dd')
    rDate.grid(row=1, column=4)

    #SHOW EXPENSE TOTAL LABEL
    expenseLabel = Label(expenseToIncomeWindow, text='Total expenses:')
    expenseLabel.grid(row=3, column=1)
    expenseTotal = Label(expenseToIncomeWindow, text='')
    expenseTotal.grid(row=3, column=2)

    #SHOW INCOME TOTAL LABLE
    incomeLabel = Label(expenseToIncomeWindow, text='Total Income:')
    incomeLabel.grid(row=4, column=1)
    incomeTotal = Label(expenseToIncomeWindow, text='')
    incomeTotal.grid(row=4, column=2)

    #SHOW INCOME MINUS EXPENSE LABEL
    netLabel = Label(expenseToIncomeWindow, text='Net:')
    netLabel.grid(row=5, column=1)
    net = Label(expenseToIncomeWindow, text='')
    net.grid(row=5, column=2)

    #TODO CONFIGURE CHECKBOX EXCEL OPTION FOR REPORTS
    #EXCEL CHECKBOX OPTION
    createExcelVar = IntVar()
    createExcelCheckBox = Checkbutton(expenseToIncomeWindow, variable=createExcelVar, text='Create Excel')
    createExcelCheckBox.grid(row=2, column=5)

    #EXECUTE EXPENSE TO INCOME REPORT
    executeExpenseToIncomeReportButton = Button(expenseToIncomeWindow, text='Execute', command= lambda: viewExpenseToIncomeReport(lDate, rDate, incomeTotal, expenseTotal, net)) #PASS TOTAL LABELS IN FUNC FOR UPDATE
    executeExpenseToIncomeReportButton.grid(row=3, column=5)


#MENU BAR TKINTER
mainMenu = Menu(windowMain)
exportMenu = Menu(mainMenu)
deleteMenu = Menu(mainMenu)
insertMenu = Menu(mainMenu)
reportMenu = Menu(mainMenu)

mainMenu.add_cascade(label='Export', menu=exportMenu)
exportMenu.add_command(label='Expense', command=newExpenseViewWindow)
exportMenu.add_separator()
exportMenu.add_command(label='Income', command=newViewIncomeWindow)
mainMenu.add_cascade(label='Delete', menu=deleteMenu)
deleteMenu.add_separator()
deleteMenu.add_command(label='Expense', command=newDeleteExpenseWindow)
deleteMenu.add_separator()
deleteMenu.add_command(label='Income', command=newDeleteIncomeWindow)
mainMenu.add_cascade(label='Insert', menu=insertMenu)
insertMenu.add_command(label='Income', command=newIncomeWindow)
mainMenu.add_cascade(label='Report', menu=reportMenu)
reportMenu.add_command(label='Expense to Income', command=newExpenseToIncomeWindow)


windowMain.config(menu=mainMenu)


#--------SQL METHODS----------#

#INSERTS PURCHASES INTO DB -------METHOD--------
def insertExpenseSQL(bdate : Calendar, amount , Where , Category):
    cxn = pymysql.connect(host= os.getenv('HOST'), user= 'root', password=os.getenv('PASSWORD'), database='budget',cursorclass=pymysql.cursors.DictCursor )
    with cxn:
        with cxn.connect() as con:
            con.execute(f"INSERT INTO expenses VALUES ('{bdate.get_date()}', {amount}, '{Where}', '{Category}')")
            

#INSERT INCOME TO SQL
def insertIncomeSQL(date : Calendar, checking, savings, retirement, source):
    cxn = create_engine(url=f"mysql+pymysql://root:{os.getenv('PASSWORD')}@localhost:3306/Budget")
    with cxn.connect() as con:
            con.execute(f"INSERT INTO income VALUES ('{date.get_date()}', {int(checking)}, {int(savings)}, {int(retirement)}, '{source}')")
            
    
def viewSQLIncome(xlName):
    cxn = create_engine(url=f"mysql+pymysql://root:{os.getenv('PASSWORD')}@localhost:3306/Budget")   
    with cxn.connect() as con:
            query = "SELECT * FROM Budget.income;"
            df = pd.read_sql(query, cxn)
        
    df.to_excel(f"{os.getenv('BUDGETIO_OUTPUT_PATH')}{xlName} {date.today()}.xlsx")
    workbook = openpyxl.load_workbook(f"{os.getenv('BUDGETIO_OUTPUT_PATH')}{xlName} {date.today()}.xlsx")
    sheet = workbook.active
    #CONFIGURE DATE COLUMN IN EXCEL
    dateCol = sheet.column_dimensions['B']
    dateCol.number_format = 'YYYY MM DD'

    workbook.save(f"{os.getenv('BUDGETIO_OUTPUT_PATH')}{xlName} {date.today()}.xlsx")


#SEARCHES SQL EXPENSE TABLE VIA RANGE -----METHOD--------
def viewExpenseRangeSQL(ldate : Calendar, rdate : Calendar, lprice, rprice, category, xlName):
    cxn = create_engine(url=f"mysql+pymysql://root:{os.getenv('PASSWORD')}@localhost:3306/Budget")
   

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
def expenseSQLWideOpen(xlName):
    cxn = create_engine(url=f"mysql+pymysql://root:{os.getenv('PASSWORD')}@localhost:3306/Budget")
    
    query = "SELECT * FROM Budget.expenses;"
    df = pd.read_sql(query, cxn)
    
        
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
    

def sqlExpenseDelete(bdate : Calendar, amount , Where , Category):
    cxn = create_engine(url=f"mysql+pymysql://{os.getenv('USER')}:{os.getenv('PASSWORD')}@localhost:3306/Budget")
    with cxn.connect() as con:
        con.execute(f"DELETE FROM expenses WHERE bdate = '{bdate}' AND price = {amount} AND location = '{Where}' AND category ='{Category}'")
    
    
        

def sqlIncomeDelete(date : Calendar, checking, savings, retirement, source):
    
    cxn = create_engine(url=f"mysql+pymysql://{os.getenv('USER')}:{os.getenv('PASSWORD')}@localhost:3306/Budget")
    with cxn.connect() as con:
        con.execute(f"DELETE FROM income WHERE idate = '{date.get_date()}' AND checking = {checking.get()} AND savings = {savings.get()} AND retirement ={retirement.get()} AND source = '{source.get()}'")
        
            

    


#INCOME EXPENSE SQL STATEMENT TO EXCEL FILE - ANALYSIS
def viewExpenseToIncomeReport(lDate : Calendar, rDate : Calendar, incomeLabel : Label, expenseLabel : Label, netLabel : Label):
    cxn = create_engine(url=f"mysql+pymysql://root:{os.getenv('PASSWORD')}@localhost:3306/Budget")
    with cxn.connect() as con:
            
        incomeQuery = f"SELECT savings, checking FROM budget.income WHERE idate BETWEEN '{lDate.get_date()}' AND '{rDate.get_date()}'"
        incomeDF = pd.read_sql(incomeQuery, cxn)
        print(incomeDF)
        incomeTotal = sum(incomeDF['savings'])
        
        incomeLabel.config(text=f'{incomeTotal}')
        incomeLabel.update()

        expenseQuery = f"SELECT price FROM budget.expenses WHERE Bdate BETWEEN '{lDate.get_date()}' AND '{rDate.get_date()}'"
        expenseDF = pd.read_sql(expenseQuery, cxn)
        expenseTotal = expenseDF['price'].sum()
        expenseLabel.config(text=f'{expenseTotal}')
        expenseLabel.update()

        
        incomeMinusExpense = round(incomeTotal - expenseTotal, 2)

        if incomeMinusExpense < 0:
            netColor = 'red'
        if incomeMinusExpense >= 0:
            netColor = 'green'

        netLabel.config(text=f'{str(incomeMinusExpense)}', foreground=netColor)
        netLabel.update()

        



windowMain.mainloop()