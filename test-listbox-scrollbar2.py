from Tkinter import *
from PIL import Image, ImageTk
#from pillow import Image, ImageTk
import os

def onselect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print 'You selected item %d: "%s"' % (index, value)
    global new_text
    new_text.delete("0.0","end")
    new_text.insert("end",value)

    #pildid
    #global pilt
    print index, len(pildid)
    if index < len(pildid):
 #       pilt.destroy()
        print pildid[index]
        global pilt
        image = Image.open(pildid[index])
        photo2 = ImageTk.PhotoImage(image)
        pilt.configure(image=photo2)
        pilt.image=photo2
    else:
        pilt.configure(image="")
        #pilt.pack()
    #b3 = Butteon(frame3,text=value)
    #b3.pack()


root = Tk()
root.geometry("1000x400")
frame1=Frame(root)
#frame1.grid(row=0, column=1,columnspan=2)
frame1.place(x=20,y=5)
frame2=Frame(root)
frame2.grid_rowconfigure(0, weight=1)
frame2.grid_columnconfigure(0, weight=1)
#frame2.grid(row=0, column=0,columnspan=2)
frame2.place(x=100,y=5)
frame3=Frame(root)
#frame3.grid(row=0, column=0,columnspan=2)
frame3.place(x=250,y=5)
frame4=Frame(root)
#frame3.grid(row=0, column=0,columnspan=2)
frame4.place(x=750,y=5)

yscrollbar = Scrollbar(frame2)
yscrollbar.grid(row=0, column=1, sticky=N+S)
xscrollbar = Scrollbar(frame2,orient=HORIZONTAL)
xscrollbar.grid(row=1, column=0, sticky=E+W)


b1 = Button(frame1,text="One")
b2 = Button(frame1,text="Two")
b1.grid(row=0, column=0)
b2.grid(row=7, column=0)

mylist = Listbox(frame2, yscrollcommand = yscrollbar.set,xscrollcommand = xscrollbar.set ,height = 10)
for line in range(1001):
   mylist.insert(END, "This is line number " + str(line))
mylist.bind('<<ListboxSelect>>', onselect)

mylist.grid(row=0, column=0, sticky=N+S+E+W)
#mylist.pack( side = LEFT, fill = BOTH )
#scrollbar.grid(row=0, column=2)
#mylist.grid(row=0, column=2)
#scrollbar.pack(side=RIGHT, fill=Y)
#scrollbar2.pack(side=BOTTOM, fill=X)
new_text = Text(frame3,width=60, height=24)
new_text.insert("end","Tere")
new_text.pack()

yscrollbar.config( command = mylist.yview )
xscrollbar.config( command = mylist.xview )
#mylist.grid(row=0, column=2)

#look up images
pildid = []
#input_folder = "C:/Users/agfasd/Downloads"
input_folder = "C:/Users/agfasd/Dropbox/programmeerimine/movies/data/cover"
for filename in os.listdir(input_folder):
    filepath = os.path.join(input_folder, filename)
    if os.path.isfile(filepath): #checks all files
        if filename[-3:].lower()== "jpg":
            pildid.append(filepath)
print pildid


video_image = Canvas(frame4)
#video_image.create_line(0, 0, 200, 100)
image = Image.open(pildid[0])
print image
photo = ImageTk.PhotoImage(image)
pilt = Label(frame4,image=photo)
#pilt.image=photo
pilt.pack()
#video_image.create_image(0,0, image = photo)
#video_image.pack()
mainloop()
