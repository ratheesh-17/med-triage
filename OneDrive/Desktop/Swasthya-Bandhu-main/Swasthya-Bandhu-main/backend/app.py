from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from config.database import init_db
from controller.controllers import router
from startup_fix import auto_fix_appointment_statuses

app = FastAPI(title="Med Triage", version="3.0.0", redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
def startup():
    try:
        init_db()
        auto_fix_appointment_statuses()
    except Exception as e:
        # If DB is not available in the local environment, log and continue so health endpoints work
        print(f"Warning: could not initialize database on startup: {e}")

@app.get("/")
def root():
    return {"message": "Swasthya Bandhu API", "version": "3.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
