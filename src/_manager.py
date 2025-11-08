import yaml
import time

from pathlib import Path
from jinja2 import Template
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class PromptVersion:
    """Represents a single prompt version."""
    template: str
    defaults: Dict[str, str] = field(default_factory=dict)


@dataclass
class Prompt:
    """Represents a full prompt with multiple versions."""
    name: str
    versions: Dict[str, PromptVersion]


class PromptManager:
    """
    Loads and manages prompt templates from YAML files.
    Supports versioning, default values, and Jinja2 templating.
    """

    def __init__(self, prompt_dir: str = "_prompts", hot_reload: bool = False):
        self.prompt_dir = Path(prompt_dir)
        self.hot_reload = hot_reload
        self._cache: Dict[str, Prompt] = {}
        self._last_load_time = 0
        self.reload_interval = 5  # seconds between hot reload checks
        self._load_all()

    def _load_all(self):
        """Loads all YAML prompts from disk into memory."""
        self._cache.clear()
        for file in self.prompt_dir.glob("*.yaml"):
            with open(file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                versions = {
                    name: PromptVersion(**version)
                    for name, version in data.get("versions", {}).items()
                }
                prompt = Prompt(
                    name=data["name"],
                    versions=versions,
                )
                self._cache[prompt.name] = prompt
        self._last_load_time = time.time()

    def _maybe_reload(self):
        """Reload prompts if hot_reload is enabled and interval has passed."""
        if not self.hot_reload:
            return
        if time.time() - self._last_load_time > self.reload_interval:
            self._load_all()

    def list_prompts(self):
        """Return a list of all loaded prompt names."""
        self._maybe_reload()
        return list(self._cache.keys())

    def get(self, name: str, version: str = "v1") -> PromptVersion:
        """Retrieve a specific prompt version."""
        self._maybe_reload()
        prompt = self._cache.get(name)
        if not prompt:
            raise KeyError(f"Prompt '{name}' not found in {self.prompt_dir}")
        if version not in prompt.versions:
            raise KeyError(f"Version '{version}' not found for prompt '{name}'")
        return prompt.versions[version]

    def render(self, name: str, version: str = "v1", **kwargs) -> str:
        """Render a prompt template with Jinja2 variables injected."""
        prompt_version = self.get(name, version)
        vars = {**prompt_version.defaults, **kwargs}
        template = Template(prompt_version.template)
        return template.render(**vars)
