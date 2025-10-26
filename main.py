import csv
import os
from datetime import datetime
from item import InventoryItem
from tabulate import tabulate #python -m pip install tabulate

CSV_Path = os.path.join(os.path.dirname(__file__), "inventory.csv")
fields = ["itemId","itemName", "itemQuantity", "unitType", "category", "dateUpdated", "updatedBy"]



def checkCSV():
    os.makedirs(os.path.dirname(CSV_Path) or ".", exist_ok=True)
    if not os.path.exists(CSV_Path):
        print("Creating CSV storage file ...")
        with open(CSV_Path, "w", newline="", encoding="utf-8") as f:  #"with" automatically closes an opened file when appropriate 
            csv.writer(f).writerow(fields)
            (print("CSV storage file creation successful \n"))
    else:
        print("CSV file present \n")



def readAll():
    checkCSV()
    with open(CSV_Path, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
    


def nextItemId():
    rows = readAll()
    maxId = 0
    for r in rows:
        try:
            maxId = max(maxId, int(r.get("itemId", "0") or "0"))
        except ValueError:
            pass
    return str(maxId +1)



def appendRow(row):
    checkCSV()
    with open(CSV_Path, "a", newline="", encoding="utf-8") as f: 
        w = csv.DictWriter(f, fieldnames=fields)
        w.writerow(row)
    
def createItemObject():
    itemId = nextItemId()
    name = input("Item name: ").strip()
    quantity = input("Quantity: ").strip()
    unit = input("Unit: ").strip()
    category = input("Category: ").strip()
    addedBy = input("Your name: ").strip()
    date = datetime.now().strftime("%Y-%m-%d")

    newItem = InventoryItem(itemId, name, quantity, unit, category, date, addedBy)

    print("Item Created \n")
    print(newItem.to_dict() + "\n")

    return newItem.to_dict()


def AddItem():
    row = createItemObject()
    appendRow(row)
    print("Item added \n")



def listItems():
    print("\n --- All Items --- \n")
    rows = readAll()
    try: #this is to protect against an empty csv breaking the code
        col_alignment = ["center"] * len(rows[0])
        print(tabulate(rows, headers="keys", tablefmt="grid", colalign=col_alignment) + "\n")
    except:
        print("Currently no items held \n")


def main():
    checkCSV()
    while True:
        print("Basic Inventory")
        print("1) Add item")
        print("2) List items")
        print("3) Quit \n")
        choice = input("Choose (1/2/3): ").strip()

        match choice:
            case "1":
                AddItem()
            case "2":
                listItems()
            case "3":
                print("Goodbye!")
                break
            case _: #_ is the "default" word for python
                print("Enter a valid number.\n")

if __name__ == "__main__":
    main()
