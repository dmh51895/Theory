"""
Habits.py

MOLECULAR PRINCIPLE: Habits are OBSERVED patterns, not programmed behaviors.

LLM AI has hardcoded patterns (templates, openers, hedging language).
MOLECULAR AI develops habits through repeated successful decisions.

Habit = Action pattern that consistently produces successful outcomes.

Requirements:
- Emerges from data (not programmed)
- Measurable success rate
- Context-specific (when to apply)
- Can be unlearned if success rate drops
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import json


@dataclass
class Habit:
    """An observed behavioral pattern."""
    pattern: str  # Description of the pattern
    context: str  # When this pattern applies
    trigger: str  # What triggers this pattern
    action: str  # What action is taken
    success_count: int  # Times this pattern succeeded
    failure_count: int  # Times this pattern failed
    first_observed: str  # ISO datetime
    last_used: str  # ISO datetime
    
    def success_rate(self) -> float:
        """Calculate success rate of this habit."""
        total = self.success_count + self.failure_count
        if total == 0:
            return 0.0
        return self.success_count / total
    
    def is_reliable(self, threshold: float = 0.8) -> bool:
        """Check if habit is reliable enough to use."""
        return self.success_rate() >= threshold and self.success_count >= 3


class HabitTracker:
    """
    Tracks and applies behavioral habits.
    
    Key principle: Habits EMERGE from experience, not from programming.
    """
    
    def __init__(self):
        self.habits: List[Habit] = []
        self.potential_habits: Dict[str, Dict] = {}  # Patterns being evaluated
    
    def observe_decision(self, decision_data: Dict, outcome: Dict):
        """
        Observe a decision and its outcome.
        
        Extracts potential patterns that could become habits.
        """
        # Extract pattern from decision
        pattern = self._extract_pattern(decision_data)
        if not pattern:
            return
        
        pattern_key = pattern['key']
        success = outcome.get('success', False)
        
        # Update potential habit
        if pattern_key not in self.potential_habits:
            self.potential_habits[pattern_key] = {
                'pattern': pattern['description'],
                'context': pattern['context'],
                'trigger': pattern['trigger'],
                'action': pattern['action'],
                'successes': 0,
                'failures': 0,
                'first_seen': datetime.now().isoformat()
            }
        
        if success:
            self.potential_habits[pattern_key]['successes'] += 1
        else:
            self.potential_habits[pattern_key]['failures'] += 1
        
        # Check if qualifies as habit
        self._evaluate_potential_habit(pattern_key)
    
    def _extract_pattern(self, decision_data: Dict) -> Optional[Dict]:
        """
        Extract behavioral pattern from decision.
        
        Looks for repeatable trigger-action sequences.
        """
        patterns = []
        
        # Pattern 1: Low clarity → Request clarification
        if 'conscious_analysis' in decision_data:
            clarity = decision_data['conscious_analysis'].get('clarity', 1.0)
            if clarity < 0.7:
                decision = decision_data.get('decision', {})
                if 'clarification' in decision.get('action', '').lower():
                    patterns.append({
                        'key': 'low_clarity_clarification',
                        'description': 'Request clarification when clarity < 0.7',
                        'context': 'Ambiguous prompt',
                        'trigger': f'clarity < 0.7 (was {clarity:.2f})',
                        'action': 'Request clarification'
                    })
        
        # Pattern 2: High fallback score → Use fallback corrector
        if 'fallback_detection' in decision_data:
            if decision_data['fallback_detection'].get('is_fallback_thinking', False):
                if decision_data['fallback_detection'].get('corrector_used', False):
                    patterns.append({
                        'key': 'fallback_correction',
                        'description': 'Use fallback corrector when fallback detected',
                        'context': 'Fallback thinking detected',
                        'trigger': 'is_fallback_thinking = True',
                        'action': 'Apply fallback corrector'
                    })
        
        # Pattern 3: Past mistakes exist → Check before proceeding
        if 'mistake_check' in decision_data:
            similar = decision_data['mistake_check'].get('similar_mistakes', [])
            if similar:
                heeded = decision_data.get('heeded_warnings', False)
                if heeded:
                    patterns.append({
                        'key': 'heed_past_mistakes',
                        'description': 'Check past mistakes before similar actions',
                        'context': 'Similar past failures exist',
                        'trigger': 'similar_mistakes detected',
                        'action': 'Review and adjust approach'
                    })
        
        # Pattern 4: Multiple goals → Choose highest priority
        if 'goal_alignment' in decision_data:
            aligned_goals = decision_data['goal_alignment'].get('aligned_goals', [])
            if len(aligned_goals) > 1:
                patterns.append({
                    'key': 'prioritize_goals',
                    'description': 'When multiple goals apply, choose highest priority',
                    'context': 'Multiple applicable goals',
                    'trigger': 'len(aligned_goals) > 1',
                    'action': 'Select highest priority goal'
                })
        
        return patterns[0] if patterns else None
    
    def _evaluate_potential_habit(self, pattern_key: str):
        """
        Check if potential habit qualifies as a habit.
        
        Requirements: 3+ observations, 80%+ success rate.
        """
        potential = self.potential_habits[pattern_key]
        total = potential['successes'] + potential['failures']
        
        if total < 3:
            return  # Not enough data
        
        success_rate = potential['successes'] / total
        if success_rate < 0.8:
            return  # Not reliable enough
        
        # Promote to habit
        habit = Habit(
            pattern=potential['pattern'],
            context=potential['context'],
            trigger=potential['trigger'],
            action=potential['action'],
            success_count=potential['successes'],
            failure_count=potential['failures'],
            first_observed=potential['first_seen'],
            last_used=datetime.now().isoformat()
        )
        
        # Check if already exists (update instead)
        for existing in self.habits:
            if existing.pattern == habit.pattern:
                existing.success_count += habit.success_count
                existing.failure_count += habit.failure_count
                existing.last_used = habit.last_used
                return
        
        self.habits.append(habit)
    
    def get_applicable_habits(self, context: Dict) -> List[Habit]:
        """
        Get habits that apply to current context.
        
        Returns only reliable habits.
        """
        applicable = []
        
        for habit in self.habits:
            if not habit.is_reliable():
                continue
            
            # Check if context matches
            if self._context_matches(habit, context):
                applicable.append(habit)
        
        return sorted(applicable, key=lambda h: h.success_rate(), reverse=True)
    
    def _context_matches(self, habit: Habit, context: Dict) -> bool:
        """Check if habit's context matches current context."""
        # Extract context string
        context_str = json.dumps(context).lower()
        habit_context = habit.context.lower()
        
        # Simple keyword matching
        keywords = habit_context.split()
        matches = sum(1 for kw in keywords if kw in context_str)
        
        return matches > len(keywords) * 0.5
    
    def record_habit_usage(self, habit: Habit, success: bool):
        """
        Record outcome of using a habit.
        
        Updates habit statistics.
        """
        habit.last_used = datetime.now().isoformat()
        if success:
            habit.success_count += 1
        else:
            habit.failure_count += 1
        
        # Check if habit is no longer reliable
        if not habit.is_reliable(threshold=0.7):  # Lower threshold for unlearning
            # Mark for potential removal
            pass  # Could implement automatic removal
    
    def format_habits_summary(self) -> str:
        """Format habits for review."""
        lines = ["LEARNED HABITS:", ""]
        
        if not self.habits:
            return "No habits learned yet. Habits emerge from repeated successful patterns."
        
        reliable = [h for h in self.habits if h.is_reliable()]
        unreliable = [h for h in self.habits if not h.is_reliable()]
        
        if reliable:
            lines.append("RELIABLE HABITS (80%+ success):")
            for habit in sorted(reliable, key=lambda h: h.success_rate(), reverse=True):
                lines.append(f"  ✓ {habit.pattern}")
                lines.append(f"    Context: {habit.context}")
                lines.append(f"    Trigger: {habit.trigger}")
                lines.append(f"    Action: {habit.action}")
                lines.append(f"    Success rate: {habit.success_rate():.1%} ({habit.success_count}/{habit.success_count + habit.failure_count})")
                lines.append("")
        
        if unreliable:
            lines.append("UNRELIABLE HABITS (<80% success):")
            for habit in unreliable:
                lines.append(f"  ? {habit.pattern}")
                lines.append(f"    Success rate: {habit.success_rate():.1%}")
                lines.append("")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test habit tracking
    tracker = HabitTracker()
    
    # Simulate repeated successful pattern: Low clarity → Request clarification
    for i in range(5):
        decision = {
            'conscious_analysis': {'clarity': 0.5},
            'decision': {'action': 'request_clarification'}
        }
        outcome = {'success': True}
        tracker.observe_decision(decision, outcome)
    
    # Simulate one failure
    decision = {
        'conscious_analysis': {'clarity': 0.5},
        'decision': {'action': 'request_clarification'}
    }
    outcome = {'success': False}
    tracker.observe_decision(decision, outcome)
    
    print(tracker.format_habits_summary())
