
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