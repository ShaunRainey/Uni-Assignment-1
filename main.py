import csv
import os
from datetime import datetime
from item import InventoryItem
from tabulate import tabulate #python -m pip install tabulate

CSV_Inventory_Path = os.path.join(os.path.dirname(__file__), "inventory.csv")
CSV_User_Path      = os.path.join(os.path.dirname(__file__), 'users.csv')

inventoryFields = ["itemId","itemName", "itemQuantity", "unitType", "category", "dateUpdated", "updatedBy"]
userFields      = ["userId", "userName", "password", "role"]

def checkCSV(path, headers): #checks to see if file exists, if not then it creates it
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    if not os.path.exists(path):
        print("Creating CSV storage file ...")
        with open(path, "w",newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(headers)
            (print("CSV storage file creation successful \n"))
    
def readAll(path, headers): #loads the contents of csv file into a variable for use
    checkCSV(path, headers)
    with open(path, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def nextItemId(path, headers): #Allows Id to incremenet with each addition
    rows = readAll(path, headers) 
    maxId = 0
    for r in rows:
        try:
            maxId = max(maxId, int(r.get("itemId", "0") or "0"))
        except ValueError:
            pass
    return str(maxId +1)

def promptInput(message): #helper function to avoid writing .strip() over and over
    return input(message).strip()

def appendRow(row, path, headers): #Adds a new entry to the bottom of the CSV file
    checkCSV(path, headers)
    with open(path, "a", newline="", encoding="utf-8") as f: 
        w = csv.DictWriter(f, fieldnames=inventoryFields)
        w.writerow(row)
    
def createItemObject(): #Creates an instance of the InventoryItem class, giving access to class methods
    while True:
        itemId = nextItemId(CSV_Inventory_Path, inventoryFields)
        name = promptInput("Item name: ")
        quantity = promptInput("Quantity: ")
        unit = promptInput("Unit: ")
        category = promptInput("Category: ")
        addedBy = promptInput("Your name: ")
        date = datetime.now().strftime("%Y-%m-%d")

        try:
            newItem = InventoryItem(itemId, name, quantity, unit, category, date, addedBy)

            print(newItem.toDict())
            print("Item Created \n")

            return newItem.toDict()
        
        except ValueError as e:
            print(f"\n Item creation failed: {e}")

def AddItem(path, headers):
    row = createItemObject()
    appendRow(row, path, headers)
    print("Item added \n")

def tabulateData(data):
    try: #this is to protect against an empty csv breaking the code
        col_alignment = ["center"] * len(data[0])
        print(tabulate(data, headers="keys", tablefmt="grid", colalign=col_alignment) + "\n")
    except:
        print("Currently no items held \n")

def listItems(path, headers):
    print("\n --- All Items --- \n")
    rows = readAll(path, headers)
    tabulateData(rows)

def searchItems(path, headers):
    print("\n --- Search Items --- \n")
    term = promptInput("Enter search term (itemName or updatedBy): ").lower()
    if not term:
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

def overWriteCSV(rows, path, headers):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

def updateItem(path, headers):
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
                        r["dateUpdated"] = datetime.now().strftime("%Y-%m-%d")
                    case "2":
                        r["itemQuantity"] = promptInput("Please enter the new value: ")
                        r["dateUpdated"] = datetime.now().strftime("%Y-%m-%d")
                    case "3":
                        r["unitType"] = promptInput("Please enter the new value: ")
                        r["dateUpdated"] = datetime.now().strftime("%Y-%m-%d")
                    case "4":
                        r["category"] = promptInput("Please enter the new value: ")
                        r["dateUpdated"] = datetime.now().strftime("%Y-%m-%d")
                    case "5":
                        break
                    case _:
                        print("Please enter a valid choice")
                        continue #restarts the loop rather than proceeding to next lines

                print("New record:")
                tabulateData([r])

                overWriteCSV(rows, path, headers)
                print("CSV file updated successfully \n")
            break
    else:
        print("\n Invalid ID \n ")    

def deleteEntry(path, headers):
    rows = readAll(path, headers)
    tabulateData(rows)
    changeId = promptInput("Please specify the ID of the item you would like to delete: ")

    for r in rows:
        if r["itemId"] == changeId:
            tabulateData([r])
            confirm = promptInput("Are you sure you want to delete this entry? Enter 'y' to confirm.\n")
            if confirm == 'y':
                rows.pop(rows.index(r)) #pop removes based on an index value
                overWriteCSV(rows, path, headers)
                print("Item deleted \n")
            else:
                print("Delete aborted \n")
    

def main():
    checkCSV(CSV_Inventory_Path, inventoryFields)
    checkCSV(CSV_User_Path, userFields)

    while True:
        print("\n What would you like to do? \n")
        print("1) List items")
        print("2) Add item")
        print("3) Update items")
        print("4) Delete items")
        print("5) Search for an item")
        print("6) Quit")
        choice = input("\n Choose (1/2/3/4/5/6): ").strip()

        match choice:
            case "1":
                listItems(CSV_Inventory_Path, inventoryFields)
            case "2":
                AddItem(CSV_Inventory_Path, inventoryFields)
            case "3":
                updateItem(CSV_Inventory_Path, inventoryFields)
            case "4":
                deleteEntry(CSV_Inventory_Path, inventoryFields)
            case "5":
                searchItems(CSV_Inventory_Path, inventoryFields)
            case "6":
                print("Goodbye!")
                break
            case _: #_ is the "default" word for python
                print("Enter a valid number.\n")

if __name__ == "__main__":
    main()
