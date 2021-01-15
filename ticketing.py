import random
import time
import datetime
import sqlite3
# from PIL import ImageTK,Image
import math
import parser
from tkinter.ttk import Treeview

from tkcalendar import *
from tkinter import ttk
import tkinter as tk
import mysql.connector as mysql
from tkinter import *
import tkinter.messagebox
import pandas.io.sql as sql
import os
from reportlab.pdfgen import canvas
import tempfile
import pdf_gen
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import mysql.connector as mysql

receipt_window = Tk()

receipt_window.geometry('1700x800+0+0')
receipt_window.title('Sales Receipt')
receipt_window.iconbitmap('C:/Users/Ntokozo/Downloads/hnet.com-image.ico')
receipt_window.configure(background="#edfcf5")


def present_time():
    current_time = time.strftime("%H:%M:%S")
    label_time = Label(receipt_window, font=('arial', 16, 'bold'), justify="center", fg='black',
                       text=current_time,
                       bd=2, bg="#efc9d9", width=14, height=2, relief=RIDGE)
    label_time.after(200, present_time)
    label_time.place(x=5, y=110)

    label_title = Label(receipt_window, font=('arial', 49, 'bold'), justify="center", fg='black',
                        text='============== FIMADOST ==============',
                        bd=10, bg="#e1ecf7", relief=RIDGE)
    label_title.place(x=5, y=10)


PRODUCT_CODE = StringVar()
PRODUCTNAME = StringVar()
QUANTITY = StringVar()
RATE = StringVar()
vat_ = StringVar()
exclude_VAT = StringVar()
total_ = StringVar()
check = StringVar()

receipt_ref = StringVar()
date_of_order = StringVar()
time_of_order = StringVar()

paid_vat = StringVar()
subTotal_ = StringVar()
total_cost = StringVar()
ref_no = StringVar()
entry_to = StringVar()
entry_from = StringVar()
change_ = StringVar()
paid_ = StringVar()


def subTotal():
    if PRODUCT_CODE.get() == '' or PRODUCTNAME.get() == '' or QUANTITY.get() == '' or RATE.get() == '':
        return

    else:
        amount = []
        price = float(RATE.get()) * int(QUANTITY.get())
        amount.append(price)


amount = []


def total():
    if PRODUCT_CODE.get() == '' or PRODUCTNAME.get() == '' or QUANTITY.get() == '' or RATE.get() == '':
        return

    else:

        price = float(RATE.get()) * int(QUANTITY.get())
        amount.append(price)
        subtotal = sum(amount)
        my_vat = sum(amount) * 0.15
        tot = subtotal + my_vat
        total_.set(f'{tot:.2f}')

        my_vat = sum(amount) * 0.15
        vat_.set(f'{my_vat:.2f}')

        subtotal = sum(amount)
        subTotal_.set(f'{subtotal:.2f}')
        paid_.set(paid_entry.get())
        change_.set(change_entry.get())


def excludeVAT():
    vat_.set(0)
    price = float(RATE.get()) * int(QUANTITY.get())
    amount.append(price)
    subtotal = sum(amount)
    my_vat = sum(amount) * 0.0
    tot = subtotal + my_vat
    total_.set(f'{tot:.2f}')

    my_vat = sum(amount) * 0.0
    vat_.set(f'{my_vat:.2f}')

    subtotal = sum(amount)
    subTotal_.set(f'{subtotal:.2f}')


purchases = []


def SubmitData():
    code = (Productcode_entry.get())
    products = (Product_entry.get())
    quantity = (Quantity_entry.get())
    rate = (Rate_entry.get())
    if PRODUCT_CODE.get() == '' or PRODUCTNAME.get() == '' or QUANTITY.get() == '' or RATE.get() == '':
        tkMessageBox.showwarning("INVALID!",
                                 "Entries For Product Code, Product Name, Quantity and Rate Must Not Be Empty")

    else:
        receipt.insert(END, "  " + code + " \t" + products + "\t\t\t" + quantity + "  \t\t    ""R" + rate + "\n")
        purchases.append((code, products, quantity, rate))
        [float(i) for i in rate]
        print(rate)
        # for i in purchases:

        # print(i[3])
        PRODUCT_CODE.set("")
        PRODUCTNAME.set("")

        QUANTITY.set(1)
        RATE.set(0)
        ref_no.set(str(random.randint(1003, 9010099)))


