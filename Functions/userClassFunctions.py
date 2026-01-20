from .utilityFunctions import *
from .CSVFunctions import nextItemId, readAll, appendRow, overWriteCSV
from user import User
import os
import sys

CSV_User_Path = os.path.join(os.path.dirname(__file__), '../users.csv')
userFields = ["userId", "userName", "password", "role"]

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

def addUser(path, headers):
    row = createUserObject()
    appendRow(row, path, headers)
    print("User created")
    return row

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
            
            return r
    else:
        print("\n Invalid ID \n ")   

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
            print(f"\nLogin successful. Welcome {user.userName} \n")
            return user
        else:
            print("Invalid login attempt, please try again \n")
    print("Excess failed login attempts. Terminating program...")
    sys.exit()

