from fastapi import APIRouter, HTTPException, Query
import logging

router = APIRouter()

# Configuração de logging
LOG_FILE = "app_logs.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),  # Continua exibindo no console
    ],
)

logging.info("Logging configurado.")

logging.basicConfig(level=logging.INFO)

@router.get("/logs", status_code=200, tags=["Logs"],
    summary="Logs dos Endpoints",
    description="Retorna os logs armazenados no arquivo com filtros opcionais.",)
def get_logs(
    level: str = Query("INFO", description="Nível do log (INFO, ERROR, DEBUG, etc.)"),
    keyword: str = Query(
        None, description="Palavra-chave para filtrar os logs (opcional)"
    ),
    lines: int = Query(50, description="Número de linhas de log para retornar"),
):
    """
    Retorna os logs armazenados no arquivo com filtros opcionais.
    """
    logging.info(
        f"Logs acessados - Nível: {level}, Palavra-chave: {keyword}, Linhas: {lines}"
    )
    try:
        with open(LOG_FILE, "r") as log_file:
            logs = log_file.readlines()

        # Filtro por nível de log
        filtered_logs = [log for log in logs if f"- {level.upper()} -" in log]

        # Filtro por palavra-chave, se especificado
        if keyword:
            filtered_logs = [log for log in filtered_logs if keyword in log]

        # Retorna apenas as últimas `lines` linhas
        return {"logs": filtered_logs[-lines:]}
    except Exception as e:
        logging.error(f"Erro ao acessar os logs: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao acessar os logs")
