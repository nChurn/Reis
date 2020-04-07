from django.test import RequestFactory, TestCase
from passport_app.calc.calc import * 

class CalcTest(TestCase):

    def test_math_operators(self):
        result = math_operators("(", 34.9, 134.09)
        self.assertEqual(result, None)

        result = math_operators("+", 34.9, 134.09)
        self.assertEqual(result, 168.99)

        result = math_operators("-", 34.9, 134.09)
        self.assertEqual(result, -99.19)

        result = math_operators("*", 34.9, 134.09)
        self.assertEqual(result, 4679.741)

        result = math_operators("/", 34.9, 134.09)
        self.assertEqual(result, 0.26027295100305764)

        result = math_operators("^", 2, 3)
        self.assertEqual(result, 8)

        result = math_operators("^", 8, 0.33)
        self.assertEqual(result, 1.9861849908740719)

    def test_find_lowest_indx(self):
        min_indx, min_key = find_lowest_indx({'+':0, '-':-1})
        self.assertEqual(min_indx, 0)
        self.assertEqual(min_key, '+')

        min_indx, min_key = find_lowest_indx({'+':-1, '-':-1})        
        self.assertEqual(min_key, '')

        min_indx, min_key = find_lowest_indx({'+':2, '-':0})
        self.assertEqual(min_indx, 0)
        self.assertEqual(min_key, '-')

        min_indx, min_key = find_lowest_indx({'+':0, '-':0})
        self.assertEqual(min_indx, 0)
        self.assertEqual(min_key, '+')

    def test_find_end_bracket(self):
        indx = find_end_bracket("7-3)/(6+9)")
        self.assertEqual(indx, 3)

        indx = find_end_bracket("7-3*(6+9))/(7-9)")
        self.assertEqual(indx, 9)

        indx = find_end_bracket("5-1)")
        self.assertEqual(indx, 3)

    def test_find_sym(self):
        sym, left_str, right_str = find_sym("125/5")
        self.assertEqual(sym, '/')
        self.assertEqual(left_str, '125')
        self.assertEqual(right_str, '5')

        sym, left_str, right_str = find_sym("125/(5-1)")
        self.assertEqual(sym, '/')
        self.assertEqual(left_str, '125')
        self.assertEqual(right_str, '4.0')

        sym, left_str, right_str = find_sym("125/(5-(-1.5))")
        self.assertEqual(sym, '/')
        self.assertEqual(left_str, '125')
        self.assertEqual(right_str, '6.5')

        

    def test_calc(self):
        res = calc("125/5")
        self.assertEqual(res, 25.0)
        
        res = calc("125/(5-1)")
        self.assertEqual(res, 31.25)
        
        res = calc("125/(5-(-1.5))")
        self.assertEqual(res, 19.23076923076923)