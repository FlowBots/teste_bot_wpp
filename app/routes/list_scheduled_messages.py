from fastapi import APIRouter, HTTPException
from app.scheduler import scheduler
import logging

router = APIRouter()

@router.get("/scheduled-messages", status_code=200)
def list_scheduled_messages():
    """
    Lista todas as mensagens agendadas no sistema.
    """
    try:
        jobs = scheduler.get_jobs()
        logging.info(f"Recuperando {len(jobs)} mensagens agendadas.")
        
        # Formata os dados das mensagens agendadas
        scheduled_messages = []
        for job in jobs:
            scheduled_messages.append({
                "id": job.id,
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
                "func_name": job.func_ref,  # Nome da função que será executada
                "args": job.args,
                "kwargs": job.kwargs,
            })

        return {"status": "success", "scheduled_messages": scheduled_messages}
    except Exception as e:
        logging.error(f"Erro ao listar mensagens agendadas: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Erro ao listar mensagens agendadas"
        )
