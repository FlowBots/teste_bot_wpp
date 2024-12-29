import os
from dotenv import load_dotenv
import pytz
import logging

load_dotenv()

# Timezone
BRASILIA_TZ = pytz.timezone("America/Sao_Paulo")

# Configurações de Log
LOG_FILE = "app_logs.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),  # Continua exibindo no console
    ],
)
logging.info("Logging configurado. No config.py")

# Configurações de Banco e API
DATABASE_URL = os.getenv("DATABASE_URL")
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

# Verificação de variáveis de ambiente obrigatórias
if not all([ACCESS_TOKEN, APP_ID, VERIFY_TOKEN]):
    raise ValueError("Variáveis de ambiente não configuradas corretamente.")
