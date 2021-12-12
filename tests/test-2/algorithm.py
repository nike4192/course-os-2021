from page import Page
from memory import Memory
from logger import TableLogger


def page_replace_decorator(algorithm_func):
    def tmp(requests, max_size = 10, **kwargs):
        memory = Memory(max_size)
        logger = TableLogger(max_size)

        for (i, request) in enumerate(requests):
            fault_flag = False
            if request in memory:
                for page in memory:
                    if page == request: page.counter += 1
            else:
                request_page = Page(*request)
                if len(memory) < memory.max_size:
                    memory.append(request_page)
                else:
                    algorithm_func(requests, memory, request_page, i, **kwargs)
                    fault_flag = True
            logger.write(request, memory, fault_flag)

        return logger
    return tmp


@page_replace_decorator
def opt(requests, *args, **kwargs):
    memory, request_page, i = args
    max_steps = 0
    target_page = next(iter(memory))
    for page in memory:
        match_flag = False
        for j in range(i, len(requests)):
            if requests[j] == page:
                if j - i > max_steps:
                    max_steps = j - i
                    target_page = page
                break
            elif j == len(requests) - 1:
                match_flag = True
                break
        if match_flag: break
            
    memory.remove(target_page)
    memory.append(request_page)


@page_replace_decorator
def fifo(requests, *args, **kwargs):
    memory, request_page, _ = args
    memory.pop(0)
    memory.append(request_page)


@page_replace_decorator
def lru(requests, *args, **kwargs):
    memory, request_page, i = args
    max_steps = 0
    target_page = next(iter(memory))
    for page in memory:
        for j in range(i):
            if requests[i - j] == page:
                if j > max_steps:
                    max_steps = j
                    target_page = page
                break
            
    memory.remove(target_page)
    memory.append(request_page)


@page_replace_decorator
def nfu(requests, *args, **kwargs):
    memory, request_page, i = args
    min_use_count = min([p.counter for p in memory])
    for page in memory:
        if page.counter == min_use_count:
            memory.remove(page)
            memory.append(request_page)
            break
