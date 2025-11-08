import os
import importlib.util

from typing import List

def load_attack(module_name: str, file_path : str):

    base_dir = os.path.dirname(os.path.abspath(__file__))  # path to this script
    config_path = os.path.join(base_dir, "..", file_path)
    config_path = os.path.abspath(config_path)
    class_path = os.path.join(config_path, f"{module_name}.py")

    spec = importlib.util.spec_from_file_location(module_name, class_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    model_class = getattr(module, module_name)

    return model_class()

def get_attacks(folder_path: str) -> List[str]:
    
    attack_types = [
        os.path.splitext(f)[0]  # removes the .py extension
        for f in os.listdir(folder_path)
        if f.endswith('.py') and os.path.isfile(os.path.join(folder_path, f))
    ]
    return attack_types