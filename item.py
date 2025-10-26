class InventoryItem:
    def __init__(self, itemId, itemName, itemQuantity, unitType, category, dateUpdated, updatedBy):
        
        self.itemId = str(itemId) # no validation needed, the programme is in control of this value

        if not itemName.strip(): #ensures name is truthy
            raise ValueError("Please enter a valid string")  
        self.itemName = itemName.strip()

        try:
            quantity = int(itemQuantity) #check to see if the value is numeric. If this fails, move to except
            if quantity <= 0:
                print("Quantity must be greater than 0. \n")
                return
        except ValueError: 
            print("Quantity must be a whole number")
            return
        self.itemQuantity = itemQuantity.strip()

        if not unitType.strip(): #ensures unitType is truthy
            raise ValueError("Please enter a valid string")  
        self.unitType = unitType.strip()

        if not category.strip():
            raise ValueError("Please enter a valid string")
        self.category = category.strip()

        self.dateUpdated = dateUpdated

        self.updatedBy = updatedBy

    def __str__(inventoryItem): #This method dictates what is printed if you just print the object
        return f"{inventoryItem.itemId} {inventoryItem.itemName} {inventoryItem.itemQuantity} {inventoryItem.unitType} {inventoryItem.category} {inventoryItem.dateUpdated} {inventoryItem.updatedBy}"
    
    def toDict(inventoryItem): #create a dictionary object from class properties
        return {
            "itemId"      : inventoryItem.itemId,
            "itemName"    : inventoryItem.itemName,
            "itemQuantity": inventoryItem.itemQuantity,
            "unitType"    : inventoryItem.unitType,
            "category"    : inventoryItem.category,
            "dateUpdated" : inventoryItem.dateUpdated,
            "updatedBy"   : inventoryItem.updatedBy
        }
    
    def fromDict(cls, data): #cls = class. Effectively takes information and structures it to the class blueprint. Maintains all validation from the class
        return cls( #this method takes a dictionary, and creates an InventoryItem object
            itemId       = data["itemId"],
            itemName     = data["itemName"],
            itemQuantity = data["itemQuantity"],
            unitType     = data["unitType"],
            category     = data["category"],
            dateUpdated  = data["dateUpdated"],
            updatedBy    = data["updatedBy"]
        )
