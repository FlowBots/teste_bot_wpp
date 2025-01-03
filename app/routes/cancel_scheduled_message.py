from fastapi import APIRouter, HTTPException
from app.scheduler import scheduler
import logging

router = APIRouter()

@router.delete("/scheduled-messages/{schedule_id}", status_code=200, tags=["Messages"],
    summary="Deletar mensagem agendada",
    description="Faz a exclusão de mensagem agendada",)
def cancel_scheduled_message(schedule_id: str):
    """
    Cancela uma mensagem agendada pelo ID.
    """
    try:
        job = scheduler.get_job(schedule_id)
        if not job:
            logging.warning(f"Mensagem agendada com ID {schedule_id} não encontrada.")
            raise HTTPException(status_code=404, detail="Mensagem agendada não encontrada")

        job.remove()
        logging.info(f"Mensagem agendada com ID {schedule_id} cancelada com sucesso.")
        return {
            "status": "success",
            "message": f"Mensagem agendada com ID {schedule_id} cancelada com sucesso."
        }
    except Exception as e:
        logging.error(f"Erro ao cancelar mensagem agendada: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Erro ao cancelar mensagem agendada"
        )
