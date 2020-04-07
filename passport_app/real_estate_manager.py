from django.views import View
from passport_app.models import *

def create_new_real_estate(params, user, address_params, form):
    owner = Owner()  #"""todo need fix"""
    owner.save()

    real_property = RealEstate()
    real_property.owner = owner
    real_property.user = user
    if form:
        real_property.form = form
    real_property.country_name = address_params['country']
    real_property.region_name = address_params['province']
    real_property.district_name = address_params['province2']
    real_property.locality_name = address_params['locality']
    real_property.street_name = address_params['street']
    real_property.house_number = address_params['house']
    real_property.address = address_params['text_address']

    pos = address_params['point'].split(' ')
    real_property.latitude = pos[0]
    real_property.longitude = pos[1]

    # if params['base']['kadastr_number']:
    #     print("save cn="+params['base']['kadastr_number'])
    #     real_property.kadastr_number = params['base']['kadastr_number']
    # if params['base']['address']:
    #     real_property.address = params['base']['address']
    real_property.save()

    for cl_item in params:
        # classifier = Classifier.objects.get(name=cl_item)
        for field_item in params[cl_item]:
            field_data_item = DataField(** {'value': params[cl_item][field_item]})
            field = Field.objects.filter(name = field_item)
            print ("field:"+field_item)
            print (field)
            if field:
                field_data_item.field = field[0]
                field_data_item.real_estate = real_property
                field_data_item.save();
                print("save field "+field[0].name)

def update_real_estate(params, address_params, real_property_id):
    real_property = RealEstate.objects.get(id=int(real_property_id))

    for item in params:
        field = Field.objects.filter(name = item)
        field_data_item_arr = DataField.ojects.filter(field_id = field.id, real_estate_id = real_property.id)

        if field_data_item_arr and field_data_item_arr.size == 1:
            field_data_item = field_data_item_arr[0]
            field_data_item.field = params[item]
            field_data_item.save()

def create_property_dict():
    params = {}
    classifiers = Classifier.objects.all()
    for cl_item in classifiers:
        params[cl_item.name] = {}
        for field_item in Field.objects.filter(classifier_id = cl_item.id):
            params[cl_item.name][field_item.name] = ''
    print (params)
    return params

def create_new_by_old(user, fields):
    print (fields)
    temp_id = -1
    for temp_field in fields:
        if temp_field['id']:
            temp_id = int(temp_field['id'])
            break
    data_field = DataField.objects.get(id=temp_id)
    old_realestate = data_field.real_estate

    owner = Owner()
    owner.save()

    real_property = RealEstate()
    real_property.owner = owner
    real_property.user = user
    if real_property.search_form:
        real_property.form = old_realestate.search_form
    real_property.country_name = old_realestate.country_name
    real_property.region_name = old_realestate.region_name
    real_property.district_name = old_realestate.district_name
    real_property.locality_name = old_realestate.locality_name
    real_property.street_name = old_realestate.street_name
    real_property.house_number = old_realestate.house_number
    real_property.address = old_realestate.address

    real_property.latitude = old_realestate.latitude
    real_property.longitude = old_realestate.longitude

    real_property.save()


    for field_item in fields:
        try:
            id = field_item['id']
            data_field = DataField.objects.get(id = id)
            new_data_field = DataField(real_estate_id = real_property.id, field_id = data_field.field.id)

            new_data_field.value = field_item['value']
            new_data_field.rate = field_item['rate']
            new_data_field.field = data_field.field
            new_data_field.real_estate = real_property

            new_data_field.save()
        except Exception as e:
            pass

    print(real_property.create_date)
    return real_property