class Server:
    def __init__(self, id, size, capacity):
        self.id = id
        self.capacity = capacity
        self.size = size
        self.row = -1
        self.slot = -1
    
    def __repr__(self):
        return "S[{}]: size={}, capacity={}, row={}, slot={}".format(self.id, self.size, self.capacity, self.row, self.slot)