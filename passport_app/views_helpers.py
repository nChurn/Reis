from passport_app.models import *
#Сервисные классы для вертикального поиска
def GetTextFromLink(str_):
    import re
    p=re.compile("<.*?>|&nbsp;|&amp;", re.DOTALL | re.M)
    str_=p.sub('', str_)
    vals=str_.split('"')
    print('008',vals)
    str_txt=''
    for item in vals:
        print(item)
        str_txt=str_txt+item
    str_txt = "'"+'124'+"'"
    return  str_txt

class RealEstateFormDecorator:
    def Run(self,str_,el):
        id_=str(el.item.id)
        str_txt = GetTextFromLink(str_)
        s='<a href=# onclick=RealEstatesLink('+id_+',' + str_txt +')>'+str_+'</a>'
        return  s
class UserFormDecorator:
    def Run(self,str_,el):
        id_=str(el.item.id)
        str_txt = GetTextFromLink(str_)
        s='<a href=# onclick=UsersLink('+id_+',' + str_txt +')>'+str_+'</a>'
        return  s
class LinkFormDecorator:
    def Run(self,str_,el):
        id_=str(el.item.id)
        s='<a href=# onclick=FormsLink('+id_+')>'+str_+'</a>'
        return  s
class CategoryFormDecorator:
    def Run(self,str_,el):
        id_=str(el.item.id)
        s='<a href=javascript:CategoryLink('+id_+')>'+str_+'</a>'
        return  s
class ParametersFormDecorator:
    def Run(self,str_,el):
        id_=str(el.item.id)
        str_txt = GetTextFromLink(str_)
        print('1243678', str_txt)
        s='<a href=# onclick=ParametersLink(' + id_ + ',' + str_txt + ')>' + str_ + '</a>'
        print('12436789', s)
        return  s
class TypeOfValueFormDecorator:
    def Run(self,str_,el):
        id_=str(el.item.id)
        str_txt = GetTextFromLink(str_)
        print(str_txt)
        #s='<a href=# onclick=TypeOfValuesLink('+id_+')>'+str_+'</a>'
        s = '<a href=# onclick=TypeOfValuesLink(' + id_ + ',' + str_txt + ')>' + str_ + '</a>'
        return  s
class UnitFormDecorator:
    def Run(self,str_,el):
        id_=str(el.item.id)
        print(str)
        str_txt=GetTextFromLink(str_)
        print('124367',str_txt)
        s='<a href=# onclick=UnitLink('+id_+','+str_txt+')>'+str_+'</a>'
        print('12436789', s)
        return  s
class ParserFormDecorator:
    def Run(self,str_,el):
        id_=str(el.item.id)
        s='<a href=# onclick=ParserLink('+id_+')>'+str_+'</a>'
        return  s
class DictItem:
    def __init__(self):
        self.item = []  # Текущий элемент
        self.parent = []  # Предок
    def __init__(self,item,parent):
        self.item=item #Текущий элемент
        self.parent=parent #Предок
    def toString(self):
        str=''
        try:
            str = self.item.name + '|' + self.parent.name
        except:
            str=self.item.name
        return str
class DictItems:
    def __init__(self):
        self.data=[]
    def Create(self,nodes):
        res = []
        for obj in nodes:
            res = res + self.CreateObj(obj)
        self.data=res
    def CreateObj(self,obj):
        res = []
        # Если есть потомки
        if not obj.categories is None:
            for item in obj.categories.all():
                item_dict=DictItem(item,obj)
                res.append(item_dict)
            # Пускаем поиск по ветке
            for item in obj.categories.all():
                res = res + self.CreateObj(item)
        else:
            pass
        return res
    # Поиск объекта по ключу
    def FindByItem(self,item):
        matches = list(filter(lambda obj: obj.item.id == item.id, self.data))
        return matches
    #Поиск объекта по предку
    def FindByParent(self,item):
        matches = list(filter(lambda obj: obj.parent.id == item.id, self.data))
        return matches

#Классы для горизонтального поиска
def CommonParser(str):
    list_ = list()
    str = str.strip()
    list_ = str.split()
    m = len(list_)
    dict_list = list()
    for j in range(m):
        name = ''
        name_ru = ''
        for i in range(j):
            name = name + list_[i] + ' '
        for i in range(j, m):
            name_ru = name_ru + list_[i] + ' '
        name = name.strip()
        name_ru = name_ru.strip()
        dict_ = {'name': name, 'name_ru': name_ru}
        dict_list.append(dict_)
        dict_ = {'name': name_ru, 'name_ru': name}
        dict_list.append(dict_)
    return dict_list

