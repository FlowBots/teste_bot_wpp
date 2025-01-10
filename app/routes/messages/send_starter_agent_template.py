from fastapi import APIRouter, HTTPException
from app.models.SendStarterAgentTemplate import TemplateRequest
from app.services.send_starter_agent_service import send_starter_agent_template

router = APIRouter()


@router.post("/send-starter-agent")
def send_starter_agent(request: TemplateRequest):
    """
    Endpoint para enviar o template `starter_agent`.
    """
    try:
        response = send_starter_agent_template(request.recipient)
        return {"status": "success", "response": response}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
