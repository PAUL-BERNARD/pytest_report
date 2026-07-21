from xml.etree import ElementTree
from collections import defaultdict


class TestFunc:
    def __init__(self, name: str):
        self.name = name
        self.testcases = []
    
    def add_testcase(self, testcase):
        self.testcases.append(testcase)


class TestCase:
    def __init__(self, name: str, time: int):
        self.name = name
        self.time = time


class TestClass:
    ### A file (e.g. deepinv.tests.test_models), can be a test class (e.g. deepinv.tests.test_external_libraries.TestTomographyWithAstra)
    def __init__(self, classname: str):
        self.classname = classname
        self.testcases: list[TestCase] = []

    def add_testcase(self, testcase: TestCase):
        self.testcases.append(testcase)
    
    def duration(self):
        return sum(testcase.time for testcase in self.testcases)


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
                other_duration = sum(t.time for t in testclasses[i:])
                num_other_classes = len(testclasses)-i
                print(f" - Other ({num_other_classes} classes)                                          : {other_duration:>10}s ({100*other_duration/total_duration:>5.2f}%) Avg. duration: {other_duration/num_other_classes:.2f}s")
                return

            print(f" - {testclass.classname:<61}: {current_duration:>10}s ({100*current_duration/total_duration:>5.2f}%)")

    def print_report_class(self, classname, *, limit=0.0):
        tests = self.testclasses[classname]
        tests = sorted(tests, key=lambda t: t.time, reverse=True)

        print(f"{classname}: {len(tests)} tests found")

        total_duration = sum(test.time for test in tests)
        for i, test in enumerate(tests):
            if test.time < limit:
                other_duration = sum(t.time for t in tests[i:])
                num_other_tests = len(tests)-i
                print(f" - Other ({num_other_tests} tests)                                              : {other_duration:>10}s ({100*other_duration/total_duration:>5.2f}%) Avg. duration: {other_duration/num_other_tests:.2f}s")
                return

            print(f" - {test.name:<61}: {test.time:>10}s ({100*test.time/total_duration:>5.2f}%)")

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
    testsuite.print_report()


if __name__ == "__main__":
    main()
