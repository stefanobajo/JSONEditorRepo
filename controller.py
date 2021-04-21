from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from tkinter import Message
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import json
from functools import partial
import os
import traceback

content = ""
#directory = ""
changes = dict()

class TabManager:

    def __init__(self, mw, nb):
        nb.grid_propagate(True)
        nb.bind_all("<<Paste>>", partial(onPaste, mw))
        
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
                    "directory": "",
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
            
            self.tabContents.append(tk.Text(self.tabFrames[t["index"]], width=500, height=180))
            #app.grid_rowconfigure(2, weight=1)
            self.tabContents[t["index"]].insert(tk.INSERT, t["content"])
            self.tabContents[t["index"]].pack()
            #tabContent.pack()
            #tabContent.place(anchor='e')
            #self.tabFrames[t["index"]].pack()
            self.nb.add(self.tabFrames[t["index"]], text=t["title"])



def focusElement(text, s):
    text.tag_remove('found', '1.0', tk.END)
    
    if s:
        idx = '1.0'
        while 1:
            idx = text.search(s, idx, nocase=1, stopindex=tk.END)
            if not idx: break
            lastidx = '%s+%dc' % (idx, len(s))
            text.tag_add('found', idx, lastidx)
            idx = lastidx
            text.see(idx)  # Once found, the scrollbar automatically scrolls to the text
        text.tag_config('found', foreground='red')

def onPaste(mw, event):
    global content
    content = mw.app.clipboard_get()
    global contentObj
    contentObj = json.loads(content)
    createTree(mw.explorerMenu, contentObj, "root")
        
def openDialog(mw):
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    global directory
    directory = askopenfilename(initialdir = "C:/", title = "Select file", filetypes = (("json files","*.json"), ("all files","*.*"))) # show an "Open" dialog box and return the path to the selected file
    f = open(directory)
    global content
    content = f.read()
    f.close()
    global filename
    filename = directory[::-1].split("/")[0][::-1]
    mw.sheets.appendTab(filename, content)

    content.lstrip("{")
    content.rstrip("}")
    global contentObj
    contentObj = json.loads(content)
    createTree(mw.explorerMenu, contentObj, "root")
    mw.setSeqBtn.pack(side = tk.BOTTOM, fill=tk.X)
    
def createTree(tree, jsonObj, fatherName):
    if fatherName == "root":
        fatherName = ""

    jsonString = json.dumps(jsonObj)
    if(jsonString.startswith("{") or jsonString.startswith("[")):
        counter = 0
        for item in jsonObj:
            if jsonString.startswith("["):
                try:
                    tree.insert(fatherName, 'end', fatherName+str(counter), text='"'+ item["camp"] + '"')
                except:
                    tree.insert(fatherName, 'end', fatherName+str(counter), text=str(counter))
                nodeText = createTree(tree, item, fatherName+str(counter))
            else:
                tree.insert(fatherName, 'end', fatherName+str(item), text=str(item))
                val = jsonObj[item]
                nodeText = createTree(tree, val, fatherName+str(item))

            if nodeText.find("{") + nodeText.find("[") == -2:
                if jsonString.startswith("["):
                    tree.delete(fatherName + str(counter))
                    tree.insert(fatherName, 'end', fatherName + str(counter), text=str(counter) + ": " + nodeText)
                else:
                    tree.delete(fatherName + str(item))
                    tree.insert(fatherName, 'end', fatherName + str(item), text='"' + str(item) + '": ' + nodeText)

                

            counter += 1
    else:
        pass
    return jsonString

def getField(name):
    fld = contentObj["def"]["flds"]["fld"]

    for item in fld:
        if item["camp"].casefold() == name.casefold():
            return item
    return None

def isField(element):
    if getField(element) is not None:
        return True
    else:
        return False

def getBooleanVals(element):
    
    values = list()
    item = getField(element)
    for camp in item:
        if item[camp] == 0 and camp != "seq":
            values.append(False)
        else:
            if item[camp] == 1 and camp != "seq":
                values.append(True)
    return values

def insertChange(name, changeType, event):
    if changeType == "FLAGCHANGE" : changes[name] = not changes[name]
    else:
        val = event.widget.get("1.0", tk.END)
        val.rstrip("\n")
        changes[name] = val

def setSeq():
    f = open(directory, 'r')
    flines = f.readlines()
    counter = 1
    for line in range(len(flines)):
        whiteSpaces = flines[line].count(" ")
        flines[line] = flines[line].strip()
        if flines[line].startswith('"seq":'):
            s = ""
            for i in range(whiteSpaces):
                s += " "
            flines[line] = s + '"seq": ' + str(counter) + ',\n'
            counter += 1
        s = ""
        for i in range(whiteSpaces):
            s += " "
        flines[line] = s + flines[line] + '\n'
    
    f = open(directory, 'w')
    f.writelines(flines)
    f = open(directory, 'r')
    string = f.read()
    f.close()
    mw.sheets.removeTab(filename)
    mw.sheets.appendTab(filename, string)
    messagebox.showinfo("Changes Saved!", "Sequence numbers setted")

def saveChanges(mw):
    item = getField(mw.editForm.cget("text"))
    
    try:
        for ch in changes:
            
            if isinstance(changes[ch], bool):
                if changes[ch]:
                    item[ch] = 1
                else:
                    item[ch] = 0
            else:
                if ch=="id" or ch=="seq" or ch=="width" or ch=="len":
                    item[ch] = int(changes[ch])
                else:
                    item[ch] = json.loads(changes[ch])
        globalSave(None, json.dumps(contentObj, indent=4))
    except:
        messagebox.showwarning("Errore!", "Forse hai commesso degli errori!")
    
    
def globalSave(mw, text):
    if mw is not None:
        text = mw.sheets.tabContents[0].get("1.0", tk.END)
    f = None
    global content
    content = text
    global contentObj 
    contentObj = None
    try:
        contentObj = json.loads(content)
    except:
        messagebox.showwarning("Errore!", "Forse hai commesso degli errori!")
        
    if contentObj is not None:

        try:
            global directory
            f = open(directory, 'w')
        except:
            traceback.print_exc()
            Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
            #global directory
            directory = askopenfilename(initialdir = "C:/", title = "Select file", filetypes = (("json files","*.json"), ("all files","*.*"))) # show an "Open" dialog box and return the path to the selected file
            global filename
            filename = directory[::-1].split("/")[0][::-1]

        if f is None: f = open(directory, 'w')
        
        try:
            f.write(text)
        except:
            print("Error Saving")
        
        try:
            mw.sheets.removeTab(filename)
            mw.sheets.appendTab(filename, text)
        except:
            print("No filename found")

        messagebox.showinfo("Save was succesfull", "File " + directory + " was successfully saved!")

def formatStr(s):
    formattedString = ""
    for c in s:
        if c =="'": 
            c="\""
        formattedString += c
    return json.dumps(json.loads(formattedString), indent = 4)



