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


Page.mode = PageMode.GLOBAL
alg_name = 'nfu'
strict = False

max_size = 10
requests = make_requests(student_list)

logger = getattr(algorithm, alg_name)(requests, max_size, strict=True)

print(Page.mode.value.title(), alg_name, ('nostrict', 'strict')[strict])
logger.print()

print(logger.faults)
