from fastapi import FastAPI
from backend.routes.event_routes import router
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI(
    title="AI Event Planner",
    description="An AI-powered event planning application",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return{
        "message":"Welcome to AI Event Planner!"
    }

app.include_router(router,prefix='/event',tags=["Events"])

