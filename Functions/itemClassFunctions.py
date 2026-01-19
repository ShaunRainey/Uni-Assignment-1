from .utilityFunctions import *
from .CSVFunctions import nextItemId, readAll, appendRow, overWriteCSV
from item import InventoryItem
import os
from datetime import datetime

CSV_Inventory_Path = os.path.join(os.path.dirname(__file__), "../inventory.csv")
inventoryFields = ["itemId","itemName", "itemQuantity", "unitType", "category", "dateUpdated", "updatedBy"]

def createItemObject(user): #Creates an instance of the InventoryItem class, giving access to class methods
    while True:
        itemId   = nextItemId(CSV_Inventory_Path, inventoryFields)
        name     = promptInput("Item name: ")
        quantity = promptInput("Quantity: ")
        unit     = promptInput("Unit: ")
        category = promptInput("Category: ")
        addedBy  = user.userName
        date     = datetime.now().strftime("%Y-%m-%d")

        try:
            newItem = InventoryItem(itemId, name, quantity, unit, category, date, addedBy) #Create an instance of the InventoryItem class

            print(newItem.toDict())
            print("Item Created \n")

            return newItem.toDict()
        
        except ValueError as e:
            print(f"\n Item creation failed: \n {e}")

def addItem(path, headers, user): #Create an object, takes in user details, adds it to CSV file
    row = createItemObject(user)
    print(row)
    appendRow(row, path, headers)
    print("Item added \n")
    return row

def searchItems(path, headers):
    print("\n --- Search Items --- \n")
    term = promptInput("Enter search term (itemName or updatedBy): ").lower()
    if not term: #Data validation to make sure a term has been input
        print("Empty search term \n")
        return

    rows = readAll(path, headers)
    results = []
    for r in rows:
        combined = (r.get('itemName','') + ' ' + r.get('updatedBy','')).lower()
        if term in combined:
            results.append(r)
    if not results:
        print ("No matches found")
        return
    tabulateData(results)

def updateItem(path, headers, currentlyLoggedIn):
    rows = readAll(path, headers)
    tabulateData(rows)
    changeId = promptInput("Please specify the ID of the item you would like to change: ")

    for r in rows:
        if r["itemId"] == changeId:
            tabulateData([r])
            
            while True:
                print("Please choose the property to update:")
                print("1) itemName")
                print("2) itemQuantity")
                print("3) unitType")
                print("4) category")
                print("5) exit")
                changeProperty = promptInput("\n Choose (1/2/3/4/5): \n")

                match changeProperty:
                    case "1":
                        r["itemName"] = promptInput("Please enter the new value: ")
                    case "2":
                        r["itemQuantity"] = promptInput("Please enter the new value: ")
                    case "3":
                        r["unitType"] = promptInput("Please enter the new value: ")
                    case "4":
                        r["category"] = promptInput("Please enter the new value: ")
                    case "5":
                        break
                    case _:
                        print("Please enter a valid choice")
                        continue #restarts the loop rather than proceeding to next lines

                r["dateUpdated"] = datetime.now().strftime("%Y-%m-%d")
                r["updatedBy"] = currentlyLoggedIn.userName

                print("New record:")
                tabulateData([r])

                overWriteCSV(rows, path, headers)
                print("CSV file updated successfully \n")
        
            return r
    else:
        print("\n Invalid ID \n ")