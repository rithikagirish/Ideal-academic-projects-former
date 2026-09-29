"""
Agentic AI Team Former - Data Models
File: models.py
Description: Pydantic models for students, team formation requests, and results.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class Student(BaseModel):
    id: str
    name: str
    skills: List[str]
    interests: List[str]
    preferred_roles: List[str]
    past_collaborators: Dict[str, float] = Field(
        default_factory=dict,
        description="Map of student_id -> synergy score (+1.0 positive, -1.0 conflict, 0.0 neutral)"
    )
    experience_level: str = "Intermediate"  # Beginner, Intermediate, Advanced


class TeamFormationRequest(BaseModel):
    team_size: int = 3
    weight_skills: float = 0.4
    weight_interests: float = 0.3
    weight_synergy: float = 0.3
    custom_constraint: Optional[str] = None


class AssignedMember(BaseModel):
    student_id: str
    name: str
    assigned_role: str
    skills: List[str]
    interests: List[str]
    experience_level: str


class TeamAnalysis(BaseModel):
    team_id: int
    team_name: str
    members: List[AssignedMember]
    skill_coverage_score: float
    interest_alignment_score: float
    synergy_score: float
    overall_balance_score: float
    detected_gaps: List[str]
    agent_rationale: str
    dominant_interests: List[str]


class FormationResult(BaseModel):
    teams: List[TeamAnalysis]
    global_balance_score: float
    agent_thought_logs: List[str]
    total_students_processed: int
    unassigned_students: List[str]
