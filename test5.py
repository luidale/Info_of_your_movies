from Tkinter import*

dict = {"1":["a"],"2":["b","c"],"3":["c"]}
dict2 = {"a":"aa","b":"bb","c":"cc"}
def func(value):
    var2 = StringVar()
    var2.set(dict[value][0])
    pr(dict[value][0])
    DropDownMenu2=OptionMenu(root, var2, *dict[value],command=pr)
    DropDownMenu2.place(x=10, y=60)

def pr(value):
    print value
    par1.set(dict2[value])

root = Tk()

var = StringVar()
var.set("1")
DropDownMenu=OptionMenu(root, var, "1", "2", "3", command=func)
DropDownMenu.place(x=10, y=10)

par1 = StringVar()
silt4 = Label(root, textvariable=par1)
silt4.place(x=100, y=5)

func("1")
root.mainloop()
