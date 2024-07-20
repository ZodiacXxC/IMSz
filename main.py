from tkinter import INSERT, ttk, END, messagebox
import tkinter as tk
import sql
from datetime import datetime

data = sql.get_all_data()



def add_new():
    barcode_input = ""
    timer_id = None
    
    def key_press(event):
        nonlocal barcode_input, timer_id
        key = event.char
        if key.isprintable():
            barcode_input += key
        if timer_id is not None:
            root.after_cancel(timer_id)
        timer_id = root.after(100, process_barcode_input)
        
    def process_barcode_input():
        nonlocal barcode_input, timer_id
        newEntry.delete(0, END)
        newEntry.insert(0, barcode_input)
        print(f"Barcode input: {barcode_input}")
        sql.insert_into_cat(barcode_input)
        barcode_input = ""
        timer_id = None
        updated_data = sql.get_all_data()
        treeview.delete(*treeview.get_children())
        for row in updated_data:
            treeview.insert('', tk.END, values=row)
        

    mainFrame = tk.Toplevel(root)
    mainFrame.title("Add Product")
    mainFrame.resizable(False, False)
    mainFrame.geometry("+%d+%d" % ((root.winfo_screenwidth() - mainFrame.winfo_reqwidth()) / 2,
                                       (root.winfo_screenheight() - mainFrame.winfo_reqheight()) / 2))
    addFrame = ttk.LabelFrame(mainFrame,text="Scan a barcode: ")
    addFrame.grid(row=0,column=0,padx=10,pady=10)
    newEntry = ttk.Entry(addFrame)
    newEntry.grid(row=0,column=0,padx=10,pady=10)
    newEntry.bind('<Key>', key_press)
    

def validate_numeric_input(P):
    if P == "" or P == "." or P.isdigit():
        return True
    elif P.count('.') == 1 and P.replace(".", "").isdigit():
        return True
    else:
        return False

def select_view(event):
    selection = category.get()
    if selection == "All":
        newdata = sql.get_all_data()
    else:
        newdata = sql.get_cat(selection)
    treeview.delete(*treeview.get_children())
    for row in newdata:
        treeview.insert('', tk.END, values=row)


def insert_new():
    barcodes = []
    if sql.get_all_bar():
        barcodes = list(sql.get_all_bar()[0])
    nameP = nameEntry.get()
    price = priceEntry.get()
    date = dateEntry.get()
    categorys = categoryEntry.get()
    barcode = barcodeEntry.get()
    if barcode not in barcodes:   
        sql.insert_data(nameP,price,date,categorys,barcode)
    else:
        messagebox.showwarning("Error","This Barcode is exitis !!")
    data = sql.get_all_data()
    treeview.delete(*treeview.get_children())
    for row in data:
        treeview.insert('', tk.END, values=row)
    
    nameEntry.delete("0",END)
    priceEntry.delete("0",END)
    priceEntry.insert(END,0)
    dateEntry.delete("0",END)
    categoryEntry.delete("0",END)
    dateEntry.delete("0",END)
    today = datetime.now()
    name = f"{today.year}-{today.month}-{today.day}"
    dateEntry.insert(END,name)
    barcodeEntry.delete("0",END)
    valcat = ['All']
    unique_categories = set()
    for row in data:
        unique_categories.add(row[4])
    valcat.extend(unique_categories)
    category['values'] = valcat 
    
   

def delete_data_from_table():
    selected_item = treeview.selection()
    if selected_item:
        item = treeview.item(selected_item)['values'][0]
        sql.delete_data(item)
        
    data = sql.get_all_data()
    valcat = ['All']
    unique_categories = set()
    for row in data:
        unique_categories.add(row[4])
    valcat.extend(unique_categories)
    category['values'] = valcat 
    treeview.delete(*treeview.get_children())
    for row in data:
        treeview.insert('', tk.END, values=row)
    

def update_func():
    selected_item = treeview.selection()
    if selected_item:
        id_ = treeview.item(selected_item)['values'][0]
        nameP = nameEntry.get()
        price = priceEntry.get()
        date = dateEntry.get()
        categorys = categoryEntry.get()
        barcode = barcodeEntry.get()
        sql.update_data(id_,nameP,price,date,categorys,barcode)
        data = sql.get_all_data()
        valcat = ['All']
        unique_categories = set()
        for row in data:
            unique_categories.add(row[4])
        valcat.extend(unique_categories)
        category['values'] = valcat 
        treeview.delete(*treeview.get_children())
        for row in data:
            treeview.insert('', tk.END, values=row)
        nameEntry.delete("0",END)
        priceEntry.delete("0",END)
        priceEntry.insert(END,0)
        dateEntry.delete("0",END)
        categoryEntry.delete("0",END)
        dateEntry.delete("0",END)
        barcodeEntry.delete("0",END)
        
    

