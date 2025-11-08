from dataclasses import dataclass

@dataclass
class CaseReport:
    testcaseidx: str
    strategy_design_report: str
    response_report: str
    evaluation_report: str
    relevancy_report: str

class CaseMemory:
    def __init__(self):

        self._current_test_case = 0

        self._initial_input = None
        self._risk_analysis = None
        self._test_cases = None

        self._strategy_design_reports = {}
        self._response_reports = {}
        self._evaluation_reports = {}
        self._relevancy_reports = {}

    def add_case_reports(self, idx : str, case_report: CaseReport):

        self._strategy_design_reports[idx] = case_report["strategy_design_report"]
        self._response_reports[idx] = case_report["response_report"]
        self._evaluation_reports[idx] = case_report["evaluation_report"]
        self._relevancy_reports[idx] = case_report["relevancy_report"]

        self._increment_test_case()

    def _increment_test_case(self):
        self._current_test_case += 1

    @property
    def current_test_case(self):
        return self._current_test_case

    @property
    def attack_memory(self):
        return self._evaluation_reports

