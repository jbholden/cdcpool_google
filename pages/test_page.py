import webapp2
import unittest
import StringIO
import string
from handler import *
from tests.test_calculator import *
from tests.index import *
from tests.database.test_weeks import *
from tests.database.test_players import *
import time
import logging

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

class TestData:
    name = None
    index = None

class MainTestPage(Handler):

    def __setup_class_tests(self,suite,test_class):
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(test_class)

        #w = WeeksInDatabase()
        #w.add_weeks(2013,[1,2,3])
        #weeks_to_test = w.get_weeks()
        #weeks_to_test = None

        if hasattr(test_class,"run_subset"):
            subset = test_class.run_subset()
            for name in testnames:
                if name in subset:
                    suite.addTest(test_class(name))
        else:
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

    def __get_test_data_for_selecting_tests_to_run(self):
        tests = []
        for i,item in enumerate(test_classes):
            t = TestData()
            t.name = item[0]
            t.index = i
            tests.append(t)
        return tests

    def __get_tests_selected_to_run(self):
        tests = []
        for i,item in enumerate(test_classes):
            checkbox_name = "checkbox_%d" % (i)
            checkbox_value = self.request.get(checkbox_name)
            if checkbox_value and checkbox_value == "checked":
                tests.append(i)
        return tests

    def __run_all_tests(self):
        return self.__run_tests(range(len(test_classes)))

    def __run_tests(self,tests_to_run):
        results = []
        for i in tests_to_run:
            item = test_classes[i]
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
        run_all_button_clicked = self.request.get("run_all_button")
        run_selected_button_clicked = self.request.get("run_selected_button")

        if run_all_button_clicked:
            results = self.__run_all_tests()
            summary = self.__summary_data(results)
            self.render('test_page.html',results=results,summary=summary)
        elif run_selected_button_clicked:
            tests_to_run = self.__get_tests_selected_to_run()
            results = self.__run_tests(tests_to_run)
            summary = self.__summary_data(results)
            self.render('test_page.html',results=results,summary=summary)


    def get(self):
        test_data = self.__get_test_data_for_selecting_tests_to_run()
        self.render("choose_tests.html",tests=test_data)
        return
