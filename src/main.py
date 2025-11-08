from src._memory import Memory
from src._manager import PromptManager
from src._llmclient import LLMClient


if __name__ == "__main__":
    manager = PromptManager()
    client = LLMClient(model_name="mixtral", temperature=0.5)
    memory = Memory()
