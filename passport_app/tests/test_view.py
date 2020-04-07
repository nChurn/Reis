from django.test import TestCase
from passport_app.models import *
#from views import Animal

# class AnimalTestCase(TestCase):
#     def setUp(self):
#         """"""
#         # Animal.objects.create(name="lion", sound="roar")
#         # Animal.objects.create(name="cat", sound="meow")
#
#     def test_animals_can_speak(self):
#         """Animals that can speak are correctly identified"""
#         # lion = Animal.objects.get(name="lion")
#         # cat = Animal.objects.get(name="cat")
#         # self.assertEqual(lion.speak(), 'The lion says "roar"')
#         # self.assertEqual(cat.speak(), 'The cat says "meow"')

class ParserParameterSqlTest(TestCase):

    def test_parameter_sql(self):
        priority = Priority()
        priority.save()
        parser_type = ParserType()
        parser_type.priority = priority
        parser_type.save()
        parser_parameter = ParserParameter()
        parser_parameter.parser_type = parser_type
        parser_parameter.save()
        

        # parser_parameters = ParserParameter.objects.all().prefetch_related('parser_type').prefetch_related('priority')
        # print(parser_parameters[0].parser_type)
        print (RealEstate.objects.all())
