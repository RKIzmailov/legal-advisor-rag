import yaml

config_path = '..\\config.yaml'

def load_config(yaml_file: str = config_path) -> dict:
    
    if not yaml_file.endswith(".yaml"):
        raise TypeError("Not yaml file")
    
    # Load the config file
    with open(yaml_file, 'rt') as f:
        config = yaml.safe_load(f.read())
        
    return config