def get_search_row(event):
    item = treeV.item(treeV.focus())
    PRODUCT_CODE.set(item['values'][0])
    PRODUCTNAME.set(item['values'][1])
    RATE.set(item['values'][2])


def printreceipt():
    printR = receipt.get("1.0", "end-1c")
    filename = tempfile.mktemp(".txt")
    open(filename, "w").write(printR)
    os.startfile(filename, "print")



    with open(r"./teller.text","a") as my_file:
        my_file.write("{}".format(receipt.get("1.0","end-1c")))



def display(rows):
    myDB = mysql.connect(
        host="localhost",
        user="root",
        passwd="syssy777",
        database="company_data",
    )

    myDB.cursor()
    treeV.delete(*treeV.get_children())
    for i in rows:
        treeV.insert('', END, values=i)


def search_receipt():
    myDB = mysql.connect(
        host="localhost",
        user="root",
        passwd="syssy777",
        database="company_data",
    )

    c = myDB.cursor()
    see = check.get()
    query = "SELECT* FROM sales_receipt WHERE receipt_number LIKE '%" + see + "%' "

    c.execute(query)
    rows = c.fetchall()
    display(rows)


def search_():
    myDB = mysql.connect(
        host="localhost",
        user="root",
        passwd="syssy777",
        database="company_data",
    )

    c = myDB.cursor()
    see = check.get()
    query = "SELECT Product_Code,Product_Name,Retail_Price FROM store_inventory WHERE Product_Code LIKE'%" + see + "%' OR Product_Name LIKE'%" + see + "%' "

    c.execute(query)
    rows = c.fetchall()
    display(rows)


def reset_():
    check.set('')
    treeV.delete(*treeV.get_children())
    PRODUCT_CODE.set("")
    PRODUCTNAME.set("")
    total_.set('')
    subTotal_.set(0)
    vat_.set(0)
    RATE.set(0)
    ref_no.set("")
    paid_.set("")
    change_.set("")
    receipt.delete('1.0', END)


def i_exit():
    iExit = tkinter.messagebox.askyesno('Exit?', ' Confirm Exit')
    if iExit > 0:
        receipt_window.destroy()
        return


def insert_receipt():
    myDB = mysql.connect(
        host="localhost",
        user="root",
        passwd="syssy777",
        database="company_data",
    )

    c = myDB.cursor()
    query = "INSERT INTO sales_receipt(receipt_number, total_amount, vat,amount_paid,change_received, date,time) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    data = (reference_entry.get(), total_entry.get(), vat_entry.get(), paid_entry.get(), change_entry.get(),
            time.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"))
    c.execute(query, data)

    myDB.commit()
    myDB.close()


