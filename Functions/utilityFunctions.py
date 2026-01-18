from tabulate import tabulate
from .CSVFunctions import readAll, overWriteCSV

def promptInput(message): #helper function to avoid writing .strip() over and over
    return input(message).strip()

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

def deleteEntry(path, headers):
    rows = readAll(path, headers)
    tabulateData(rows)
    
    while True:
        changeId = promptInput("Please specify the ID of the item you would like to delete: ")
        if len(changeId) != 0:
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
                rows.pop(rows.index(r)) #pop removes based on an index value
                overWriteCSV(rows, path, headers)
                print("Item deleted \n")
            else:
                print("Delete aborted \n")
                break

        elif userId == changeId: #to activate this, itemId has been confirmed not present, therefor userId has to be present. No truthy check needed
            tabulateData([r])
            confirm = promptInput("Are you sure you want to delete this entry? Enter 'y' to confirm, else delete will be aborted.\n")
            if confirm == 'y':
                rows.pop(rows.index(r))
                overWriteCSV(rows, path, headers)
                print("User deleted \n")
            else:
                print("Delete aborted \n")
                break
    else:
        print("No matching entry found, delete aborted \n")
    