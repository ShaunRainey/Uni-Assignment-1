import os
import csv

CSV_User_Path = os.path.join(os.path.dirname(__file__), '../users.csv')
userFields = ["userId", "userName", "password", "role"]

CSV_Inventory_Path = os.path.join(os.path.dirname(__file__), "../inventory.csv")
inventoryFields = ["itemId","itemName", "itemQuantity", "unitType", "category", "dateUpdated", "updatedBy"]

def checkCSV(path, headers):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    if not os.path.exists(path): # if the file doesn't exist, create it
        print("Creating CSV storage file ...")
        with open(path, "w",newline="", encoding="utf-8") as f: #as f gives a name to the object returned by open(), it's effectively a file handle
            csv.writer(f).writerow(headers) #write the desired headers to the file handle
            (print("CSV storage file creation successful \n"))

def readAll(path, headers): #loads the contents of csv file into a variable for use
    checkCSV(path, headers)
    with open(path, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f)) #creates a list containing dictionarys of the objects held in the CSV file
    
def nextItemId(path, headers): #Allows Id to increment with each addition
    rows = readAll(path, headers) #Rows is a list containing dictionaries
    maxId = 0

    for r in rows: #iterate though each row
        itemId = r.get("itemId") #depending on the csv path, there will only be one of these 2 variables. If not using r.get, the system will crash
        userId = r.get("userId")
        try:
            if(itemId):
                maxId = max(maxId, int(r.get("itemId", "0") or "0"))
            elif(userId):
                maxId = max(maxId, int(r.get("userId", "0") or "0"))
        except ValueError:
            pass
    return str(maxId +1)
    
def appendRow(row, path, headers): #Adds a new entry to the bottom of the CSV file
    checkCSV(path, headers)
    with open(path, "a", newline="", encoding="utf-8") as f: #a = append
        w = csv.DictWriter(f, fieldnames=headers) #allows you to write dictionaries directly to a csv file
        w.writerow(row)

def overWriteCSV(rows, path, headers): #Allows edits to be made to the CSV file without having to delete and re-create it
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)