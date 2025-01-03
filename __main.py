from fastapi import FastAPI
from app.scheduler import shutdown_scheduler
from app.routes import webhook, send_template_message, logs, schedule_message, send_instant_message, update_token, current_token, expiration_time

app = FastAPI(title="Chatbot WhatsApp Scheduler")

# Incluindo rotas
app.include_router(current_token.router)
app.include_router(expiration_time.router)
app.include_router(logs.router)
app.include_router(schedule_message.router)
app.include_router(send_instant_message.router)
app.include_router(send_template_message.router)
app.include_router(update_token.router)
app.include_router(webhook.router)

@app.on_event("shutdown")
def shutdown():
    shutdown_scheduler()
