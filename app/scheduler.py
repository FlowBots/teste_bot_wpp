from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.date import DateTrigger
from app.config import DATABASE_URL
import logging

scheduler = BackgroundScheduler(
    jobstores={"default": SQLAlchemyJobStore(url=DATABASE_URL)}
)
scheduler.start()

def add_job(job_id, func, trigger_date, **kwargs):
    logging.info(f"Adicionando job ao agendador - ID: {job_id}, Data: {trigger_date}")
    scheduler.add_job(func, trigger=DateTrigger(run_date=trigger_date), id=job_id, kwargs=kwargs)

def shutdown_scheduler():
    logging.info("Encerrando o agendador.")
    scheduler.shutdown()
