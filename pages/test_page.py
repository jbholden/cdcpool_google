import webapp2
import unittest
import StringIO
import string
from handler import *
from tests.test_calculator import *
from tests.test_database import *
from tests.index import *
from tests.database.weeks_in_database import *
from tests.database.test_weeks import *
from tests.database.test_players import *
import time

# runs the tests in tests/index.py
# alternative:  jquery posts to run tests, display status messages
# - example:  run picks week 1 (show message), run picks week 2 (show message), ...
# alternative:  select which tests to run
# - checkbox?
# - run button
# - run all?

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

    def __setup_class_tests(self,suite,test_class):
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(test_class)

        #w = WeeksInDatabase()
        #w.add_weeks(2013,[1,2,3])
        #weeks_to_test = w.get_weeks()
        #weeks_to_test = None

        for name in testnames:
            suite.addTest(test_class(name))

    def __run_test(self,test_class):
        suite = unittest.TestSuite()
        self.__setup_class_tests(suite,test_class)

        # TODO use loadTestsFromModule to find all tests in the directory?
        # TODO use discover?
        # http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases/
        #w = WeeksInDatabase()
        #w.add_weeks(2013,[1,2,3])
        #weeks_to_test = w.get_weeks()
        #self.suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestWeeks(weeks_to_test=weeks_to_test)))
        #self.suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_class))

        output = StringIO.StringIO()
        test_result = unittest.TextTestRunner(stream=output).run(suite)
        output_text = output.getvalue()
        output.close()

        num_tests = test_result.testsRun
        num_failures = len(test_result.failures) + len(test_result.errors)
        passed = test_result.wasSuccessful()

        return passed,num_tests,num_failures,output_text

    def __run_all_tests(self):
        results = []
        for item in test_classes:
            name = item[0]
            test_class = item[1]

            start_time = time.time()
            all_passed,num_tests,num_failures,test_output = self.__run_test(test_class)
            elapsed_time = time.time() - start_time

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
