class InventoryItem:
    def __init__(inventoryItem, itemId, itemName, itemQuantity, unitType, category, dateUpdated, updatedBy):
        
        inventoryItem.itemId = str(itemId) # no validation needed, the programme is in control of this value

        if not itemName.strip(): #ensures name is truthy
            raise ValueError("Please enter a valid string")  
        inventoryItem.itemName = itemName.strip()

        try:
            quantity = int(itemQuantity) #check to see if the value is numeric. If this fails, move to except
            if quantity <= 0:
                print("Quantity must be greater than 0. \n")
                return
        except ValueError: 
            print("Quantity must be a whole number")
            return
        inventoryItem.itemQuantity = itemQuantity.strip()

        if not unitType.strip(): #ensures unitType is truthy
            raise ValueError("Please enter a valid string")  
        inventoryItem.unitType = unitType.strip()

        if not category.strip():
            raise ValueError("Please enter a valid string")
        inventoryItem.category = category.strip()

        inventoryItem.dateUpdated = dateUpdated

        inventoryItem.updatedBy = updatedBy

    def __str__(inventoryItem): #This method dictates what is printed if you just print the object
        return f"{inventoryItem.itemId} {inventoryItem.itemName} {inventoryItem.itemQuantity} {inventoryItem.unitType} {inventoryItem.category} {inventoryItem.dateUpdated} {inventoryItem.updatedBy}"
    
    def to_dict(inventoryItem): #create a dictionary object from class properties
        return {
            "itemId"      : inventoryItem.itemId,
            "itemName"    : inventoryItem.itemName,
            "itemQuantity": inventoryItem.itemQuantity,
            "unitType"    : inventoryItem.unitType,
            "category"    : inventoryItem.category,
            "dateUpdated" : inventoryItem.dateUpdated,
            "updatedBy"   : inventoryItem.updatedBy
        }