class OutData:
    def __init__(self):
        self.item=[]
        self.first_name=''
        self.second_name=''
        self.first_name_ru = ''
        self.second_name_ru = ''
        self.name=''
        self.name_ru=''
        self.name_=''
        self.isname=False
        self.isname_ru=False
        self.id_name=-1
        self.id_name_ru = -1
    def create_obj(self,vals,param):
        item = self.item
        index_name = -1
        index_name_ru = -1
        res=False
        if param==0: #Участвуют два параметра
            name=vals[0]
            name_ru=vals[1]
            # Вхождение поисковой части в слово name
            try:
                index_name = item.name.lower().index(name.lower())
            except:
                pass
            if index_name >= 0:  # Есть вхождение
                first_=item.name[:index_name]
                second_=item.name[index_name:index_name+len(name)]
                three_=item.name[index_name+len(name):]
                self.name=first_+'<b>'+second_+'</b>'+three_
                self.isname=True
                self.id_name=len(second_)
            else:  # Нет вхождений
                self.name = item.name
            # Вхождение поисковой части в слово name_ru
            try:
                index_name_ru = item.name_ru.lower().index(name_ru.lower())
            except:
                pass
            if index_name_ru >= 0:  # Есть вхождение
                first_ = item.name_ru[:index_name_ru]
                second_ = item.name_ru[index_name_ru:index_name_ru + len(name_ru)]
                three_ = item.name_ru[index_name_ru + len(name_ru):]
                print(first_,' ',second_,' ',three_)
                self.name_ru = first_ + '<b>' + second_ + '</b>' + three_
                self.isname_ru = True
                self.id_name_ru = len(second_)
            else:  # Нет вхождений
                self.name_ru = item.name_ru
            # print('0:', index_name)
            # print('0:', index_name_ru)
            max_=max(self.id_name,self.id_name_ru)
            if max_>=0:
                if self.id_name==max_:
                    self.name_=self.name
                if self.id_name_ru==max_:
                    self.name_=self.name_ru
        if param==1: #Задается только name
            name = vals[0]
            index_name=-1
            try:
                index_name = item.name.lower().index(name.lower())
            except:
                pass
            if index_name >= 0:  # Есть вхождение
                first_=item.name[:index_name]
                second_=item.name[index_name:index_name+len(name)]
                three_=item.name[index_name+len(name):]
                self.name=first_+'<b>'+second_+'</b>'+three_
                self.isname = True
                self.id_name = len(second_)
                self.name_=self.name
               # print('2:', first_, ' ', second_, ' ', three_)
            else:  # Нет вхождений
                self.name = item.name
            self.name_ru = item.name_ru
            # print('1:', index_name)
            # print('1:', index_name_ru)
            # print([index_name, index_name_ru])

        if param==2: #Задается только name_ru
            name_ru = vals[0]
            index_name_ru=-1
            try:
                index_name_ru = item.name_ru.lower().index(name_ru.lower())
            except:
                pass
            if index_name_ru >= 0:  # Есть вхождение
                first_ = item.name_ru[:index_name_ru]
                second_ = item.name_ru[index_name_ru:index_name_ru + len(name_ru)]
                three_ = item.name_ru[index_name_ru + len(name_ru):]
                self.name_ru = first_ + '<b>' + second_ + '</b>' + three_
                self.isname_ru = True
                self.id_name_ru = len(second_)
                self.name_=self.name_ru
                # print('2:',first_, ' ', second_, ' ', three_)
            else:  # Нет вхождений
                self.name_ru = item.name_ru
            self.name = item.name
            # print('2:',index_name)
            # print('2:', index_name_ru)
            # print([index_name, index_name_ru])

        return  index_name+index_name_ru

class BaseHelper:
    def __init__(self):
        #Модель данных
        self.Model = []
        #Входные данные
        self.input_str = ''
        # Название справочника
        self.Name=''
        #Есть ли права
        self.IsMaster=False
        self.Decorator=None
