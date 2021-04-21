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
        #app.geometry("1080x500")
        #width = app.winfo_screenwidth()               
        app.state('zoomed')
        #height = app.winfo_screenheight()               

        #app.geometry("%dx%d" % (width, height))

        appMenu = self.drawMenuBar(app)

        
        app.config(menu=appMenu)
        
        '''
        app.grid_rowconfigure(0, weight=1)
        app.grid_rowconfigure(1, weight=1)
        app.grid_rowconfigure(2, weight=1)
        app.grid_columnconfigure(0, weight=1)
        '''
        app.grid_rowconfigure(0, weight=1)
        app.grid_rowconfigure(1, weight=1)
        app.grid_rowconfigure(2, weight=1)
        app.grid_rowconfigure(3, weight=6)
        app.grid_columnconfigure(0, weight=1)
        app.grid_columnconfigure(1, weight=4)
        app.grid_columnconfigure(2, weight=5)
        #app.grid_columnconfigure(3, weight=3)

        explorerFrame = ttk.Frame(app)
        explorerFrame.grid(row=0, column=0, rowspan=3, padx=(5,0))
        
        explorerLabel = ttk.Label(
            explorerFrame, 
            text ="Treeview(hierarchical)"
        )
        explorerLabel.pack(side = tk.TOP, fill=tk.BOTH, anchor="n")
        
        # Creating treeview window
        explorerMenu = ttk.Treeview(explorerFrame)
        #explorerMenu["columns"]=("Edit")
        #explorerMenu.column("Edit", width=270, minwidth=270, stretch=tk.NO)
        #explorerMenu.heading("Edit", text="Edit",anchor=tk.W)
        #explorerMenu["displaycolumns"] = ("")
        explorerMenu.pack(side = tk.TOP, fill=tk.BOTH, anchor="n")

        setSeqBtn = ttk.Button(explorerFrame, text="Set seq", command=partial(controller.setSeq, self))
        setSeqBtn.pack(side = tk.TOP, fill=tk.BOTH, anchor="n")
        setSeqBtn.pack_forget()

        disablingList = [False] * 26
        
        '''
        editForm = self.drawEditForm(app, "test", disablingList)
        editForm.grid(row=3, column=0, columnspan=3)
        editForm.grid_forget()
        
        '''
        
        
        # Calling pack method on the treeview

        # Inserting items to the treeview
        # Inserting parent
        
        # Placing each child items in parent widget
        sheetsFrame = ttk.Frame(app)
        noteBook = ttk.Notebook(
            sheetsFrame
        )
        
        sheets = controller.TabManager(self, noteBook)
        sheets.appendTab("new 1", "")
        sheets.nb.pack(side=tk.TOP, expand=True)
        #side=tk.RIGHT, fill=tk.BOTH, expand=True
        sheetsFrame.grid(row=0, column=1, rowspan=3, columnspan=2, padx=(10,0))
        

        self.app = app
        self.appMenu = appMenu
        self.explorerFrame = explorerFrame
        self.explorerLabel = explorerLabel
        self.explorerMenu = explorerMenu
        self.setSeqBtn = setSeqBtn
        self.sheets = sheets
        self.editForm = ttk.LabelFrame(self.app)
        self.explorerMenu.bind("<Double-1>", self.onTreeClick)

        app.mainloop()
        
    def drawMenuBar(self, app):
        menubar = tk.Menu(app)


        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command = partial(controller.openDialog, self))
        filemenu.add_command(label="Save", command = partial(controller.globalSave, self, ""))
        filemenu.add_command(label="Exit", command = exit)

        menubar.add_cascade(label="File", menu=filemenu)
        return menubar

    def drawEditForm(self, app, element, vals):
        group = ttk.Labelframe(app, text=element)
        flags = list()
        textFlds = list()
        counter = 0
        counterTxt = 0
        try:
            item = controller.getField(element)
            for camp in item:

                r = counter % 4
                c = int(counter / 4)

                if (item[camp] == 0 or item[camp] == 1) and camp != "seq":
                                   
                    
                    flags.append(tk.Checkbutton(group, text=camp, command=partial(controller.insertChange, camp, "FLAGCHANGE", None)))
                    
                    if vals[counter]: 
                        flags[len(flags)-1].select()
                        controller.changes[camp] = True
                    else:
                        flags[len(flags)-1].deselect()
                        controller.changes[camp] = False
                    flags[len(flags)-1].grid(row=r, column=c)
                    counter += 1
                

            

            for camp in item:

                r = counterTxt % 4
                c = int(counterTxt / 4)

                if (item[camp] != 0 and item[camp] != 1 and camp!="cedt" and camp!="lbl") or camp == "seq":
                    txtFrame = ttk.Frame(group)
                    txtLabel = ttk.Label(txtFrame, text=camp)
                    txtLabel.pack(side=tk.LEFT)
                    txtText = tk.Text(txtFrame, width=15, height=1)
                    txtText.bind('<KeyRelease>', partial(controller.insertChange, camp, "TEXTCHANGE"))
                    try:
                        txtText.insert(tk.INSERT, item[camp])
                    except:
                        print("ROTTO")

                    txtText.pack(side=tk.RIGHT)

                    textFlds.append(txtFrame)
                    txtFrame.grid(row=4+r, column=c)
                    counterTxt +=1
            #-------------CASO CAMPO CEDT-------------------
            txtFrame1 = ttk.Frame(group)
            txtLabel1 = ttk.Label(txtFrame1, text="cedt")
            txtLabel1.pack(side=tk.LEFT)
            txtText1 = tk.Text(txtFrame1, width=35, height=4)
            txtText1.bind('<KeyRelease>', partial(controller.insertChange, "cedt", "TEXTCHANGE"))
            #print(controller.formatStr('{"prova": 0,"di":0,"formattazione":2}'))
            try:
                txtText1.insert(tk.INSERT, controller.formatStr(str(item["cedt"])))
            except:
                print("ROTTO")

            txtText1.pack(side=tk.RIGHT)

            textFlds.append(txtFrame1)
            c = int(counterTxt / 4) + 1
            txtFrame1.grid(row=4, column=c, rowspan=4)

            #-----------CAMPO LBL-----------------------
            txtFrame2 = ttk.Frame(group)
            txtLabel2 = ttk.Label(txtFrame2, text="lbl")
            txtLabel2.pack(side=tk.LEFT)
            txtText2 = tk.Text(txtFrame2, width=35, height=4)
            txtText2.bind('<KeyRelease>', partial(controller.insertChange, "lbl", "TEXTCHANGE"))
            try:
                txtText2.insert(tk.INSERT, controller.formatStr(str(item["lbl"])))
            except:
                print("ROTTO")

            txtText2.pack(side=tk.RIGHT)

            textFlds.append(txtFrame2)
            c+=1
            txtFrame2.grid(row=4, column=c, rowspan=4)
    

                
                    

        except:
            traceback.print_exc()
        
        
        saveBtn = ttk.Button(group, text="Save", command=partial(controller.saveChanges, self))    
        saveBtn.grid(row=2, column=6)
        addBtn = ttk.Button(group, text="Add", command=partial(controller.addElement, self))
        addBtn.grid(row=3, column=6)

        return group
       
    def onTreeClick(self, event):
        item = self.explorerMenu.identify('item',event.x,event.y)
        element = self.explorerMenu.item(item, "text")
        controller.focusElement(self.sheets.tabContents[0], element)
        element = str(element)
        element = element.strip("\"")
        if controller.isField(element):
            self.editForm.grid_forget()
            global flags
            flags = controller.getBooleanVals(element)
            self.editForm = self.drawEditForm(self.app, element, flags)
            self.editForm.grid(row=3, column=0, columnspan=3, padx=(5,0))
        else:
            self.editForm.grid_forget()


        

mw = MainWindow(tk.Tk())