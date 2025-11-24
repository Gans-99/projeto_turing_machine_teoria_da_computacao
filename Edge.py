class Edge:
    def __init__(self, read, write=None, move=None):
        self.read = read
        self.write = write
        self.move = move

    def getC(self):
        return self.read

    def getWrite(self):
        return self.write

    def getMove(self):
        return self.move

    @staticmethod
    def instance(read, write=None, move=None):
        return Edge(read, write, move)

    def equals(self, o):
        if isinstance(o, Edge):
            return self.read == o.read
        return False

    def __repr__(self):
        return f'[{self.read},{self.write},{self.move}]'
