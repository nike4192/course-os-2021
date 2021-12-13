
class Memory(list):
    def __init__(self, max_size):
        self.max_size = max_size

    def replace_with(self, replaced, new):
        ind = self.index(replaced)
        if ind != -1: self[ind] = new
