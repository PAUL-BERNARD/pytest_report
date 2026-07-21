from xml.etree import ElementTree
import re



class TestCase:
    def __init__(self, name: str, time: int):
        self.name = name
        self.time = time


class TestFunc:
    def __init__(self, name: str):
        self.name: str = name
        self.testcases: list[TestCase] = []
    
    def add_testcase(self, testcase):
        self.testcases.append(testcase)
    
    def duration(self):
        return sum(c.time for c in self.testcases)
    
    def print_report(self, *, limit=0.0):
        testcases = sorted(self.testcases, key=lambda c: c.time, reverse = True)
        total_duration = self.duration()

        print(f"{self.name}: {len(self.testcases)} tests ; Total duration: {total_duration}s")
        for i, testcase in enumerate(testcases):
            if testcase.time < limit:
                other_duration = sum(c.time for c in testcases[i:])
                num_other_cases = len(testcases)-i
                print(f" - OTHER ({num_other_cases} cases <{limit}s)                                       : {other_duration:>10.2f}s ({100*other_duration/total_duration:>5.2f}%) Avg. duration: {other_duration/num_other_cases:.2f}s")
                return

            print(f" - {testcase.name:<61}: {testcase.time:>10.2f}s ({100*testcase.time/total_duration:>5.2f}%)")


class TestClass:
    ### A file (e.g. deepinv.tests.test_models), can be a test class (e.g. deepinv.tests.test_external_libraries.TestTomographyWithAstra)
    def __init__(self, classname: str):
        self.classname = classname
        self.testcases: list[TestCase] = []
        self.testfuncs: dict[str, TestFunc] = {}

    def add_testcase(self, testcase: TestCase):
        # split testcase name between name_function[parameters]
        res = re.search(r"([a-z_]*)\[([a-z0-9-]*)\]", testcase.name)
        is_parametrized = res is not None
        if is_parametrized:
            func_name, parameters = res.groups()
        else:
            func_name = testcase.name
        
        if not func_name in self.testfuncs:
            self.testfuncs[func_name] = TestFunc(func_name)
        
        self.testfuncs[func_name].add_testcase(testcase)
        self.testcases.append(testcase)
    
    def duration(self):
        return sum(testcase.time for testcase in self.testcases)
    
    def print_report(self, *, limit=0.0):
        testclass = self
        tests = sorted(testclass.testcases, key=lambda t: t.time, reverse=True)

        print(f"{self.classname}: {len(tests)} tests found")

        total_duration = sum(test.time for test in tests)
        for i, test in enumerate(tests):
            if test.time < limit:
                other_duration = sum(t.time for t in tests[i:])
                num_other_tests = len(tests)-i
                print(f" - OTHER ({num_other_tests} tests <{limit}s)                                      : {other_duration:>10.2f}s ({100*other_duration/total_duration:>5.2f}%) Avg. duration: {other_duration/num_other_tests:.2f}s")
                return

            print(f" - {test.name:<61}: {test.time:>10.2f}s ({100*test.time/total_duration:>5.2f}%)")


class TestSuite:
    def __init__(
        self,
        name: str,
        errors: int,
        failures: int,
        skipped: int,
        tests: int,
        time: float,
        timestamp: str,
        hostname: str,
    ):
        self.name = name
        self.errors = errors
        self.failures = failures
        self.skipped = skipped
        self.tests = tests
        self.time = time
        self.timestamp = timestamp
        self.hostname = hostname
        self.testclasses: dict[str, TestClass] = dict()

    def add_testcase(self, classname: str, testcase: TestCase):
        if not self.testclasses.get(classname):
            self.testclasses[classname] = TestClass(classname)
        
        self.testclasses[classname].add_testcase(testcase)
    
    def duration(self):
        return sum(testclass.duration() for testclass in self.testclasses.values())

    def print_report(self, *, limit=0.0):
        total_duration = self.duration()
        testclasses = sorted(self.testclasses.values(), key = lambda t: t.duration(), reverse=True)
        print(f"Total duration: {total_duration}s")
        print(f"{self.tests} tests ; {self.errors} errors ; {self.failures} failures ; {self.skipped} skipped")

        for i, testclass in enumerate(testclasses):
            current_duration = testclass.duration()

            if current_duration < limit:
                other_duration = sum(t.duration() for t in testclasses[i:])
                num_other_classes = len(testclasses)-i
                print(f" - OTHER ({num_other_classes} classes <{limit}s)                                  : {other_duration:>10.2f}s ({100*other_duration/total_duration:>5.2f}%) Avg. duration: {other_duration/num_other_classes:.2f}s")
                return

            print(f" - {testclass.classname:<61}: {current_duration:>10.2f}s ({100*current_duration/total_duration:>5.2f}%)")
    
    def print_report_class(self, classname, **kwargs):
        self.testclasses[classname].print_report(**kwargs)

def parse_xml(path):
    tree = ElementTree.parse(path)
    root = tree.getroot()

    assert root.tag == "testsuites"

    if len(root) != 1:
        raise ValueError(f"Expected 1 testsuite, got {len(root)}")

    testsuite_node = root[0]

    assert testsuite_node.tag == "testsuite"

    testsuite = TestSuite(**testsuite_node.attrib)

    for testcase in testsuite_node:
        classname = testcase.attrib["classname"]
        time = float(testcase.attrib["time"])
        name = testcase.attrib["name"]
        testcase = TestCase(name, time)
        testsuite.add_testcase(classname=classname, testcase=testcase)
    
    return testsuite


def main():
    testsuite = parse_xml("tests/full_report.xml")
    
    # testsuite.print_report_class("deepinv.tests.test_models", limit=10.0)
    # testsuite.print_report()
    testsuite.testclasses["deepinv.tests.test_models"].testfuncs["test_denoiser_sigma_color"].print_report(limit=10)


if __name__ == "__main__":
    main()
