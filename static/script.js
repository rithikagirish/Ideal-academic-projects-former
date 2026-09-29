/**
 * TeamFormer AI - Frontend JavaScript Application Logic
 */

let allStudents = [];
let formedTeamsData = null;

// On page load
document.addEventListener('DOMContentLoaded', () => {
  fetchStudents();
});

// Fetch Student Roster from Backend
async function fetchStudents() {
  try {
    const res = await fetch('/api/students');
    if (!res.ok) throw new Error('Failed to fetch students');
    allStudents = await res.json();
    
    document.getElementById('stat-total-students').innerText = allStudents.length;
    document.getElementById('roster-count').innerText = allStudents.length;
    renderRoster(allStudents);
  } catch (err) {
    console.error('Error fetching students:', err);
  }
}

// Render Roster Grid
function renderRoster(students) {
  const container = document.getElementById('students-container');
  container.innerHTML = '';

  if (students.length === 0) {
    container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 2rem;">No students in roster. Click "Reset Mock Data" to load sample students.</div>';
    return;
  }

  students.forEach(st => {
    const card = document.createElement('div');
    card.className = 'student-card';

    const skillChips = st.skills.map(s => `<span class="chip">${s}</span>`).join('');
    const interestChips = st.interests.map(i => `<span class="chip interest">${i}</span>`).join('');
    
    // Past collaboration summary
    let collabText = '';
    const posCollabs = Object.entries(st.past_collaborators).filter(([_, val]) => val > 0).map(([id, _]) => id);
    const negCollabs = Object.entries(st.past_collaborators).filter(([_, val]) => val < 0).map(([id, _]) => id);
    
    if (posCollabs.length > 0) collabText += `<span style="color: var(--accent-emerald); font-size: 0.72rem;">💚 Synergy: ${posCollabs.join(', ')}</span> `;
    if (negCollabs.length > 0) collabText += `<span style="color: var(--accent-rose); font-size: 0.72rem;">⚠️ Conflict: ${negCollabs.join(', ')}</span>`;
    if (!collabText) collabText = '<span style="color: var(--text-subtle); font-size: 0.72rem;">No past history</span>';

    card.innerHTML = `
      <div class="student-header">
        <span class="student-name">${st.name} <small style="font-size:0.75rem; color:var(--text-muted);">(${st.id})</small></span>
        <span class="exp-badge ${st.experience_level}">${st.experience_level}</span>
      </div>
      <div>
        <div style="font-size: 0.72rem; color: var(--text-muted); margin-bottom: 0.2rem;">SKILLS:</div>
        <div class="chip-group">${skillChips}</div>
      </div>
      <div>
        <div style="font-size: 0.72rem; color: var(--text-muted); margin-bottom: 0.2rem;">INTERESTS:</div>
        <div class="chip-group">${interestChips}</div>
      </div>
      <div style="margin-top: 0.2rem;">
        <div style="font-size: 0.72rem; color: var(--text-muted); margin-bottom: 0.1rem;">COLLABORATION HISTORY:</div>
        <div>${collabText}</div>
      </div>
      <div style="display: flex; justify-content: flex-end; margin-top: 0.4rem;">
        <button class="btn-danger" onclick="deleteStudent('${st.id}')">Delete</button>
      </div>
    `;
    container.appendChild(card);
  });
}

// Filter Roster by Search
function filterRoster() {
  const query = document.getElementById('roster-search').value.toLowerCase();
  const filtered = allStudents.filter(st => 
    st.name.toLowerCase().includes(query) ||
    st.skills.some(s => s.toLowerCase().includes(query)) ||
    st.interests.some(i => i.toLowerCase().includes(query))
  );
  renderRoster(filtered);
}

