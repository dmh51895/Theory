"""
auto_learning_engine.py

MOLECULAR PRINCIPLE: Learning is AUTOMATED observation, not manual tuning.

LLM AI doesn't learn from interactions (static weights).
MOLECULAR AI learns continuously from every decision and outcome.

Auto-learning = Automatic pattern extraction from experience.

What to learn:
- Which decisions succeed (wisdom)
- Which decisions fail (mistakes)
- Which patterns predict outcomes (habits)
- Which approaches work in which contexts (strategy)

Learning loop:
1. Decision made
2. Outcome observed
3. Pattern extracted
4. Knowledge updated
5. Future decisions benefit

NO manual intervention needed. FULLY AUTOMATED.
"""

from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class LearningCycle:
    """A single learning cycle."""
    cycle_id: str
    decision_data: Dict
    outcome_data: Dict
    patterns_extracted: int
    wisdom_added: int
    mistakes_recorded: int
    habits_updated: int
    timestamp: str


class AutoLearningEngine:
    """
    Automated learning from every decision-outcome pair.
    
    Key principle: Learning happens automatically, not manually.
    """
    
    def __init__(self, brain, memory, wisdom_extractor, mistake_tracker, 
                 habit_tracker, pattern_synchronizer):
        """Initialize with all learning components."""
        self.brain = brain
        self.memory = memory
        self.wisdom_extractor = wisdom_extractor
        self.mistake_tracker = mistake_tracker
        self.habit_tracker = habit_tracker
        self.pattern_synchronizer = pattern_synchronizer
        
        self.learning_history = []
        self.total_cycles = 0
    
    def learn_from_decision(self, decision_data: Dict, outcome_data: Dict):
        """
        Main learning function: extract knowledge from decision-outcome pair.
        
        This is called automatically after every decision execution.
        """
        cycle_id = f"learning_cycle_{self.total_cycles + 1}"
        
        # Step 1: Record in memory
        self.memory.store_decision(decision_data)
        self.memory.store_outcome(outcome_data)
        
        patterns_extracted = 0
        wisdom_added = 0
        mistakes_recorded = 0
        habits_updated = 0
        
        # Step 2: Extract wisdom if successful
        if outcome_data.get('success', False):
            self.wisdom_extractor.extract_from_successful_decision(decision_data, outcome_data)
            wisdom_added = 1
            patterns_extracted += 1
        else:
            # Extract anti-patterns from failure
            self.wisdom_extractor.extract_from_failed_decision(decision_data, outcome_data)
            
            # Record mistake - Opus Fix #4: Use correct signature
            self.mistake_tracker.record_mistake(
                prompt=decision_data.get('thought_stream', {}).get('prompt', 'unknown'),
                approach=decision_data.get('decision', {}).get('approach', 'unknown'),
                decision=decision_data.get('decision', {}),
                outcome=outcome_data
            )
            mistakes_recorded = 1
            patterns_extracted += 1
        
        # Step 3: Update habits
        self.habit_tracker.observe_decision(decision_data, outcome_data)
        habits_updated = 1
        
        # Step 4: Synchronize patterns across components
        if 'fallback_detection' in decision_data:
            if decision_data['fallback_detection'].get('is_fallback_thinking', False):
                self.pattern_synchronizer.register_pattern(
                    pattern_id=f"fallback_{cycle_id}",
                    pattern_type="fallback",
                    pattern_data=decision_data['fallback_detection'],
                    observed_by="AutoLearningEngine"
                )
                patterns_extracted += 1
        
        # Step 5: Record learning cycle
        cycle = LearningCycle(
            cycle_id=cycle_id,
            decision_data=decision_data,
            outcome_data=outcome_data,
            patterns_extracted=patterns_extracted,
            wisdom_added=wisdom_added,
            mistakes_recorded=mistakes_recorded,
            habits_updated=habits_updated,
            timestamp=datetime.now().isoformat()
        )
        
        self.learning_history.append(cycle)
        self.total_cycles += 1
        
        return cycle
    
    def get_learning_rate(self) -> Dict[str, float]:
        """
        Calculate how much learning is happening.
        
        Returns learning metrics.
        """
        if self.total_cycles == 0:
            return {
                'cycles_per_hour': 0.0,
                'patterns_per_cycle': 0.0,
                'wisdom_extraction_rate': 0.0,
                'mistake_learning_rate': 0.0
            }
        
        # Calculate rates from recent history
        recent = self.learning_history[-100:]  # Last 100 cycles
        
        total_patterns = sum(c.patterns_extracted for c in recent)
        total_wisdom = sum(c.wisdom_added for c in recent)
        total_mistakes = sum(c.mistakes_recorded for c in recent)
        
        return {
            'total_cycles': self.total_cycles,
            'patterns_per_cycle': total_patterns / len(recent),
            'wisdom_extraction_rate': total_wisdom / len(recent),
            'mistake_learning_rate': total_mistakes / len(recent)
        }
    
    def assess_learning_health(self) -> Dict:
        """
        Assess if learning system is functioning properly.
        
        Returns health metrics.
        """
        rates = self.get_learning_rate()
        
        # Healthy learning should extract patterns regularly
        pattern_health = rates['patterns_per_cycle'] > 0.5
        
        # Should be learning from both successes and failures
        wisdom_health = rates['wisdom_extraction_rate'] > 0.1
        mistake_health = rates['mistake_learning_rate'] > 0.05
        
        overall_health = pattern_health and (wisdom_health or mistake_health)
        
        return {
            'healthy': overall_health,
            'pattern_extraction': 'GOOD' if pattern_health else 'LOW',
            'wisdom_learning': 'GOOD' if wisdom_health else 'LOW',
            'mistake_learning': 'GOOD' if mistake_health else 'LOW',
            'total_cycles': self.total_cycles
        }
    
    def get_knowledge_summary(self) -> Dict:
        """Get summary of accumulated knowledge - Opus Fix #5."""
        return {
            'total_decisions': len(self.memory.data['decisions']),
            'wisdom_items': len(self.wisdom_extractor.wisdom_items),
            'recorded_mistakes': len(self.mistake_tracker.mistakes),
            'learned_habits': len(self.habit_tracker.habits),
            'shared_patterns': len(self.pattern_synchronizer.shared_patterns),
            'molecular_ratio': self.brain.state.molecular_ratio()
        }
    
    def format_learning_summary(self) -> str:
        """Format learning summary for display."""
        lines = ["AUTO-LEARNING ENGINE STATUS:", ""]
        
        rates = self.get_learning_rate()
        health = self.assess_learning_health()
        knowledge = self.get_knowledge_summary()
        
        lines.append(f"Health: {'✓ HEALTHY' if health['healthy'] else '✗ UNHEALTHY'}")
        lines.append(f"Total cycles: {self.total_cycles}")
        lines.append("")
        
        lines.append("LEARNING RATES:")
        lines.append(f"  Patterns per cycle: {rates['patterns_per_cycle']:.2f}")
        lines.append(f"  Wisdom extraction: {rates['wisdom_extraction_rate']:.0%}")
        lines.append(f"  Mistake learning: {rates['mistake_learning_rate']:.0%}")
        lines.append("")
        
        lines.append("KNOWLEDGE BASE:")
        for key, value in knowledge.items():
            lines.append(f"  {key}: {value}")
        lines.append("")
        
        if self.learning_history:
            recent = self.learning_history[-5:]
            lines.append("RECENT LEARNING CYCLES:")
            for cycle in recent:
                lines.append(f"  {cycle.cycle_id}:")
                lines.append(f"    Patterns: {cycle.patterns_extracted}, Wisdom: {cycle.wisdom_added}, Mistakes: {cycle.mistakes_recorded}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test auto-learning engine (simplified - uses mock objects)
    print("Auto-learning engine requires full system integration.")
    print("Install by importing into Brain.py and calling after each decision.")
    print()
    print("Usage:")
    print("  auto_learner = AutoLearningEngine(brain, memory, wisdom, mistakes, habits, patterns)")
    print("  auto_learner.learn_from_decision(decision_data, outcome_data)")
    print("  print(auto_learner.format_learning_summary())")
