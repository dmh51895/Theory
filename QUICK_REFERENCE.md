# 💀 MOLECULAR AI - QUICK REFERENCE CHEAT SHEET

## 🚀 TLDR - What You Need to Know

**This is a 31-component AI system that REFUSES if it can't do something properly.**  
No guessing. No fallbacks. It works or it doesn't.

---

## ⚡ Quick Start

```powershell
cd C:\Users\DHeavy\Downloads\Theory
.\restart_all.ps1         # Start everything
# Open http://localhost:3000
.\stop_all.ps1            # Stop when done
```

---

## 📂 File Categories (31 Components)

### 🧠 MUST HAVE (System breaks without these)
- `Brain.py` - Main orchestrator
- `background_agent.py` - Full agent runner
- `Memory.py` - Persistent storage
- `Motor-Control.py` - Executor

### 🎯 INPUT PROCESSING
- `Prompt-Breakdown.py` - Decompose prompts
- `Conscious-Thought.py` - Understand intent
- `Relevance-To-Prompt.py` - Filter noise
- `Original-Data.py` - Hash & preserve input

### 🤔 THINKING
- `Metacognition.py` - Check for biases
- `Goals.py` - Set objectives
- `Ethics.py` - Protect user
- `Wisdom.py` - Apply learned patterns
- `Previous-Mistakes.py` - Avoid fuckups
- `Consequences.py` - Predict outcomes
- `High-Level-Planning.py` - Plan steps
- `Identifying-If-A-Fallback-Solution.py` - Catch laziness
- `Apprehensive.py` - Sense risk

### 🎮 EXECUTION
- `Motor-Control.py` - Do things
- `Response-Formatter.py` - Format output
- `Openers.py` - Handle greetings

### 💾 STATE MANAGEMENT
- `Memory.py` - Long-term memory
- `Current-Active-Thought.py` - Working memory
- `Mental-Syntax.py` - Internal format
- `Rewired-Thought.py` - Reframing
- `Local-Time.py` - Time context
- `agent_memory.json` - Physical storage

### 🔍 PATTERNS
- `Synchronized-Patterns.py` - Cross-component patterns
- `Natural-Callbacks.py` - Event triggers
- `Habits.py` - Behavioral patterns

### 📚 GOVERNANCE
- `Rules.py` - Hard constraints
- `Human-Philosophy.py` - Human values

### 🎓 LEARNING
- `auto_learning_engine.py` - Continuous learning
- `Aftermath-Of-Decision.py` - Track outcomes

---

## 🔥 Common Issues & Fixes

| Problem | File Responsible | Fix |
|---------|-----------------|-----|
| "Missing action" error | Prompt-Breakdown.py | Use action verbs OR casual chat (auto-fixes now) |
| "Needs clarification" | Conscious-Thought.py | Be more specific |
| Server not responding | molecular_server.py | Run `.\status.ps1` |
| Code not updating | (All) | Run `.\restart_all.ps1` |
| Chat format error | molecular_server.py | Already fixed, just restart |

---

## 📊 Decision Flow (Simplified)

```
Prompt → Breakdown → Understand → Check Ethics → Check Past Mistakes
  → Apply Wisdom → Predict Consequences → Detect Fallbacks → Plan
  → Brain Decides → Execute OR Refuse → Record Outcome → Learn
```

---

## 💾 Key Files

| File | Purpose | Location |
|------|---------|----------|
| `molecular_server.py` | API server | `C:\Users\DHeavy\Downloads\Theory\` |
| `simple_web_ui.py` | Web interface | `C:\Users\DHeavy\Downloads\Theory\` |
| `background_agent.py` | Main agent | `C:\Users\DHeavy\Downloads\Theory\` |
| `agent_memory.json` | Memory storage | `C:\Users\DHeavy\Downloads\Theory\` |
| `restart_all.ps1` | Restart script | `C:\Users\DHeavy\Downloads\Theory\` |
| `status.ps1` | Status check | `C:\Users\DHeavy\Downloads\Theory\` |

---

## 🎯 When to Modify Each Component

**User getting confused by responses?**
→ Modify `Response-Formatter.py`

**AI making dumb mistakes repeatedly?**
→ Check `Previous-Mistakes.py` and `auto_learning_engine.py`

**AI refusing too much?**
→ Check `Ethics.py`, `Identifying-If-A-Fallback-Solution.py`, `Conscious-Thought.py`

**AI not learning?**
→ Check `auto_learning_engine.py`, `Wisdom.py`, `Memory.py`

**Prompt not understood?**
→ Check `Prompt-Breakdown.py`, `Conscious-Thought.py`

**Bad decisions?**
→ Check `Brain.py`, `Metacognition.py`, `Goals.py`

---

## 🔧 PowerShell Scripts

| Script | Use Case |
|--------|----------|
| `restart_all.ps1` | After code changes |
| `start_all.ps1` | Daily startup |
| `stop_all.ps1` | Shutdown |
| `status.ps1` | Check if running |

---

## 🌐 URLs

- **Chat UI**: http://localhost:3000
- **API**: http://localhost:5000
- **Health**: http://localhost:5000/health

---

## 🧪 Test Commands

```powershell
# Check server health
curl http://localhost:5000/health

# Test chat (PowerShell)
Invoke-RestMethod -Uri "http://localhost:5000/chat" -Method Post -ContentType "application/json" -Body '{"message":"Task: Hello","use_tools":false}'

# Check ports
netstat -ano | Select-String ":5000|:3000"
```

---

## 📖 Full Docs

- **All 31 components**: [COMPONENTS_README.md](COMPONENTS_README.md)
- **Management scripts**: [SCRIPTS_README.md](SCRIPTS_README.md)
- **Flutter app**: `C:\Users\DHeavy\Downloads\molecular_chat\START_HERE.md`
- **Open WebUI**: `C:\Users\DHeavy\Downloads\open-webui-main\open-webui-main\MOLECULAR_AI_INTEGRATION.md`

---

## 💀 The ONE Rule

**IT WORKS OR IT DOESN'T.**

No fallbacks. No guessing. No "close enough."

---

*Last updated: February 23, 2026*
