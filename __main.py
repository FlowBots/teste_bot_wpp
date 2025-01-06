from fastapi import FastAPI
from app.scheduler import shutdown_scheduler

# Importação de rotas
from app.routes.logs import *
from app.routes.messages import *
from app.routes.meta import *

from app.routes import manage_templates, list_templates, check_user_status # ROTAS em desenvolvimento

app = FastAPI(title="Chatbot WhatsApp Scheduler")

# Incluindo rotas
app.include_router(schedule_recurring_router) # FUNCIONAMENTO OK PORÉM AINDA PRECISA MAIS TESTES, NO MOMENTO PARA TESTES MANDA HELLO WORLD!!
app.include_router(send_bulk_messages_router) # FUNCIONAMENTO OK, NO MOMENTO PARA TESTES MANDA HELLO WORLD!!
#app.include_router(manage_templates_router) # NÃO CONSEGUI VERIFICAR O FUNCIONAMENTO DESSE ENDPOINT
#app.include_router(list_templates_router) # NÃO CONSEGUI VERIFICAR O FUNCIONAMENTO DESSE ENDPOINT
app.include_router(cancel_scheduled_message_router)
app.include_router(list_scheduled_messages_router)
#app.include_router(check_user_status_router) # NÃO CONSEGUI VERIFICAR O FUNCIONAMENTO DESSE ENDPOINT
app.include_router(current_token_router)
app.include_router(expiration_time_router)
app.include_router(logs_router)
app.include_router(schedule_message_router)
app.include_router(send_instant_message_router)
app.include_router(send_template_message_router)
app.include_router(update_token_router)
app.include_router(webhook_router)

@app.on_event("shutdown")
def shutdown():
    shutdown_scheduler()