// Trigger Agentic Team Formation
async function triggerTeamFormation() {
  const teamSize = parseInt(document.getElementById('input-team-size').value);
  const wSkills = parseFloat(document.getElementById('input-w-skills').value);
  const wInterests = parseFloat(document.getElementById('input-w-interests').value);
  const wSynergy = parseFloat(document.getElementById('input-w-synergy').value);
  const constraint = document.getElementById('input-constraint').value.trim();

  const logBox = document.getElementById('agent-logs');
  logBox.innerHTML = '<div class="agent-log-line step1">🤖 Initializing Agentic AI Matchmaker...</div>';

  const btn = document.getElementById('btn-run-agent');
  btn.disabled = true;
  btn.innerHTML = '<span>⏳</span> Agent Thinking...';

  try {
    const res = await fetch('/api/form-teams', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        team_size: teamSize,
        weight_skills: wSkills,
        weight_interests: wInterests,
        weight_synergy: wSynergy,
        custom_constraint: constraint || null
      })
    });

    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.detail || 'Team formation failed');
    }

    formedTeamsData = await res.json();

    // Stream logs with animation
    await animateAgentLogs(formedTeamsData.agent_thought_logs);

    // Update statistics
    document.getElementById('stat-formed-teams').innerText = formedTeamsData.teams.length;
    document.getElementById('stat-global-score').innerText = formedTeamsData.global_balance_score + '/100';

    // Render teams
    renderTeams(formedTeamsData.teams);

    // Switch to teams tab
    switchTab('teams');

  } catch (err) {
    logBox.innerHTML += `<div class="agent-log-line" style="border-color:var(--accent-rose); color:var(--accent-rose);">❌ Error: ${err.message}</div>`;
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>⚡</span> Form Balanced Teams';
  }
}

// Animate Agent Logs line by line
async function animateAgentLogs(logs) {
  const logBox = document.getElementById('agent-logs');
  logBox.innerHTML = '';
  
  for (let i = 0; i < logs.length; i++) {
    const line = logs[i];
    const logEl = document.createElement('div');
    
    let stepClass = 'step1';
    if (line.includes('Step 2')) stepClass = 'step2';
    else if (line.includes('Step 3')) stepClass = 'step3';
    else if (line.includes('Step 4')) stepClass = 'step4';
    else if (line.includes('Step 5')) stepClass = 'step5';
    
    logEl.className = `agent-log-line ${stepClass}`;
    logEl.innerText = line;
    logBox.appendChild(logEl);
    logBox.scrollTop = logBox.scrollHeight;
    
    // Short delay to give a realistic "Agent thinking" feel
    await new Promise(r => setTimeout(r, 120));
  }
}

// Render Teams Cards
function renderTeams(teams) {
  const container = document.getElementById('teams-container');
  container.innerHTML = '';

  teams.forEach(team => {
    const card = document.createElement('div');
    card.className = 'team-card';

    const scoreClass = team.overall_balance_score >= 85 ? '' : 'medium';
    
    // Render Members
    const membersHtml = team.members.map(m => `
      <div class="member-item">
        <div class="member-info">
          <h4>${m.name}</h4>
          <span class="member-role">📌 ${m.assigned_role}</span>
        </div>
        <div class="chip-group" style="max-width: 180px; justify-content: flex-end;">
          ${m.skills.slice(0, 3).map(s => `<span class="chip">${s}</span>`).join('')}
        </div>
      </div>
    `).join('');

    // Format markdown-like rationale HTML
    let rationaleHtml = team.agent_rationale
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br>');

    // Format Gaps Alerts
    let gapsHtml = '';
    if (team.detected_gaps && team.detected_gaps.length > 0) {
      gapsHtml = `
        <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: var(--radius-sm); padding: 0.6rem; font-size: 0.78rem; color: #fde68a;">
          <strong style="color: #fbbf24;">Agent Reflection Note:</strong>
          <ul style="padding-left: 1.2rem; margin-top: 0.3rem;">
            ${team.detected_gaps.map(g => `<li>${g}</li>`).join('')}
          </ul>
        </div>
      `;
    }

    card.innerHTML = `
      <div class="team-card-header">
        <span class="team-name">${team.team_name}</span>
        <span class="score-badge ${scoreClass}">${team.overall_balance_score} / 100</span>
      </div>

      <div class="metrics-row">
        <div class="metric-box">
          <label>Skill Diversity</label>
          <span>${team.skill_coverage_score}%</span>
        </div>
        <div class="metric-box">
          <label>Interest Harmony</label>
          <span>${team.interest_alignment_score}%</span>
        </div>
        <div class="metric-box">
          <label>Synergy</label>
          <span>${team.synergy_score}%</span>
        </div>
      </div>

      <div>
        <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.4rem; font-weight: 600;">ASSIGNED MEMBERS & ROLES</div>
        <div class="members-list">${membersHtml}</div>
      </div>

      ${gapsHtml}

      <div class="rationale-box">
        <div style="font-weight: 700; color: var(--accent-cyan); margin-bottom: 0.3rem; font-size: 0.82rem;">🧠 Agent Strategy Rationale</div>
        <div>${rationaleHtml}</div>
      </div>
    `;

    container.appendChild(card);
  });
}

