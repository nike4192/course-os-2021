from itertools import zip_longest


alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def compare_lists(l1, l2):
    if len(l1) != len(l2):
        return False
    else:
        for (i, v) in enumerate(l1):
            if v != l2[i]:
                return False
    return True


def calculate_sequence(person):
    sequence = []
    pieces = person.split(' ')
    n = len(pieces[1])
    for piece in pieces:
        for char in piece:
            number = (alphabet.index(char.lower()) + 1) % n
            if number: sequence.append(number)
            
    return sequence


def gen_sequences(person_list):
    for person in person_list:
        yield calculate_sequence(person)


def gen_requests(sequences):
    for column in zip_longest(*sequences):
        for i, c in enumerate(column):
            if c: yield (i + 1, c)


def make_requests(person_list):
    return list(gen_requests(gen_sequences(person_list)))


def declension(number, endings):
    number = number % 100
    if number in range(11, 20):
        return endings[2]
    else:
        i = number % 10
        return \
            endings[0] if i == 1 else \
            endings[1] if i in range(2, 5) else \
            endings[2]

def declension_faults(number):
    return 'промах' + declension(number, ['', 'а', 'ов'])
