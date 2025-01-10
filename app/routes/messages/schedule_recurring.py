from fastapi import APIRouter, HTTPException
from app.scheduler import scheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.services.send_message_instant import send_message_instant
from app.models.RecurringScheduleRequest import RecurringScheduleRequest
import logging
import uuid

router = APIRouter()

@router.post("/schedule/recurring", status_code=201, tags=["Messages"],
    summary="Agendar mensagem em intervalos",
    description="Agenda mensagens recorrentes para serem enviadas em intervalos específicos.")
def schedule_recurring_message(request: RecurringScheduleRequest):
    """
    Agenda mensagens recorrentes para serem enviadas em intervalos específicos.
    """
    logging.info(f"Agendando mensagem recorrente para {request.recipient} com frequência {request.frequency}.")
    
    interval_mapping = {
        "daily": {"days": 1},
        "weekly": {"weeks": 1},
        "monthly": {"weeks": 4},  # Simulação para 1 mês
    }
    
    if request.frequency not in interval_mapping:
        raise HTTPException(status_code=400, detail="Frequência inválida")

    schedule_id = str(uuid.uuid4())
    trigger_args = interval_mapping[request.frequency]
    start_time = request.start_time

    try:
        scheduler.add_job(
            send_message_instant,
            trigger=IntervalTrigger(start_date=start_time, end_date=request.end_time, **trigger_args),
            id=schedule_id,
            kwargs={
                "recipient": request.recipient,
                "message": request.message,
            }
        )

        logging.info(f"Mensagem recorrente agendada com sucesso - ID: {schedule_id}")
        return {
            "status": "success",
            "message": "Mensagem recorrente agendada com sucesso.",
            "schedule_id": schedule_id
        }
    except Exception as e:
        logging.error(f"Erro ao agendar mensagem recorrente: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao agendar mensagem recorrente")
