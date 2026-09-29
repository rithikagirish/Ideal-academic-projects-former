"""
Agentic AI Team Former - Database Layer
File: database.py
Description: In-memory student database with rich seed data.
"""

from typing import Dict
from models import Student

STUDENTS_DB: Dict[str, Student] = {}


def seed_initial_students():
    """Seed sample student data representing a diverse classroom."""
    mock_students = [
        Student(
            id="S01",
            name="Alex Chen",
            skills=["Python", "FastAPI", "Machine Learning", "PyTorch"],
            interests=["AI & Healthcare", "Data Science"],
            preferred_roles=["AI Specialist", "Team Lead"],
            past_collaborators={"S02": 1.0, "S05": -1.0},
            experience_level="Advanced"
        ),
        Student(
            id="S02",
            name="Sarah Jenkins",
            skills=["React", "TypeScript", "Tailwind CSS", "UI/UX Design"],
            interests=["AI & Healthcare", "EdTech"],
            preferred_roles=["Frontend Developer", "UI/UX Designer"],
            past_collaborators={"S01": 1.0, "S03": 1.0},
            experience_level="Advanced"
        ),
        Student(
            id="S03",
            name="Michael Rodriguez",
            skills=["PostgreSQL", "Docker", "Node.js", "System Architecture"],
            interests=["FinTech", "Cloud Platforms"],
            preferred_roles=["Backend Architect", "DevOps Engineer"],
            past_collaborators={"S02": 1.0, "S04": 0.5},
            experience_level="Intermediate"
        ),
        Student(
            id="S04",
            name="Priya Patel",
            skills=["Python", "Data Analysis", "SQL", "UI/UX Design"],
            interests=["FinTech", "AI & Healthcare"],
            preferred_roles=["Data Analyst", "Fullstack"],
            past_collaborators={"S03": 0.5, "S06": -1.0},
            experience_level="Intermediate"
        ),
        Student(
            id="S05",
            name="David Kim",
            skills=["Java", "Spring Boot", "Cybersecurity", "React"],
            interests=["Cybersecurity", "Cloud Platforms"],
            preferred_roles=["Security Engineer", "Team Lead"],
            past_collaborators={"S01": -1.0, "S06": 1.0},
            experience_level="Advanced"
        ),
        Student(
            id="S06",
            name="Emma Watson",
            skills=["UI/UX Design", "Figma", "HTML/CSS", "JavaScript"],
            interests=["EdTech", "Game Dev"],
            preferred_roles=["UI/UX Designer", "Frontend Developer"],
            past_collaborators={"S04": -1.0, "S05": 1.0},
            experience_level="Beginner"
        ),
        Student(
            id="S07",
            name="James Wilson",
            skills=["Python", "NLP", "TensorFlow", "FastAPI"],
            interests=["AI & Healthcare", "NLP"],
            preferred_roles=["AI Specialist", "Research Lead"],
            past_collaborators={"S08": 1.0},
            experience_level="Advanced"
        ),
        Student(
            id="S08",
            name="Aisha Khan",
            skills=["Vue.js", "CSS3", "JavaScript", "GraphQL"],
            interests=["NLP", "Web App"],
            preferred_roles=["Frontend Developer"],
            past_collaborators={"S07": 1.0, "S09": 1.0},
            experience_level="Intermediate"
        ),
        Student(
            id="S09",
            name="Lucas Garcia",
            skills=["Python", "MongoDB", "Express", "React"],
            interests=["Web App", "FinTech"],
            preferred_roles=["Fullstack Developer"],
            past_collaborators={"S08": 1.0, "S10": 0.5},
            experience_level="Intermediate"
        ),
        Student(
            id="S10",
            name="Sophia Martinez",
            skills=["Cloud/AWS", "Docker", "Kubernetes", "Go"],
            interests=["Cloud Platforms", "FinTech"],
            preferred_roles=["DevOps Engineer", "Backend Architect"],
            past_collaborators={"S09": 0.5, "S11": 1.0},
            experience_level="Advanced"
        ),
        Student(
            id="S11",
            name="Daniel Lee",
            skills=["Python", "PyTorch", "Computer Vision", "OpenCV"],
            interests=["Robotics", "Game Dev"],
            preferred_roles=["AI Specialist"],
            past_collaborators={"S10": 1.0, "S12": -0.5},
            experience_level="Intermediate"
        ),
        Student(
            id="S12",
            name="Olivia Taylor",
            skills=["UI/UX Design", "React Native", "Mobile Dev", "Figma"],
            interests=["Robotics", "EdTech"],
            preferred_roles=["Mobile Developer", "UI/UX Designer"],
            past_collaborators={"S11": -0.5, "S02": 0.5},
            experience_level="Beginner"
        )
    ]
    for s in mock_students:
        STUDENTS_DB[s.id] = s


def load_dataset_students(limit: int = 100):
    """Load sample students from dataset.csv"""
    import csv
    import os
    filepath = "dataset.csv"
    if not os.path.exists(filepath):
        return

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                if count >= limit:
                    break
                
                # We can filter to only professionals or just take any
                response_id = row.get("ResponseId", str(count))
                student_id = f"CSV_{response_id}"
                name = f"Dev_{response_id}"
                
                skills = []
                for col in ["LanguageHaveWorkedWith", "DatabaseHaveWorkedWith", "PlatformHaveWorkedWith", "WebframeHaveWorkedWith"]:
                    val = row.get(col, "")
                    if val and val != "NA":
                        skills.extend(val.split(";"))
                skills = list(set(skills))
                if not skills:
                    skills = ["Python"]
                
                roles = []
                dev_type = row.get("DevType", "")
                if dev_type and dev_type != "NA":
                    roles.extend(dev_type.split(";"))
                if not roles:
                    roles = ["Software Engineer"]
                
                interests = roles[:2]
                
                years = row.get("YearsCode", "0")
                if years == "Less than 1 year":
                    y = 0
                elif years == "More than 50 years":
                    y = 51
                elif years == "NA":
                    y = 3
                else:
                    try:
                        y = int(years)
                    except ValueError:
                        y = 3
                        
                if y < 3:
                    exp = "Beginner"
                elif y < 8:
                    exp = "Intermediate"
                else:
                    exp = "Advanced"
                    
                student = Student(
                    id=student_id,
                    name=name,
                    skills=skills,
                    interests=interests,
                    preferred_roles=roles,
                    past_collaborators={},
                    experience_level=exp
                )
                STUDENTS_DB[student_id] = student
                count += 1
    except Exception as e:
        print(f"Error loading dataset: {e}")


# Seed on module load
seed_initial_students()
load_dataset_students(limit=100)
