import algorithm
from page import Page, PageMode
from utils import make_requests, declension


student_list = [
#   'Добрынин Антон Сергеевич',
    'Дюкин Петр Радиевич',
    'Ермаков Никита Евгеньевич',
    'Ершова Ксения Глебовна',
#   'Зернюков Никита Андреевич'
]

Page.mode = PageMode.LOCAL

max_size = 6
requests = make_requests(student_list)

logger = algorithm.opt(requests, max_size)
logger.print()

print(logger.faults)