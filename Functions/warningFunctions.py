from .CSVFunctions import *
from .utilityFunctions import tabulateData

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

def tabulateWarnings(warningList):
    
    for warning in warningList:
        warning["messages"] = "\n".join(warning["messages"])
    
    tabulateData(warningList)

def warningAlert(warningList):
    print(f"There are currently {len(warningList)} warnings in the system \n")