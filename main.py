from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    pprint(contacts_list)


def standardize_name(rows):
    result = [tuple(' '.join(person[0:3]).split(' ')[0:3] + person[3:7]) for person in rows]
    return result


def eliminate_duplicates(correct_name_list):
    no_duplicates = []
    seen_names = set()

    for compared in correct_name_list:
        name_tuple = tuple(compared[0:2])  # Преобразуем первые два элемента в кортеж
        if name_tuple not in seen_names:
            no_duplicates.append(compared)
            seen_names.add(name_tuple)

    return no_duplicates


def unify_phone(rows, regular, new):
    pattern = re.compile(regular)
    phonebook = [[pattern.sub(new, string) for string in strings] for strings in rows]
    return phonebook


correct_name_list = standardize_name(contacts_list)
no_duplicates_list = eliminate_duplicates(correct_name_list)
regular = r'(\+7|8)+[\s(]*(\d{3,3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})'
correct_list = unify_phone(no_duplicates_list, regular, r'+7(\2)\3-\4-\5')
regular_2 = r'(\+7|8)+[\s(]*(\d{3,3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})[\s]*[(доб.\s]*(\d+)[)]*'
correct_phonebook = unify_phone(correct_list, regular_2, r'+7(\2)\3-\4-\5 доб.\6')

with open("phonebook.csv", "w", encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(correct_phonebook)