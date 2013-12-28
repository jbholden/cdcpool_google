from handler import *
from tests.visual_index import *

class PageData:
    number = None
    description = None
    link = None
    verify = None
    setup = None
    cleanup = None

class VisualTestPage(Handler):

    def __build_page_data(self):
        page_data = []
        for index,test_class in enumerate(test_classes):
            obj = test_class()
            d = PageData()
            d.number = index
            d.description = obj.description
            d.link = obj.link
            d.verify = []
            #d.verify = obj.verify

            if hasattr(test_class,"setup"):
                d.setup = True
            else:
                d.setup = False

            if hasattr(test_class,"cleanup"):
                d.cleanup = True
            else:
                d.cleanup = False

            page_data.append(d)

        return page_data


    def get(self):
        data = self.__build_page_data()
        self.render("visual_tests.html",data=data)
        return

class VisualSetupPage(Handler):
    def post(self):
        test_number_param = self.request.get("test_number")

        if not(test_number_param):
            self.error(400)
            self.write('<html><body>Test number is invalid</body></html>')
            return

        try:
            test_number = int(test_number_param)
        except ValueError:
            self.error(400)
            self.write('<html><body>Test number %s is not an integer</body></html>' % (test_number_param))
            return

        if test_number not in range(len(test_classes)):
            self.error(400)
            self.write('<html><body>Test number %s is not valid</body></html>' % (test_number_param))
            return

        test_class = test_classes[test_number]
        obj = test_class()
        obj.setup()

        self.response.out.write('success')

class VisualCleanupPage(Handler):
    def post(self):
        test_number_param = self.request.get("test_number")

        if not(test_number_param):
            self.error(400)
            self.write('<html><body>Test number is invalid</body></html>')
            return

        try:
            test_number = int(test_number_param)
        except ValueError:
            self.error(400)
            self.write('<html><body>Test number %s is not an integer</body></html>' % (test_number_param))
            return

        if test_number not in range(len(test_classes)):
            self.error(400)
            self.write('<html><body>Test number %s is not valid</body></html>' % (test_number_param))
            return

        test_class = test_classes[test_number]
        obj = test_class()
        obj.cleanup()

        self.response.out.write('success')
