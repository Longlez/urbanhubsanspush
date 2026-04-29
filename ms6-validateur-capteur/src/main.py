from fastapi import FastAPI

from src.adapters.api.routes import router

app = FastAPI(
    title="MS6 Validateur Capteur",
    version="1.0.0",
    description="Microservice de validation des données capteurs et de fenêtres de trafic.",
)

app.include_router(router)
