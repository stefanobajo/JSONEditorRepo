from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from tkinter import Message
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
import json
from functools import partial
import os
import traceback
import ast

#content = ""
#directory = ""
changes = dict()

class TabManager:

    def __init__(self, mw, nb):
        nb.grid_propagate(True)
        nb.bind_all("<<Paste>>", partial(onPaste, mw))
        self.mw = mw
        self.nb = nb
        self.nb.bind_all("<<NotebookTabChanged>>", self.tabSelected)
        self.tabList = list()
        self.tabFrames = list()
        self.tabContents = list()
    
    def removeSelectedTab(self):
        index = self.nb.index(self.nb.select())
        self.removeTab(self.tabList[index]["title"])
        

    def removeTab(self, tabName):
        
        index = -1
        for t in self.tabList:
            if t["title"] == tabName:
                index = t["index"]
            '''    
            else:
                if tabName.startswith("new") and t["title"].startswith("new") and t["directory"] == "":
                    t["title"] = "new " + str(counter)
                    self.nb.tab(t["index"], text = t["title"])
                    counter += 1
            '''
        
        self.nb.forget(index)
        self.tabContents.remove(self.tabContents[index])
        self.tabFrames.remove(self.tabFrames[index])
        self.tabList.remove(t)
        self.updateIndexes()
        try:
            self.nb.select(0)
        except:
            print("Tabs cleared")
        for t in self.tabList:
            if t["title"].startswith("new") and t["directory"] == "":
                newTitle = "new " + str(t["index"])
                t["title"] = newTitle
                self.nb.tab(t["index"], text = newTitle)

        self.mw.explorerMenu.delete(*self.mw.explorerMenu.get_children())
        self.mw.editForm.grid_forget()
                
        
        #self.updateNoteBook()
    
    def updateIndexes(self):
        for i in range(len(self.tabList)):
            self.tabList[i]["index"] = i

    def countNewTabs(self):
        counter = 0
        for t in self.tabList:
            if t["title"].startswith("new") and t["directory"] == "":
                counter += 1
        return counter

    def appendTab(self, tabName, content, path):
        alreadyIn = False

        if tabName == "":
            tabName = "new " + str(self.countNewTabs())
            #path = ""
        
        for t in self.tabList:
            if t["title"] == tabName and t["directory"] == path:
                self.editTab(tabName, content)
                alreadyIn = True

        index = len(self.tabList)
        if not alreadyIn:
            self.tabList.append(
                {
                    "title": tabName,
                    "content": content,
                    "directory": path,
                    "index": index
                }
            )
            f = ttk.Frame(self.nb)
            
            txt = tk.Text(f)
            sc = ttk.Scrollbar(f, orient=tk.VERTICAL ,command=txt.yview)
            txt['yscrollcommand'] = sc.set
            #, width=500, height=180))
            #app.grid_rowconfigure(2, weight=1)
            txt.insert(tk.INSERT, content)
            sc.pack(side=tk.RIGHT, fill=tk.Y)
            txt.pack(fill=tk.BOTH)
            #f.grid(row=0, column=0, sticky="NSWE")
            #self.tabFrames[t["index"]].pack(fill=tk.BOTH)
            #tabContent.pack()
            #tabContent.place(anchor='e')
            #self.tabFrames[t["index"]].pack()
            self.nb.add(f, text=tabName)
            self.tabContents.append(txt)
            self.tabFrames.append(f)

        self.nb.select(index)
        #self.tabSelected(None)

    def editTab(self, tabName, text):
        tab = None
        tabWidget = None
        for t in self.tabList:
            if t["title"] == tabName:
                tab = t
        if tab is not None:
            tab["content"] = text
            tabWidget = self.tabContents[tab["index"]]
        
        if tabWidget is not None:
            tabWidget.delete("1.0", tk.END)
            tabWidget.insert(tk.INSERT, text)
        
    def tabSelected(self, event):
        tabIndex = self.nb.index(self.nb.select())
        global directory
        directory = self.tabList[tabIndex]["directory"]
        global filename
        filename = self.tabList[tabIndex]["title"]
        global content
        content = self.tabList[tabIndex]["content"]
        global contentObj
        try:
            content.lstrip("{")
            content.rstrip("}")
            contentObj = json.loads(content)
            self.mw.setSeqBtn.pack(side = tk.BOTTOM, fill=tk.X)
        except:
            contentObj = None 
        self.mw.explorerMenu.delete(*self.mw.explorerMenu.get_children())
        self.mw.editForm.grid_forget()
        createTree(self.mw.explorerMenu, contentObj, "root")

        child_id = "deffldsfld0"
        try:
            self.mw.explorerMenu.see(child_id)
        except:
            print("not datasource")
        

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
    
    try:
        contentObj = json.loads(content)
    except:
        contentObj = None

    if contentObj is not None:
        mw.explorerMenu.delete(*mw.explorerMenu.get_children())
        mw.editForm.grid_forget()
        createTree(mw.explorerMenu, contentObj, "root")
        mw.setSeqBtn.pack(side = tk.BOTTOM, fill=tk.X)
        child_id = "deffldsfld0"
        #self.mw.explorerMenu.focus_set()
        #self.mw.explorerMenu.selection_set((child_id, child_id))
        try:
            mw.explorerMenu.see(child_id)
        except:
            print("not datasource")
    
