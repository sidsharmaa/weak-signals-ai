# src/config.py
import yaml
from pydantic import BaseModel
from pathlib import Path

# Define the project's root directory dynamically.
# Path(__file__) is the path to this file (src/config.py).
# .parent is the directory of this file (src/).
# .parent.parent is the parent of that directory (the project root).
PROJECT_ROOT = Path(__file__).resolve().parent.parent

class DataConfig(BaseModel):
    """Pydantic model for data paths."""
    raw_path: str
    processed_path: str

class AppConfig(BaseModel):
    """Main application configuration model."""
    data: DataConfig

def load_config() -> AppConfig:
    """
    Loads, parses, and validates the application configuration from the root directory.
    """
    config_path = PROJECT_ROOT / "config/config.yaml"
    with open(config_path, "r") as f:
        config_dict = yaml.safe_load(f)
    
    return AppConfig(**config_dict)

# Create a single config instance to be imported by other modules
config = load_config()