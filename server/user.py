class User:
    """For each connection, a user is created,
    has name, socket client and IP adress
    """
    def __init__(self, addr, client):
        self.addr = addr
        self.client = client
        self.name = None

    def __repr__(self):
        return f"User({self.name}, {self.addr})"

    def set_name(self,name):
        self.name = name

    #def __str__(self):