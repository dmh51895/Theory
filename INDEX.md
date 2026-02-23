# 💀🧬 MOLECULAR AI - DOCUMENTATION INDEX

## **Start Here → [README.md](README.md)**

---

## 📚 Complete Documentation Set

| Document | Purpose | Read Time | When to Use |
|----------|---------|-----------|-------------|
| **[README.md](README.md)** | Main entry point | 10 min | First time here |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | Cheat sheet | 2 min | Quick lookup |
| **[COMPONENTS_README.md](COMPONENTS_README.md)** | All 31 components | 30 min | Understanding architecture |
| **[SCRIPTS_README.md](SCRIPTS_README.md)** | PowerShell scripts | 5 min | Managing server |
| **[DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md)** | File tree | 5 min | Finding files |
| **[INDEX.md](INDEX.md)** | This file | 1 min | Navigation |

---

## ⚡ By Use Case

### "I just want to use it"
1. [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. Run `.\restart_all.ps1`
3. Open http://localhost:3000

### "I want to understand how it works"
1. [README.md](README.md) - Overview
2. [COMPONENTS_README.md](COMPONENTS_README.md) - Deep dive
3. [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) - Structure

### "I need to manage the server"
1. [SCRIPTS_README.md](SCRIPTS_README.md) - All scripts
2. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick commands

### "Something is broken"
1. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Common issues
2. Run `.\status.ps1`
3. Run `.\restart_all.ps1`
4. Check [COMPONENTS_README.md](COMPONENTS_README.md) troubleshooting

### "I want to modify the code"
1. [COMPONENTS_README.md](COMPONENTS_README.md) - Find responsible component
2. [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) - Modification patterns
3. Edit file
4. Run `.\restart_all.ps1`

---

## 🎯 By Topic

### Architecture
- [COMPONENTS_README.md](COMPONENTS_README.md) - Complete breakdown
- [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) - File relationships

### Usage
- [README.md](README.md) - Getting started
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Common tasks

### Management
- [SCRIPTS_README.md](SCRIPTS_README.md) - Scripts guide
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick commands

### Development
- [COMPONENTS_README.md](COMPONENTS_README.md) - Component details
- [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) - Code patterns

---

## 🔍 Quick Lookup

**"How do I start the system?"**
→ [QUICK_REFERENCE.md](QUICK_REFERENCE.md#quick-start)

**"What are all the components?"**
→ [COMPONENTS_README.md](COMPONENTS_README.md#file-structure-31-components)

**"Where is Brain.py?"**
→ [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md#file-tree)

**"How do I restart after code changes?"**
→ [SCRIPTS_README.md](SCRIPTS_README.md#restart_allps1---full-restart)

**"What makes this different from LLM AI?"**
→ [README.md](README.md#what-makes-this-different)

**"Which component handles X?"**
→ [COMPONENTS_README.md](COMPONENTS_README.md) - Search for your use case

**"How do the components work together?"**
→ [COMPONENTS_README.md](COMPONENTS_README.md#data-flow-how-it-all-works)

**"What's the ONE rule?"**
→ **IT WORKS OR IT DOESN'T** (see any doc)

---

## 📖 Reading Order

### For Users:
1. [README.md](README.md) - 10 min
2. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 2 min
3. Start using it!

### For Developers:
1. [README.md](README.md) - 10 min
2. [COMPONENTS_README.md](COMPONENTS_README.md) - 30 min
3. [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) - 5 min
4. Read component files themselves

### For System Admins:
1. [SCRIPTS_README.md](SCRIPTS_README.md) - 5 min
2. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 2 min
3. Run `.\status.ps1` regularly

---

## 🎓 By Skill Level

### Level 1 - Beginner
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- [README.md](README.md) (Getting Started section)
- [SCRIPTS_README.md](SCRIPTS_README.md) (Common Workflows)

### Level 2 - Intermediate
- [README.md](README.md) (full read)
- [COMPONENTS_README.md](COMPONENTS_README.md) (overview sections)
- [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md)

### Level 3 - Advanced
- [COMPONENTS_README.md](COMPONENTS_README.md) (complete)
- All 31 component source files
- `agent_memory.json` analysis

### Level 4 - Expert
- All documentation
- All source code
- Modify architecture
- Add new components

---

## 🚀 Quick Actions

```powershell
# Start everything
.\restart_all.ps1

# Check status
.\status.ps1

# Stop everything
.\stop_all.ps1
```

See [SCRIPTS_README.md](SCRIPTS_README.md) for details.

---

## 🌐 URLs

**Web UI**: http://localhost:3000  
**API**: http://localhost:5000  
**Health**: http://localhost:5000/health

---

## 📞 Support Flow

1. **Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Common issues
2. **Run `.\status.ps1`** - System health
3. **Run `.\restart_all.ps1`** - Reset
4. **Check [COMPONENTS_README.md](COMPONENTS_README.md)** - Troubleshooting
5. **Read component source** - Deep dive

---

## 💾 Key Files

| File | Purpose | Doc Reference |
|------|---------|---------------|
| `Brain.py` | Orchestrator | [COMPONENTS_README.md](COMPONENTS_README.md#brainpy) |
| `background_agent.py` | Agent runner | [COMPONENTS_README.md](COMPONENTS_README.md#background_agentpy) |
| `molecular_server.py` | API server | [README.md](README.md#access-points) |
| `simple_web_ui.py` | Web UI | [README.md](README.md#access-points) |
| `agent_memory.json` | Memory | [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md#memory-structure) |

---

## 🔥 Most Important Docs

**For 90% of users:**
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

**For understanding:**
- [COMPONENTS_README.md](COMPONENTS_README.md)

**For setup:**
- [README.md](README.md)

**For management:**
- [SCRIPTS_README.md](SCRIPTS_README.md)

**For navigation:**
- [INDEX.md](INDEX.md) (this file)

---

## 🎯 Documentation Goals

✅ Get users running quickly ([QUICK_REFERENCE.md](QUICK_REFERENCE.md))  
✅ Explain architecture deeply ([COMPONENTS_README.md](COMPONENTS_README.md))  
✅ Provide daily management ([SCRIPTS_README.md](SCRIPTS_README.md))  
✅ Show file structure ([DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md))  
✅ Serve as hub ([README.md](README.md))  
✅ Enable navigation ([INDEX.md](INDEX.md))  

---

## 💀 The Philosophy

**IT WORKS OR IT DOESN'T.**

See any doc for details on the molecular principle.

---

**Created: February 23, 2026**  
**By: Copilot + DHeavy**  
**Components: 31**  
**Lines of Code: ~9,000**  
**Docs: 6**  
**Principle: NO FALLBACKS 🧬**

---

## Navigation Tips

- **Ctrl+F** to search within docs
- Links are clickable (VS Code file links)
- All docs cross-reference each other
- Start at [README.md](README.md), branch out as needed

---

*Lost? Go back to [README.md](README.md)*
