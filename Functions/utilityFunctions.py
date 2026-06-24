#This is a set of assistance based functions

from tabulate import tabulate
from .CSVFunctions import readAll, overWriteCSV

#helper function to avoid writing .strip() over and over
def promptInput(message):
    return input(message).strip()

#Creates a table to display the CSV contents
def tabulateData(data): 
    try: #this is to protect against an empty csv breaking the program
        col_alignment = ["center"] * len(data[0])
        print(tabulate(data, headers="keys", tablefmt="grid", colalign=col_alignment) + "\n")
    except:
        print("Currently no entries held \n")

#Present the CSV file to user
def listEntries(path, headers):
    print("\n --- All Entries --- \n")
    rows = readAll(path, headers)
    tabulateData(rows)
    
#Delete an item from CSV storage. 
#As this is a generic function rather than specific for user/item, it's placed in utility. If put into a more specific file as is, there will
#be a circular dependancy/import error
#This could be expanded to delete logs too
def deleteEntry(path, headers):
    rows = readAll(path, headers)
    tabulateData(rows)
    
    while True:
        changeId = promptInput("Please specify the ID of the item you would like to delete: ")
        if len(changeId) != 0: #empty input will abort the process
            break
        else:
            print("Invalid input, please try again")
    
    for r in rows:
        itemId = r.get("itemId")
        userId = r.get("userId")

        if itemId and itemId == changeId: #if the itemID is valid/contained within the CSV and is equal to the user input....
            tabulateData([r])
            confirm = promptInput("Are you sure you want to delete this entry? Enter 'y' to confirm, else delete will be aborted.\n")
            if confirm == 'y':
                deletedItem = rows.pop(rows.index(r)) #pop removes based on an index value
                overWriteCSV(rows, path, headers)
                print("Item deleted \n")
                return deletedItem
            else:
                print("Delete aborted \n")
                break

        elif userId == changeId: #to activate this, itemId has been confirmed not present, therefore userId has to be present. No truthy check needed
            tabulateData([r])
            confirm = promptInput("Are you sure you want to delete this entry? Enter 'y' to confirm, else delete will be aborted.\n")
            if confirm == 'y':
                deletedUser = rows.pop(rows.index(r))
                overWriteCSV(rows, path, headers)
                print("User deleted \n")
                return deletedUser
            else:
                print("Delete aborted \n")
                break
    else:
        print("No matching entry found, delete aborted \n")
    
