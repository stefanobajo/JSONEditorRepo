# Python program to illustrate the usage
# of hierarchical treeview in python GUI
# application using tkinter
 
# Importing tkinter
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
        explorerLabel.grid(row=0, column=0, padx=(5,0))
        
        # Creating treeview window
        explorerMenu = self.drawExplorerMenu(explorerFrame)
        explorerMenu["columns"]=("Edit")
        explorerMenu.column("Edit", width=270, minwidth=270, stretch=tk.NO)
        explorerMenu.heading("Edit", text="Edit",anchor=tk.W)
        explorerMenu["displaycolumns"] = ("")
        explorerMenu.grid(row=1, column=0, padx=(5,0))
        
        editButton = ttk.Button(app, text = "Edit", command=partial(controller.startEdit, self))
        editButton.grid(row=2, column=0, pady=(0, 5))
        

        
        
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
        app.mainloop()
        
    def drawMenuBar(self, app):
        menubar = tk.Menu(app)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command = partial(controller.openDialog, self))
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Exit", command = exit)

        menubar.add_cascade(label="File", menu=filemenu)
        return menubar

    def drawExplorerMenu(self, fr):
        
        expMenu = ttk.Treeview(fr)
        '''
        expMenu.insert('', '0', 'item1',
                    text ='GeeksforGeeks')
    
        # Inserting child
        expMenu.insert('item1', '1', 'item2',
                        text ='Computer Science')
        expMenu.insert('item1', '2', 'item3',
                        text ='GATE papers')
        expMenu.insert('item1', 'end', 'item4',
                        text ='Programming Languages')
        
        # Inserting more than one attribute of an item
        expMenu.insert('item2', 'end', 'Algorithm',
                        text ='Algorithm') 
        expMenu.insert('item2', 'end', 'Data structure',
                        text ='Data structure')
        expMenu.insert('item3', 'end', '2018 paper',
                        text ='2018 paper') 
        expMenu.insert('item3', 'end', '2019 paper',
                        text ='2019 paper')
        expMenu.insert('item4', 'end', 'Python',
                        text ='Python')
        expMenu.insert('item4', 'end', 'Java',
                        text ='Java')
        '''
        
        return expMenu 
        
        

mw = MainWindow(tk.Tk())