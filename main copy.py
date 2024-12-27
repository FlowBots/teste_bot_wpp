from fastapi import FastAPI
from routes import router
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import logging
from dotenv import load_dotenv
import os
import certifi

# Configuração de logging
LOG_FILE = "app_logs.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
load_dotenv()

# Configurações iniciais
DATABASE_URL = os.getenv("DATABASE_URL")
scheduler = BackgroundScheduler(jobstores={"default": SQLAlchemyJobStore(url=DATABASE_URL)})
scheduler.start()

# Inicialização do FastAPI
app = FastAPI(title="Chatbot WhatsApp Scheduler")
app.include_router(router)

@app.on_event("shutdown")
def shutdown():
    logging.info("Aplicação finalizando. Scheduler será desligado.")
    scheduler.shutdown()
