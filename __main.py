from fastapi import FastAPI
from app.scheduler import shutdown_scheduler
from app.routes import *

app = FastAPI(title="Chatbot WhatsApp Scheduler")

# Incluindo rotas
app.include_router(current_token_router)
app.include_router(expiration_time_router)
app.include_router(logs_router)
app.include_router(schedule_message_router)
app.include_router(send_instant_message_router)
app.include_router(send_message_template_router)
app.include_router(update_token_router)
app.include_router(webhook_router)
app.include_router(send_hello_word_router)


@app.on_event("shutdown")
def shutdown():
    shutdown_scheduler()