// Tab Switching Logic
function switchTab(tabName) {
  document.getElementById('tab-teams-btn').classList.toggle('active', tabName === 'teams');
  document.getElementById('tab-students-btn').classList.toggle('active', tabName === 'students');
  
  document.getElementById('tab-teams').classList.toggle('active', tabName === 'teams');
  document.getElementById('tab-students').classList.toggle('active', tabName === 'students');
}

// Add Student Modal Controls
function openAddStudentModal() {
  document.getElementById('add-student-modal').classList.add('active');
}

function closeAddStudentModal() {
  document.getElementById('add-student-modal').classList.remove('active');
}

// Submit Add Student Form
async function submitAddStudent() {
  const id = document.getElementById('new-id').value.trim();
  const name = document.getElementById('new-name').value.trim();
  const skillsStr = document.getElementById('new-skills').value.trim();
  const interestsStr = document.getElementById('new-interests').value.trim();
  const rolesStr = document.getElementById('new-roles').value.trim();
  const exp = document.getElementById('new-exp').value;

  const newStudent = {
    id,
    name,
    skills: skillsStr.split(',').map(s => s.trim()).filter(Boolean),
    interests: interestsStr.split(',').map(i => i.trim()).filter(Boolean),
    preferred_roles: rolesStr.split(',').map(r => r.trim()).filter(Boolean),
    past_collaborators: {},
    experience_level: exp
  };

  try {
    const res = await fetch('/api/students', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newStudent)
    });

    if (!res.ok) {
      const err = await res.json();
      alert(err.detail || 'Failed to add student');
      return;
    }

    closeAddStudentModal();
    document.getElementById('add-student-form').reset();
    fetchStudents();
  } catch (err) {
    alert('Error adding student: ' + err.message);
  }
}

// Delete Student
async function deleteStudent(studentId) {
  if (!confirm(`Are you sure you want to remove student ${studentId}?`)) return;
  try {
    const res = await fetch(`/api/students/${studentId}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete student');
    fetchStudents();
  } catch (err) {
    alert('Error deleting student: ' + err.message);
  }
}

// Reset Roster to Mock Data
async function resetRoster() {
  if (!confirm('Reset student roster back to sample seed dataset?')) return;
  try {
    const res = await fetch('/api/students/reset', { method: 'POST' });
    if (!res.ok) throw new Error('Reset failed');
    fetchStudents();
    document.getElementById('teams-container').innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 4rem 1rem; color: var(--text-muted);">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
        <h3>No Teams Formed Yet</h3>
        <p style="margin-top: 0.5rem; font-size: 0.9rem;">Click <strong>"Form Balanced Teams"</strong> on the left panel to execute the Agentic AI matchmaker.</p>
      </div>
    `;
    document.getElementById('stat-formed-teams').innerText = '0';
    document.getElementById('stat-global-score').innerText = '--';
  } catch (err) {
    alert('Error resetting roster: ' + err.message);
  }
}
