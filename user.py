class User:

    validRoles = ["admin", "write", "read"]

    def __init__(self, userId, userName, password, role):
        self.userId = str(userId)

        if not userName.strip(): #ensures name is truthy
            raise ValueError("Please enter a valid string for user name \n")  
        self.userName = userName.strip()

        if not password.strip(): #ensures name is truthy
            raise ValueError("Please enter a valid string for password \n")  
        self.password = password.strip()

        role = role.lower().strip()
        if role not in User.validRoles:
            raise ValueError(f"Invalid role, please enter 'admin', 'write' or 'read'")
        self.role = role

    def __str__(self): #This method dictates what is printed if you just print the object
        return f"{self.userId} {self.userName} {self.password} {self.role}"

    def displayRights(self):
        print(f"Access rights for: {self.userName} ({self.role})")
        print("\n What would you like to do? \n")
        match self.role:
            case "read":
                print("1) List items")
                print("2) Search for an item")
                print("3) Exit programme")
            case "write":
                print("1) List items")
                print("2) Search for an item")
                print("3) Add item")
                print("4) Update items")
                print("5) Exit programme")
            case "admin":
                print("1)  List items")
                print("2)  Search for an item")
                print("3)  Add item")
                print("4)  Update item")
                print("5)  Delete item") 
                print("6)  List users")
                print("7)  Search for a user") 
                print("8)  Create user") 
                print("9)  Update user") 
                print("10) Delete user") 
                print("11) Exit programme")
            case _:
                print("Unknown user role")

    def toDict(self): #create a dictionary object from class properties
        return {
            "userId"   : self.userId,
            "userName" : self.userName,
            "password" : self.password,
            "role"     : self.role
        }
    
    def fromDict(cls, data): #cls = class. Effectively takes information and structures it to the class blueprint. Maintains all validation from the class
        return cls( #this method takes a dictionary, and creates an InventoryItem object
            userId   = data["userId"],
            userName = data["userName"],
            password = data["password"],
            role     = data["role"]
        )
