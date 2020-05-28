import math 
import operator
import re


def math_operators (sym , val1, val2):
    if sym == '^':
        return pow(val1, val2)    
    if sym == '/':
        return val1 / val2
    if sym == '*':
        return val1 * val2
    if sym == '+':
        return val1 + val2
    if sym == '-':
        return val1 - val2

    return None

def find_lowest_indx(hash_param):    
    min_indx = 10000000
    res_key = ''
    for temp_key in hash_param.keys():
        if hash_param[temp_key] != -1 and hash_param[temp_key] < min_indx:                                   
            min_indx = hash_param[temp_key]  
            res_key = temp_key            
    return min_indx, res_key

def find_end_bracket(formula):
    count = 1
    temp_count = 0
    for i in range(len(formula)):        
        if formula[i] == '(':
            count+=1

        if formula[i] == ')':
            temp_count+=1

        if temp_count == count:
            return i
    return -1


def find_sym(formula, symbols_arr=["(", "^", "/,*", "+,-"]):
    for sym_item in symbols_arr:
        temp_symbols_arr = sym_item.split(',')
        temp_hash = {}
        for temp_sym in temp_symbols_arr:
            indx = formula.find(temp_sym)
            if indx == -1:
                continue
            
            if temp_sym == "-" and indx == 0:
                return '', formula, None
                        
            temp_hash[temp_sym] = indx
        
        min_indx, min_sym = find_lowest_indx(temp_hash)

        if min_sym != '':
            if min_sym == '(':
                print(formula[(min_indx+1):])
                bracket_str = formula[(min_indx+1):]
                temp_indx = find_end_bracket(bracket_str)                            
                print(bracket_str[0:temp_indx])
                bracket_res = calc(bracket_str[0:temp_indx])                
                temp_formula = "".join((formula[:min_indx], str(bracket_res) , bracket_str[(temp_indx+1):]))    
                formula = temp_formula
                continue           
            else:
                return formula[min_indx], calc(formula[:min_indx]), calc(formula[(min_indx + 1):])
    return '', formula, None

def calc(formula_text):
    res = None
    try:
        sym, left_str, right_str = find_sym(formula_text)
        if sym == '':
            res = left_str
        else:
            res = math_operators(sym, float(left_str), float(right_str))
    except Exception as e:
        print(e)
    return res

def __parse_category_points(data):
    result = []
    if '-' in data:
        start_point = data.split('-')[0]
        end_point = data.split('-')[1]
        while start_point != end_point:
            result.append(start_point)

            arr = list(map(int, start_point.split('.')))
            arr[-1] = arr[-1] + 1
            start_point = ".".join(str(x) for x in arr)
        result.append(end_point)
    else:
        arr = data.split(',')
        for a in arr:
            result.append(a)

    return result

def __calc_category_sum(category_points, category_data):
    items = []
    for item in category_data:
        if item['point'] in category_points:
            if item['rate'] is not None:
                items.append(float(item['rate']))
    return sum(items)

def __calc_category_average(category_points, category_data):
    items = []
    for item in category_data:
        if item['point'] in category_points:
            if item['rate'] is not None:
                items.append(float(item['rate']))
    return sum(items) / len(items)

def calc_formula_obj(formula_obj, category_data):
    if not formula_obj or not formula_obj.formula:
        return 0
    formula = formula_obj.formula.replace('x', formula_obj.rate) \
            .replace('y', formula_obj.amount).replace(' ', '')
    
    try:
        check = re.match(r'sum\((.*?)\)', formula)
        if check and category_data is not None:
            _sum = __calc_category_sum(__parse_category_points(check.group(1)), category_data)
            formula = formula.replace(check.group(0), str(_sum))

        check = re.match(r'avrg\((.*?)\)', formula)
        if check and category_data is not None:
            _sum = __calc_category_average(__parse_category_points(check.group(1)), category_data)
            formula = formula.replace(check.group(0), str(_sum))

        return calc(formula)
    except Exception as e:
        print(e)
        return None
    

