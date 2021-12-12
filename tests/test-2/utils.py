alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def compare_lists(l1, l2):
    if len(l1) != len(l2):
        return False
    else:
        for (i, v) in enumerate(l1):
            if v != l2[i]:
                return False
    return True

def calculate_sequences(person_list):
    sequences = []
    for person in person_list:
        pieces = person.split(' ')
        n = len(pieces[1])
        sequence = []
        for piece in pieces:
            for char in piece:
                if number := (alphabet.index(char.lower()) + 1) % n:
                    sequence.append(number)
                    
        sequences.append(sequence)
    return sequences
        
def merge_sequences(sequences):
    for i in range(max(map(len, sequences))):
        for j in range(len(sequences)):
            if i < len(sequences[j]):
                yield (j + 1, sequences[j][i])
                
def make_requests(person_list):
    return list(merge_sequences(calculate_sequences(person_list)))

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