#Хелпер для вертикального поиска
class TreeSearchHelper(BaseHelper):
    def ConvertResult(self):
        res_=self.Run()
        print('???',res_)
        res_find=[]
        for item in res_:
            list_=[self.Name]+item
            res_find.append(list_)
        return res_find
    def GetParentsFromId(self,id_):
        # Категории как вершины графа
        categories = self.Model.objects.filter(parent_categories=None).order_by('point')
        obj_items = DictItems()
        obj_items.Create(categories)
        for item in categories:
            obj_items.data.append(DictItem(item, None))
        item=self.Model.objects.get(id=id_)
        obj = OutData()
        obj.item = item
        matches = self.GetParents(obj, obj_items)
        return  matches
    def GetParents(self,item_,dict_items):
        res_=[]
        #Начальный объект
        curr=item_
        first=True
        while curr is not None:
            res_.append(curr)
            if first:
                curr=item_.item
                first=False
            #Поиск в словаре по текущему объекту
            obj_dict=dict_items.FindByItem(curr)
            if len(obj_dict)!=0:
                obj_dict=obj_dict[0] #Если есть объект
            else:
                break #Выход из цикла
            curr=obj_dict.parent #Переход к полю-предку
        return res_
    def toString(self,obj):
        s=obj.name+' '+obj.name_ru
        return s
    #Конвертация элементов
    def querySet_to_list(qs):
        return [dict(q) for q in qs]
    #Поиск объектов
        # Обход дерева категорий
    def Find(self, obj, vals):
        res = []
        # Если есть потомки
        if not obj.categories is None:
            # Пускаем поиск по ветке
            for item in obj.categories.all():
                res = res + self.Find(item, vals)
        else:
            pass
        # Если передано два параметра
        obj_ = OutData()
        obj_.item = obj
        if len(vals) == 2:
            name = vals[0]
            name_ru = vals[1]
            vals = [name, name_ru]
            if vals[0] != '' and vals[1] != '':
                if obj_.create_obj(vals, 0) > -2:
                    res.append(obj_)
            else:
                vals.remove('')
                if obj_.create_obj(vals, 1) > -2 or obj_.create_obj(vals, 2) > -2:
                    res.append(obj_)
            # if obj.name.lower() == name.lower() or obj.name_ru.lower() == name_ru.lower():
            #     res.append(obj)
        else:  # Если передан только один параметр
            if len(vals) == 1:
                name = vals[0]
                #print(obj_.create_obj(vals, 1),'!!!!', obj_.create_obj(vals, 2))
                if obj_.create_obj(vals, 1) > -2 or obj_.create_obj(vals, 2) > -2:
                     res.append(obj_)
                # if (obj.name.lower() == name.lower()) or (obj.name_ru.lower() == name.lower()):
                #     res.append(obj)
        return res
    def Search(self,category,vals):
        from django.db.models import Q
        res=[]
        for obj in category:
            res=res+self.Find(obj,vals)
        return  res
    def RunAll(self):
        dict_ = CommonParser(self.input_str)
        print(dict_)
        results = []
        for item in dict_:
            print('.!.',item)
            name=item['name']
            name_ru=item['name_ru']
            list_=self.SubRunAll(name,name_ru)
            print(item,'<>',list_)
            for obj_list in list_:
                results.append(obj_list)
        print(results)
        results = list(dict.fromkeys(results))
        print(results)
        return results
    def Run(self):
        dict_ = CommonParser(self.input_str)
        print(dict_)
        results = []
        for item in dict_:
            print('.!.',item)
            name=item['name']
            name_ru=item['name_ru']
            list_=self.SubRun(name,name_ru)
            print(item,'<>',list_)
            for obj_list in list_:
                results.append(obj_list)
        print(results)
        list_ = list()
        if len(results) > 1:
            for item_list in results:
                s=''
                for obj in item_list:
                    s=s+obj+';'
                list_.append(s.strip())
            print(list_)
            list_ = list(dict.fromkeys(list_))
            print(list_)
            results=[]
            for obj in list_:
                vals=obj.strip().split(';')
                vals.remove(vals[len(vals)-1])
                vals.reverse()
                results.append(vals)
        return results
    def SubRunAll(self,name,name_ru):
        # Категории как вершины графа
        categories = self.Model.objects.filter(parent_categories=None).order_by('point')
        obj_items = DictItems()
        obj_items.Create(categories)
        for item in categories:
            obj_items.data.append(DictItem(item, None))
        vals = []
        if name_ru != '':
            vals = [name, name_ru]
        else:
            vals = [name]
        print('!!!???', vals)
        # Список объектов
        res = self.Search(categories, vals)
        #Копирование в промежуточный список
        res_list=list()
        for item in categories:
           res_list.append(item)
        ind_list=list()
        for item in categories:
           ind_list.append(item.id)
        print(ind_list)
        print('99',res_list)
        #Поиск элементов в дереве
        res_find = self.Search(categories, vals)
        print(res_find)
        for item in res_find:
            # Ищем позицию элемента в списке
            print('100',ind_list)
            # Ветка предков
            matches = self.GetParents(item, obj_items)
            # Преобразуем первый элемент
            matches[0] = matches[0].item
            matches.reverse()
            print(matches)
            index_=ind_list.index(matches[0].id)
            print(index_)
            if index_>=0:
                res_list.insert(index_+1,matches)

        #Формат "плоского" списка
        flat_list=[]
        for item in res_list:
            if isinstance(item,list):
                for obj in item:
                    flat_list.append(obj)
            else:
                flat_list.append(item)
        print('101',flat_list)
        return flat_list


    def SubRun(self,name,name_ru):
        html = ''
        # Категории как вершины графа
        categories = self.Model.objects.filter(parent_categories=None).order_by('point')
        obj_items = DictItems()
        obj_items.Create(categories)
        for item in categories:
            obj_items.data.append(DictItem(item, None))
        vals = []
        if name_ru != '':
            vals = [name, name_ru]
        else:
            vals = [name]
        print('!!!???',vals)
        # Список объектов
        res = self.Search(categories, vals)
        print('!', res)
        # Цикл по найденным объектам
        count_ = 4
        list_matches_names = []
        for item in res:
            print(item.name, ' ', item.name_ru)
            # Поиск объектов в словаре
            matches = self.GetParents(item, obj_items)
            print('0000',matches)
            # Цикл по найденным объектам
            for el in matches:
                print(el.name, ' ', el.name_ru)
            mathes_ = []
            if len(matches) > count_:
                mathes_ = matches[:2]  # Берем первые три элемента от начала
                mathes_.append(matches[len(matches) - 1])  # Берем последний
                matches = mathes_
                print('0001', matches)
            if len(matches) < count_:
                for i in range(count_ - len(matches)):
                    matches.append(None)
            list_matches = []
            index_pos=0
            for el in matches:
                if el is not None:
                    #Если элемент первый в списке
                    if index_pos==0:
                        #Если права
                        if self.IsMaster:
                            res_ = el.name+' '+el.name_ru
                            res_ = self.Decorator.Run(res_,el)

                            list_matches.append(res_)
                        else:
                            print(el.item.id)
                            if self.Decorator is not None:
                                res_=el.name_
                                res_=self.Decorator.Run(res_,el)
                                list_matches.append(res_)
                            else:
                                list_matches.append(el.name_)
                    else:
                        list_matches.append(el.name_ru)
                else:
                    list_matches.append(' ')
                index_pos+=1
            #list_matches.reverse()
            list_matches_names.append(list_matches)
        return list_matches_names

