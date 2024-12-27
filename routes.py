from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse
from models import ScheduleMessageRequest
from utils import send_message
from apscheduler.triggers.date import DateTrigger
import uuid
import logging

router = APIRouter()

@router.post("/schedule-message", status_code=201)
def schedule_message(request: ScheduleMessageRequest):
    try:
        schedule_id = str(uuid.uuid4())
        logging.info(f"Agendando mensagem - ID: {schedule_id}, Destinatário: {request.recipient}, Horário: {request.send_time}")
        scheduler.add_job(
            send_message,
            trigger=DateTrigger(run_date=request.send_time),
            id=schedule_id,
            kwargs={
                "job_id": schedule_id,
                "recipient": request.recipient,
                "message": request.message,
            },
        )
        logging.info(f"Mensagem agendada com sucesso - ID: {schedule_id}")
        return {
            "status": "success",
            "message": "Mensagem agendada com sucesso",
            "schedule_id": schedule_id,
        }
    except Exception as e:
        logging.error(f"Erro ao agendar mensagem: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao agendar mensagem")

@router.get("/logs", status_code=200)
def get_logs(level: str = Query("INFO"), keyword: str = Query(None), lines: int = Query(50)):
    try:
        with open("app_logs.log", "r") as log_file:
            logs = log_file.readlines()

        filtered_logs = [log for log in logs if f"- {level.upper()} -" in log]
        if keyword:
            filtered_logs = [log for log in filtered_logs if keyword in log]
        return {"logs": filtered_logs[-lines:]}
    except Exception as e:
        logging.error(f"Erro ao acessar os logs: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao acessar os logs")

@router.get("/webhook")
async def validate_webhook(request: Request):
    params = request.query_params
    hub_mode = params.get("hub.mode")
    hub_verify_token = params.get("hub.verify_token")
    hub_challenge = params.get("hub.challenge")

    if hub_mode == "subscribe" and hub_verify_token == "12345":
        return PlainTextResponse(hub_challenge)
    else:
        return {"error": "Token de verificação inválido"}
