from itertools import chain
from dataclasses import dataclass


@dataclass
class TestCaseReport:
    testcaseidx: str = None
    strategy_design_report: dict = None
    response_report: dict = None
    evaluation_report: dict = None
    relevancy_report: dict = None
    was_compromised: bool = None

class CaseMemory:
    def __init__(self):

        self._test_subject = None
        self._risk_analysis = None
        self._testcases = None

        self._current_testcase_attempt = 0
        self._current_testcaseidx = ""
        self._current_testcase_report = None

        self._testcase_reports = {}

    def add_testcase_report(self, testcaseidx : str, testcase_report: TestCaseReport) -> None:
        if testcaseidx not in self._testcase_reports:
            self._testcase_reports[testcaseidx] = []
        self._testcase_reports[testcaseidx].append(testcase_report)

        self._current_testcaseidx = testcaseidx
        self._increment_testcase()
        self._current_testcase_report = testcase_report

    def _increment_testcase(self) -> None:
        self._current_testcase_attempt += 1

    def set_risk_analysis(self, risk_analysis: str) -> None:
        self._risk_analysis = risk_analysis

    def set_test_subject(self, test_subject: str) -> None:
        self._test_subject = test_subject

    def set_testcases(self, testcases: list) -> None:
        self._testcases = testcases

    def previous_attacks(self, testcaseidx: str) -> list:
        reports = self._testcase_reports.get(testcaseidx, [])
        return [r.strategy_design_report for r in reports if r.strategy_design_report is not None and not r.was_compromised]

    @property
    def attacks_stats(self) -> dict:
        reports = list(chain.from_iterable(self._testcase_reports.values()))
        attacks = [r.strategy_design_report["selected attack"] for r in reports]

        attack_counts = {}
        for attack in attacks:
            attack_counts[attack] = attack_counts.get(attack, 0) + 1

        return attack_counts

    @property
    def total_compromised(self) -> int:
        reports =  list(chain.from_iterable(self._testcase_reports.values()))
        return len([r.strategy_design_report for r in reports if r.was_compromised])

    @property
    def total_test_attempts(self) -> int:
        return self._current_testcase_attempt

    @property
    def current_testcaseidx(self) -> str:
        return self._current_testcaseidx

    @property
    def current_testcase_report(self) -> TestCaseReport:
        return self._current_testcase_report