#Хелпер для горизонтального поиска
class HorizontalSearchHelper(BaseHelper):
    def ConvertResult(self):
        res_=self.Run()
        print('???', res_)
        res_find=[]
        for item in res_:
            #Имя справочника и поля для предков. Они пустые
            list_=[self.Name,'','','']
            if self.IsMaster:
                res_ = item.name + ' ' + item.name_ru
                if self.Decorator is not None:
                    res_ = self.Decorator.Run(res_, item)
                list_.append(res_)
            else:
                res_ = item.name_
                if self.Decorator is not None:
                    res_ = self.Decorator.Run(res_, item)
                list_.append(res_)
            #list_.append(item.name_ru)
            res_find.append(list_)
        return  res_find
    def Run(self):
        # Парсим входную строку
        dict_ = CommonParser(self.input_str)
        print(dict_)
        results = []
        for item in dict_:
            print(item)
            name = item['name']
            name_ru = item['name_ru']
            m_count=-1
            if type(self.Model)==models.base.ModelBase:
                searchforms = self.Model.objects.all()
                m_count=searchforms.count()
            else:
                searchforms=self.Model
                m_count=len(searchforms)
            # Если оба поля непустые
            if name_ru != '' and name != '':
                if m_count != 0:
                    for item in searchforms:
                        obj = OutData()
                        obj.item = item
                        vals = [name, name_ru]
                        if obj.create_obj(vals, 0) > -2:
                            results.append(obj)
                if m_count != 0:
                    for item in searchforms:
                        obj = OutData()
                        obj.item = item
                        vals = [name, name_ru]
                        if obj.create_obj(vals, 0) > -2:
                            results.append(obj)
            else:  # Если поле name_ru непустое
                if name_ru != '' and name == '':
                    if m_count != 0:
                        for item in searchforms:
                            obj = OutData()
                            obj.item = item
                            vals = [name_ru]
                            if obj.create_obj(vals, 2) > -2:
                                obj.first_name = item.name
                                results.append(obj)
                # Если поле name непустое
                if name != '' and name_ru == '':
                    if m_count != 0:
                        for item in searchforms:
                            obj = OutData()
                            obj.item = item
                            vals = [name]
                            if obj.create_obj(vals, 1) > -2:
                                obj.first_name_ru = item.name_ru
                                results.append(obj)
        list_ = list()
        if len(results) > 1:
            for item in results:
                list_.append(item.name + '\r' + item.name_ru);
            print(list_)
            list_ = list(dict.fromkeys(list_))
            print(list_)
            #print(results)
            res_ = list()
            for val in list_:
                vals = val.split('\r')
                name = vals[0]
                name_ru = vals[1]
                print(vals)
                for item in results:
                    if item.name.lower() == name.lower() and item.name_ru.lower() == name_ru.lower():
                        res_.append(item)
                        break
                    if item.name_ru.lower() == name.lower() and item.name.lower() == name_ru.lower():
                        res_.append(item)
                        break
        else:
            res_ = results
        return res_

