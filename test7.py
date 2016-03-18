from Tkinter import *

class app:
    def __init__(self, root):
        win1 = Frame(root)
        win1.grid(row=0,column=0)

        self.variable = StringVar(win1)                               
        self.variable.set(42)
        self.type = OptionMenu(win1, self.variable,
                          "None", "Clear", "Dark", "Heavy",
                          command = self.varMenu)
        self.type.grid(row=1, column=3, sticky="nsew", padx=1, pady=1)


        self.variableunit = StringVar(win1)
        self.variableunit.set('mm')
        self.variableunit2 = StringVar()
        self.variableunit2.set('cm')
        self.unit = OptionMenu(win1,
                          self.variableunit, "mm", "colour", "shade",command = self.varMenu2)
        self.unit.grid(row=1, column=5, sticky="nsew", padx=1, pady=1)
        self.unit2 = OptionMenu(win1,
                          self.variableunit2, "mm", "violet", "blue")
        self.unit2.grid(row=1, column=7, sticky="nsew", padx=1, pady=1)


    def varMenu(self, selection):

        if selection == "Heavy":
            self.variableunit.set("colour")
            #self.unit.config(state = DISABLED)
        else:
            self.variableunit.set("mm")
            #self.unit.config(state = NORMAL)
        print "A",self.variableunit.get()
        self.varMenu2(self.variableunit.get())

    def varMenu2(self, selection2):
        if selection2 == "colour":
            print "s"
            self.variableunit2.set("violet")
            #self.unit.config(state = DISABLED)
        else:
            print "t"
            self.variableunit2.set("cm")
            #self.unit.config(state = NORMAL)
        print "B",self.variableunit2.get()
root = Tk()
a = app(root)
root.mainloop()
