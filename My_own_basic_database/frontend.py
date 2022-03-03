from tkinter import *
import backend

def get_selected_row(event):
    global selected_row
    index = data.curselection()[0]
    selected_row = data.get(index)
    e1.delete(0,END)
    e1.insert(END,selected_row[1])
    e2.delete(0,END)
    e2.insert(END,selected_row[2])
    e3.delete(0,END)
    e3.insert(END,selected_row[3])
    e4.delete(0,END)
    e4.insert(END,selected_row[4])
    e5.delete(0,END)
    e5.insert(END,selected_row[5])
    e6.delete(0,END)
    e6.insert(END,selected_row[6])

def clean_list_command():
    data.delete(0,END)

def delete_command():
    backend.delete(selected_row[0])

def view_command():
    data.delete(0,END)
    for row in backend.view():
        data.insert(END,row)

def search_command():
    data.delete(0,END)
    for row in backend.search(date_text.get(), appliance_text.get(), active_energy_text.get(),
                              reactive_energy_text.get(),timestamp_text.get(), state_text.get()):
        data.insert(END,row)

def add_command():
    backend.insert(date_text.get(), appliance_text.get(), active_energy_text.get(),
                              reactive_energy_text.get(),timestamp_text.get(), state_text.get())

    data.delete(0,END)
    data.insert(END,(date_text.get(), appliance_text.get(), active_energy_text.get(),
                              reactive_energy_text.get(),timestamp_text.get(), state_text.get()))

win = Tk()

win.wm_title('Basic database to save event in energy consume')

l1 = Label(win, text='Date [Y-M-D]')
l1.grid(row=0,column=0)
l2 = Label(win, text='Appliance')
l2.grid(row=0,column=2)
l3 = Label(win, text='Active Energy [W]')
l3.grid(row=1,column=0)
l4 = Label(win, text='Reactive Energy [VA]')
l4.grid(row=1,column=2)
l5 = Label(win, text='Timestamp [H:M:S]')
l5.grid(row=2,column=0)
l6 = Label(win, text='State')
l6.grid(row=2,column=2)

date_text = StringVar()
e1 = Entry(win, textvariable=date_text)
e1.grid(row=0,column=1)

appliance_text = StringVar()
e2 = Entry(win, textvariable=appliance_text)
e2.grid(row=0,column=3)

active_energy_text = StringVar()
e3 = Entry(win, textvariable=active_energy_text)
e3.grid(row=1,column=1)

reactive_energy_text = StringVar()
e4 = Entry(win, textvariable=reactive_energy_text)
e4.grid(row=1,column=3)

timestamp_text = StringVar()
e5 = Entry(win, textvariable=timestamp_text)
e5.grid(row=2,column=1)

state_text = StringVar()
e6 = Entry(win, textvariable=state_text)
e6.grid(row=2,column=3)

data = Listbox(win,height=8,width=35)
data.grid(row=3,column=0,rowspan=9,columnspan=2)

sb = Scrollbar(win)
sb.grid(row=3,column=2,rowspan=9)

data.bind('<<ListboxSelect>>',get_selected_row)

b1 = Button(win,text='Add an event',width=12,pady=5,command=add_command)
b1.grid(row=3,column=3)

b2 = Button(win,text='Search',width=12,pady=5,command=search_command)
b2.grid(row=4,column=3)

b3 = Button(win,text='Delete an event',width=12,pady=5,command=delete_command)
b3.grid(row=5,column=3)

b4 = Button(win,text='View all',width=12,pady=5,command=view_command)
b4.grid(row=6,column=3)

b5 = Button(win,text='Close',width=12,pady=5,command = win.destroy)
b5.grid(row=7,column=3)

b6 = Button(win,text='Clean list',width=12,pady=5,command = clean_list_command)
b6.grid(row=8,column=3)

win.mainloop()
