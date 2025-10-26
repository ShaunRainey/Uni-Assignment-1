import csv
import os
from datetime import datetime
from item import InventoryItem
from tabulate import tabulate #python -m pip install tabulate

CSV_Path = os.path.join(os.path.dirname(__file__), "inventory.csv")
fields = ["itemId","itemName", "itemQuantity", "unitType", "category", "dateUpdated", "updatedBy"]

def checkCSV(): #checks to see if file exists, if not then it creates it
    os.makedirs(os.path.dirname(CSV_Path) or ".", exist_ok=True)
    if not os.path.exists(CSV_Path):
        print("Creating CSV storage file ...")
        with open(CSV_Path, "w", newline="", encoding="utf-8") as f:  #"with" automatically closes an opened file when appropriate 
            csv.writer(f).writerow(fields)
            (print("CSV storage file creation successful \n"))

def readAll(): #loads the contents of csv file into a variable for use
    checkCSV()
    with open(CSV_Path, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def nextItemId(): #Allows Id to incremenet with each addition
    rows = readAll() 
    maxId = 0
    for r in rows:
        try:
            maxId = max(maxId, int(r.get("itemId", "0") or "0"))
        except ValueError:
            pass
    return str(maxId +1)

def promptInput(message): #helper function to avoid writing .strip() over and over
    return input(message).strip()

def appendRow(row):
    checkCSV()
    with open(CSV_Path, "a", newline="", encoding="utf-8") as f: 
        w = csv.DictWriter(f, fieldnames=fields)
        w.writerow(row)
    
def createItemObject():
    itemId = nextItemId()
    name = promptInput("Item name: ")
    quantity = promptInput("Quantity: ")
    unit = promptInput("Unit: ")
    category = promptInput("Category: ")
    addedBy = promptInput("Your name: ")
    date = datetime.now().strftime("%Y-%m-%d")

    newItem = InventoryItem(itemId, name, quantity, unit, category, date, addedBy)

    print("Item Created \n")
    print(newItem.toDict())

    return newItem.toDict()

def AddItem():
    row = createItemObject()
    appendRow(row)
    print("Item added \n")

def tabulateData(data):
    try: #this is to protect against an empty csv breaking the code
        col_alignment = ["center"] * len(data[0])
        print(tabulate(data, headers="keys", tablefmt="grid", colalign=col_alignment) + "\n")
    except:
        print("Currently no items held \n")

def listItems():
    print("\n --- All Items --- \n")
    rows = readAll() #index of an item is at itemId - 1, rows is a list of dictionaries
    tabulateData(rows)

def searchById(): #This currently looks for the item in a specified position, NOT its ID number
    searchId = int(input("Please enter the desired itemId: "))
    rows = readAll()
    rowById = rows[searchId - 1]
    tabulateData([rowById]) #tabulateData expects a list

def overWriteCSV(rows):
    with open(CSV_Path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def updateItem():
    rows = readAll()
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

                overWriteCSV(rows)
                print("CSV file updated successfully \n")
            break
    else:
        print("\n Invalid ID \n ")

            

def main():
    checkCSV()
    while True:
        print("What would you like to do?")
        print("1) Add item")
        print("2) List items")
        print("3) Quit")
        print("4) test search")
        print("5) test update")
        choice = input("Choose (1/2/3/4/5): ").strip()

        match choice:
            case "1":
                AddItem()
            case "2":
                listItems()
            case "3":
                print("Goodbye!")
                break
            case "4":
                searchById()
            case "5":
                updateItem()
            case _: #_ is the "default" word for python
                print("Enter a valid number.\n")

if __name__ == "__main__":
    main()
