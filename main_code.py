import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f, open("phonebook.csv", "w", encoding="utf-8", newline='') as res:
    contacts_list = list(csv.reader(f, delimiter=","))
    headers = contacts_list.pop(0)                                  # Сохранить заголовки в отдельную переменную
    new_list = [' '.join(row[0:3]).split() for row in contacts_list]  # Разделить ФИО и добавить в новый список
    name_dict = {}
    for i in range(len(new_list)):                                  # Добавить к ФИО остальные данные
        new_list[i].extend(contacts_list[i][3:])
        k = tuple(new_list[i][:2])
        name_dict.setdefault(k, []).extend(new_list[i][2:])         # Объединить записи об одних и тех же людях

    res_list = [[*k, *list(dict.fromkeys(v))] for k, v in name_dict.items()]
    for row in res_list:                                            # Распределить по своим ячейкам телефон, email
        if '@' not in row[-1]:
            if len(row) == 7:
                a = row.pop(6)
                row[4] = a
            row.append('')

    pattern = re.compile(r'(\+7|8)\s*\(*(\d{3})\)*\s*-*(\d{3})-*(\d{2})-*(\d{2})\s*\(*(доб\.)*\s*(\d*)\)*')
    subst_pattern = r'+7(\2)\3-\4-\5 \6\7'
    for row in res_list:                                             # Привести номера к единому формату
        result = pattern.sub(subst_pattern, row[5])
        row[5] = result.rstrip()

    datawriter = csv.writer(res, delimiter=',')                  # Запись заголовков и списка контактов в новый csv файл
    datawriter.writerow(headers)
    datawriter.writerows(res_list)


