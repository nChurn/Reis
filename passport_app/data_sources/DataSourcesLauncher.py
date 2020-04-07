from passport_app.models import *


class DataSourcesLauncher():
    __real_estate : RealEstate

    def __init__(self, real_estate: RealEstate):
        self.__real_estate = real_estate

    def start_parsing():
        logger = logging.getLogger(__name__)
        result = {}
        
        parsers = ParserType.objects.order_by('id').all()
        for parser in parsers:
            


    def __save_data(self, data):
        pass