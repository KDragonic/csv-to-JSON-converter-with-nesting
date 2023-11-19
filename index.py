import csv
import copy
import json


def csv_to_json(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data

default_template = {}

def create_all_keys(data):
    result = []
    for item in data:
        for key in item.keys():
            if key not in result:
                result.append(key)
    return result

def create_default_template(data):
    result = {}
    for item in create_all_keys(data):
        if "--" in item:
            key, value = item.split("--")
            if key not in result:
                result[key] = {}
        else:
            result[item] = None

    return result

def convert_to_nested_dict(prods):
    result = {}
    for prod in prods:
        name = prod['name']
        if name not in result:
            result[name] = copy.deepcopy(default_template)

        not_use_item = []

        for prod_key, prod_value in prod.items():
            if prod_key in not_use_item:
                continue

            keys : list = prod_key.split("--")
            keys_count = len(keys)
            if keys_count == 1: key_1 = keys[0]
            if keys_count == 2: key_1, key_2 = keys
            # if keys_count == 3: key_3 = keys[2]

            if keys_count == 1:
                result[name][key_1] = prod_value


            # Но key mode (Вместо dict будет простой list)
            if keys_count == 2:

                under_obj = {}

                under_keys = [str.replace(key, key_1 + "--", "") for key in prod.keys() if key.find(key_1 + "--") > -1]
                under_keys.sort()

                is_empty = True

                for key in under_keys:
                    full_key = f"{key_1}--{key}"
                    under_obj[key] = prod[full_key]
                    if len(prod[full_key]) != 0:
                        is_empty = False

                    not_use_item.append(full_key)

                if not is_empty:
                    merged_value = ".".join(under_obj.values())

                    if merged_value not in result[name][key_1].keys():
                        result[name][key_1][merged_value] = list(under_obj.values())

    return result


def save_as_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)




obj_dict = csv_to_json('eparkt.csv')
save_as_json(obj_dict, 'result.json')

default_template = create_default_template(obj_dict)

obj_nested_dict = convert_to_nested_dict(obj_dict)
save_as_json(obj_nested_dict, 'result_2.json')
