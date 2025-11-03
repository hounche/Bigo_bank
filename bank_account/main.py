# main.py
from fastapi import FastAPI
from infrastructure.api.routes import router as accounts_router
from infrastructure.persistence.db import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# Créer les tables au démarrage
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bank Account Hexagonal API")

# Configuration CORS (front en Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en prod -> limiter au domaine front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes de ton API
app.include_router(accounts_router)

@app.get("/")
def root():
    return {"message": "API Bank Account en ligne 🚀"}
