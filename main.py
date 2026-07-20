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

    def print_class_percentages(self):
        total = sum(sum(testcase.time for testcase in self.testclasses[testclass]) for testclass in self.testclasses)
        print(f"Total duration: {total}s")

        for testclass in self.testclasses:
            current_duration = sum(testcase.time for testcase in self.testclasses[testclass])
            print(f" - {testclass:<61}: {current_duration:>10}s ({100*current_duration/total:>5.2f}%)")


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

    testsuite.print_class_percentages()


if __name__ == "__main__":
    main()
