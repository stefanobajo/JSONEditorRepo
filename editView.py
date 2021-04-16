from tkinter import ttk
import tkinter as tk
import json
import controller
from functools import partial

class EditView:
    def __init__(self, app, jsonFile):
        jsonFile.lstrip("{")
        jsonFile.rstrip("}")
        self.jsonObject = json.loads(jsonFile)

        app.title("Edit File")
        app.geometry("900x400")
        app.after(1, lambda: app.focus_force())

        appMenu = self.drawMenuBar(app)

        
        app.config(menu=appMenu)

        self.treeFrame = ttk.Frame(app)
        self.treeFrame.grid(row=0, column=0)
        
        #self.treeFrame.pack()
        
        self.jsonTree = ttk.Treeview(self.treeFrame)
        self.jsonTree.bind("<Double-1>", self.onTreeClick)
        
        self.jsonTree["columns"]=("Edit")
        self.jsonTree.column("Edit", width=270, minwidth=270, stretch=tk.NO)
        self.jsonTree.heading("Edit", text="Edit",anchor=tk.W)

        if jsonFile != "":
            controller.createTree(self.jsonTree, self.jsonObject, "root")

        

        self.jsonTree.pack(side=tk.TOP, fill=tk.BOTH, anchor="w")

        self.editFrame = ttk.Frame(app)
        self.editFrame.grid(row=0, column=1)
        self.editor = controller.EditorManager(self.editFrame)
        #self.editFrame.pack(side=tk.TOP, fill=tk.Y, anchor="e")

        self.app = app
        
        self.app.mainloop()
    
    def onTreeClick(self, event):
        item = self.jsonTree.identify('item',event.x,event.y)
        element = self.jsonTree.item(item,"text")
        print("you clicked on", element)
        self.editor.addItem(element)

    def drawMenuBar(self, app):
        menubar = tk.Menu(app)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Set Seq", command=partial(controller.setSeq, self.jsonObject))
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Exit", command = exit)

        menubar.add_cascade(label="File", menu=filemenu)
        return menubar