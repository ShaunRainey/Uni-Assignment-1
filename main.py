import os
from Functions.CSVFunctions import *
from Functions.utilityFunctions import *
from Functions.userClassFunctions import *
from Functions.itemClassFunctions import *
from Functions.loggingFunctions import *
from Functions.warningFunctions import *

def main():
    checkCSV(CSV_Inventory_Path, inventoryFields)
    checkCSV(CSV_User_Path, userFields)
    checkCSV(CSV_Logging_Path, logFields)

    currentlyLoggedIn = loginLoop()
    addLog(CSV_Logging_Path, logFields, currentlyLoggedIn, 7)

    warnings = getWarnings(CSV_Inventory_Path, inventoryFields)
    warningAlert(warnings)

    while True:

        match currentlyLoggedIn.role:
            
            case "read":
                currentlyLoggedIn.displayRights()
                choice = promptInput("\n Choose (1/2/3/4): ")

                match choice:
                    case "1":
                        listEntries(CSV_Inventory_Path, inventoryFields)
                    case "2":
                        searchItems(CSV_Inventory_Path, inventoryFields)
                    case "3":
                        warnings = getWarnings(CSV_Inventory_Path, inventoryFields)
                        tabulateWarnings(warnings)
                    case "4":
                        print("Goodbye!")
                        addLog(CSV_Logging_Path, logFields, currentlyLoggedIn, 8)
                        currentlyLoggedIn = None
                        break
                    case _:
                        print("Invalid choice")
            case "write":
                currentlyLoggedIn.displayRights()
                choice = promptInput("\n Choose (1/2/3/4/5/6): ")

                match choice:
                    case "1":
                        listEntries(CSV_Inventory_Path, inventoryFields)
                    case "2":
                        searchItems(CSV_Inventory_Path, inventoryFields)
                    case "3":
                        addItem(CSV_Inventory_Path, inventoryFields, currentlyLoggedIn)
                        addLog(CSV_Logging_Path, logFields, currentlyLoggedIn, 1)
                    case "4":
                        updateItem(CSV_Inventory_Path, inventoryFields, currentlyLoggedIn)
                    case "5":
                        warnings = getWarnings(CSV_Inventory_Path, inventoryFields)
                        tabulateWarnings(warnings)
                    case "6":
                        print("Goodbye!")
                        addLog(CSV_Logging_Path, logFields, currentlyLoggedIn, 8)
                        currentlyLoggedIn = None
                        break
                    case _:
                        print("Invalid choice")
            case "admin":
                currentlyLoggedIn.displayRights()
                choice = promptInput("\n Choose (1/2/3/4/5/6/7/8/9/10/11/12/13): ")

                match choice:
                    case "1":
                        listEntries(CSV_Inventory_Path, inventoryFields)
                    case "2":
                        searchItems(CSV_Inventory_Path, inventoryFields)
                    case "3":
                        newItem = addItem(CSV_Inventory_Path, inventoryFields, currentlyLoggedIn)
                        addLog(CSV_Logging_Path, logFields, currentlyLoggedIn, 1, newItem)
                    case "4":
                        updatedItem = updateItem(CSV_Inventory_Path, inventoryFields, currentlyLoggedIn)
                        addLog(CSV_Logging_Path, logFields, currentlyLoggedIn, 2, updatedItem)
                    case "5":
                        deletedItem = deleteEntry(CSV_Inventory_Path, inventoryFields)
                        addLog(CSV_Logging_Path, logFields, currentlyLoggedIn, 3, deletedItem)
                    case "6":
                        listEntries(CSV_User_Path, userFields)
                    case "7":
                        searchUsers(CSV_User_Path, userFields)
                    case "8":
                        newUser = addUser(CSV_User_Path, userFields)
                        addLog(CSV_Logging_Path, logFields, currentlyLoggedIn, 4, newUser)
                    case "9":
                        updatedUser = updateUser(CSV_User_Path, userFields)
                        addLog(CSV_Logging_Path, logFields, currentlyLoggedIn, 5, updatedUser)
                    case "10":
                        deletedUser = deleteEntry(CSV_User_Path, userFields)
                        addLog(CSV_Logging_Path, logFields, currentlyLoggedIn, 6, deletedUser)
                    case "11":
                        listEntries(CSV_Logging_Path, logFields)
                    case "12":
                        warnings = getWarnings(CSV_Inventory_Path, inventoryFields)
                        tabulateWarnings(warnings)
                    case "13":
                        print("Goodbye!")
                        addLog(CSV_Logging_Path, logFields, currentlyLoggedIn, 8)
                        currentlyLoggedIn = None
                        break
                    case _:
                        print("Invalid choice")

if __name__ == "__main__":
    main()