from handler import *
from tests.visual_index import *

class PageData:
    category = None
    number = None
    description = None
    link = None
    verify = None
    setup = None
    cleanup = None

class VisualTestPage(Handler):

    def __build_page_data(self):
        page_data = dict()
        categories = sorted(tests.keys())
        for index,category in enumerate(categories):
            page_data[category] = self.__build_page_data_for_category(category,index)
        return page_data

    def __build_page_data_for_category(self,category,category_index):
        page_data = []
        for index,test_class in enumerate(tests[category]):
            obj = test_class()
            d = PageData()
            d.category = category_index
            d.number = index
            d.description = obj.description
            d.link = obj.link
            d.verify = obj.verify

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
        category_names = sorted(data.keys())
        self.render("visual_tests.html",data=data,category_names=category_names)
        return

class VisualSetupPage(Handler):
    def post(self):
        category_param = self.request.get("category")
        test_number_param = self.request.get("test_number")

        if not(test_number_param):
            self.error(400)
            self.write('<html><body>Test number is invalid</body></html>')
            return

        if not(category_param):
            self.error(400)
            self.write('<html><body>Category is invalid</body></html>')
            return

        try:
            test_number = int(test_number_param)
        except ValueError:
            self.error(400)
            self.write('<html><body>Test number %s is not an integer</body></html>' % (test_number_param))
            return

        try:
            category = int(category_param)
        except ValueError:
            self.error(400)
            self.write('<html><body>Category number %s is not an integer</body></html>' % (category_param))
            return

        try:
            category_name = self.__lookup_category_name(category)
        except:
            self.error(400)
            self.write('<html><body>Category number %s is not valid</body></html>' % (category_param))
            return

        if test_number not in range(len(tests[category_name])):
            self.error(400)
            self.write('<html><body>Test number %s is not valid</body></html>' % (test_number_param))
            return


        test_class = tests[category_name][test_number]
        obj = test_class()
        obj.setup()

        self.response.out.write('success')


    def __lookup_category_name(self,number):
        categories = sorted(tests.keys())
        return categories[number]


class VisualCleanupPage(Handler):
    def post(self):
        category_param = self.request.get("category")
        test_number_param = self.request.get("test_number")

        if not(test_number_param):
            self.error(400)
            self.write('<html><body>Test number is invalid</body></html>')
            return

        if not(category_param):
            self.error(400)
            self.write('<html><body>Category is invalid</body></html>')
            return

        try:
            test_number = int(test_number_param)
        except ValueError:
            self.error(400)
            self.write('<html><body>Test number %s is not an integer</body></html>' % (test_number_param))
            return

        try:
            category = int(category_param)
        except ValueError:
            self.error(400)
            self.write('<html><body>Category number %s is not an integer</body></html>' % (category_param))
            return

        try:
            category_name = self.__lookup_category_name(category)
        except:
            self.error(400)
            self.write('<html><body>Category number %s is not valid</body></html>' % (category_param))
            return

        if test_number not in range(len(tests[category_name])):
            self.error(400)
            self.write('<html><body>Test number %s is not valid</body></html>' % (test_number_param))
            return

        test_class = tests[category_name][test_number]
        obj = test_class()
        obj.cleanup()

    def __lookup_category_name(self,number):
        categories = sorted(tests.keys())
        return categories[number]
