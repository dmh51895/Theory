# 💀🧬 MOLECULAR AI - DIRECTORY STRUCTURE

## File Tree

```
C:\Users\DHeavy\Downloads\Theory\
│
├── 📚 DOCUMENTATION (START HERE)
│   ├── README.md                          ← Main entry point (START HERE!)
│   ├── QUICK_REFERENCE.md                 ← 2-minute cheat sheet
│   ├── COMPONENTS_README.md               ← All 31 components explained
│   ├── SCRIPTS_README.md                  ← PowerShell scripts guide
│   └── DIRECTORY_STRUCTURE.md             ← This file
│
├── 🎯 CRITICAL SYSTEM FILES
│   ├── Brain.py                           ← Central orchestrator (433 lines)
│   ├── background_agent.py                ← Full agent runner (316 lines)
│   ├── molecular_server.py                ← Flask API server (585 lines)
│   ├── simple_web_ui.py                   ← Web chat interface (496 lines)
│   └── agent_memory.json                  ← Persistent memory storage
│
├── 🧠 COGNITIVE COMPONENTS (31 files)
│   │
│   ├── INPUT PROCESSING
│   │   ├── Prompt-Breakdown.py            ← Decompose prompts (346 lines)
│   │   ├── Conscious-Thought.py           ← Understand intent (283 lines)
│   │   ├── Relevance-To-Prompt.py         ← Filter relevance (253 lines)
│   │   └── Original-Data.py               ← Hash & preserve (215 lines)
│   │
│   ├── COGNITIVE ANALYSIS
│   │   ├── Metacognition.py               ← Detect biases (274 lines)
│   │   ├── Goals.py                       ← Set objectives (234 lines)
│   │   ├── Ethics.py                      ← Protect user (184 lines)
│   │   ├── Wisdom.py                      ← Learned patterns (348 lines)
│   │   ├── Previous-Mistakes.py           ← Error memory (267 lines)
│   │   ├── Consequences.py                ← Outcome prediction (198 lines)
│   │   ├── Aftermath-Of-Decision.py       ← Track outcomes (254 lines)
│   │   └── Identifying-If-A-Fallback-Solution.py  ← Quality control (312 lines)
│   │
│   ├── DECISION SUPPORT
│   │   ├── High-Level-Planning.py         ← Strategic planning (289 lines)
│   │   ├── Habits.py                      ← Behavioral patterns (243 lines)
│   │   ├── Rules.py                       ← Hard constraints (276 lines)
│   │   └── Apprehensive.py                ← Risk sensing (231 lines)
│   │
│   ├── EXECUTION LAYER
│   │   ├── Motor-Control.py               ← Action executor (198 lines)
│   │   ├── Response-Formatter.py          ← Output structuring (342 lines)
│   │   └── Openers.py                     ← Conversation starters (187 lines)
│   │
│   ├── CONTEXT MANAGEMENT
│   │   ├── Memory.py                      ← Long-term memory (212 lines)
│   │   ├── Current-Active-Thought.py      ← Working memory (176 lines)
│   │   ├── Mental-Syntax.py               ← Internal format (203 lines)
│   │   ├── Rewired-Thought.py             ← Reframing (245 lines)
│   │   └── Local-Time.py                  ← Temporal context (156 lines)
│   │
│   ├── PATTERN DETECTION
│   │   ├── Synchronized-Patterns.py       ← Cross-component (268 lines)
│   │   └── Natural-Callbacks.py           ← Event triggers (219 lines)
│   │
│   ├── PHILOSOPHICAL GROUNDING
│   │   └── Human-Philosophy.py            ← Human values (287 lines)
│   │
│   └── LEARNING SYSTEM
│       └── auto_learning_engine.py        ← Continuous learning (324 lines)
│
└── ⚡ MANAGEMENT SCRIPTS
    ├── restart_all.ps1                    ← Full restart (loads code changes)
    ├── start_all.ps1                      ← Normal startup
    ├── stop_all.ps1                       ← Shutdown
    └── status.ps1                         ← Health check

Total: 31 cognitive components + 4 critical files + 4 scripts + 5 docs = 44 files
```

---

## File Sizes (Approximate)

| Category | Total Lines | Files |
|----------|------------|-------|
| Critical System | ~2,000 | 4 |
| Input Processing | ~1,100 | 4 |
| Cognitive Analysis | ~2,100 | 8 |
| Decision Support | ~1,000 | 4 |
| Execution | ~700 | 3 |
| Context Management | ~900 | 5 |
| Pattern Detection | ~500 | 2 |
| Philosophical | ~300 | 1 |
| Learning | ~300 | 1 |
| **Total** | **~9,000** | **32** |

---

## Critical Dependencies

