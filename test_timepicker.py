from tkinter import*
import os, fnmatch

def submitForm():    
    strFile = optVariable.get()
    # Print the selected value from Option (Combo Box)    
    if (strFile !=''):        
        print('Selected Value is : ' + strFile)


root = Tk()
root.geometry('500x500')
root.title("Demo Form ")


label_2 = Label(root, text="Choose Files ",width=20,font=("bold", 10))
label_2.place(x=68,y=250)

flist = fnmatch.filter(os.listdir('.'), '*.mp4')
optVariable = StringVar(root)
optVariable.set("   Select   ") # default value
optFiles = OptionMenu(root, optVariable,*flist)
optFiles.pack()
optFiles.place(x=240,y=250)

Button(root, text='Submit', command=submitForm, width=20,bg='brown',fg='white').place(x=180,y=380)


root.mainloop()