class User:
    def __init__(self, userName, password, role):
        self.userName = userName
        self.password = password
        self.role = role

    def displayRights(self):
        print(f"Access rights for: {self.userName} ({self.role})")

        match self.role:
            case "basic":
                print("1) List items")
                print("2) Search items")
            case "writeAccess":
                print("1) List items")
                print("2) Search items")
                print("3) Add items")
                print("4) Update items")
            case "admin":
                print("1) List items")
                print("2) Search items")
                print("3) Add items")
                print("4) Update items")
                print("5) Delete items")
                print("6) List users")
                print("7) Create users")
                print("8) Update users")
                print("9) Delete users")
            case _:
                print("Unknown user role")
