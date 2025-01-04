from fastapi import APIRouter, HTTPException
from app.models.ScheduleMessageRequest import ScheduleMessageRequest
from app.services.send_message_scheduled import send_message_scheduled
from apscheduler.triggers.date import DateTrigger
from app.scheduler import scheduler
import logging
import uuid

router = APIRouter()

# Endpoint para agendamento
@router.post("/schedule-message", status_code=201, tags=["Messages"],
    summary="Agendar mensagem",
    description="Faz o agendamento de mensagem por data e hora e destino",)
def schedule_message(
    request: ScheduleMessageRequest,
    # api_key: str = Depends(authenticate)
):
    try:
        schedule_id = str(uuid.uuid4())
        logging.info(
            f"Agendando mensagem - ID: {schedule_id}, Destinatário: {request.recipient}, Horário: {request.send_time}"
        )
        scheduler.add_job(
            send_message_scheduled,
            trigger=DateTrigger(run_date=request.send_time),
            id=schedule_id,
            kwargs={
                "job_id": schedule_id,
                "recipient": request.recipient,
                "message": request.message,
            },
        )
        logging.info(
            f"Mensagem agendada com sucesso - ID: {schedule_id} HORÁRIO: {request.send_time}"
        )
        return {
            "status": "success",
            "message": "Mensagem agendada com sucesso",
            "schedule_id": schedule_id,
        }
    except Exception as e:
        logging.error(f"Erro ao agendar mensagem: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao agendar mensagem")