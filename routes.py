"""
Agentic AI Team Former - API Routes
File: routes.py
Description: FastAPI route definitions for student management and team formation.
"""

from fastapi import APIRouter, HTTPException
from typing import List

from models import Student, TeamFormationRequest, FormationResult
from database import STUDENTS_DB, seed_initial_students, load_dataset_students
from agent import AgenticTeamFormer

router = APIRouter()


# --- Student CRUD Endpoints ---

@router.get("/students", response_model=List[Student])
def get_students():
    """Returns the list of all registered students."""
    return list(STUDENTS_DB.values())


@router.post("/students", response_model=Student)
def create_student(student: Student):
    """Adds a new student to the roster."""
    if student.id in STUDENTS_DB:
        raise HTTPException(status_code=400, detail="Student ID already exists")
    STUDENTS_DB[student.id] = student
    return student


@router.put("/students/{student_id}", response_model=Student)
def update_student(student_id: str, student: Student):
    """Updates an existing student profile."""
    if student_id not in STUDENTS_DB:
        raise HTTPException(status_code=404, detail="Student not found")
    STUDENTS_DB[student_id] = student
    return student


@router.delete("/students/{student_id}")
def delete_student(student_id: str):
    """Removes a student from the roster."""
    if student_id not in STUDENTS_DB:
        raise HTTPException(status_code=404, detail="Student not found")
    del STUDENTS_DB[student_id]
    return {"message": f"Student {student_id} deleted successfully"}


@router.post("/students/reset")
def reset_students():
    """Resets student list back to standard seed dataset."""
    STUDENTS_DB.clear()
    seed_initial_students()
    load_dataset_students(limit=100)
    return {"message": "Roster reset to seed dataset", "total": len(STUDENTS_DB)}


# --- Team Formation Endpoint ---

@router.post("/form-teams", response_model=FormationResult)
def form_teams(req: TeamFormationRequest):
    """Triggers the Agentic AI Team Matchmaking Pipeline."""
    students_list = list(STUDENTS_DB.values())
    if not students_list:
        raise HTTPException(status_code=400, detail="No students available in the roster.")

    former = AgenticTeamFormer(
        students=students_list,
        team_size=req.team_size,
        w_skills=req.weight_skills,
        w_interests=req.weight_interests,
        w_synergy=req.weight_synergy,
        constraint=req.custom_constraint
    )
    return former.run_agent_formation()
