import json
import re

from parser_api.models import Product


def string_to_integer(string):
    return int(re.findall(r'\d+', string)[0])


def string_to_float(string):
    return float(re.findall(r'\d+\.\d+|\d+', string)[0])


def represent_string(string):
    try:
        string_to_integer(string)
    except ValueError:
        string_to_float(string)


def split_string(string):
    return string.split()[0]


def create_json_file(products_list: list[dict[str, str]]):
    with open('product.json', 'w', encoding="utf-8") as json_file:
        json.dump(products_list, json_file, ensure_ascii=False, indent=4)


def bulk_create_product(products_list: list[dict[str, str]]):
    for product in products_list:
        lookup_param = {"title": product.pop("title")}
        Product.objects.update_or_create(**lookup_param, defaults=product)
