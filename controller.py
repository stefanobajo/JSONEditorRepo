from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from tkinter import Message
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk 
import model
import json
import editView

content = ""

class TabManager:

    def __init__(self, nb):
        nb.grid_propagate(True)
        self.nb = nb
        self.tabList = list()
        self.tabFrames = list()
        self.tabContents = list()
    
    def removeTab(self, tabName):
        for t in self.tabList:
            if t["title"] == tabName:
                self.tabList.remove(t)
        self.updateIndexes()
        self.updateNoteBook()
    
    def updateIndexes(self):
        for i in range(len(self.tabList)):
            self.tabList[i]["index"] = i

    def appendTab(self, tabName, content):
        alreadyIn = False
        if (len(self.tabList) == 1 and self.tabList[0]["title"] == "new 1"):
            self.removeTab("new 1")
        for t in self.tabList:
            if t["title"] == tabName:
                t["content"] = content
                alreadyIn = True

        index = len(self.tabList)
        if not alreadyIn:
            self.tabList.append(
                {
                    "title": tabName,
                    "content": content,
                    "index": index
                }
            )
        self.updateNoteBook()
        #self.showTabs()

    def updateNoteBook(self):
        self.tabContents.clear()
        self.tabFrames.clear()
        for t in self.tabList:
            try:
                self.nb.forget(t["index"])
                
            except:
                print("")
            finally:
                print(self.nb.tabs())
            
            self.tabFrames.append(ttk.Frame(self.nb))
            self.tabContents.append(tk.Text(self.tabFrames[t["index"]], height="300", width="400"))
            self.tabContents[t["index"]].insert(tk.INSERT, t["content"])
            self.tabContents[t["index"]].pack()
            #tabContent.pack()
            #tabContent.place(anchor='e')
            #self.tabFrames[t["index"]].pack()
            self.nb.add(self.tabFrames[t["index"]], text=t["title"])
    
    #def showTabs(self):
       # for f in self.tabFrames:
       #     f.pack()
            #.pack(expand = True, side = RIGHT)

        
def openDialog(mw):
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    global directory
    directory = askopenfilename(initialdir = "C:/Users/stebag/Desktop/Roba/", title = "Select file", filetypes = (("json files","*.json"), ("all files","*.*"))) # show an "Open" dialog box and return the path to the selected file
    f = open(directory)
    global content
    content = f.read()
    filename = directory[::-1].split("/")[0][::-1]
    mw.sheets.appendTab(filename, content)

    content.lstrip("{")
    content.rstrip("}")
    contentObj = json.loads(content)
    createTree(mw.explorerMenu, contentObj, "root")
    
    messagebox.showinfo("Complimenti!", "Call succesful: " + filename)

def createTree(tree, jsonObj, fatherName):
    if fatherName == "root":
        fatherName = ""

    jsonString = json.dumps(jsonObj)
    if(jsonString.startswith("{") or jsonString.startswith("[")):
        counter = 0
        for item in jsonObj:
            if jsonString.startswith("["):
                tree.insert(fatherName, 'end', fatherName+str(counter), text=str(counter), values=(""))
                nodeText = createTree(tree, item, fatherName+str(counter))
            else:
                tree.insert(fatherName, 'end', fatherName+str(item), text=str(item), values=(""))
                val = jsonObj[item]
                nodeText = createTree(tree, val, fatherName+str(item))

            if nodeText.find("{") + nodeText.find("[") == -2:
                if jsonString.startswith("["):
                    tree.delete(fatherName + str(counter))
                    tree.insert(fatherName, 'end', fatherName + str(counter), text=str(counter) + ": " + nodeText, values=(""))
                else:
                    tree.delete(fatherName + str(item))
                    tree.insert(fatherName, 'end', fatherName + str(item), text=str(item) + ": " + nodeText, values=(""))

                

            counter += 1
    else:
        print("Dead Node Reached")
    return jsonString

def startEdit(mw):
    editWindow = tk.Tk()
    ew = editView.EditView(editWindow, mw.explorerMenu, content)

def onTreeClick():
    pass
            

       



