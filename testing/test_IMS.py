import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import nextItemId, readAll

CSV_Inventory_Path = os.path.join(os.path.dirname(__file__), "inventory.csv")
CSV_User_Path      = os.path.join(os.path.dirname(__file__), 'testUsers.csv')

inventoryFields = ["itemId","itemName", "itemQuantity", "unitType", "category", "dateUpdated", "updatedBy"]
userFields      = ["userId", "userName", "password", "role"]

def test_nextItemId():
    print(f"Current number of items in file: {len(readAll(CSV_User_Path,userFields))}")
    assert len(readAll(CSV_User_Path,userFields)) == 6
    print(f"Next Id to be assigned: {nextItemId(CSV_User_Path,userFields)}")
    assert nextItemId(CSV_User_Path,userFields)

