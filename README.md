# ⚡ TeamFormer AI - Agentic AI Project Team Former

An autonomous, agentic system designed for the subject **Agentic AI**. It automatically forms balanced, high-synergy project teams by analyzing students' technical skills, domain interests, and past collaboration history.

---

## 🚀 Key Features

1. **Multi-Vector Profiling**: Ingests student skills, interest domain vectors, preferred roles, and pairwise collaboration matrix (past synergy / conflicts).
2. **Multi-Step Agent Reasoning Loop**:
   - **Step 1: Agent Profiling**: Normalizes skill matrices and parses user constraints.
   - **Step 2: Strategy Planning**: Evaluates initial candidate clusters and picks team anchor leads.
   - **Step 3: Agent Reflection**: Critiques draft team compositions for skill gaps and conflict risks.
   - **Step 4: Iterative Self-Correction**: Runs simulated annealing / hill-climbing optimization swaps to maximize the global Team Balance Index.
   - **Step 5: Role & Rationale Generation**: Assigns specialized roles (e.g. Team Lead, Frontend & UI Lead, AI Specialist) and outputs natural language strategy rationales.
3. **Live Agent Thought Log**: Real-time animated terminal-style log demonstrating the agent's multi-step decision-making process.
4. **Modern Glassmorphic UI**: Fast, responsive dark-mode web application featuring metric badges, interactive sliders, gap detection alerts, and student roster management.

---

## 🛠️ Project Structure

```
project_team_former/
├── app.py                # FastAPI server & Agentic AI Team Matchmaker logic
├── static/
│   ├── index.html        # Main HTML5 Glassmorphic UI
│   ├── style.css         # Styling system & animations
│   └── script.js         # Interactive dashboard & real-time log rendering
├── requirements.txt      # Dependencies (FastAPI, Uvicorn, Pydantic)
└── README.md             # Project documentation
```

---

## 💻 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```
*Or using Uvicorn directly:*
```bash
uvicorn app:app --reload --port 8000
```

### 3. Access the Web Dashboard
Open your web browser and navigate to:
```text
http://127.0.0.1:8000
```

---

## 🧠 Agentic AI Architecture Diagram

```
 [Student Roster Data] ──► [Agent Profiler]
                                 │
                                 ▼
                     [Heuristic Clustering]
                                 │
                                 ▼
                    [Agent Reflection & Critique]
                        (Detect Gaps & Conflicts)
                                 │
                                 ▼
                    [Iterative Swap Optimizer] ◄─── (Self-Correction Loop)
                                 │
                                 ▼
                    [Final Role & Strategy Output]
```

---

## 📜 License
Developed for educational demonstration in **Agentic AI**.