def openDialog(mw):
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    
    if len(mw.sheets.tabList) > 0: 
        initialdir = mw.sheets.tabList[len(mw.sheets.tabList)-1]["directory"]
    else:
        initialdir = "C:/"
    directory = askopenfilename(initialdir = initialdir, title = "Select file", filetypes = (("json files","*.json"), ("all files","*.*"))) # show an "Open" dialog box and return the path to the selected file
    f = open(directory)
    #global content
    content = f.read()
    f.close()
    #global filename
    filename = directory[::-1].split("/")[0][::-1]
    mw.sheets.appendTab(filename, content, directory)
        
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
                #print(fatherName+str(counter))
                nodeText = createTree(tree, item, fatherName+str(counter))
            else:
                tree.insert(fatherName, 'end', fatherName+str(item), text=str(item))
                #print(fatherName+str(item))
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

def getFieldFromId(fid):
    fld = contentObj["def"]["flds"]["fld"]

    for item in fld:
        if item["id"] == fid:
            return item
    return None

def getField(name):
    try:
        fld = contentObj["def"]["flds"]["fld"]

        for item in fld:
            if item["camp"].casefold() == name.casefold():
                return item
        return None
    except:
        messagebox.showerror("Errore!", "Non sono riuscito a leggere uno dei campi :(")
        return None

def isField(element):
    if contentObj is not None and getField(element) is not None:
        return True
    else:
        return False

def getBooleanVals(element):
    
    values = list()
    item = getField(element)
    for camp in item:
        if item[camp] == 0 and camp != "seq" and camp != "soab":
            values.append(False)
        else:
            if item[camp] == 1 and camp != "seq" and camp != "soab":
                values.append(True)
    return values

def insertChange(name, changeType, event=None):
    name = name.strip(" ")
    if changeType == "FLAGCHANGE" : 
        changes[name] = not changes[name]
    else:
        val = event.widget.get("1.0", tk.END)
        val = val.rstrip("\n")
        changes[name] = val

def setSeq(mw):

    currentTab = mw.sheets.nb.index(mw.sheets.nb.select())
    text = mw.sheets.tabContents[currentTab].get("1.0", tk.END)

    #global directory
    #f = open(directory, 'r')
    #flines = f.readlines()
    counter = 1
    string = ""
    for line in iter(text.splitlines()):#range(len(flines)):
        whiteSpaces = line.count(" ")
        line = line.strip()
        if line.startswith('"seq":'):
            s = ""
            for i in range(whiteSpaces):
                s += " "
            line = s + '"seq": ' + str(counter) + ',\n'
            
            counter += 1
        else:
            s = ""
            for i in range(whiteSpaces):
                s += " "
            line = s + line + '\n'
        string += line

    global directory
    if directory != "":
        try:
            f = open(directory, 'w')
            f.write(json.dumps(json.loads(string), indent=4))
            f.close()
        except:
            print("Directory machine broke :(")
    global filename
    mw.sheets.editTab(filename, string)
    
    #mw.sheets.appendTab(filename, string, directory)
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
                if ch=="id" or ch=="seq" or ch=="width" or ch=="len" or ch=="soab":
                    item[ch] = int(changes[ch])
                else:
                    if ch=="cedt" or ch=="lbl":
                        item[ch] = json.loads(changes[ch])
                    else: 
                        item[ch] = changes[ch]
        globalSave(mw, json.dumps(contentObj, indent=4), False)
        global directory
        #messagebox.showinfo("Save was succesfull", "File " + directory + " was successfully saved!")
    except:
        traceback.print_exc()
        messagebox.showwarning("Errore!", "Rilevato un errore nella seguente modifica: \n" + changes[ch])
    
def globalSave(mw, text, fromMenu):
    global directory
    if directory is None or directory == "":
        saveAs(mw)
    else:
        currentTab = mw.sheets.nb.index(mw.sheets.nb.select())
        
        if fromMenu:
            #currentTab = mw.sheets.nb.index(mw.sheets.nb.select())
            text = mw.sheets.tabContents[currentTab].get("1.0", tk.END)

        mw.sheets.tabList[currentTab]["content"] = text
        f = None
        global content
        content = text
        global contentObj 
        contentObj = None
        global filename
        try:
            contentObj = json.loads(content)
        except:
            if filename.endswith(".json"): 
                messagebox.showwarning("Errore!", "Forse hai commesso degli errori!")

        if contentObj is not None:

            try:
                #global directory
                f = open(directory, 'w')
            except:
                
                traceback.print_exc()
                '''
                Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
                #global directory
                directory = askopenfilename(initialdir = "C:/", title = "Select file", filetypes = (("json files","*.json"), ("all files","*.*"))) # show an "Open" dialog box and return the path to the selected file
                
                filename = directory[::-1].split("/")[0][::-1]
                '''
            if f is None: f = open(directory, 'w')
            
            try:
                f.write(text)
            except:
                print("Error Saving")
            
            try:
                #global filename
                mw.sheets.editTab(filename, text)
            except:
                print("No filename found")

            messagebox.showinfo("Save was succesfull", "File " + directory + " was successfully saved!")

            mw.explorerMenu.delete(*mw.explorerMenu.get_children())
            mw.editForm.grid_forget()
            createTree(mw.explorerMenu, contentObj, "root")
            child_id = "deffldsfld0"
        
            try:
                self.mw.explorerMenu.see(child_id)
            except:
                print("not datasource")
        else:
            if filename.endswith(".txt") and directory != "":
                f = open(directory, 'w')
                f.write(text)
                f.close()
                messagebox.showinfo("Save was succesfull", "File " + directory + " was successfully saved!")



