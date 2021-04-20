# Python program to illustrate the usage
# of hierarchical treeview in python GUI
# application using tkinter
 
# Importing tkinter
import traceback
import sys
import tkinter as tk
import controller
# Importing ttk from tkinter
from tkinter import ttk 
from functools import partial
# Creating app window



    
# Defining title of the app
class MainWindow:

    def __init__(self, app):
        
        app.title("GUI Application of Python") 
        app.geometry("1080x500")

        appMenu = self.drawMenuBar(app)

        
        app.config(menu=appMenu)
        app.grid_rowconfigure(0, weight=1)
        app.grid_columnconfigure(0, weight=1)
        #app.grid_propagate(True)
        # Defining label of the app and calling a geometry
        # management method i.e, pack in order to organize
        # widgets in form of blocks before locating them
        # in the parent widget
        explorerFrame = ttk.Frame(app)
        explorerFrame.grid(row=0, column=0)
        
        explorerLabel = ttk.Label(
            explorerFrame, 
            text ="Treeview(hierarchical)"
        )
        explorerLabel.grid(row=0, column=0, padx=(5,0), sticky='W')
        
        # Creating treeview window
        explorerMenu = ttk.Treeview(explorerFrame)
        #explorerMenu["columns"]=("Edit")
        #explorerMenu.column("Edit", width=270, minwidth=270, stretch=tk.NO)
        #explorerMenu.heading("Edit", text="Edit",anchor=tk.W)
        #explorerMenu["displaycolumns"] = ("")
        explorerMenu.grid(row=1, column=0, padx=(5,0), sticky='W')
        
        disablingList = [False] * 26
        editForm = self.drawEditForm(app, "test", disablingList)
        editForm.grid(row=2, column=0, columnspan=2)
        editForm.grid_forget()
        

        
        
        # Calling pack method on the treeview

        # Inserting items to the treeview
        # Inserting parent
        
        # Placing each child items in parent widget
        
        noteBook = ttk.Notebook(
            app,
            height="310",
            width="410"
        )
        sheets = controller.TabManager(noteBook)
        sheets.appendTab("new 1", "")
        sheets.nb.grid(row=0, column=1, rowspan=2, sticky='N')
        

        self.app = app
        self.appMenu = appMenu
        self.explorerFrame = explorerFrame
        self.explorerLabel = explorerLabel
        self.explorerMenu = explorerMenu
        self.sheets = sheets
        self.editForm = editForm
        self.explorerMenu.bind("<Double-1>", self.onTreeClick)
        app.mainloop()
        
    def drawMenuBar(self, app):
        menubar = tk.Menu(app)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command = partial(controller.openDialog, self))
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Exit", command = exit)

        menubar.add_cascade(label="File", menu=filemenu)
        return menubar

    def drawEditForm(self, app, element, vals):
        group = ttk.Labelframe(app, text=element)
        flags = list()
        counter = 0
        try:
            item = controller.getField(element)
            for camp in item:
                if (item[camp] == 0 or item[camp] == 1) and camp != "seq":
                                   
                    
                    flags.append(tk.Checkbutton(group, text=camp, command=partial(controller.insertChange, camp)))
                    
                    if vals[counter]: 
                        flags[len(flags)-1].select()
                        controller.changes[camp] = True
                    else:
                        flags[len(flags)-1].deselect()
                        controller.changes[camp] = False
                    
                    r = counter % 4
                    c = int(counter / 4)
                    
                    flags[len(flags)-1].grid(row=r, column=c)
                    counter += 1
        except:
            traceback.print_exc()
        

        saveBtn = ttk.Button(group, text="Save", command=partial(controller.saveChanges, group))    
        saveBtn.grid(row=2, column=6)
        
        return group
       
        '''    
        varFlle = tk.BooleanVar(value=vals[0])
        flle = tk.Checkbutton(group, text="flle", variable=varFlle)
        if vals[0]: flle.select()
        #flle.deselect()
        varStato = tk.BooleanVar(value=vals[1])
        stato = tk.Checkbutton(group, text="stato", variable=varStato)
        if vals[1]: stato.select() 
        #stato.deselect()
        varSoab = tk.BooleanVar(value=vals[2])
        soab = tk.Checkbutton(group, text="soab", variable=varSoab)
        if vals[2]: soab.select()
        #soab.deselect()
        varFlgt = tk.BooleanVar(value=vals[3])
        flgt = tk.Checkbutton(group, text="flgt", variable=varFlgt)
        if vals[3]: flgt.select()
        #flgt.deselect()
        varFlne = tk.BooleanVar(value=vals[4])
        flne = tk.Checkbutton(group, text="flne", variable=varFlne)
        if vals[4]: flne.select()
        #flne.deselect()
        varFlbt = tk.BooleanVar(value=vals[5])
        flbt = tk.Checkbutton(group, text="flbt", variable=varFlbt)
        if vals[5]: flbt.select()
        #.deselect()
        varRepl = tk.BooleanVar(value=vals[6])
        repl = tk.Checkbutton(group, text="repl", variable=varRepl)
        if vals[6]: repl.select()
        #repl.deselect()
        varClbl = tk.BooleanVar(value=vals[7])
        clbl = tk.Checkbutton(group, text="clbl", variable=varClbl)
        if vals[7]: clbl.select()
        #clbl.deselect()
        varDec = tk.BooleanVar(value=vals[8])
        dec = tk.Checkbutton(group, text="dec", variable=varDec)
        if vals[8]: dec.select()
        #dec.deselect()
        varFlge = tk.BooleanVar(value=vals[9])
        flge = tk.Checkbutton(group, text="flge", variable=varFlge)
        if vals[9]: flge.select()
        #flge.deselect()
        varFlin = tk.BooleanVar(value=vals[10])
        flin = tk.Checkbutton(group, text="flin", variable=varFlin)
        if vals[10]: flin.select()
        #flin.deselect()
        varRnd = tk.BooleanVar(value=vals[11])
        rnd = tk.Checkbutton(group, text="rnd", variable=varRnd)
        if vals[11]: rnd.select()
        #rnd.deselect()
        varUpab = tk.BooleanVar(value=vals[12])
        upab = tk.Checkbutton(group, text="upab", variable=varUpab)
        if vals[12]: upab.select()
        #upab.deselect()
        varCcls = tk.BooleanVar(value=vals[13])
        ccls = tk.Checkbutton(group, text="cls", variable=varCcls)
        if vals[13]: ccls.select()
        #ccls.deselect()
        varFleq = tk.BooleanVar(value=vals[14])
        fleq = tk.Checkbutton(group, text="fleq", variable=varFleq)
        if vals[14]: fleq.select()
        #fleq.deselect()
        varTsep = tk.BooleanVar(value=vals[15])
        tsep = tk.Checkbutton(group, text="tsep", variable=varTsep)
        if vals[15]: tsep.select()
        #tsep.deselect()
        varAlign = tk.BooleanVar(value=vals[16])
        align = tk.Checkbutton(group, text="align", variable=varAlign)
        if vals[16]: align.select()
        #align.deselect()
        varInab = tk.BooleanVar(value=vals[17])
        inab = tk.Checkbutton(group, text="inab", variable=varInab)
        if vals[17]: inab.select()
        #inab.deselect()
        varVis = tk.BooleanVar(value=vals[18])
        vis = tk.Checkbutton(group, text="vis", variable=varVis)
        if vals[18]: vis.select()
        #vis.deselect()
        varSign = tk.BooleanVar(value=vals[20])
        sign = tk.Checkbutton(group, text="sign", variable=varSign)
        if vals[19]: sign.select()
        #sign.deselect()
        varFllt = tk.BooleanVar(value=vals[21])
        fllt = tk.Checkbutton(group, text="fllt", variable=varFllt)
        if vals[20]: fllt.select()
        #fllt.deselect()
        #seq = tk.Checkbutton(group, text="seq", var = vals[21])
        #seq.deselect()
        varWrk = tk.BooleanVar(value=vals[22])
        wrk = tk.Checkbutton(group, text="wrk", variable=varWrk)
        if vals[21]: wrk.select()
        #wrk.deselect()
        varReq = tk.BooleanVar(value=vals[23])
        req = tk.Checkbutton(group, text="req", variable=varReq)
        if vals[22]: req.select()
        #req.deselect()
        varFllk = tk.BooleanVar(value=vals[24])
        fllk = tk.Checkbutton(group, text="fllk", variable=varFllk)
        if vals[23]: fllk.select()
        #fllk.deselect()
        varLoadv = tk.BooleanVar(value=vals[25])
        loadv = tk.Checkbutton(group, text="loadv", variable=varLoadv)
        if vals[24]: loadv.select()
        #loadv.deselect()
        varPk = tk.BooleanVar(value=vals[26])
        pk = tk.Checkbutton(group, text="pk", variable=varPk)
        if vals[25]: pk.select()
        #pk.deselect()
        saveBtn = ttk.Button(group, text="Save", command=partial(controller.saveChanges, group))
        
        flle.grid(row=0, column=0)
        stato.grid(row=1, column=0)
        soab.grid(row=2, column=0)
        flgt.grid(row=3, column=0)
        flne.grid(row=0, column=1)
        flbt.grid(row=1, column=1)
        repl.grid(row=2, column=1)
        clbl.grid(row=3, column=1)
        dec.grid(row=0, column=2)
        flge.grid(row=1, column=2)
        flin.grid(row=2, column=2)
        rnd.grid(row=3, column=2)
        upab.grid(row=0, column=3)
        ccls.grid(row=1, column=3)
        fleq.grid(row=2, column=3)
        tsep.grid(row=3, column=3)
        align.grid(row=0, column=4)
        inab.grid(row=1, column=4)
        vis.grid(row=2, column=4)
        sign.grid(row=3, column=4)
        fllt.grid(row=0, column=5)
        #seq.grid(row=1, column=5)
        wrk.grid(row=1, column=5)
        req.grid(row=2, column=5)
        fllk.grid(row=3, column=5)
        loadv.grid(row=0, column=6)
        pk.grid(row=1, column=6)
        saveBtn.grid(row=2, column=6)
        '''
        



       
        
    def onTreeClick(self, event):
        item = self.explorerMenu.identify('item',event.x,event.y)
        element = self.explorerMenu.item(item,"text")
        controller.focusElement(self.sheets.tabContents[0], element)
        if controller.isField(element):
            self.editForm.grid_forget()
            global flags
            flags = controller.getBooleanVals(element)
            self.editForm = self.drawEditForm(self.app, element, flags)
            self.editForm.grid(row=2, column=0, columnspan=2)
        else:
            self.editForm.grid_forget()


        

mw = MainWindow(tk.Tk())