import csv
import os

CSV_Path = os.path.join(os.path.dirname(__file__), "inventory.csv")
fields = ["itemId", "name", "quantity", "unitType", "category", "location", "reorderLevel", "reorderQuantity", "dateUpdated", "updatedBy"]

def checkCSV():
    os.makedirs(os.path.dirname(CSV_Path) or ".", exist_ok=True)
    if not os.path.exists(CSV_Path):
        print("Creating CSV file ...")
        with open(CSV_Path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(fields)
            (print("CSV file creation successful"))
    else:
        print("CSV file present")
    
