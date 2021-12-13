from enum import Enum


class PageMode(Enum):
    GLOBAL = 'global'
    LOCAL = 'local'


class Page:

    mode = PageMode.GLOBAL  # static field

    def __init__(self, ps_num, pg_num):
        self.ps_num = ps_num
        self.pg_num = pg_num
        self.counter = 0

    def __eq__(self, other):
        if isinstance(other, tuple):        
            return self.ps_num == other[0] and self.pg_num == other[1]
        if isinstance(other, Page):
            return self.ps_num == other.ps_num and self.pg_num == other.pg_num
        return False

    def __str__(self):
        return f'{self.ps_num}-{self.pg_num}'
            