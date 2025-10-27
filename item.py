class InventoryItem:
    def __init__(self, itemId, itemName, itemQuantity, unitType, category, dateUpdated, updatedBy):
        
        self.itemId = str(itemId) # no validation needed, the programme is in control of this value

        if not itemName.strip(): #ensures name is truthy
            raise ValueError("Please enter a valid string for item name \n")  
        self.itemName = itemName.strip()

        try:
            q = int(itemQuantity)
            if q <= 0:
                raise ValueError("Quantity must be 0 or greater \n")
        except ValueError:
            raise ValueError("\n Quantity must be a whole number \n")
        self.itemQuantity = itemQuantity.strip()

        if not unitType.strip(): #ensures unitType is truthy
            raise ValueError("Please enter a valid string for unit type \n")  
        self.unitType = unitType.strip()

        if not category.strip():
            raise ValueError("Please enter a valid string for category \n")
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
