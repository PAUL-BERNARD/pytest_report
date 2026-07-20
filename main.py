from xml.etree import ElementTree
from collections import defaultdict


class TestCase:
    def __init__(self, name: str, time: int):
        self.name = name
        self.time = time


class TestClass:
    def __init__(self, classname: str):
        self.classname = classname
        self.testcases: list[TestCase] = []

    def add_testcase(self, testcase: TestCase):
        self.testcases.append(testcase)


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
        self.testclasses: dict[str, list[TestCase]] = defaultdict(list)

    def add_testcase(self, classname: str, name, time: float):
        testcase = TestCase(name, time)
        self.testclasses[classname].append(testcase)

    def print_report(self):
        total_duration = sum(sum(testcase.time for testcase in self.testclasses[testclass]) for testclass in self.testclasses)
        print(f"Total duration: {total_duration}s")
        print(f"{self.tests} tests ; {self.errors} errors ; {self.failures} failures ; {self.skipped} skipped")

        for testclass in self.testclasses:
            current_duration = sum(testcase.time for testcase in self.testclasses[testclass])
            print(f" - {testclass:<61}: {current_duration:>10}s ({100*current_duration/total_duration:>5.2f}%)")

    def print_report_class(self, classname, *, limit=0.0):
        tests = self.testclasses[classname]
        tests = sorted(tests, key=lambda t: t.time, reverse=True)

        print(f"{classname}: {len(tests)} tests found")

        total_duration = sum(test.time for test in tests)
        for test in tests:
            if test.time < limit:
                other_duration = sum(t.time for t in tests[i:])
                num_other_tests = len(tests)-i
                print(f" - Other ({num_other_tests} tests)                                              : {other_duration:>10}s ({100*other_duration/total_duration:>5.2f}%) Avg. duration: {other_duration/num_other_tests:.2f}s")
                return

            print(f" - {test.name:<61}: {test.time:>10}s ({100*test.time/total_duration:>5.2f}%)")

def main():
    tree = ElementTree.parse("tests/full_report.xml")
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
        testsuite.add_testcase(classname=classname, name=name, time=time)

    testsuite.print_report_class("deepinv.tests.test_models", limit=10.0)


if __name__ == "__main__":
    main()
