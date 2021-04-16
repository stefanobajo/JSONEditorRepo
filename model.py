
#def buildJSONTree(json):

'''
def createTreeFromObject(tree, jsonObj, fathername):
    
    
    try:
        for item in jsonObj:
            
                val = jsonObj[item]
            

                firstCurly = json.dumps(val).startswith("{")
                firstSquare = json.dumps(val).startswith("[")
                
                if firstCurly or firstSquare:
                    tree.insert(fathername, 'end', item, text=item)
                    if firstCurly: 
                        createTreeFromObject(tree, val, item)
                    else:
                        if firstSquare:
                            createTreeFromArray(tree, val, item)
    except:
        tree.insert(fathername, 'end', str(jsonObj), text=str(jsonObj))
        print("Object rendered")
          
        
        

def createTreeFromArray(tree, jsonArray, fathername):
        
    try:
        for item in range(len(jsonArray)):
            
            val = jsonArray[item]
            

            firstCurly = json.dumps(val).startswith("{")
            firstSquare = json.dumps(val).startswith("[")
            if(firstCurly or firstSquare):
                tree.insert(fathername, 'end', str(item), text=str(item))
                if firstCurly: 
                    createTreeFromObject(tree, val, str(item))
                else:
                    if firstSquare:
                        createTreeFromArray(tree, val, str(item))
    except:
        tree.insert(fathername, 'end', str(jsonObj), text=str(jsonObj))
        print("Array rendered")
'''
'''
import tkinter as tk # python3
from tkinter import ttk
root = tk.Tk()
myList = tk.Listbox(root)
myText = "A list item"

fr = ttk.Frame(myList)
fr.pack()

lbl = tk.Label(fr, text=myText, anchor="w", font=("Helvetica", "24"))
lbl.pack(side="top", fill="x", anchor="w")

button = ttk.Button(fr, text="BUTTON")
button.pack(side="top", fill="x", anchor="e")

myList.insert(tk.END, fr)
myList.pack()

root.mainloop()
'''