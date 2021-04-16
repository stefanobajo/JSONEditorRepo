from tkinter import ttk
import tkinter as tk
import json
import controller

class EditView:
    def __init__(self, app, tree, jsonFile):
        app.title("Edit File")
        app.geometry("900x400")
        app.after(1, lambda: app.focus_force())

        treeFrame = ttk.Frame(app)
        treeFrame.pack(side=tk.TOP, fill=tk.BOTH, anchor="w")
        jsonTree = ttk.Treeview(treeFrame)
        if jsonFile != "":
            jsonFile.lstrip("{")
            jsonFile.rstrip("}")
            jsonObj = json.loads(jsonFile)
            controller.createTree(jsonTree, jsonObj, "root")

        jsonTree["columns"]=("Edit")
        jsonTree.column("Edit", width=270, minwidth=270, stretch=tk.NO)
        jsonTree.heading("Edit", text="Edit",anchor=tk.W)

        jsonTree.pack(side=tk.TOP, fill=tk.BOTH, anchor="w")

        
        editFrame = ttk.Frame(app)
        editList = tk.Listbox(editFrame)
        itemFrame = ttk.Frame(editList)
        saveButton = ttk.Button(editList, text="SAVE")

        jsonLabel = ttk.Label(itemFrame, text="TEST")
        jsonEdit = tk.Text(itemFrame)

        editFrame.pack(side=tk.TOP, fill=tk.BOTH, anchor="e")
        editList.pack(side=tk.TOP, fill=tk.Y, anchor="n")
        saveButton.pack(side=tk.TOP, fill=tk.X, anchor="n")
        itemFrame.pack(side=tk.LEFT, fill=tk.X, anchor="w")
        jsonLabel.pack(side=tk.LEFT, anchor="w")
        jsonEdit.pack(side=tk.RIGHT, anchor="e")

        self.app = app
        self.treeFrame = treeFrame
        self.jsonTree= jsonTree
        self.app.mainloop()