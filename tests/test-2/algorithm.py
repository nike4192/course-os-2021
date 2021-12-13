from page import Page, PageMode
from memory import Memory
from logger import TableLogger


def page_replace_decorator(algorithm_func):
    def tmp(requests, max_size = 10, **kwargs):
        memory = Memory(max_size)
        logger = TableLogger(max_size)

        kwargs = {'strict': False, **kwargs}

        for (i, request) in enumerate(requests):
            target_page = None
            fault_flag = False
            if request in memory:
                for page in memory:
                    if page == request: page.counter += 1
            else:
                request_page = Page(*request)
                if len(memory) < memory.max_size:
                    memory.append(request_page)
                else:
                    target_page = algorithm_func(requests, memory, request_page, i, **kwargs)
                    fault_flag = True
            logger.write(request, memory, fault_flag, target_page)

        return logger
    return tmp


@page_replace_decorator
def opt(requests, *args, **kwargs):
    memory, request_page, i = args
    max_steps = 0
    target_page = None if kwargs['strict'] else next(iter(memory))
    for page in memory:

        if Page.mode == PageMode.LOCAL and \
            page.ps_num != request_page.ps_num:
            continue

        if i == len(requests) - 1:  # Last request
            target_page = page
            break

        match_flag = False
        for j in range(i, len(requests)):
            if requests[j] == page:
                if j - i > max_steps:
                    max_steps = j - i
                    target_page = page
                break
            elif j == len(requests) - 1:
                match_flag = True
                target_page = page
                break
        if match_flag: break

    if target_page is None:
        raise Exception('Not found target page')
            
    memory.replace_with(target_page, request_page)
    return target_page


@page_replace_decorator
def fifo(requests, *args, **kwargs):
    memory, request_page, _ = args
    target_page = None if kwargs['strict'] else next(iter(memory))
    for page in memory:

        if Page.mode == PageMode.LOCAL and \
            page.ps_num != request_page.ps_num:
            continue

        target_page = page
        break

    if target_page is None:
        raise Exception('Not found target page')

    memory.remove(target_page)
    memory.append(request_page)
    return target_page


@page_replace_decorator
def lru(requests, *args, **kwargs):
    memory, request_page, i = args
    max_steps = 0
    target_page = None if kwargs['strict'] else next(iter(memory))
    for page in memory:

        if Page.mode == PageMode.LOCAL and \
            page.ps_num != request_page.ps_num:
            continue

        for j in range(i):
            if requests[i - j] == page:
                if j > max_steps:
                    max_steps = j
                    target_page = page
                break

    if target_page is None:
        raise Exception('Not found target page')
            
    memory.replace_with(target_page, request_page)
    return target_page


@page_replace_decorator
def nfu(requests, *args, **kwargs):
    memory, request_page, i = args
    target_page = None if kwargs['strict'] else next(iter(memory))

    min_use_count = float('Inf')
    for page in memory:

        if Page.mode == PageMode.LOCAL and \
            page.ps_num != request_page.ps_num:
            continue

        if page.counter < min_use_count:
            min_use_count = page.counter
            target_page = page

    if target_page is None:
        raise Exception('Not found target page')

    memory.replace_with(target_page, request_page)
    return target_page
