from utils import make_requests, calculate_sequences, merge_sequences, compare_lists

test_person_list = [
    'Васильев Аркадий Владимирович',
    'Иванов Петр Сергеевич',
    'Миронов Андрей Вячеславович'
]

test_sequences = [
    [3, 1, 5, 3, 6, 2, 6, 3, 1, 4, 5, 1, 5, 3, 4, 3, 6, 1, 5, 3, 3, 4, 2, 3, 3, 4],
    [2, 3, 1, 3, 3, 1, 2, 2, 3, 2, 2, 2, 2, 3, 2, 1],
    [2, 4, 4, 3, 4, 3, 1, 3, 5, 5, 3, 3, 1, 1, 1, 1, 3, 4, 3, 4, 1]
] #                                                     ^ In pdf document 2 is wrong

test_sequence = [
    (1, 3), (2, 2), (3, 2), (1, 1), (2, 3), (3, 4), (1, 5), (2, 1), (3, 4), (1, 3), (2, 3), (3, 3), (1, 6), (2, 3), (3, 4), (1, 2), (2, 1), (3, 3), (1, 6), (2, 2), (3, 1), (1, 3), (2, 2), (3, 3), (1, 1), (2, 3), (3, 5), (1, 4), (2, 2), (3, 5), (1, 5), (2, 2), (3, 3), (1, 1), (2, 2), (3, 3), (1, 5), (2, 2), (3, 1), (1, 3), (2, 3), (3, 1), (1, 4), (2, 2), (3, 1), (1, 3), (2, 1), (3, 1), (1, 6), (3, 3), (1, 1), (3, 4), (1, 5), (3, 3), (1, 3), (3, 4), (1, 3), (3, 1), (1, 4), (1, 2), (1, 3), (1, 3), (1, 4)
] #                                                                                                                                                                                                                                                                                                                                                                                                                             ^ In pdf 2 is wrong

check_sequences = calculate_sequences(test_person_list)  # person_list -> sequences
result_1 = all([compare_lists(l1, l2) for l1, l2 in zip(test_sequences, check_sequences)])
print('Test calculate sequences:', 'OK' if result_1 else 'ERROR')

check_sequence = list(merge_sequences(test_sequences))  # sequences -> sequence
result_2 = compare_lists(test_sequence, check_sequence)
print('Test merge sequences:', 'OK' if result_2 else 'ERROR')

check_make_sequence = make_requests(test_person_list)  # person_list -> sequence
result_3 = compare_lists(test_sequence, check_make_sequence)
print('Test make sequence:', 'OK' if result_3 else 'ERROR')
