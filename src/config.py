import yaml
from pydantic import BaseModel

class DataConfig(BaseModel):
    raw_path: str
    processed_path: str

class AppConfig(BaseModel):
    data: DataConfig

def load_config(path: str = "config/config.yaml") -> AppConfig:
    with open(path, "r") as f:
        config_dict = yaml.safe_load(f)
    return AppConfig(**config_dict)

config = load_config()