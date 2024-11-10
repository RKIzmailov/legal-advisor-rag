import yaml
from pathlib import Path

config_path = "..\..\config.yaml"
config_path = Path(__file__).resolve().parent.parent.parent / "config.yaml"

def load_config(yaml_file: Path = config_path) -> dict:
    if yaml_file.suffix != ".yaml":
        raise TypeError("Not a YAML file")
    
    # Load the config file
    with yaml_file.open('rt') as f:
        config = yaml.safe_load(f.read())
        
    return config