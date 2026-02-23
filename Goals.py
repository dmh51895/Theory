#!/usr/bin/env python3
"""
🎯 GOALS 🎯

MOLECULAR PRINCIPLE: Know what you're trying to achieve.

This is NOT a vague mission statement.
This is CONCRETE OBJECTIVES.

Tracks:
- What we're trying to accomplish (current goals)
- Why we're doing it (purpose alignment)
- How success is measured (concrete metrics)
- Progress toward goals (quantified)

The difference:
- LLM AI: "Help the user" (vague, unmeasurable)
- MOLECULAR AI: "Complete user's request with X criteria met" (specific, measurable)

Goals inform every decision. If an action doesn't serve a goal, why do it?

Goals are COMMITTED. Once set, they guide all thinking until:
1. Goal achieved (measured success)
2. Goal abandoned (explicit decision)
3. Goal modified (reasoned change)

No drift. No vague "kinda sorta working toward something."
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json
from pathlib import Path


@dataclass
class Goal:
    """A concrete, measurable objective."""
    id: str
    description: str
    purpose: str  # Why this goal exists
    success_criteria: List[str]  # How we know it's achieved
    priority: str  # "critical", "high", "medium", "low"
    status: str  # "active", "achieved", "abandoned", "blocked"
    created_at: str
    progress: float  # 0.0 to 1.0
    dependencies: List[str]  # Other goal IDs this depends on
    
    def is_achieved(self) -> bool:
        return self.status == "achieved"
    
    def is_active(self) -> bool:
        return self.status == "active"


class GoalManager:
    """
    Manages system goals and tracks progress.
    
    This ensures all actions serve a purpose.
    """
    
    def __init__(self, goals_file: str = "agent_memory.json"):
        self.goals_file = Path(goals_file)
        self.goals: List[Goal] = []
        self._load_goals()
    
    def _load_goals(self):
        """Load goals from memory."""
        if self.goals_file.exists():
            try:
                with open(self.goals_file, 'r') as f:
                    data = json.load(f)
                    goals_data = data.get('goals', [])
                    self.goals = [Goal(**g) for g in goals_data]
            except Exception:
                pass
    
    def _save_goals(self):
        """Persist goals to memory."""
        try:
            # Load existing data
            data = {}
            if self.goals_file.exists():
                with open(self.goals_file, 'r') as f:
                    data = json.load(f)
            
            # Update goals section
            data['goals'] = [asdict(g) for g in self.goals]
            
            # Save
            with open(self.goals_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise RuntimeError(f"Failed to save goals: {e}")
    
    def add_goal(self, description: str, purpose: str, 
                 success_criteria: List[str], priority: str = "high") -> Goal:
        """Add a new goal."""
        goal = Goal(
            id=f"goal_{len(self.goals) + 1}_{datetime.now().timestamp()}",
            description=description,
            purpose=purpose,
            success_criteria=success_criteria,
            priority=priority,
            status="active",
            created_at=datetime.now().isoformat(),
            progress=0.0,
            dependencies=[]
        )
        
        self.goals.append(goal)
        self._save_goals()
        return goal
    
    def check_alignment(self, proposed_action: str) -> Dict[str, Any]:
        """
        Check if a proposed action aligns with active goals.
        
        Returns:
            {
                "aligns_with_goals": bool,
                "aligned_goals": List[str],
                "conflicts": List[str],
                "priority": str
            }
        """
        
        active_goals = [g for g in self.goals if g.is_active()]
        
        if not active_goals:
            return {
                "aligns_with_goals": False,
                "aligned_goals": [],
                "conflicts": ["No active goals - action has no purpose"],
                "priority": "none"
            }
        
        # Check which goals this action serves
        aligned = []
        for goal in active_goals:
            if self._action_serves_goal(proposed_action, goal):
                aligned.append(goal.id)
        
        if not aligned:
            return {
                "aligns_with_goals": False,
                "aligned_goals": [],
                "conflicts": ["Action doesn't serve any active goal"],
                "priority": "none"
            }
        
        # Get highest priority of aligned goals
        priorities = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        max_priority = max(priorities.get(g.priority, 0) 
                          for g in active_goals if g.id in aligned)
        priority_map = {v: k for k, v in priorities.items()}
        
        return {
            "aligns_with_goals": True,
            "aligned_goals": aligned,
            "conflicts": [],
            "priority": priority_map.get(max_priority, "low")
        }
    
    def _action_serves_goal(self, action: str, goal: Goal) -> bool:
        """Check if an action serves a goal."""
        action_lower = action.lower()
        goal_lower = goal.description.lower()
        
        # Simple keyword matching
        action_words = set(action_lower.split())
        goal_words = set(goal_lower.split())
        overlap = action_words & goal_words
        
        return len(overlap) >= 2  # At least 2 words in common
    
    def update_progress(self, goal_id: str, progress: float):
        """Update goal progress."""
        for goal in self.goals:
            if goal.id == goal_id:
                goal.progress = max(0.0, min(1.0, progress))
                if goal.progress >= 1.0:
                    goal.status = "achieved"
                self._save_goals()
                break
    
    def get_active_goals(self) -> List[Goal]:
        """Get all active goals."""
        return [g for g in self.goals if g.is_active()]
    
    def get_summary(self) -> str:
        """Get human-readable summary of goals."""
        active = self.get_active_goals()
        achieved = [g for g in self.goals if g.is_achieved()]
        
        if not active and not achieved:
            return "No goals set. System has no purpose."
        
        lines = ["Current Goals:"]
        for goal in active:
            lines.append(f"  [{goal.priority.upper()}] {goal.description}")
            lines.append(f"    Progress: {goal.progress:.0%}")
            lines.append(f"    Purpose: {goal.purpose}")
        
        if achieved:
            lines.append(f"\nAchieved: {len(achieved)} goals completed")
        
        return "\n".join(lines)


if __name__ == "__main__":
    manager = GoalManager("test_goals.json")
    
    # Add a goal
    goal = manager.add_goal(
        description="Build molecular AI system",
        purpose="Replace LLM AI with committed decision-making",
        success_criteria=[
            "All components implemented",
            "Fallback detection working",
            "Molecular ratio > 90%"
        ],
        priority="critical"
    )
    
    print(manager.get_summary())
    print()
    
    # Check alignment
    alignment = manager.check_alignment("Implement fallback detector")
    print(f"Action alignment: {alignment}")
