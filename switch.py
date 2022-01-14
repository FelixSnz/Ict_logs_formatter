from tkinter import *
from  tkinter import ttk


ws  = Tk()
ws.title('PythonGuides')
ws.geometry('300x400')

preview_table = ttk.Treeview(ws)
preview_table.pack()

preview_table['columns']= test_names
preview_table.column("#0", width=0,  stretch=NO)
preview_table.heading("#0",text="",anchor=CENTER)

for test_name in test_names:
    preview_table.column(test_name ,anchor=CENTER, width=80)
    preview_table.heading(test_name,text=test_name,anchor=CENTER)


for idx, vals in enumerate(set_of_values):
    preview_table.insert(parent='',index='end',iid=idx,text='', values=vals)



ws.mainloop()