class Server:
    def __init__(self, id, capacity, size):
        self.id = id
        self.capacity = capacity
        self.size = size
        self.row = -1
        self.slot = -1