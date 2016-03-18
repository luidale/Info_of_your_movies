from Tkinter import *

class app:
    def __init__(self, root):
        win1 = Frame(root)
        win1.grid(row=0,column=0)

        self.variableCont = StringVar(win1)                               
        self.variableCountry = StringVar(win1)
        self.variableState = StringVar(win1)
        self.variableCont.set(sorted(list(continentList.keys()))[0])
        currentCountries = sorted(list(continentList[self.variableCont.get()]))
        self.variableCountry.set(sorted(list(continentList[self.variableCont.get()]))[0])
        currentStates = sorted(list(continentList[self.variableCont.get()][self.variableCountry.get()]))
        self.variableState.set(sorted(list(continentList[self.variableCont.get()][self.variableCountry.get()]))[0])


        self.variableCont.set(sorted(list(continentList.keys()))[0])                               
        self.variableCountry.set(sorted(list(continentList[self.variableCont.get()]))[0])
        self.variableState.set(sorted(list(continentList[self.variableCont.get()][self.variableCountry.get()]))[0])
        self.type = OptionMenu(win1, self.variableCont,
                          *continentList.keys(),
                          command = self.varMenuCountry)
        self.type.grid(row=1, column=3, sticky="nsew", padx=1, pady=1)
        self.unit = OptionMenu(win1,
                          self.variableCountry, *currentCountries,command = self.varMenuState)
        self.unit.grid(row=1, column=5, sticky="nsew", padx=1, pady=1)
        self.unit2 = OptionMenu(win1,
                          self.variableState, *currentStates))
        self.unit2.grid(row=1, column=7, sticky="nsew", padx=1, pady=1)

http://stackoverflow.com/questions/19794069/tkinter-gui-update-choices-of-an-option-menu-depending-on-a-choice-from-another
    def update_GUI_choices(option):
        if option == 'option1':
            if GUI_options.option1.get()==1:
                global choices4option2       
                choices4option2 = [4,5]
            else: pass
        elif option == 'option2':
            if GUI_options.option2.get()==4:
                global choices4option3       
                choices4option3 = [8,9]
            else: pass
        else: pass


    def varMenuCountry(self, selection):
        print "a",selection
        print continentList[selection]
        print continentList[selection].keys()
        self.variableCountry.set(sorted(list(continentList[selection].keys()))[0])
        #menu = self.unit["menu"]
        #menu.delete(0,"end")
        #for x in sorted(list(continentList[selection].keys())):
        #    print x
#            menu.add_command(label=x,command=lambda nation=x: self.variableCountry.set(nation))
        #    menu.add_command(label=x,command=lambda nation=x: self.variableCountry.set(nation))
        #menu.insert("end", command, command = self.varMenuState)
#        menu.add_command(command = self.varMenuState)
 
        #self.unit = OptionMenu(Frame(root),
        #                  self.variableCountry, *sorted(list(continentList[selection].keys())),command = self.varMenuState)
        #self.unit.grid(row=1, column=5, sticky="nsew", padx=1, pady=1)

        #self.variableCountry.set(countryList[listCont.index(self.variableCont.get())])

        #if selection == "Heavy":
        #    self.variableunit.set("colour")
        #    #self.unit.config(state = DISABLED)
        #else:
        #    self.variableunit.set("mm")
            #self.unit.config(state = NORMAL)
        self.varMenuState(self.variableCountry.get())
    
    def varMenuState(self, selection):
        self.variableState.set(sorted(continentList[self.variableCont.get()][selection])[0])
        #print self.variableState.get()
        menu = self.unit2["menu"]
        menu.delete(0,"end")
        for x in continentList[self.variableCont.get()][selection]:
            menu.add_command(label=x,command=lambda state=x: self.variableState.set(state))
        #if selection2 == "colour":
        #    print "s"
        #    self.variableunit2.set("violet")
        #    #self.unit.config(state = DISABLED)
        #else:
        #    print "t"
        #    self.variableunit2.set("cm")
        #    #self.unit.config(state = NORMAL)
        #print "B",self.variableunit2.get()

continentList = {'N.America':{'Canada':['BC','Alberta','Saskatchewan','others'],
                'USA':['California','Oregon','Washington','others'],'Mexico':['Michoacan','Oaxaca','Monterrey','others']},
                 'C. America':{'Guatemala':['Guatemala states'],'Nicaragua':['Nicaragua states'],'Panama':['Panama states']},
                 'S. America':{'Venezuela':['Venezuela states'],'Colombia':['Colombia states'],'Ecuador':['Ecuador states']}}
countryList = [['Canada','USA','Mexico'],
['Guatemala','Nicaragua','Panama'],
['Venezuela','Colombia','Ecuador']]
stateList = [[['BC','Alberta','Saskatchewan','others'],
['California','Oregon','Washington','others'],
['Michoacan','Oaxaca','Monterrey','others']],
[['Guatemala states'],['Nicaragua states'],['Panama states']],
[['Venezuela states'],['Colombia states'],['Ecuador states']]]
root = Tk()
a = app(root)
root.mainloop()