```
background_agent.py
    ↓ imports all 31 components
    ↓ orchestrates decision flow
    ↓ uses Brain.py as coordinator
    ↓ stores in agent_memory.json

molecular_server.py
    ↓ imports background_agent.py
    ↓ exposes Flask API
    ↓ serves HTTP on port 5000

simple_web_ui.py
    ↓ calls molecular_server.py
    ↓ serves web UI on port 3000
    ↓ used by browser
```

---

## Data Flow

```
USER (browser)
    ↓ http://localhost:3000
simple_web_ui.py (Web UI)
    ↓ POST http://localhost:5000/chat
molecular_server.py (API)
    ↓ calls background_agent.process_prompt()
background_agent.py (Agent)
    ↓ orchestrates 31 components
Brain.py (Orchestrator)
    ↓ uses 31 components
    ↓ makes decision
    ↓ stores in Memory.py
agent_memory.json (Storage)
    ↓ persists on disk
molecular_server.py
    ↓ returns JSON response
simple_web_ui.py
    ↓ displays to user
USER sees response
```

---

## Modification Patterns

### To change AI behavior:
```
Edit Brain.py decision logic
  → Run restart_all.ps1
  → Test in Web UI
```

### To improve understanding:
```
Edit Prompt-Breakdown.py or Conscious-Thought.py
  → Run restart_all.ps1
  → Test with ambiguous prompts
```

### To add ethics rules:
```
Edit Ethics.py rules
  → Run restart_all.ps1
  → Test with edge cases
```

### To customize responses:
```
Edit Response-Formatter.py
  → Run restart_all.ps1
  → See formatting changes
```

### To add new capabilities:
```
Edit Motor-Control.py
  → Add new execute_* functions
  → Run restart_all.ps1
  → Test with agent commands
```

---

## Access Patterns

### Daily Use:
```
.\start_all.ps1
  → Browser: http://localhost:3000
  → Chat naturally
  → .\stop_all.ps1 when done
```

### Development:
```
Edit component file
  → .\restart_all.ps1 (reload code)
  → .\status.ps1 (verify running)
  → Test changes
  → Check agent_memory.json (see learning)
```

### Debugging:
```
.\status.ps1 (check health)
  → View server terminal (error logs)
  → Check agent_memory.json (decision history)
  → curl http://localhost:5000/health (API test)
  → .\restart_all.ps1 (if stuck)
```

---

## Memory Structure

```
agent_memory.json
├── decisions: []              ← Every decision made
├── outcomes: []               ← What actually happened
├── mistakes: []               ← Recorded errors
├── wisdom: []                 ← Extracted patterns
├── goals: []                  ← Active objectives
└── patterns: []               ← Behavioral patterns

Grows over time. Never cleared. Foundation of learning.
```

---

## Component Categories by Function

### Want AI to understand prompts better?
→ `Prompt-Breakdown.py`, `Conscious-Thought.py`, `Relevance-To-Prompt.py`

### Want AI to make better decisions?
→ `Brain.py`, `Metacognition.py`, `Wisdom.py`, `High-Level-Planning.py`

### Want AI to avoid mistakes?
→ `Previous-Mistakes.py`, `Consequences.py`, `Identifying-If-A-Fallback-Solution.py`

### Want AI to learn faster?
→ `auto_learning_engine.py`, `Wisdom.py`, `Memory.py`, `Aftermath-Of-Decision.py`

### Want AI to be safer?
→ `Ethics.py`, `Apprehensive.py`, `Rules.py`

### Want better responses?
→ `Response-Formatter.py`, `Openers.py`

---

## Related Directories

```
C:\Users\DHeavy\Downloads\
├── Theory\                                    ← Molecular AI (this directory)
├── molecular_chat\                            ← Flutter mobile app
│   └── START_HERE.md
├── open-webui-main\open-webui-main\          ← Open WebUI integration
│   └── MOLECULAR_AI_INTEGRATION.md
└── CHOOSE_YOUR_INTERFACE.md                   ← Interface comparison
```

---

## Quick File Lookup

**Need to...**

Start the system? → `restart_all.ps1`  
Check if running? → `status.ps1`  
See the memory? → `agent_memory.json`  
Understand architecture? → `COMPONENTS_README.md`  
Quick reference? → `QUICK_REFERENCE.md`  
Main entry point? → `README.md`  
Change decision logic? → `Brain.py`  
Add ethics rules? → `Ethics.py`  
Improve prompt understanding? → `Prompt-Breakdown.py`  
Customize responses? → `Response-Formatter.py`  
Add file operations? → `Motor-Control.py`  
See server code? → `molecular_server.py`  
See web UI code? → `simple_web_ui.py`  
Full agent code? → `background_agent.py`  

---

## Ports & URLs

| Service | Port | URL |
|---------|------|-----|
| Web UI | 3000 | http://localhost:3000 |
| API Server | 5000 | http://localhost:5000 |
| Health Check | 5000 | http://localhost:5000/health |
| API Chat | 5000 | http://localhost:5000/chat |

---

**Made with 💀🧬 - February 23, 2026**
