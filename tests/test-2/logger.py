from page import Page


class Logger:
    def __init__(self):
        self.faults = 0


class TableLogger(Logger):
    def __init__(self, max_size):
        Logger.__init__(self)
        rows = [[''] for i in range(max_size + 2)]
        rows[0][0]  = 'sequence'
        rows[1][0]  = 'memory'
        rows[-1][0] = 'faults'
        self.rows = rows
        self.max_size = max_size
        
    def write(self, request_page, memory, fault_flag):
        rows = self.rows
        rows[0].append(self.cell_format(request_page))
        for (i, page) in enumerate(memory):
            rows[i + 1].append(self.cell_format(page))
        for i in range(len(memory), self.max_size):
            rows[i + 1].append('')
        rows[-1].append('F' if fault_flag else '')
        if fault_flag: self.faults += 1;

    @staticmethod
    def cell_format(cell):
        return \
            cell                           if type(cell) == str   else \
            f'{cell[0]}-{cell[1]}'         if type(cell) == tuple else \
            f'{cell.ps_num}-{cell.pg_num}' if type(cell) == Page  else ''
        
    @staticmethod
    def print_delimeter(sizes):
        print('+' + '+'.join(['-' * size for size in sizes]) + '+') 
        
    def print(self):
        rows = self.rows
        groups = [[rows[0]], rows[1:-1], [rows[-1]]]
        sizes = [max(map(len, column)) for column in zip(*rows)]
        for group in groups:
            self.print_delimeter(sizes)
            for row in group:
                print('|', end='')
                for i, size in enumerate(sizes):
                    output_cell = self.cell_format(row[i])
                    if i == 0:
                        output_cell = output_cell.ljust(size)
                    else:
                        output_cell = output_cell.rjust(size)
                    print(output_cell + '|', end='')
                print()
        self.print_delimeter(sizes)