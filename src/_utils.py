import os
import importlib.util

def load_attack(module_name: str, path: str = "attacks"):

    base_dir = os.path.dirname(os.path.abspath(__file__))  # path to this script
    config_path = os.path.join(base_dir, "..", path)
    config_path = os.path.abspath(config_path)
    class_path = os.path.join(config_path, f"{module_name}.py")

    spec = importlib.util.spec_from_file_location(module_name, class_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    model_class = getattr(module, module_name)

    return model_class()