def insert_quantity():
    myDB = mysql.connect(
        host="localhost",
        user="root",
        passwd="syssy777",
        database="company_data",
    )

    c = myDB.cursor()
    query = "INSERT INTO sales_record(Quantity,Product_Code, Total_Amount, Date,Time) VALUES (%s,%s,%s,%s)"
    data = (Quantity_entry.get(), Productcode_entry.get(), time.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"))
    c.execute(query, data)

    myDB.commit()
    myDB.close()


def view_custom_history():
    myDB = mysql.connect(
        host="localhost",
        user="root",
        passwd="syssy777",
        database="company_data",
    )

    c = myDB.cursor(prepared=True)
    from_ = entry_from.get()
    to_ = entry_to.get()
    query = "SELECT*  FROM sales_receipt WHERE Date BETWEEN  %s AND %s "
    c.execute(query, (from_, to_))

    rows = c.fetchall()
    display(rows)
    print(from_)
    print(to_)
    print(rows)


def search_custom_amount():
    myDB = mysql.connect(
        host="localhost",
        user="root",
        passwd="syssy777",
        database="company_data",
    )

    c = myDB.cursor(prepared=True)
    see = check.get()
    from_ = entry_from.get()
    to_ = entry_to.get()
    query = "SELECT SUM(total_amount) FROM sales_receipt WHERE Date BETWEEN  %s AND %s "
    c.execute(query, (from_, to_))
    rows = c.fetchall()
    display(rows)


def daily_Amount():
    myDB = mysql.connect(
        host="localhost",
        user="root",
        passwd="syssy777",
        database="company_data",
    )

    c = myDB.cursor()
    query = "SELECT SUM(Total_Amount) FROM sales_receipt WHERE Date = CURDATE() "

    c.execute(query)
    rows = c.fetchall()
    display(rows)


def todaySale():
    myDB = mysql.connect(
        host="localhost",
        user="root",
        passwd="syssy777",
        database="company_data",
    )

    c = myDB.cursor()
    today = time.strftime("%Y-%m-%d")
    query = "SELECT* FROM sales_receipt WHERE Date LIKE '%" + today + "%' "

    c.execute(query)
    rows = c.fetchall()
    display(rows)





def header():
    reference= ref_number()
    receipt_ref.set('FIMADOST(Sandton) ' + reference)

    receipt.insert(END,
                   "\n\n" + "\t\t\t\tSub Total:  R " + subtotal_entry.get() + "\n" + "\t\t\t\tVAT:         R " + vat_entry.get() + "\n" + "\t\t\t\tTotal:        R " + total_entry.get() + "\n" + "\t\t\t\tPaid:         R " + paid_entry.get() + "\n" + "\t\t\t\tChange:    R " + change_entry.get())
    receipt.insert(END,
                   "\n ----------------------------------------------------------------------------------------------------------------------------------------------------\n")
    receipt.insert(END, " ************************** CUSTOMER RECEIPT *********************")

    receipt.insert(1.0, "  _____\t" + " ____________\t\t\t" + "________\t\t " + "    ____" + "\n\n")
    receipt.insert(1.0, "  Code\t" + "  Product Name\t\t\t" + "Quantity\t \t" + "    Rate" + "\n")

    receipt.insert(1.0, '\n\n  FIMADOST(Sandton) \n'
                   + "  Receipt Reference: " + reference_entry.get() + "\n  Date: " + date_of_order.get() + "\n  Time: " + time_of_order.get() + "\n\n")
    receipt.insert(1.0,
                   "--------------------------------------------------------------------------------------------------------------------------------------------------------")
    receipt.insert(1.0, "\n************************** CUSTOMER RECEIPT ********************* CUSTOMER RECEIPT ********************* CUSTOMER RECEIPT *********************\n")


def ref_number():
    x = random.randint(3, 789)
    y = random.randint(1, 999)
    z = random.randint(1, 88)
    ref = str(f'{x}{y}{z}')
    ref_no.set(ref)


def get_change():
    if paid_entry == " ":
        return
    else:
        tot = total_entry.get()
        paid = paid_entry.get()
        change = float(paid) - float(tot)
        change_.set(f"{change:.2f}")


time_of_order.set(time.strftime("%H:%M:%S"))
date_of_order.set(time.strftime("%d-%m-%Y"))

titleLabel = Label(receipt_window, text='Sales Receipt', bg="#edfcf5", font=('arial', 30, 'bold'))
titleLabel.place(x=650, y=120)

lbl_reference = Label(receipt_window, text="Receipt Ref.", font=('arial', 16), bd=5, bg="#edfcf5")
lbl_reference.place(x=20, y=180)
reference_entry = Entry(receipt_window, bd=2, textvariable=ref_no, font=('arial', 16), width=24, state=DISABLED)
reference_entry.place(x=170, y=180)


lbl_productcode = Label(receipt_window, text="Product Code", font=('arial', 16), bd=5, bg="#edfcf5")
lbl_productcode.place(x=20, y=230)
Productcode_entry = Entry(receipt_window, bd=2, textvariable=PRODUCT_CODE, font=('arial', 16), width=24, state=DISABLED)
Productcode_entry.place(x=170, y=230)

lbl_productname = Label(receipt_window, text="Product Name", font=('arial', 16), bd=5, bg="#edfcf5")
lbl_productname.place(x=20, y=280)
Product_entry = Entry(receipt_window, bd=2, textvariable=PRODUCTNAME, font=('arial', 16), width=24, state=DISABLED)
Product_entry.place(x=170, y=280)

lbl_quantity = Label(receipt_window, text="Quantity", font=('arial', 16), bd=5, bg="#edfcf5")
lbl_quantity.place(x=20, y=330)
Quantity_entry = Entry(receipt_window, textvariable=QUANTITY, bd=2, font=('arial', 16), width=24)
Quantity_entry.place(x=170, y=330)
QUANTITY.set(1)

lbl_rate = Label(receipt_window, text="Rate             R", font=('arial', 16), bd=5, bg="#edfcf5")
lbl_rate.place(x=20, y=380)
Rate_entry = Entry(receipt_window, textvariable=RATE, bd=2, font=('arial', 16), width=24, state=DISABLED)
Rate_entry.place(x=170, y=380)
# RATE.set(0)


vatLabel = Label(receipt_window, text="VAT", font=('arial', 14), bd=5, bg="#edfcf5")
vatLabel.place(x=550, y=490)
vat_entry = Entry(receipt_window, bd=7, textvariable=vat_, font=('arial', 18), width=11, state=DISABLED)
vat_entry.place(x=555, y=520)

excludeVat_btn = Button(receipt_window, font=('arial', 8,), text='Exclude', bg="#efc9d9", height=2, command=excludeVAT)
excludeVat_btn.place(x=508, y=522)

subtotalLabel = Label(receipt_window, text="Sub Total", font=('arial', 14), bd=5, bg="#edfcf5")
subtotalLabel.place(x=730, y=490)
subtotal_entry = Entry(receipt_window, bd=7, textvariable=subTotal_, font=('arial', 18), width=11, state=DISABLED)
subtotal_entry.place(x=735, y=520)

totalLabel = Label(receipt_window, text="Total", font=('arial', 14), bd=5, bg="#edfcf5")
totalLabel.place(x=910, y=490)
total_entry = Entry(receipt_window, bd=7, textvariable=total_, font=('arial', 18), width=11, bg="#ffe9e5",
                    state=DISABLED)
total_entry.place(x=915, y=520)

search_entry = Entry(receipt_window, font=('arial', 21,), justify="left", width=15, bg="#f7fbff",
                     textvariable=check)
search_entry.place(x=10, y=528)

receipt = Text(receipt_window, bd=2, width=60, height=31, bg="#f7fbff", font=('arial', 7,), )
receipt.place(x=1090, y=230)

lbl_paid = Label(receipt_window, text="PAID", font=('arial', 12, "bold"), bd=5, bg="#edfcf5")
lbl_paid.place(x=1085, y=155)
paid_entry = Entry(receipt_window, bd=2, textvariable=paid_, font=('arial', 16), width=12, bg="#bee4e9")
paid_entry.place(x=1090, y=180)

lbl_change = Label(receipt_window, text="CHANGE", font=('arial', 12, "bold"), bd=5, bg="#edfcf5")
lbl_change.place(x=1245, y=155)
change_entry = Entry(receipt_window, bd=2, textvariable=change_, font=('arial', 16), width=12, bg="#bee4e5",
                     state=DISABLED)
change_entry.place(x=1250, y=180)

history = Label(receipt_window, font=('sans', 15, 'bold'), justify="center", fg='black', text="Sales History",
                bg="#edfcf5")
history.place(x=730, y=230)

from_label = Label(receipt_window, font=('arial', 10, 'bold'), justify="center", fg='black', text="From", bg="#edfcf5")
from_label.place(x=646, y=270)

from_label = Label(receipt_window, font=('arial', 8), justify="center", fg='black', text="(YYYY-MM-DD)", bg="#edfcf5")
from_label.place(x=680, y=270)
history_entry_from = Entry(receipt_window, font=('arial', 15,), justify="left", width=10, fg='black', bg='#f7fbff',
                           textvariable=entry_from)
history_entry_from.place(x=650, y=290)

to_label = Label(receipt_window, font=('arial', 10, 'bold'), justify="center", fg='black', text="To", bg="#edfcf5")
to_label.place(x=790, y=270)
from_label = Label(receipt_window, font=('arial', 8), justify="center", fg='black', text="(YYYY-MM-DD)", bg="#edfcf5")
from_label.place(x=810, y=270)

history_entry_to = Entry(receipt_window, font=('arial', 15,), justify="left", width=10, fg='black', bg='#f7fbff',
                         textvariable=entry_to)
history_entry_to.place(x=795, y=290)

# ======================================== buttons =====================================================
btn_add_item = Button(receipt_window, text="Add Item To Cart", width=35, font=('arial', 10, "bold"), height=2,
                      bg="#e5e0e0", command=lambda: (total(), SubmitData()))
btn_add_item.place(x=171, y=415)

button_receipt = Button(receipt_window, pady=1, padx=15, bd=10, fg='black', font=('arial', 12, 'bold'), width=5,
                        bg="#e5e0e0",
                        text='TOTAL', command=header)
button_receipt.place(x=1090, y=740)

button_paid = Button(receipt_window, pady=1, padx=15, bd=10, fg='black', font=('arial', 20, 'bold'), width=15, height=1,
                     bg="#e5e0e0",
                     text='PAY', command=lambda: (ref_number(),get_change()))
button_paid.place(x=1090, y=590)

button_reset = Button(receipt_window, pady=1, padx=15, bd=10, fg='black', font=('arial', 12, 'bold'), width=5,
                      text='PRINT', bg="#e5e0e0", command=lambda: (printreceipt(), insert_receipt()))
button_reset.place(x=1195, y=740)

button_exit = Button(receipt_window, pady=1, padx=15, bd=10, fg='black', font=('arial', 12, 'bold'), width=5,
                     text='RESET', bg="#e5e0e0", command=reset_)
button_exit.place(x=1303, y=740)

button_exit = Button(receipt_window, pady=1, padx=15, bd=10, fg='black', font=('arial', 12, 'bold'), width=5,
                     text='EXIT', bg='red', command=i_exit)
button_exit.place(x=1410, y=740)

search_btn = Button(receipt_window, text='Search', font=('arial', 14, 'bold'), width=11,
                    bg="#e5e0e0", command=search_).place(x=190, y=525)

receipt_search_btn = Button(receipt_window, text='Receipt', font=('arial', 14, 'bold'), width=11,
                            bg="#e5e0e0", command=search_receipt).place(x=333, y=525)

history_employee_SalesAmount_btn = Button(text='History Sales Amount', font=('arial', 9, 'bold'), width=36,
                                          justify=CENTER, bg="#e5e0e0",

                                          command=search_custom_amount).place(x=650,
                                                                              y=320)

todaySales_btn = Button(text='Today\'s Sales', font=('arial', 9, 'bold'), bg="#e5e0e0", width=36, justify=CENTER,
                        command=todaySale).place(
    x=650,
    y=346)

SalesAmount_btn = Button(text='Daily Amount', font=('arial', 9, 'bold'), bg="#e5e0e0", width=36, justify=CENTER,
                         command=daily_Amount
                         ).place(x=650,
                                 y=373)

view_btn = Button(text='View', font=('italic', 9, 'bold'), bg="#e5e0e0", width=6, command=view_custom_history).place(
    x=910, y=290)

# =========================== treeview ==========================================
display_invoice = Frame(receipt_window, width=80, bd=8, relief=RIDGE)
display_invoice.place(x=10, y=570)
scrollbarx1 = Scrollbar(display_invoice, orient=HORIZONTAL)
scrollbary1 = Scrollbar(display_invoice, orient=VERTICAL)
treeV = ttk.Treeview(display_invoice,
                     columns=(
                     "sales_receipt_id", "receipt_number", "total_amount", "vat", "amount_paid", "change_received",
                     "date", "time"),
                     height=8,
                     selectmode="extended", yscrollcommand=scrollbary1.set, xscrollcommand=scrollbarx1.set)
scrollbary1.config(command=treeV.yview)
scrollbary1.pack(side=RIGHT, fill=Y)
scrollbarx1.config(command=treeV.xview)
scrollbarx1.pack(side=BOTTOM, fill=X)
treeV.heading("sales_receipt_id", text="ID", anchor=W)
treeV.heading("receipt_number", text="Receipt Number", anchor=W)
treeV.heading("total_amount", text="Total Amount", anchor=W)
treeV.heading("vat", text="VAT", anchor=W)
treeV.heading("amount_paid", text="Amount Paid", anchor=W)
treeV.heading("change_received", text="Change", anchor=W)
treeV.heading("date", text="Date", anchor=W)
treeV.heading("time", text="Time", anchor=W)

treeV.bind('<Double 1>', get_search_row)
treeV.column('#0', width=0, stretch=NO)
treeV.column('#1', stretch=NO, minwidth=0, width=150)
treeV.column('#2', stretch=NO, minwidth=0, width=150)
treeV.column('#3', stretch=NO, minwidth=0, width=140)
treeV.column('#4', stretch=NO, minwidth=0, width=145)
treeV.column('#5', stretch=NO, minwidth=0, width=145)
treeV.column('#6', stretch=NO, minwidth=0, width=90)
treeV.column('#7', stretch=NO, minwidth=0, width=90)
treeV.column('#8', stretch=NO, minwidth=0, width=120)

treeV.pack()

present_time()

receipt_window.mainloop()
