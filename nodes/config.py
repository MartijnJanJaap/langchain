from pathlib import Path
from dataclasses import dataclass

@dataclass
class AppConfig:
    workspace_path: Path
    prompts_dir: Path
    llm_model: str
    llm_api_key: str
    llm_base_url: str | None = None
