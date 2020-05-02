import os
import sys
import django
sys.path.append("D:\Work Projects\passport_app\property_passport")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'property_passport.settings')
django.setup()

from passport_app.models import *

def create_parser_param(name, name_ru, parser_type_id, parser_parameter_type):
    pp = ParserParameter()
    pp.name = name
    pp.name_ru = name_ru
    pp.parser_type_id = parser_type_id
    pp.parser_parameter_type = parser_parameter_type

    pp.save()
    return pp

def create_param(name, name_ru, parser_parameters):
    p = Parameter()
    p.name = name
    p.name_ru = name_ru

    p.save()

    for param in parser_parameters:
        p.parser_parameters.add(param)

    p.save()
    return p


def create_category(lines, i):
    arr = lines[i].split(';')
    index = arr[0]

    category = Category()
    category.name_ru = arr[1]
    category.name = arr[2]
    category.point = index

    category.save()

    if len(index.split('.')) > 1:
        parent_index = '.'.join(index.split('.')[:-1])
        parent = Category.objects.filter(point = parent_index).first()

        if parent_index == '1':
            parent = Category.objects.first()
            parent.categories.add(category)
            parent.save()
        else:
            parent.categories.add(category)

        category.parent_categories.add(parent)

    category.save()

    #add param to category
    if len(index.split('.')) >= len(lines[i+1].split(';')[0].split('.')) and len(index.split('.')) != 1:
        param = Parameter.objects.filter(name = category.name).first()
        if param is not None:
            category.parameters.add(param)
        else:
            print("param " + category.name_ru + " not found")

            parser_params = ParserParameter.objects.filter(name = category.name).all()
            if len(parser_params) > 1:
                print('error')

            if len(parser_params) == 0:
                print('parser_param not found')

                parser_params = []
                if arr[3] == '+':
                    p = create_parser_param(category.name + " Google", category.name_ru + " Google", 2, 'social')
                    parser_params.append(p)

                    p = create_parser_param(category.name + " Yandex", category.name_ru + " Yandex", 3, 'social')
                    parser_params.append(p)
                else:
                    parser_params = [create_parser_param(category.name, category.name_ru, arr[4], '')]

            param = create_param(category.name, category.name_ru, parser_params)

            category.parameters.add(param)
            print('addedd')

        category.save()

def strat():
    f = open(r"C:\Users\Dmitriev Ivan\Desktop\парсинг питон\набор 1, ктагории для загрузки.csv", "r", encoding='utf8')
    lines = f.read().splitlines()

    for i in range(0, len(lines)):
        create_category(lines, i)
        

def create_params():
    f = open(r"C:\Users\Dmitriev Ivan\Desktop\парсинг питон\parser_parameters_fix.csv", "r", encoding='utf8')
    lines = f.read().splitlines()

    for line in lines:
        arr = line.split(';')

        check = ParserParameter.objects.filter(name = arr[0] + " Yandex").first()
        if check is None:
            pp = ParserParameter()
            pp.name = arr[0] + " Yandex"
            pp.name_ru = arr[1] + " Yandex"
            pp.parser_type_id = 3
            pp.parser_parameter_type = 'social'

            pp.save()


        check = ParserParameter.objects.filter(name = arr[0] + " Google").first()
        if check is None:
            pp = ParserParameter()
            pp.name = arr[0] + " Google"
            pp.name_ru = arr[1] + " Google"
            pp.parser_type_id = 2
            pp.parser_parameter_type = 'social'

            pp.save()

    for line in lines:
        arr = line.split(';')
        p_params = ParserParameter.objects.filter(name_ru__contains = arr[1]).order_by('name_ru')

        if p_params.count() <= 0:
            continue

        p = Parameter()
        p.name = p_params[0].name.replace("Google", "").replace("Yandex", "").strip()
        p.name_ru = arr[1]



        check = Parameter.objects.filter(name = p.name).first()
        if check is None:
            p.save()

            p.parser_parameters.add(p_params[0])
            p.parser_parameters.add(p_params[1])

            p.save()


def delete_all():
    cat = Category.objects.all().delete()
    Parameter.objects.all().delete()
    ParserParameter.objects.all().delete()

delete_all()
strat()
    