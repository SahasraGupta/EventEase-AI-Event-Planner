
from fastapi import APIRouter

from backend.schemas.event_schema import (
    EventRequest,
    EventRecommendations
)

from agent.agent import run_agent


router = APIRouter()


@router.post(
    "/requirements",
    response_model=EventRecommendations
)
def get_event_requirements(event: EventRequest):

    response = run_agent(event.user_query)

    return response
