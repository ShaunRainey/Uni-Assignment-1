import os
from Functions.CSVFunctions import *
from Functions.utilityFunctions import *
from Functions.userClassFunctions import *
from Functions.itemClassFunctions import *

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