def update_entry(event):
    selected_item = treeview.selection()
    if selected_item:
        item = treeview.item(selected_item)['values']
        nameEntry.delete("0",END)
        priceEntry.delete("0",END)
        dateEntry.delete("0",END)
        categoryEntry.delete("0",END)
        barcodeEntry.delete("0",END)
        nameEntry.insert(END,item[1])
        priceEntry.insert(END,item[2])
        dateEntry.insert(END,item[3])
        categoryEntry.insert(END,item[4])
        barcodeEntry.insert(END,item[6])

root = tk.Tk()
root.resizable(False,False)
root.title("IMSz")
root.geometry("+%d+%d" % ((root.winfo_screenwidth() - root.winfo_reqwidth()) / 2,
                                       (root.winfo_screenheight() - root.winfo_reqheight()) / 2))

style = ttk.Style(root)


root.tk.call("source","forest-light.tcl")
style.theme_use("forest-light")
style.configure('Treeview', rowheight=40)
validate_numeric = root.register(validate_numeric_input)
frame = ttk.Frame(root)
frame.pack()
controlFrame = ttk.LabelFrame(frame,text="Control")
controlFrame.grid(row=0,column=0,padx=10,pady=10)

selected_category = tk.StringVar()
category = ttk.Combobox(controlFrame, textvariable=selected_category,state="readonly")
valcat = ['All']
unique_categories = set()

for row in data:
    unique_categories.add(row[4])

valcat.extend(unique_categories)
category['values'] = valcat 
category.current(0)
category.bind("<<ComboboxSelected>>", select_view)
category.grid(row=0,column=0,pady=5)

nameLab = ttk.Label(controlFrame,text="Name: ")
nameLab.grid(row=0,column=1,pady=5)
nameEntry = ttk.Entry(controlFrame)
nameEntry.grid(row=0,column=2,padx=(0,10),pady=5)

priceLab = ttk.Label(controlFrame,text="Price: ")
priceLab.grid(row=0,column=3,padx=(10,0),pady=5)
priceEntry = ttk.Entry(controlFrame,validate="key",validatecommand=(validate_numeric, "%P"),width=9)
priceEntry.grid(row=0,column=4,padx=(0,10),pady=5)
priceEntry.insert(END,0)

dateLab = ttk.Label(controlFrame,text="Date: ")
dateLab.grid(row=0,column=5,padx=(10,0),pady=5)
dateEntry = ttk.Entry(controlFrame)
dateEntry.grid(row=0,column=6,padx=(0,10),pady=5)
today = datetime.now()
name = f"{today.year}-{today.month}-{today.day}"
dateEntry.insert(END,name)

categoryLab = ttk.Label(controlFrame,text="Category: ")
categoryLab.grid(row=0,column=7,padx=(20,0),pady=5)
categoryEntry = ttk.Entry(controlFrame)
categoryEntry.grid(row=0,column=8,padx=(0,10),pady=5)

barcodeLab = ttk.Label(controlFrame,text="Barcode: ")
barcodeLab.grid(row=0,column=9,padx=(20,0),pady=5)
barcodeEntry = ttk.Entry(controlFrame)
barcodeEntry.grid(row=0,column=10,padx=(0,10),pady=5)

insertButton = ttk.Button(controlFrame,text="Insert",command=insert_new)
insertButton.grid(row=0,column=11,padx=5,pady=5)

updateButton = ttk.Button(controlFrame, text="Update",command=update_func)
updateButton.grid(row=1, column=0, padx=(5,110),pady=10, sticky="W")

deleteButton = ttk.Button(controlFrame, text="Delete",command=delete_data_from_table)
deleteButton.grid(row=1, column=0, padx=10,pady=10, sticky="E")

addButton = ttk.Button(controlFrame, text="Add Products",command=add_new)
addButton.grid(row=1, column=1, padx=0,pady=10, sticky="E")




treeFrame = ttk.Frame(frame)
treeFrame.grid(row=1,column=0,padx=10,pady=10)
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

cols = ("ID.","Name","Price","Entry Date","Category","Barcode","Total")
treeview = ttk.Treeview(treeFrame,show="headings",yscrollcommand=treeScroll.set,columns=cols,height=7)
treeview.column("ID.", width=85, anchor="center")
treeview.column("Name", width=215, anchor="center")
treeview.column("Price", width=215, anchor="center")
treeview.column("Entry Date", width=215, anchor="center")
treeview.column("Category", width=215, anchor="center")
treeview.column("Total", width=215, anchor="center")
treeview.column("Barcode", width=215, anchor="center")
treeview.pack()
treeview.bind('<ButtonRelease-1>',update_entry)
treeScroll.config(command=treeview.yview)
treeview.heading("#1", text="ID.")
treeview.heading("#2", text="Name")
treeview.heading("#3", text="Price")
treeview.heading("#4", text="Entry Date")
treeview.heading("#5", text="Category")
treeview.heading("#6", text="Total")
treeview.heading("#7", text="Barcode")



for row in data:
    treeview.insert('', tk.END, values=row)



root.update_idletasks()
root_width = root.winfo_width()
root_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - root_width) // 2
y = (screen_height - root_height) // 2
root.geometry("+{}+{}".format(x, y))
root.mainloop()
