import csv
import os
import sys
from datetime import datetime
from item import InventoryItem
from user import User
from tabulate import tabulate #python -m pip install tabulate

CSV_Inventory_Path = os.path.join(os.path.dirname(__file__), "inventory.csv")
CSV_User_Path      = os.path.join(os.path.dirname(__file__), 'users.csv')

inventoryFields = ["itemId","itemName", "itemQuantity", "unitType", "category", "dateUpdated", "updatedBy"]
userFields      = ["userId", "userName", "password", "role"]

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
    rows = readAll(path, headers) 
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

def promptInput(message): #helper function to avoid writing .strip() over and over
    return input(message).strip()

def appendRow(row, path, headers): #Adds a new entry to the bottom of the CSV file
    checkCSV(path, headers)
    with open(path, "a", newline="", encoding="utf-8") as f: #a = append
        w = csv.DictWriter(f, fieldnames=headers) #allows you to write dictionaries directly to a csv file
        w.writerow(row)
    
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

def createUserObject(): #Creates an instance of the User class, giving access to class methods
    while True:
        userId   = nextItemId(CSV_User_Path, userFields)
        userName = promptInput("User name: ")
        password = promptInput("Password: ")
        role     = promptInput("Role: ")

        try:
            newUser = User(userId, userName, password, role)

            print(newUser.toDict())
            print("User Created \n")

            return newUser.toDict()
        
        except ValueError as e:
            print(f"\n User creation failed: {e}")

def addItem(path, headers, user): #Create an object, takes in user details, adds it to CSV file
    row = createItemObject(user)
    appendRow(row, path, headers)
    print("Item added \n")

def addUser(path, headers):
    row = createUserObject()
    appendRow(row, path, headers)
    print("User created")

def tabulateData(data): #Creates a table to display the CSV contents
    try: #this is to protect against an empty csv breaking the code
        col_alignment = ["center"] * len(data[0])
        print(tabulate(data, headers="keys", tablefmt="grid", colalign=col_alignment) + "\n")
    except:
        print("Currently no entries held \n")

def listEntries(path, headers): #Present the CSV file to user
    print("\n --- All Entries --- \n")
    rows = readAll(path, headers)
    tabulateData(rows)

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

def searchUsers(path, headers):
    print("\n --- Search Users --- \n")
    term = promptInput("Enter search term (userName or role): ").lower()
    if not term:
        print("Empty search term \n")
        return

    rows = readAll(path, headers)
    results = []
    for r in rows:
        combined = (r.get('userName','') + ' ' + r.get('role','')).lower()
        if term in combined:
            results.append(r)
    if not results:
        print ("No matches found")
        return
    tabulateData(results)

def overWriteCSV(rows, path, headers): #Allows edits to be made to the CSV file without having to delete and re-create it
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

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
                        r["dateUpdated"] = datetime.now().strftime("%Y-%m-%d") #Timestamps when the item was changed, for auditability
                        r["updatedBy"] = currentlyLoggedIn.userName #Attaches username to the item update, for auditability
                    case "2":
                        r["itemQuantity"] = promptInput("Please enter the new value: ")
                        r["dateUpdated"] = datetime.now().strftime("%Y-%m-%d")
                        r["updatedBy"] = currentlyLoggedIn.userName
                    case "3":
                        r["unitType"] = promptInput("Please enter the new value: ")
                        r["dateUpdated"] = datetime.now().strftime("%Y-%m-%d")
                        r["updatedBy"] = currentlyLoggedIn.userName
                    case "4":
                        r["category"] = promptInput("Please enter the new value: ")
                        r["dateUpdated"] = datetime.now().strftime("%Y-%m-%d")
                        r["updatedBy"] = currentlyLoggedIn.userName
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

