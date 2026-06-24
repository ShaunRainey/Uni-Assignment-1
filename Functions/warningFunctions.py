# Functions to create and display any warnings from the inventory CSV storage

from .CSVFunctions import *
from .utilityFunctions import tabulateData

#Check the system at the time of calling for the specified issues, append any matches to a list
def getWarnings(path, headers):
    
    warningList = []
    rows=readAll(path, headers)
    threshold = 10
    
    for r in rows:
        messages = []
        
        if int(r["itemQuantity"]) < threshold:
            messages.append(f"Quantity beneath threshold ({threshold})")

        if r["status"] == "faulty":
            messages.append("Faulty item present")

        if int(r["itemQuantity"]) == 0:
            messages.append(f"Item out of stock")

        if messages:
            warningList.append({
                "itemId"  : r["itemId"],
                "itemName": r["itemName"],
                "messages": messages
            })

    return warningList

#Displays the list created above
def tabulateWarnings(warningList):
    
    for warning in warningList:
        warning["messages"] = "\n".join(warning["messages"]) #Presents each issue for the same warning on a separate line for clarity
    
    tabulateData(warningList)

#Prints to the console how many warnings are currently in the system
def warningAlert(warningList):
    print(f"There are currently {len(warningList)} warnings in the system \n")
