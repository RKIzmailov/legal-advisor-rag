import yaml
import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

# Получение переменных из окружения
api_key = os.getenv('API_KEY')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

# Создание словаря для хранения этих данных
config_data = {
    'api_key': api_key,
    'database': {
        'host': db_host,
        'port': db_port
    }
}

# Запись данных в config.yaml
with open('config.yaml', 'w') as yaml_file:
    yaml.dump(config_data, yaml_file, default_flow_style=False)

print("Переменные успешно записаны в config.yaml")
