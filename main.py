from fastapi import FastAPI
from app.scheduler import shutdown_scheduler
from app.routes import webhook, messages, logs

app = FastAPI(title="Chatbot WhatsApp Scheduler")

# Incluindo rotas
app.include_router(webhook.router)
app.include_router(messages.router)
app.include_router(logs.router)

@app.on_event("shutdown")
def shutdown():
    shutdown_scheduler()
