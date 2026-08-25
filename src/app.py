"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.

Type Contracts:
- Activities: Dict[str, Activity]
- Activity: TypedDict with description, schedule, max_participants, participants
"""

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
    name="static"
)

class Activity(TypedDict):
    """Typed dictionary representing an extracurricular activity.
    
    Attributes:
        description: Detailed description of the activity
        schedule: Meeting schedule as a string
        max_participants: Maximum number of participants allowed
        participants: List of student emails currently signed up
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
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root() -> RedirectResponse:
    """Root endpoint that redirects to the static frontend.
    
    Returns:
        RedirectResponse: HTTP redirect to the static index.html page
    """
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities() -> Dict[str, Activity]:
    """Retrieve all available extracurricular activities.
    
    Returns:
        Dict[str, Activity]: Dictionary mapping activity names to their details
    """
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str) -> Dict[str, str]:
    """Sign up a student for an extracurricular activity.
    
    Args:
        activity_name: Name of the activity to sign up for
        email: Student's email address
        
    Returns:
        Dict[str, str]: Confirmation message
        
    Raises:
        HTTPException: 404 if activity doesn't exist
    """
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
