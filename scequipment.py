#: ------------------------------- IMPORTS --------------------------------------

from tkinter import *
from tkinter import messagebox
import datetime
import pandas as pd


#: ------------------------------- CONSTANTS --------------------------------------

FINAL_PATH = "K:\SC Support\Equipment Tracking"


#  ------------------------------ FUNCTIONS ----------------------------------------

radio_butn_dict = {0:"NoDevice",
                   1:"Laptop",
                       2:"PC",
                       3:"Docking Station",
                       4:"Monitor",
                       5:"Headset"}


def radio_btn_data():
    item_num = 0
    item_num = radio_state.get()
    global device_selected
    device_selected = radio_butn_dict[item_num]


def submit_data():


    what_department = ""
    for i in dep_listbox.curselection():
        what_department = dep_listbox.get(i)

    what_device = device_selected
    what_serial = serial_num_entry.get()
    what_invoice = invoice_entry.get()
    what_time = datetime.date.today()

    if len(what_serial) <= 0 or len(what_invoice) <= 0 or what_department == "" or what_device == "NoDevice":
        messagebox.showinfo(title="Error!", message="Please do not leave any fields empty!")
    
    else:
        # messagebox is used to verify if user wants to save their password.
        # is_ok is a boolean vaiable. Clicking "OK" = True
        is_ok = messagebox.askokcancel(title="Verify Entry", message=f"\nDevice: {what_device} \n\nSerial: {what_serial} \n\nInvoice: {what_invoice} \n\nDepartment: {what_department} \n\nDate: {what_time}")

        if is_ok:

            try:
            # Try to see if file exists. If it does we will open it with read.
                with open(FINAL_PATH+"\scsupportequipment.csv", "r") as file:
                    df = file.read()
                    

            except FileNotFoundError:
            # If file does not exist then we must create a new one. 
                data = {'Device': [what_device],
                            'Serial': [what_serial],
                            'Invoice':[what_invoice],
                            'Department': [what_department],
                            "Date": [what_time]}
                df = pd.DataFrame(data)
                df.to_csv(FINAL_PATH+"\scsupportequipment.csv", header=True, index=0)


            else:
            # Since the file exist we will append to it.
                data = {'Device': [what_device],
                            'Serial': [what_serial],
                            'Invoice':[what_invoice],
                            'Department': [what_department],
                            "Date": [what_time]}
                df = pd.DataFrame(data)
                df.to_csv(FINAL_PATH+"\scsupportequipment.csv", mode='a', header=False, index=0)

            finally:
                serial_num_entry.delete(0, END)
                invoice_entry.delete(0, END)
                dep_listbox.selection_clear(0, END)
                





#  ------------------------------ UI ----------------------------------------

window = Tk()
window.title("SC Equipment Tracker Tool")
window.config(padx=50, pady=50)

# Logo: 
canvas = Canvas(width=200, height=200)
computer_image = PhotoImage(file="complogo.png")

# These x and y cooridinates need to be provided to show where image will be placed. 
canvas.create_image(100, 100, image=computer_image)
canvas.grid(row=0, column=1)


# Device: --------------------------------------------------------------


#Variable to hold on to which radio button value is checked.
radio_state = IntVar()
radiobutton1 = Radiobutton(text="Laptop", value=1, variable=radio_state, command=radio_btn_data)
radiobutton2 = Radiobutton(text="PC", value=2, variable=radio_state, command=radio_btn_data)
radiobutton3 = Radiobutton(text="Docking Station", value=3, variable=radio_state, command=radio_btn_data)
radiobutton4 = Radiobutton(text="Monitor", value=4, variable=radio_state, command=radio_btn_data)
radiobutton5 = Radiobutton(text="Headset", value=5, variable=radio_state, command=radio_btn_data)

radiobutton1.grid(row=1, column=0, columnspan=2)
radiobutton2.grid(row=2, column=0, columnspan=2)
radiobutton3.grid(row=3, column=0, columnspan=2)
radiobutton4.grid(row=4, column=0, columnspan=2)
radiobutton5.grid(row=5, column=0, columnspan=2)



# Serial Number: --------------------------------------------------------------
serial_num_label = Label(text="Serial Number:")
serial_num_label.grid(row=6, column=0)

serial_num_entry = Entry(width=40)
serial_num_entry.grid(row=6, column=1)

# Invoice: --------------------------------------------------------------

invoice_label = Label(text="Invoice:")
invoice_label.grid(row=7, column=0)

invoice_entry = Entry(width=40)
invoice_entry.grid(row=7, column=1)

# Department: --------------------------------------------------------------

department_label = Label(text="Department:")
department_label.grid(row=8, column=0)



dep_listbox = Listbox(height=14, width=50)
department = ["Accounting", "AP", "Compliance", 
              "HR/Benefits", "HRIS", "IT",
              "Learning and Devlopment", "Legal",
              "Other", "Payroll", "Recruiting",
              "SC Market Resource", "Transactions"]
for item in department:
    dep_listbox.insert(department.index(item), item)

dep_listbox.grid(row=8, column=1)


# Submit Button: --------------------------------------------------------------

submit_button = Button(text="Submit", width=21, command=submit_data)
submit_button.grid(row=9, column=1)

# Sets value to 0 unless user selects from the listbox
radio_btn_data()


window.mainloop()
