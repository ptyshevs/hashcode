class Server:
    def __init__(self, id, size, capacity):
        self.id = id
        self.capacity = capacity
        self.size = size
        self.row = -1
        self.slot = -1
        self.pool = -1
    
    def __repr__(self):
        return "S[{}]: size={}, capacity={}, row={}, slot={} | P[{}]".format(self.id, self.size, self.capacity, self.row, self.slot, self.pool)
    
    def copy(self):
        cpy = Server(self.id, self.size, self.capacity)
        cpy.row = self.row
        cpy.slot = self.slot
        cpy.pool = self.pool
        return cpy