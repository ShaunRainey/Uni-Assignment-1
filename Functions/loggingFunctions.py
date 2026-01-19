import os
from .CSVFunctions import checkCSV, nextItemId, appendRow
from .utilityFunctions import promptInput
from datetime import datetime

CSV_Logging_Path = os.path.join(os.path.dirname(__file__), '../log.csv')
logFields = ["logId", "userName", "action", "message", "timeStamp"]

def createLog(user, actionCode, target=None):
    actionOptions = {
        1: "add item",
        2: "update item",
        3: "delete item",
        4: "add user",
        5: "update user",
        6: "delete user",
        7: "logged in",
        8: "logged out",
        9: "low stock warning"
        }

    logId     = nextItemId(CSV_Logging_Path, logFields)
    userName  = user.userName
    action    = actionOptions[actionCode]
    message   = messageBuilder(userName, actionCode, target)
    timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    newLog = {"logId":logId, "userName":userName, "action":action, "message": message, "timeStamp":timeStamp}

    return newLog

def addLog(path, headers, user, actionCode, target=None):
    row = createLog(user, actionCode, target)
    appendRow(row, path, headers)
    print("Log added \n")

def messageBuilder(userName, actionCode, target=None):

    message = ""
    
    match actionCode:
        case 1:
            message = f"{userName} has added {target["itemQuantity"]} unit/s of \"{target["itemName"]}\""
        case 2:
            message = f"{userName} has updated itemId: {target["itemQuantity"]}"
        case 3:
            message = f"{userName} has deleted itemId: {target["itemQuantity"]}, {target["itemName"]}"
        case 4:
            message = f"{userName} has added user {target["userName"]}, with {target["role"]} rights"
        case 5:
            message = f"{userName} has updated userId: {target["userId"]}"
        case 6:
            message = f"{userName} has deleted userId: {target["userId"]}, {target["userName"]}"
        case 7:
            message = f"{userName} has logged in"
        case 8:
            message = f"{userName} has logged out"
        case 9:
            pass
    
    return message
    


