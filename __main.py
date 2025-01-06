from fastapi import FastAPI
from app.scheduler import shutdown_scheduler
from app.routes.meta import webhook, update_token, expiration_time, current_token
from app.routes.messages import schedule_message, cancel_scheduled_message, list_scheduled_messages, schedule_recurring, send_bulk_messages, send_instant_message, send_template_message
from app.routes.logs import logs

from app.routes import manage_templates, list_templates, check_user_status # ROTAS em desenvolvimento

app = FastAPI(title="Chatbot WhatsApp Scheduler")

# Incluindo rotas
app.include_router(schedule_recurring.router) # FUNCIONAMENTO OK PORÉM AINDA PRECISA MAIS TESTES, NO MOMENTO PARA TESTES MANDA HELLO WORLD!!
app.include_router(send_bulk_messages.router) # FUNCIONAMENTO OK, NO MOMENTO PARA TESTES MANDA HELLO WORLD!!
#app.include_router(manage_templates.router) # NÃO CONSEGUI VERIFICAR O FUNCIONAMENTO DESSE ENDPOINT
#app.include_router(list_templates.router) # NÃO CONSEGUI VERIFICAR O FUNCIONAMENTO DESSE ENDPOINT
app.include_router(cancel_scheduled_message.router)
app.include_router(list_scheduled_messages.router)
#app.include_router(check_user_status.router) # NÃO CONSEGUI VERIFICAR O FUNCIONAMENTO DESSE ENDPOINT
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