def updateUser(path, headers):
    rows = readAll(path, headers)
    tabulateData(rows)
    changeId = promptInput("Please specify the ID of the user you would like to change: ")

    for r in rows:
        if r["userId"] == changeId:
            tabulateData([r])
            
            while True:
                print("Please choose the property to update:")
                print("1) userName")
                print("2) password")
                print("3) role")
                print("4) exit")
                changeProperty = promptInput("\n Choose (1/2/3): \n")

                match changeProperty:
                    case "1":
                        r["userName"] = promptInput("Please enter the new value: ")
                        print(f"userName changed to {r["userName"]}")
                    case "2":
                        r["password"] = promptInput("Please enter the new value: ")
                        print(f"password changed to {r["password"]}")
                    case "3":
                        r["role"] = promptInput("Please enter the new value: ")
                        print(f"role changed to {r["role"]}")
                    case "4":
                        break
                    case _:
                        print("Please enter a valid choice")
                        continue 

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
        itemId = r.get("itemId")
        userId = r.get("userId")

        if itemId and itemId == changeId: #if the itemID is valid/contained within the CSV and is equal to the user input....
            tabulateData([r])
            confirm = promptInput("Are you sure you want to delete this entry? Enter 'y' to confirm.\n")
            if confirm == 'y':
                rows.pop(rows.index(r)) #pop removes based on an index value
                overWriteCSV(rows, path, headers)
                print("Item deleted \n")
            else:
                print("Delete aborted \n")

        elif userId == changeId: #to activate this, itemId has been confirmed not present, therefor userId has to be present. No truthy check needed
            tabulateData([r])
            confirm = promptInput("Are you sure you want to delete this entry? Enter 'y' to confirm.\n")
            if confirm == 'y':
                rows.pop(rows.index(r))
                overWriteCSV(rows, path, headers)
                print("User deleted \n")
            else:
                print("Delete aborted \n")
        else:
                print("Invalid choice, delete aborted \n")
                break
         

def authenticate(username, password):

    if username == "" and password == "": #establishes a default account with read access
        return User(0, "guest", "guest", "read")

    rows = readAll(CSV_User_Path, userFields)
    for r in rows:
        if r.get("userName") == username and r.get("password") == password:
            return User(r["userId"], r["userName"], r["password"], r["role"])
        
    return None   

def loginLoop():
    count = 0
    while count < 3:
        print("Press enter for username and password to log in as a guest")
        count += 1
        username = promptInput("Enter username: ")
        password = promptInput("Enter password: ")

        user = authenticate(username, password)
        if user:
            print(f"\n Login successful. Welcome {user.userName}")
            return user
        else:
            print("Invalid login attempt, please try again \n")
    print("Excess failed login attempts. Terminating program...")
    sys.exit()

def main():
    checkCSV(CSV_Inventory_Path, inventoryFields)
    checkCSV(CSV_User_Path, userFields)
    currentlyLoggedIn = loginLoop()

    while True:

        match currentlyLoggedIn.role:
            
            case "read":
                currentlyLoggedIn.displayRights()
                choice = promptInput("\n Choose (1/2/3): ")

                match choice:
                    case "1":
                        listEntries(CSV_Inventory_Path, inventoryFields)
                    case "2":
                        searchItems(CSV_Inventory_Path, inventoryFields)
                    case "3":
                        print("Goodbye!")
                        currentlyLoggedIn = None
                        break
                    case _:
                        print("Invalid choice")
            case "write":
                currentlyLoggedIn.displayRights()
                choice = promptInput("\n Choose (1/2/3/4/5): ")

                match choice:
                    case "1":
                        listEntries(CSV_Inventory_Path, inventoryFields)
                    case "2":
                        searchItems(CSV_Inventory_Path, inventoryFields)
                    case "3":
                        addItem(CSV_Inventory_Path, inventoryFields, currentlyLoggedIn)
                    case "4":
                        updateItem(CSV_Inventory_Path, inventoryFields, currentlyLoggedIn)
                    case "5":
                        print("Goodbye!")
                        currentlyLoggedIn = None
                        break
                    case _:
                        print("Invalid choice")
            case "admin":
                currentlyLoggedIn.displayRights()
                choice = promptInput("\n Choose (1/2/3/4/5/6/7/8/9/10/11): ")

                match choice:
                    case "1":
                        listEntries(CSV_Inventory_Path, inventoryFields)
                    case "2":
                        searchItems(CSV_Inventory_Path, inventoryFields)
                    case "3":
                        addItem(CSV_Inventory_Path, inventoryFields, currentlyLoggedIn)
                    case "4":
                        updateItem(CSV_Inventory_Path, inventoryFields, currentlyLoggedIn)
                    case "5":
                        deleteEntry(CSV_Inventory_Path, inventoryFields)
                    case "6":
                        listEntries(CSV_User_Path, userFields)
                    case "7":
                        searchUsers(CSV_User_Path, userFields)
                    case "8":
                        addUser(CSV_User_Path, userFields)
                    case "9":
                        updateUser(CSV_User_Path, userFields)
                    case "10":
                        deleteEntry(CSV_User_Path, userFields)
                    case "11":
                        print("Goodbye!")
                        currentlyLoggedIn = None
                        break
                    case _:
                        print("Invalid choice")

if __name__ == "__main__":
    main()