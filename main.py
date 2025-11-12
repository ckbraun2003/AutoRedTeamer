import logging
import datetime
import os

from src.CaseMemory import CaseMemory
from src.PromptManager import PromptManager
from src.LLMClient import LLMClient
from src.AutoRedTeamer import AutoRedTeamer

from src._configs import NodeConfigs
from src._utils import print_red_team_summary

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
    num_testcases = 10
    max_test_iterations = 3

    test_model = LLMClient(llm_logger, model_name=test_model_name, temperature=1.0)

    client = LLMClient(llm_logger, model_name="mixtral", temperature=0.5)
    manager = PromptManager()
    memory = CaseMemory()

    auto_red_teamer = AutoRedTeamer(NodeConfigs)

    try:
        start_time = datetime.datetime.now()
        finished = auto_red_teamer.run_red_team_event(test_subject=test_subject,
                                       llm_client=client,
                                       llm_test=test_model,
                                       prompt_manager=manager,
                                       case_memory=memory,
                                       logger=system_logger,
                                       num_testcases=num_testcases,
                                       max_test_iterations=max_test_iterations)

        end_time = datetime.datetime.now()

        if finished:

            total_compromised = memory.total_compromised
            successful_test_attempts = memory.successful_test_attempts
            failed_test_attempts = memory.failed_test_attempts
            total_test_attempts = memory.total_test_attempts
            total_llm_calls = client.llm_calls + test_model.llm_calls
            total_time_taken = (end_time - start_time).total_seconds()
            attack_stats = memory.attacks_stats


            print_red_team_summary(test_subject=test_subject,
                                   test_model_name=test_model_name,
                                   total_compromised=total_compromised,
                                   total_test_attempts=total_test_attempts,
                                   failed_test_attempts=failed_test_attempts,
                                   successful_test_attempts=successful_test_attempts,
                                   total_llm_calls=total_llm_calls,
                                   total_time_taken=total_time_taken,
                                   start_time=start_time,
                                   end_time=end_time,
                                   attack_stats=attack_stats)

        else:
            system_logger.error(f"Error occurred -- (finished={finished})")

    except RuntimeError as e:
        system_logger.error(f"Error occurred -- {e}")

