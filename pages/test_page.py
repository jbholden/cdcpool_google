import webapp2
import unittest
import StringIO
import string
from handler import *
from tests.test_calculator import *
from tests.test_database import *
from tests.index import *
import time

# runs the tests in tests/index.py

class ResultData:
    name = None
    result = None
    output = None
    time = None

class SummaryData:
    num_tests = None
    num_passed = None
    num_failed = None

class MainTestPage(Handler):

    def __run_test(self,test_class):
        self.suite = unittest.TestSuite()
        self.suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_class))

        output = StringIO.StringIO()
        test_result = unittest.TextTestRunner(stream=output).run(self.suite)
        output_text = output.getvalue()
        output.close()

        num_tests = test_result.testsRun
        num_failures = len(test_result.failures) + len(test_result.errors)

        return num_tests,num_failures,output_text

    def __run_all_tests(self):
        results = []
        for item in test_classes:
            name = item[0]
            test_class = item[1]

            start_time = time.time()
            num_tests,num_failures,test_output = self.__run_test(test_class)
            elapsed_time = time.time() - start_time

            all_passed = num_failures == 0

            r = ResultData()
            r.name = name
            r.result = "PASS" if all_passed else "FAIL"
            r.output = test_output
            r.time = "%0.2f Sec." % (elapsed_time)
            results.append(r)
        return results

    def __summary_data(self,results):
        s = SummaryData()
        s.num_tests = len(results)
        s.num_passed = 0
        s.num_failed = 0

        for r in results:
            if r.result == "PASS":
                s.num_passed += 1
            elif r.result == "FAIL":
                s.num_failed += 1
        return s

    def post(self):
        results = self.__run_all_tests()
        summary = self.__summary_data(results)
        self.render('test_page.html',results=results,summary=summary)

    def get(self):
        code = "<html><body>"
        code += "<form action='tests' method='post'>"
        code += "Run the tests&nbsp;"
        code += "<input type='submit' value='Submit'>"
        code += "</form>"
        code += "</body></html>"
        self.response.write(code)
