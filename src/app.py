from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from typing import Dict, List, TypedDict
import os
from pathlib import Path

app = FastAPI(
    title="Mergington High School API",
    description="API for viewing and signing up for extracurricular activities"
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
        participants: List of student emails currently signed up.
    """
    description: str
    schedule: str
    max_participants: int
    participants: List[str]


# In-memory activity database
activities: Dict[str, Activity] = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
    },
}


@app.get("/")
def root() -> RedirectResponse:
    """Root endpoint that redirects to the static frontend.
    
    Returns:
        RedirectResponse: HTTP redirect to the static index.html page.
    """
    return RedirectResponse(url="/static/index.html")


@app.get("/activities", response_model=Dict[str, Activity])
def get_activities() -> Dict[str, Activity]:
    """Return the full dictionary of activities.
    
    Returns:
        Dict[str, Activity]: Mapping from activity name to its details.
    """
    return activities


@app.post("/activities/{activity_name}/signup", response_model=Activity)
def signup_for_activity(activity_name: str, email: str) -> Activity:
    """Sign up a student for a given activity.
    
    Args:
        activity_name: The name of the activity to join.
        email: Student's email address.
    
    Returns:
        Activity: The updated activity record after successful sign‑up.
    
    Raises:
        HTTPException: 404 if the activity does not exist.
        HTTPException: 400 if the activity is full or the email is already registered.
    """
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity has reached maximum capacity")

    activity["participants"].append(email)
    return activity
