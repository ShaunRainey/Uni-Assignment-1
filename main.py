import csv
import os
from datetime import datetime

CSV_Path = os.path.join(os.path.dirname(__file__), "inventory.csv")
fields = ["itemId","itemName", "itemQuantity", "unitType", "category", "dateUpdated", "updatedBy"]



def checkCSV():
    os.makedirs(os.path.dirname(CSV_Path) or ".", exist_ok=True)
    if not os.path.exists(CSV_Path):
        print("Creating CSV file ...")
        with open(CSV_Path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(fields)
            (print("CSV file creation successful"))
    else:
        print("CSV file present")



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
    


def AddItem():
    name = input("Item name: ").strip()
    quantity = input("Quantity: ").strip()
    unit = input("Unit: ").strip()
    category = input("Category: ").strip()
    addedBy = input("Your name: ").strip()

    try:
        qty = int(quantity)
        if qty <= 0:
            print("Quantity must be greater than 0. \n")
            return
    except ValueError: 
        print("Quantity must be a number")
        return

    row = {
        "itemId": nextItemId(),
        "itemName": name,
        "itemQuantity": str(qty),
        "unitType": unit,
        "category": category,
        "dateUpdated": datetime.now().strftime("%Y-%m-%d"),
        "updatedBy": addedBy,
        }
    appendRow(row)
    print("Item added")



def listItems():
    print("\n --- All Items ---")
    rows = readAll()
    if not rows:
        print("(no items)\n")
        return
    
    print(f"{'itemId':>3} {'itemName':<20} {'itemQuantity':>4} {'unitType':<4} {'category':<20} {'dateUpdated'} {'Added By':<12}")

    for r in rows:
        print(f"{r.get('itemId',''):>3} {r.get('itemName',''):<20} {r.get('itemQuantity',''):>4} {r.get('unitType',''):<4} {r.get('category',''):<20} {r.get('dateUpdated','')} {r.get('updatedBy',''):<12}")
        print()

def main():
    checkCSV()
    while True:
        print("Basic Inventory")
        print("1) Add item")
        print("2) List items")
        print("3) Quit")
        choice = input("Choose (1/2/3): ").strip()

        if choice == "1":
            AddItem()
        elif choice == "2":
            listItems()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Unknown option.\n")

if __name__ == "__main__":
    main()
