from passport_app.email_manager import send_error
# from zeep import Client
from requests import Session
from requests.auth import HTTPBasicAuth
# from zeep.transports import Transport

# def send_request(client, data):
#     r = client.service.GetDocumentWithID(document=data)
#     return r

def search_by_jkh(address_string, keys):
    # wsdl = 'https://api.reformagkh.ru/api/wsdl'
    # session = Session()
    # session.auth = HTTPBasicAuth("ooojts@yandex.ru", "nuteve10")
    # client = Client(wsdl, transport=Transport(session=session))
    # # print(client.service.Method1('login', 'is cool'))
    # request_data = {}
    # client.service.sendData(**request_data)
    return []