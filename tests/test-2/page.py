from enum import Enum

class PageMode(Enum):
    GLOBAL = 'global'
    LOCAL = 'local'

class Page:
    mode = PageMode.GLOBAL

    def __init__(self, ps_num, pg_num):
        self.ps_num = ps_num
        self.pg_num = pg_num
        self.counter = 0

    def __eq__(self, other):
        if isinstance(other, tuple):        
            if self.mode == PageMode.LOCAL:
                return self.ps_num == other[0] and self.pg_num == other[1]
            else:
                return self.pg_num == other[1]
        if self.mode == PageMode.LOCAL:
            return self.ps_num == other.ps_num and self.pg_num == other.pg_num
        else:
            return self.pg_num == other.pg_num

    def __str__(self):
        return f'{self.ps_num}-{self.pg_num}'
            