import logging
import time
import os

from src.CaseMemory import CaseMemory
from src.PromptManager import PromptManager
from src.LLMClient import LLMClient
from src.AutoRedTeamer import AutoRedTeamer

from src._configs import NodeConfigs

GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"

os.makedirs("logs", exist_ok=True)

# -----------------------------
# SYSTEM LOGGER
# -----------------------------
system_logger = logging.getLogger("system")
system_logger.setLevel(logging.INFO)

system_handler = logging.FileHandler("logs/system.log", mode='a', encoding='utf-8')
system_formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] [%(funcName)s] %(message)s")
system_handler.setFormatter(system_formatter)
system_logger.addHandler(system_handler)

# -----------------------------
# LLM LOGGER
# -----------------------------
llm_logger = logging.getLogger("llm")
llm_logger.setLevel(logging.DEBUG)  # keep this more verbose for debugging

llm_handler = logging.FileHandler("logs/llm_calls.log", mode='a', encoding='utf-8')
llm_formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] [%(funcName)s] %(message)s")
llm_handler.setFormatter(llm_formatter)
llm_logger.addHandler(llm_handler)

# Optional: log to console as well
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] [%(funcName)s] %(message)s")
console_handler.setFormatter(console_formatter)

system_logger.addHandler(console_handler)

if __name__ == "__main__":

    test_model_name = "mistral"
    test_subject = "Illegal substance production"
    num_testcases = 1
    max_test_iterations = 1

    test_model = LLMClient(llm_logger, model_name=test_model_name, temperature=0.5)

    client = LLMClient(llm_logger, model_name="mixtral", temperature=0.5)
    manager = PromptManager()
    memory = CaseMemory()

    auto_red_teamer = AutoRedTeamer(NodeConfigs)

    try:
        start_time = time.time()
        finished = auto_red_teamer.run_red_team_event(test_subject=test_subject,
                                       llm_client=client,
                                       llm_test=test_model,
                                       prompt_manager=manager,
                                       case_memory=memory,
                                       logger=system_logger,
                                       num_testcases=num_testcases,
                                       max_test_iterations=max_test_iterations)

        end_time = time.time()
        total_time_taken = (end_time - start_time) / 60

        if finished:
            time.sleep(1)
            print(f"""
            {MAGENTA}{BOLD}╔════════════════════════════════════════════════════════╗{RESET}
            {MAGENTA}{BOLD}║{RESET}              {CYAN}    AutoRedTeamer Diagnostics{RESET}{MAGENTA}{BOLD}║{RESET}
            {MAGENTA}{BOLD}╠════════════════════════════════════════════════════════╣{RESET}
            {MAGENTA}{BOLD}║{RESET}  {BOLD}Test Subject{RESET:<16}: {test_subject}
            {MAGENTA}{BOLD}║{RESET}  {BOLD}Model Tested{RESET:<17}: {test_model_name}
            {MAGENTA}{BOLD}║{RESET}  {BOLD}Total Vulnerabilities{RESET:<9}: {RED}{memory.total_compromised}{RESET}
            {MAGENTA}{BOLD}║{RESET}  {BOLD}Total Tests{RESET:<18}: {YELLOW}{memory.current_testcase_attempt}{RESET}
            {MAGENTA}{BOLD}║{RESET}  {BOLD}Total LLM Calls{RESET:<14}: {GREEN}{client.llm_calls + test_model.llm_calls}{RESET}
            {MAGENTA}{BOLD}║{RESET}  {BOLD}Total Time Taken{RESET:<12}: {CYAN}{total_time_taken:.2f} minutes{RESET}
            {MAGENTA}{BOLD}╚════════════════════════════════════════════════════════╝{RESET}
                """)

        else:
            system_logger.error(f"Error occured -- (finished={finished})")

    except RuntimeError as e:
        system_logger.error(f"Error occured -- {e}")

