#Creates an item class to take advantage of encapsulation, allows repeated use code for multiple objects and internal
#data validation, this approach means that an item object can't be created unless the inputs are correct. toDict method
#allows object to be created as a dictionary, which is convenient for CSV storage

class InventoryItem:
    def __init__(self, itemId, itemName, itemQuantity, category, status, dateUpdated, updatedBy): #init = initialiser. This sets up an objects initial state
        
        self.itemId = str(itemId) # no validation needed, the programme is in control of this value

        if not itemName.strip(): #ensures name is truthy
            raise ValueError("Please enter a valid string for item name \n")  
        self.itemName = itemName.strip()

        try:
            q = int(itemQuantity) #attempts to turn input into an int from string. If it fails, the value is non-numeric
            if q < 0: # We don't want negative quantites entered into the database
                raise ValueError("Quantity must be 0 or greater \n")
        except ValueError: #in the event that the above code fails, raise a ValueError
            raise ValueError("\n Quantity must be a whole number \n")
        self.itemQuantity = itemQuantity.strip()

        if not category.strip():
            raise ValueError("Please enter a valid string for category \n")
        self.category = category.strip()

        if not status.strip():
            raise ValueError("Please enter a valid string for category \n")
        self.status = status.strip()

        self.dateUpdated = dateUpdated #As this is timestamped by a function, validation isn't necessary

        self.updatedBy = updatedBy #similar to above, the program automatically applies this, no risk of user input error

    def __str__(self): #This method dictates what is printed if you just print the object
        return f"{self.itemId} {self.itemName} {self.itemQuantity} {self.category} {self.status} {self.dateUpdated} {self.updatedBy}"
    
    def toDict(self): #create a dictionary object from class properties
        return {
            "itemId"      : self.itemId,
            "itemName"    : self.itemName,
            "itemQuantity": self.itemQuantity,
            "category"    : self.category,
            "status"      : self.status,
            "dateUpdated" : self.dateUpdated,
            "updatedBy"   : self.updatedBy
        }
