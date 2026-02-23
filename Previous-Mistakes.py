#!/usr/bin/env python3
"""
❌ PREVIOUS-MISTAKES ❌

MOLECULAR PRINCIPLE: Learn from failures. Don't repeat them.

This is NOT a log file that gets ignored.
This is ACTIVE LEARNING.

When Brain makes a decision that leads to failure:
1. Mistake is recorded with full context
2. Root cause is analyzed
3. Pattern is extracted
4. Check added to prevent recurrence

The difference:
- LLM AI: Repeats same mistakes infinitely (stateless)
- MOLECULAR AI: Makes each mistake exactly once (learning)

Mistake structure:
{
    "prompt": ...,
    "decision": ...,
    "outcome": ...,
    "root_cause": ...,
    "pattern": ...,
    "prevention": "How to avoid this"
}

Before each decision, Previous-Mistakes is consulted:
"Have we tried this before? Did it fail? Why?"

If yes: Don't repeat. If we must try it, acknowledge the risk.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json
from pathlib import Path


@dataclass
class Mistake:
    """A recorded failure to learn from."""
    id: str
    prompt: str
    approach: str
    decision: Dict[str, Any]
    outcome: Dict[str, Any]
    root_cause: str
    pattern: str
    prevention_strategy: str
    timestamp: str
    repeated: int  # How many times we've made this mistake


class MistakeTracker:
    """
    Tracks mistakes and prevents repetition.
    
    This is the learning mechanism.
    """
    
    def __init__(self, memory_file: str = "agent_memory.json"):
        self.memory_file = Path(memory_file)
        self.mistakes: List[Mistake] = []
        self._load()
    
    def _load(self):
        """Load mistakes from memory."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    mistakes_data = data.get('mistakes', [])
                    self.mistakes = [Mistake(**m) for m in mistakes_data]
            except Exception:
                pass
    
    def _save(self):
        """Save mistakes to memory."""
        try:
            data = {}
            if self.memory_file.exists():
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
            
            data['mistakes'] = [asdict(m) for m in self.mistakes]
            
            with open(self.memory_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise RuntimeError(f"Failed to save mistakes: {e}")
    
    def record_mistake(self, prompt: str, approach: str,
                      decision: Dict[str, Any],
                      outcome: Dict[str, Any]) -> Mistake:
        """
        Record a new mistake.
        
        Analyzes the failure and extracts learnings.
        """
        
        # Analyze root cause
        root_cause = self._analyze_root_cause(decision, outcome)
        
        # Extract pattern
        pattern = self._extract_pattern(approach, root_cause)
        
        # Determine prevention strategy
        prevention = self._determine_prevention(pattern, root_cause)
        
        # Check if we've made this mistake before
        similar = self._find_similar_mistake(pattern)
        repeated = similar.repeated + 1 if similar else 1
        
        mistake = Mistake(
            id=f"mistake_{len(self.mistakes) + 1}_{datetime.now().timestamp()}",
            prompt=prompt,
            approach=approach,
            decision=decision,
            outcome=outcome,
            root_cause=root_cause,
            pattern=pattern,
            prevention_strategy=prevention,
            timestamp=datetime.now().isoformat(),
            repeated=repeated
        )
        
        self.mistakes.append(mistake)
        self._save()
        
        return mistake
    
    def check_before_decision(self, proposed_approach: str) -> Dict[str, Any]:
        """
        Check if we've made mistakes with this approach before.
        
        Returns warnings if yes.
        """
        
        relevant = self._find_relevant_mistakes(proposed_approach)
        
        if not relevant:
            return {
                "warnings": [],
                "should_proceed": True,
                "alternative_suggested": None
            }
        
        # We've failed with this approach before
        warnings = []
        most_recent = relevant[-1]
        
        warnings.append(
            f"This approach failed before: {most_recent.root_cause}"
        )
        
        if most_recent.repeated > 1:
            warnings.append(
                f"⚠️ REPEATED MISTAKE: Failed {most_recent.repeated} times with this pattern"
            )
        
        return {
            "warnings": warnings,
            "should_proceed": False,  # Recommend not repeating
            "alternative_suggested": most_recent.prevention_strategy,
            "past_mistakes": [asdict(m) for m in relevant]
        }
    
    def _analyze_root_cause(self, decision: Dict, outcome: Dict) -> str:
        """Determine why it failed."""
        error = outcome.get('error', 'Unknown error')
        error_type = outcome.get('error_type', '')
        
        # Common root causes
        if 'FileNotFound' in error_type:
            return "File path invalid or file doesn't exist"
        elif 'Permission' in error_type:
            return "Insufficient permissions"
        elif 'NotImplemented' in error_type:
            return "Approach not implemented in Motor-Control"
        elif 'fallback' in str(decision).lower():
            return "Decision contained fallback patterns"
        else:
            return f"{error_type}: {error}"
    
    def _extract_pattern(self, approach: str, root_cause: str) -> str:
        """
        Extract the mistake pattern.
        
        Pattern is a generalization that applies to similar situations.
        """
        
        # Extract key words from approach
        approach_words = approach.lower().split('_')
        main_action = approach_words[0] if approach_words else 'unknown'
        
        # Combine with cause
        return f"{main_action}_causing_{root_cause.split(':')[0]}"
    
    def _determine_prevention(self, pattern: str, root_cause: str) -> str:
        """How to prevent this mistake in the future."""
        
        if 'file' in pattern.lower():
            return "Validate file path exists before operations"
        elif 'permission' in root_cause.lower():
            return "Check permissions before attempting operation"
        elif 'fallback' in root_cause.lower():
            return "Use molecular approach without fallbacks"
        elif 'not_implemented' in pattern.lower():
            return "Register action handler in Motor-Control before execution"
        else:
            return f"Review and fix: {root_cause}"
    
    def _find_similar_mistake(self, pattern: str) -> Optional[Mistake]:
        """Find a previously made mistake with same pattern."""
        for mistake in reversed(self.mistakes):
            if mistake.pattern == pattern:
                return mistake
        return None
    
    def _find_relevant_mistakes(self, approach: str) -> List[Mistake]:
        """Find mistakes relevant to this approach."""
        approach_words = set(approach.lower().split('_'))
        relevant = []
        
        for mistake in self.mistakes:
            mistake_words = set(mistake.approach.lower().split('_'))
            overlap = approach_words & mistake_words
            
            if len(overlap) >= 2:  # At least 2 words match
                relevant.append(mistake)
        
        return relevant
    
    def get_most_repeated_mistakes(self, limit: int = 5) -> List[Mistake]:
        """Get mistakes we keep repeating."""
        repeated = [m for m in self.mistakes if m.repeated > 1]
        repeated.sort(key=lambda m: m.repeated, reverse=True)
        return repeated[:limit]
    
    def get_summary(self) -> str:
        """Get summary of mistakes."""
        total = len(self.mistakes)
        repeated = len([m for m in self.mistakes if m.repeated > 1])
        
        if not self.mistakes:
            return "No mistakes recorded yet. (Or perfect execution!)"
        
        lines = [f"Total mistakes recorded: {total}"]
        lines.append(f"Repeated mistakes: {repeated}")
        
        if repeated > 0:
            lines.append("\nMost repeated:")
            for m in self.get_most_repeated_mistakes(3):
                lines.append(f"  - {m.pattern} (x{m.repeated}): {m.prevention_strategy}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    tracker = MistakeTracker("test_memory.json")
    
    # Record a test mistake
    mistake = tracker.record_mistake(
        prompt="Create a file",
        approach="create_file_wrong_path",
        decision={"action": "execute", "approach": "create_file_wrong_path"},
        outcome={"success": False, "error": "File path invalid", "error_type": "FileNotFoundError"}
    )
    
    print(f"Mistake recorded: {mistake.pattern}")
    print(f"Prevention: {mistake.prevention_strategy}")
    print()
    
    # Check before repeating
    check = tracker.check_before_decision("create_file_wrong_path")
    print(f"Should proceed: {check['should_proceed']}")
    print(f"Warnings: {check['warnings']}")