def formatStr(s):
    formattedString = ""
    for c in s:
        if c =="'": 
            c="\""
        if c =="\n": 
            c=""
        formattedString += c
    return json.dumps(json.loads(formattedString), indent = 4)

def addElement(mw):
    element = dict()
    global contentObj
    flds = contentObj["def"]["flds"]["fld"]
    #-----"SORT" del dictionary--------
    for item in flds[0]:
        element[item] = "temp"

    for fld in mw.editForm.winfo_children():
        if(isinstance(fld, ttk.Checkbutton)):
            name = fld.cget("text")
            val = changes[fld.cget("text")]
            element[name] = 1 if val else 0
        else:
            if(isinstance(fld, ttk.Frame)):
                frChidren = fld.winfo_children()
                name = frChidren[0].cget("text")
                val = frChidren[1].get("1.0", tk.END)
                #print(name + " ------------- " + val)
                val = val.strip(" ")
                val = val.rstrip("\n")
                if (name=="camp" and getField(val) is not None) or (name=="id" and getFieldFromId(val) is not None):
                    messagebox.showwarning("Attenzione!", "Stai cercando di inserire un elemento già presente!")
                    break

                if name=="id" or name=="seq" or name=="width" or name=="len" or name=="soab":
                    val = int(val)
                else:
                    if name == "cedt" or name == "lbl":
                        val = ast.literal_eval(val)
                        #print(json.dumps(val, indent = 4))
                    #val = json.dumps(val, indent = 4)
                element[name] = val
    print("RESULT: \n")
    #print(formatStr(str(element)))
    try:
        x = json.loads(json.dumps(element))
        flds.append(x)
        globalSave(mw, json.dumps(contentObj, indent=4), False)
        messagebox.showinfo("Successo!", "Hai aggiunto l'elemento " + x["camp"] + " al file.")
        #print(json.dumps(x, indent=4))
        #print(json.loads(formatStr(str(element))))
    except:
        traceback.print_exc()

def deleteElement(mw):
    camp = mw.editForm.cget("text")
    item = getField(camp)
    if item is None:
        messagebox.showerror("Delete error!", "You can't delete non-existing elements!")
    else:
        global contentObj
        fld = contentObj["def"]["flds"]["fld"]
        fld.remove(item)
        globalSave(mw, json.dumps(contentObj, indent=4), False)
        messagebox.showinfo("Successo!", "Hai eliminato l'elemento " + camp + " dal file.")
    
def saveAs(mw):
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

    index = mw.sheets.nb.index(mw.sheets.nb.select())
    tab = mw.sheets.tabList[index]
    tabWidget = mw.sheets.tabContents[index]

    global directory
    global filename
    global content
    global contentObj
    #global contentObj

    if directory != "":
        directory.rstrip(filename)
        saveDirectory = asksaveasfilename(initialdir = directory, title = "Save file", initialfile = filename, defaultextension = "*.*", filetypes = (("json files","*.json"), ("txt files","*.txt"))) # show an "Open" dialog box and return the path to the selected file, ("all files","*.*")
    
    else:
        saveDirectory = asksaveasfilename(initialdir = "C:/", title = "Save file", defaultextension = "*.*", initialfile = filename, filetypes = (("json files","*.json"), ("txt files","*.txt"))) # show an "Open" dialog box and return the path to the selected file
    
    if saveDirectory != "":
        directory = saveDirectory
        filename = directory[::-1].split("/")[0][::-1]
    content = tabWidget.get("1.0", tk.END)
    tab["title"] = filename
    tab["content"] = content
    tab["directory"] = directory
    mw.sheets.nb.tab("current", text= filename)
    content.lstrip("{")
    content.rstrip("}")
    try:
        contentObj = json.loads(content)
    except:
        contentObj = None
        print("NOT JSON")
    try:
        f = open(directory, 'w')
        f.write(content)
        f.close()
        messagebox.showinfo("Successo!", "File salvato con successo!")
        mw.explorerMenu.delete(*mw.explorerMenu.get_children())
        mw.editForm.grid_forget()
        createTree(mw.explorerMenu, contentObj, "root")
        child_id = "deffldsfld0"
        try:
            self.mw.explorerMenu.see(child_id)
        except:
            print("not datasource")
    except:
        messagebox.showerror("Error!", "Error saving file!")
    
        
    #mw.sheets.tabSelected(None)


