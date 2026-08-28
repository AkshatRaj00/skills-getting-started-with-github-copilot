from fastapi import FastAPI, HTTPException, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from typing import Dict, List, TypedDict, Optional
from pydantic import BaseModel, EmailStr, Field
import os
from pathlib import Path

app = FastAPI(
    title="Mergington High School API",
    description="API for viewing and signing up for extracurricular activities",
)

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(Path(__file__).parent, "static")),
    name="static",
)

class Activity(TypedDict):
    """Typed dictionary representing an extracurricular activity.
    
    Attributes:
        description: Detailed description of the activity.
        schedule: Meeting schedule as a string (e.g., "Mondays, 3:00 PM").
        max_participants: Maximum number of participants allowed (non-negative integer).
        participants: List of participant email addresses (validated as EmailStr).
    """
    description: str
    schedule: str
    max_participants: int
    participants: List[EmailStr]

class ActivityModel(BaseModel):
    """Pydantic model mirroring the Activity TypedDict for FastAPI response validation."""
    description: str = Field(..., description="Detailed description of the activity.")
    schedule: str = Field(..., description="Meeting schedule (e.g., 'Mondays, 3:00 PM').")
    max_participants: int = Field(..., ge=0, description="Maximum number of participants allowed.")
    participants: List[EmailStr] = Field(default_factory=list, description="List of participant email addresses.")

# In-memory activity database
activities: Dict[str, Activity] = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": [
            EmailStr("michael@mergington.edu"),
            EmailStr("daniel@mergington.edu"),
        ],
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": [
            EmailStr("emma@mergington.edu"),
            EmailStr("sophia@mergington.edu"),
        ],
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, and Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 25,
        "participants": [
            EmailStr("olivia@mergington.edu"),
            EmailStr("ava@mergington.edu"),
        ],
    },
}

@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """Redirect to the static index.html page."""
    return RedirectResponse(url="/static/index.html")

@app.get("/activities", response_model=Dict[str, ActivityModel])
def get_activities() -> Dict[str, ActivityModel]:
    """Retrieve all activities.
    
    Returns:
        Dict[str, ActivityModel]: A dictionary of activities with their names as keys.
    """
    return activities

@app.post("/activities/signup")
def signup_for_activity(activity_name: str, email: EmailStr) -> Dict[str, str]:
    """Sign up for an activity.
    
    Args:
        activity_name: Name of the activity to sign up for.
        email: Email address of the participant.
    
    Returns:
        Dict[str, str]: A dictionary with a success message.
    
    Raises:
        HTTPException: If the activity is not found or is full.
    """
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    activity = activities[activity_name]
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")
    
    activity["participants"].append(email)
    return {"message": f"Successfully signed up for {activity_name}"}
