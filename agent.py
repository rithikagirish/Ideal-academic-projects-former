"""
Agentic AI Team Former - Agentic Core
File: agent.py
Description: AgenticTeamFormer - autonomous multi-step reasoning engine for team formation.
"""

import math
import random
from typing import List, Dict, Optional

from models import (
    Student, AssignedMember, TeamAnalysis, FormationResult
)


class AgenticTeamFormer:
    """
    Autonomous Team Matchmaker Agent that simulates multi-step reasoning,
    reflection, vulnerability detection, and iterative self-correction to form balanced teams.
    """

    # Categorization taxonomy for skills to evaluate balance
    SKILL_CATEGORIES = {
        "Frontend & Design": ["React", "Vue.js", "TypeScript", "JavaScript", "HTML/CSS", "Tailwind CSS", "UI/UX Design", "Figma", "React Native", "CSS3"],
        "Backend & Systems": ["Python", "FastAPI", "Node.js", "Java", "Spring Boot", "Express", "Go", "PostgreSQL", "MongoDB", "SQL", "GraphQL"],
        "AI & Data Science": ["Machine Learning", "PyTorch", "TensorFlow", "NLP", "Computer Vision", "OpenCV", "Data Analysis", "Data Science"],
        "DevOps & Security": ["Docker", "Kubernetes", "Cloud/AWS", "System Architecture", "Cybersecurity", "Cloud Platforms"]
    }

    def __init__(
        self,
        students: List[Student],
        team_size: int,
        w_skills: float,
        w_interests: float,
        w_synergy: float,
        constraint: Optional[str] = None
    ):
        self.students = students
        self.team_size = max(2, min(team_size, 6))
        self.w_skills = w_skills
        self.w_interests = w_interests
        self.w_synergy = w_synergy
        self.constraint = constraint
        self.logs: List[str] = []

    def log(self, step: str, details: str):
        self.logs.append(f"[{step}] {details}")

    def evaluate_team_skill_coverage(self, team_members: List[Student]) -> float:
        """Calculates percentage of skill category diversity covered by the team."""
        covered_categories = set()
        for member in team_members:
            for skill in member.skills:
                for category, skills in self.SKILL_CATEGORIES.items():
                    if skill in skills:
                        covered_categories.add(category)

        coverage_ratio = len(covered_categories) / len(self.SKILL_CATEGORIES)
        return min(1.0, coverage_ratio * 1.2) * 100.0

    def evaluate_team_interest_alignment(self, team_members: List[Student]) -> tuple[float, List[str]]:
        """Measures interest similarity among team members."""
        if not team_members:
            return 0.0, []

        interest_counts: Dict[str, int] = {}
        for member in team_members:
            for interest in member.interests:
                interest_counts[interest] = interest_counts.get(interest, 0) + 1

        dominant_interests = [k for k, v in interest_counts.items() if v >= 2]
        if not dominant_interests and interest_counts:
            dominant_interests = [max(interest_counts, key=interest_counts.get)]

        shared_interest_count = sum(v for v in interest_counts.values() if v > 1)
        score = min(100.0, (shared_interest_count / (len(team_members) * 1.5)) * 100.0 + (30.0 if dominant_interests else 10.0))
        return score, dominant_interests

    def evaluate_team_synergy(self, team_members: List[Student]) -> float:
        """Evaluates past collaboration synergy and conflict avoidance."""
        if len(team_members) < 2:
            return 100.0

        total_pairs = 0
        synergy_sum = 0.0

        for i in range(len(team_members)):
            for j in range(i + 1, len(team_members)):
                total_pairs += 1
                s1, s2 = team_members[i], team_members[j]

                hist_score = s1.past_collaborators.get(s2.id, s2.past_collaborators.get(s1.id, 0.0))
                if hist_score > 0:
                    synergy_sum += 1.0
                elif hist_score < 0:
                    synergy_sum -= 1.5  # Heavy penalty for conflict
                else:
                    synergy_sum += 0.2  # Neutral baseline

        avg_synergy = (synergy_sum / total_pairs) if total_pairs > 0 else 0.5
        return max(0.0, min(100.0, (avg_synergy + 1.0) / 2.0 * 100.0))

    def detect_team_gaps(self, team_members: List[Student]) -> List[str]:
        """Agent reflection: detect gaps or risks in a formed team."""
        gaps = []
        covered_categories = set()
        for member in team_members:
            for skill in member.skills:
                for category, skills in self.SKILL_CATEGORIES.items():
                    if skill in skills:
                        covered_categories.add(category)

        if "Frontend & Design" not in covered_categories:
            gaps.append("⚠️ Lacks Frontend/UI Design expertise")
        if "Backend & Systems" not in covered_categories:
            gaps.append("⚠️ Lacks Backend & Systems engineering")
        if "AI & Data Science" not in covered_categories and "DevOps & Security" not in covered_categories:
            gaps.append("💡 Lacks AI or Infrastructure specialist")

        for i in range(len(team_members)):
            for j in range(i + 1, len(team_members)):
                s1, s2 = team_members[i], team_members[j]
                if s1.past_collaborators.get(s2.id, 0) < 0 or s2.past_collaborators.get(s1.id, 0) < 0:
                    gaps.append(f"❌ Conflict risk detected between {s1.name} and {s2.name}")

        exp_levels = [m.experience_level for m in team_members]
        if all(e == "Beginner" for e in exp_levels):
            gaps.append("⚠️ All team members are beginners - needs senior guidance")

        return gaps

    def calculate_overall_team_score(self, skill_score: float, interest_score: float, synergy_score: float) -> float:
        total_w = self.w_skills + self.w_interests + self.w_synergy
        if total_w == 0:
            total_w = 1.0
        weighted = (
            (skill_score * self.w_skills) +
            (interest_score * self.w_interests) +
            (synergy_score * self.w_synergy)
        ) / total_w
        return round(weighted, 1)

    def assign_roles(self, team_members: List[Student]) -> List[AssignedMember]:
        """Agent assigns complementary roles based on preferences and skill strengths."""
        assigned = []
        used_roles = set()

        for m in team_members:
            chosen_role = None
            for pref in m.preferred_roles:
                if pref not in used_roles:
                    chosen_role = pref
                    used_roles.add(pref)
                    break

            if not chosen_role:
                if any(s in ["Python", "FastAPI", "Java", "Node.js"] for s in m.skills):
                    chosen_role = "Backend Developer"
                elif any(s in ["React", "Vue.js", "UI/UX Design", "Figma"] for s in m.skills):
                    chosen_role = "Frontend & UI Lead"
                elif any(s in ["Machine Learning", "PyTorch", "NLP", "Computer Vision"] for s in m.skills):
                    chosen_role = "AI Engineer"
                else:
                    chosen_role = "Fullstack Engineer"

            assigned.append(AssignedMember(
                student_id=m.id,
                name=m.name,
                assigned_role=chosen_role,
                skills=m.skills,
                interests=m.interests,
                experience_level=m.experience_level
            ))
        return assigned

    def generate_agent_rationale(
        self,
        team_name: str,
        members: List[AssignedMember],
        dominant_interests: List[str],
        gaps: List[str],
        score: float
    ) -> str:
        """Generates natural language reasoning for the team composition."""
        interests_str = ", ".join(dominant_interests) if dominant_interests else "General Technology"
        roles_summary = ", ".join([f"{m.name} as {m.assigned_role}" for m in members])

        rationale = f"**{team_name}** was formed with an overall balance score of **{score}/100**.\n"
        rationale += f"• **Team Theme**: Centered around **{interests_str}**.\n"
        rationale += f"• **Role Hierarchy**: {roles_summary}.\n"

        if not gaps:
            rationale += "• **Agent Assessment**: Highly balanced team with great skill synergy and zero historical conflict risks."
        else:
            rationale += f"• **Agent Assessment & Reflection**: Formed with minor notes: {'; '.join(gaps)}."

        return rationale

    def run_agent_formation(self) -> FormationResult:
        """
        Executes the Multi-Step Agentic Formation Pipeline:
        Step 1: Goal Planning & Skill Vector Parsing
        Step 2: Anchor Selection & Complementary Clustering
        Step 3: Agent Reflection & Risk Assessment
        Step 4: Iterative Hill-Climbing Swap Optimization
        Step 5: Rationale & Role Generation
        """
        self.log("Step 1: Agent Profiling", f"Ingested {len(self.students)} students. Vectorizing skill matrices, interest vectors, and collaboration networks.")
        self.log("Step 1: Constraint Verification", f"Configured parameters -> Team Size: {self.team_size}, Skill Weight: {self.w_skills}, Interest Weight: {self.w_interests}, Synergy Weight: {self.w_synergy}.")

        num_students = len(self.students)
        num_teams = max(1, math.ceil(num_students / self.team_size))

        self.log("Step 2: Strategy Planning", f"Targeting {num_teams} balanced teams for {num_students} students.")

        teams_buckets: List[List[Student]] = [[] for _ in range(num_teams)]

        unassigned = list(self.students)
        random.shuffle(unassigned)

        # Greedy initial assignment
        for student in unassigned:
            best_team_idx = 0
            best_addition_score = -9999.0

            for idx in range(num_teams):
                if len(teams_buckets[idx]) >= self.team_size:
                    continue

                temp_team = teams_buckets[idx] + [student]
                sk_score = self.evaluate_team_skill_coverage(temp_team)
                int_score, _ = self.evaluate_team_interest_alignment(temp_team)
                syn_score = self.evaluate_team_synergy(temp_team)
                overall = self.calculate_overall_team_score(sk_score, int_score, syn_score)

                if overall > best_addition_score:
                    best_addition_score = overall
                    best_team_idx = idx

            teams_buckets[best_team_idx].append(student)

        self.log("Step 3: Agent Initial Reflection", "Initial draft complete. Conducting self-critique on team balances and conflict detection.")
        self.log("Step 4: Iterative Self-Correction", "Starting optimization swaps to resolve skill gaps and past conflicts...")

        max_iterations = 25
        improved = True
        iteration = 0

        def calc_global_score(buckets):
            scores = []
            for b in buckets:
                if not b:
                    continue
                sk = self.evaluate_team_skill_coverage(b)
                i_sc, _ = self.evaluate_team_interest_alignment(b)
                syn = self.evaluate_team_synergy(b)
                scores.append(self.calculate_overall_team_score(sk, i_sc, syn))
            return sum(scores) / len(scores) if scores else 0.0

        current_global_score = calc_global_score(teams_buckets)
        self.log("Step 4: Initial Baseline Score", f"Global Balance Index: {round(current_global_score, 2)}/100")

        while iteration < max_iterations and improved:
            improved = False
            iteration += 1

            for t1 in range(num_teams):
                for t2 in range(t1 + 1, num_teams):
                    for idx1, st1 in enumerate(teams_buckets[t1]):
                        for idx2, st2 in enumerate(teams_buckets[t2]):
                            teams_buckets[t1][idx1] = st2
                            teams_buckets[t2][idx2] = st1

                            new_global_score = calc_global_score(teams_buckets)

                            if new_global_score > current_global_score + 0.5:
                                self.log(
                                    "Step 4: Agent Optimization Swap",
                                    f"Iter {iteration}: Swapped {st1.name} (Team {t1+1}) with {st2.name} (Team {t2+1}). Score raised {round(current_global_score,1)} -> {round(new_global_score,1)}"
                                )
                                current_global_score = new_global_score
                                improved = True
                                break
                            else:
                                teams_buckets[t1][idx1] = st1
                                teams_buckets[t2][idx2] = st2
                        if improved:
                            break
                    if improved:
                        break

        self.log("Step 5: Agent Decision Finalization", f"Optimization converged in {iteration} iteration(s). Final Global Balance Index: {round(current_global_score, 2)}/100.")

        team_names = ["Alpha Squad", "Beta Innovators", "Gamma Labs", "Delta Syndicate", "Epsilon Systems", "Zeta Nexus"]
        final_teams: List[TeamAnalysis] = []

        for idx, bucket in enumerate(teams_buckets):
            if not bucket:
                continue

            sk_score = self.evaluate_team_skill_coverage(bucket)
            int_score, dom_interests = self.evaluate_team_interest_alignment(bucket)
            syn_score = self.evaluate_team_synergy(bucket)
            overall = self.calculate_overall_team_score(sk_score, int_score, syn_score)
            gaps = self.detect_team_gaps(bucket)
            assigned_members = self.assign_roles(bucket)

            t_name = f"Team {team_names[idx % len(team_names)]}"
            rationale = self.generate_agent_rationale(t_name, assigned_members, dom_interests, gaps, overall)

            final_teams.append(TeamAnalysis(
                team_id=idx + 1,
                team_name=t_name,
                members=assigned_members,
                skill_coverage_score=round(sk_score, 1),
                interest_alignment_score=round(int_score, 1),
                synergy_score=round(syn_score, 1),
                overall_balance_score=overall,
                detected_gaps=gaps,
                agent_rationale=rationale,
                dominant_interests=dom_interests
            ))

        return FormationResult(
            teams=final_teams,
            global_balance_score=round(current_global_score, 1),
            agent_thought_logs=self.logs,
            total_students_processed=len(self.students),
            unassigned_students=[]
        )
