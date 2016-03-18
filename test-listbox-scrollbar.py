from Tkinter import *



def onselect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print 'You selected item %d: "%s"' % (index, value)
    global new_text
    new_text.delete("0.0","end")
    new_text.insert("end",value)
    #b3 = Butteon(frame3,text=value)
    #b3.pack()


root = Tk()
root.geometry("1000x400")
frame1=Frame(root)
#frame1.grid(row=0, column=1,columnspan=2)
frame1.place(x=20,y=5)
frame2=Frame(root)
#frame2.grid(row=0, column=0,columnspan=2)
frame2.place(x=100,y=5)
frame3=Frame(root)
#frame3.grid(row=0, column=0,columnspan=2)
frame3.place(x=300,y=5)
scrollbar = Scrollbar(frame2)
scrollbar2 = Scrollbar(frame2,orient=HORIZONTAL)

b1 = Button(frame1,text="One")
b2 = Button(frame1,text="Two")
b1.grid(row=0, column=0)
b2.grid(row=7, column=0)

mylist = Listbox(frame2, yscrollcommand = scrollbar.set,xscrollcommand = scrollbar2.set ,height = 10)
for line in range(1001):
   mylist.insert(END, "This is line number " + str(line))
mylist.bind('<<ListboxSelect>>', onselect)
mylist.pack( side = LEFT, fill = BOTH )
#scrollbar.grid(row=0, column=2)
#mylist.grid(row=0, column=2)
scrollbar.pack(side=RIGHT, fill=Y)
scrollbar2.pack(side=BOTTOM, fill=X)
new_text = Text(frame3,width=60, height=24)
new_text.insert("end","Tere")
new_text.pack()

scrollbar.config( command = mylist.yview )
scrollbar2.config( command = mylist.xview )
#mylist.grid(row=0, column=2)


mainloop()
