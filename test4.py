import Tkinter as tk

def select():
    title=var.get()
    print "selected string :"+title
    print "corresponing integer value :"+str(choices[Dic[title]])


choices = [1,2,3]
Dic={'title 1':0,'title 2':1,'title 3':2}
GUI = tk.Tk()
var = tk.StringVar(GUI)
var.set('title 1')
op=tk.OptionMenu(GUI, var, *Dic.keys())
op.pack(side='left',padx=20,pady=10)
bt=tk.Button(GUI,text='check value',command=select)
bt.pack(side='left',padx=20,pady=10)
GUI.mainloop()
