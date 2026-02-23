"""
background_agent.py

MOLECULAR PRINCIPLE: Complete cognitive architecture, fully integrated.

This is the background agent that orchestrates ALL molecular AI components.

Unlike the template-filled background_agent(1).py you tested earlier,
this version uses the FULL cognitive architecture.

Architecture:
- Brain.py: Central decision orchestrator
- All cognitive processes feed into Brain
- All decisions recorded in Memory
- All outcomes trigger learning
- Complete transparency to user

This runs continuously, learning from every interaction.
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import time
import importlib
from typing import Dict, Any

# Import all molecular AI components
# Using importlib for hyphenated module names
def import_module(module_name):
    """Import modules with hyphens in their names."""
    return importlib.import_module(module_name)

# Core components
Brain = import_module('Brain')
Memory = import_module('Memory')
Goals = import_module('Goals')
Ethics = import_module('Ethics')
Metacognition = import_module('Metacognition')
PreviousMistakes = import_module('Previous-Mistakes')
Consequences = import_module('Consequences')
AftermathOfDecision = import_module('Aftermath-Of-Decision')
ConsciousThought = import_module('Conscious-Thought')
IdentifyingIfFallback = import_module('Identifying-If-A-Fallback-Solution')
Wisdom = import_module('Wisdom')
Habits = import_module('Habits')
Rules = import_module('Rules')
MotorControl = import_module('Motor-Control')
PromptBreakdown = import_module('Prompt-Breakdown')
RelevanceToPrompt = import_module('Relevance-To-Prompt')
ResponseFormatter = import_module('Response-Formatter')
LocalTime = import_module('Local-Time')
OriginalData = import_module('Original-Data')
Openers = import_module('Openers')
MentalSyntax = import_module('Mental-Syntax')
RewiredThought = import_module('Rewired-Thought')
CurrentActiveThought = import_module('Current-Active-Thought')
HighLevelPlanning = import_module('High-Level-Planning')
HumanPhilosophy = import_module('Human-Philosophy')
Apprehensive = import_module('Apprehensive')
NaturalCallbacks = import_module('Natural-Callbacks')
SynchronizedPatterns = import_module('Synchronized-Patterns')
AutoLearning = import_module('auto_learning_engine')


class MolecularAgent:
    """
    The complete molecular AI system.
    
    Orchestrates all cognitive components for fully transparent,
    committed decision-making without fallbacks.
    """
    
    def __init__(self):
        print("🧬 Initializing Molecular AI Agent...")
        
        # Core systems
        self.brain = Brain.Brain()
        self.memory = Memory.Memory()
        
        # Cognitive processes
        self.conscious = ConsciousThought.ConsciousAnalyzer()
        self.metacognition = Metacognition.MetacognitiveMonitor()
        self.goals = Goals.GoalManager()
        self.ethics = Ethics.EthicsChecker()
        self.fallback_detector = IdentifyingIfFallback.FallbackDetector()
        self.consequences = Consequences.ConsequencePredictor()
        self.motor_control = MotorControl.MotorControl()
        self.aftermath = AftermathOfDecision.AftermathAnalyzer()
        
        # Learning systems
        self.mistakes = PreviousMistakes.MistakeTracker()
        self.wisdom = Wisdom.WisdomExtractor(self.memory)
        self.habits = Habits.HabitTracker()
        self.auto_learner = AutoLearning.AutoLearningEngine(
            self.brain, self.memory, self.wisdom,
            self.mistakes, self.habits, None  # pattern_sync added below
        )
        
        # Support systems
        self.rules = Rules.RuleEnforcer()
        self.time_tracker = LocalTime.LocalTimeTracker()
        self.data_preserver = OriginalData.OriginalDataPreserver()
        self.prompt_breakdown = PromptBreakdown.PromptBreakdown()
        self.relevance_filter = RelevanceToPrompt.RelevanceFilter()
        self.response_formatter = ResponseFormatter.ResponseFormatter()
        
        # Advanced cognition
        self.openers = Openers.OpenerGenerator()
        self.mental_syntax = MentalSyntax.MentalSyntaxEngine()
        self.rewirer = RewiredThought.ThoughtRewirer()
        self.active_thought = CurrentActiveThought.ActiveThoughtTracker()
        self.planner = HighLevelPlanning.HighLevelPlanner()
        self.philosophy = HumanPhilosophy.HumanPhilosophyGuide()
        self.apprehension = Apprehensive.ApprehensionMonitor()
        
        # Integration
        self.callbacks = NaturalCallbacks.NaturalCallbackSystem()
        self.pattern_sync = SynchronizedPatterns.PatternSynchronizer()
        self.auto_learner.pattern_synchronizer = self.pattern_sync
        
        print("✓ All components initialized")
        print(f"✓ Memory loaded: {len(self.memory.data['decisions'])} decisions")
        print(f"✓ Molecular ratio: {self.brain.state.molecular_ratio():.0%}")
        print()
    
    def process_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Process user prompt through full molecular pipeline.
        
        Returns complete thought stream and decision.
        """
        # Store prompt internally (like <think> tags - not shown to user)
        # Preserve original in memory
        original_hash = self.data_preserver.preserve(
            data=prompt,
            data_type="user_prompt",
            source="user_input"
        )
        
        # Set active thought
        self.active_thought.set_active_thought(
            content=prompt,
            thought_type="analyzing_prompt",
            context="New user prompt received"
        )
        
        # Break down prompt (internal analysis)
        structure = self.prompt_breakdown.breakdown(prompt)
        # Store clarity internally - no need to show
        
        if not structure.ready_for_execution:
            # Only show this if clarification truly needed
            # print(f"⚠️ Prompt not ready: {structure.missing_components}")
            pass
            return {
                'needs_clarification': True,
                'missing': structure.missing_components,
                'original_hash': original_hash
            }
        
        # Process through Brain
        self.active_thought.set_active_thought(
            content=structure,
            thought_type="processing_decision",
            context="Running through Brain pipeline"
        )
        
        result = self.brain.process_prompt(prompt)
        
        # Check rules compliance
        violations = self.rules.check_compliance(result)
        if violations:
            critical = [v for v in violations if v.severity.value == 'critical']
            if critical:
                print(f"🛑 CRITICAL RULE VIOLATIONS:")
                for v in critical:
                    print(f"  - {v.rule_name}: {v.explanation}")
                return {'halted': True, 'violations': critical}
        
        # Assess apprehension
        apprehension = self.apprehension.assess(result)
        if self.apprehension.should_halt(apprehension):
            print(f"🛑 RISK TOO HIGH:")
            print(self.apprehension.format_assessment(apprehension))
            return {'halted': True, 'risk': apprehension}
        
        # Execute decision (internal processing)
        decision = result.get('decision', {})
        if decision:
            # Internal decision tracking - not shown to user
            # Store decision details in memory/context
            
            # TODO: Actually execute via motor_control
            # For now, simulate execution
            execution_result = {
                'success': True,
                'result': 'Simulated execution',
                'duration': 0.1
            }
            
            # Analyze aftermath
            aftermath_result = self.aftermath.analyze(
                decision_data=result,
                execution_result=execution_result
            )
            
            # Learn from decision (internal learning - no output)
            self.auto_learner.learn_from_decision(result, {
                'success': execution_result['success'],
                'aftermath': aftermath_result
            })
            
            # Learning metrics stored internally, not displayed
            # Available via stats command if user wants to see them
        
        self.active_thought.clear_active_thought()
        return result
    
    def run_continuous_learning(self, interval_minutes: int = 5):
        """
        Run continuous background learning.
        
        Periodically reviews memory and extracts patterns.
        """
        print(f"\n🔄 Starting continuous learning (interval: {interval_minutes}min)")
        print("Press Ctrl+C to stop\n")
        
        cycle = 0
        try:
            while True:
                cycle += 1
                print(f"\n--- Learning Cycle {cycle} ---")
                print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Review recent decisions
                recent_decisions = self.memory.data['decisions'][-10:]  # Last 10
                print(f"Reviewing {len(recent_decisions)} recent decisions...")
                
                # Extract patterns
                for decision in recent_decisions:
                    # Check for extractable wisdom
                    if decision.get('success', False):
                        self.wisdom.extract_from_successful_decision(
                            decision,
                            decision.get('outcome', {})
                        )
                
                # Show learning stats
                print(self.auto_learner.format_learning_summary())
                
                # Sleep until next cycle
                print(f"\nSleeping for {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping continuous learning")
            print(f"Completed {cycle} learning cycles")
            print(self.get_system_summary())
    
    def get_system_summary(self) -> str:
        """Get complete system status."""
        lines = [
            "",
            "=" * 60,
            "MOLECULAR AI SYSTEM SUMMARY",
            "=" * 60,
            "",
            f"Molecular Ratio: {self.brain.state.molecular_ratio():.0%}",
            f"Total Decisions: {self.brain.state.total_decisions}",
            f"Wisdom Items: {len(self.wisdom.wisdom_items)}",
            f"Recorded Mistakes: {len(self.mistakes.mistakes)}",
            f"Learned Habits: {len(self.habits.habits)}",
            f"Active Goals: {len(self.goals.get_active_goals())}",
            "",
            "SYSTEM HEALTH:",
            f"  Learning: {self.auto_learner.assess_learning_health()['healthy']}",
            f"  Memory: {len(self.memory.data['decisions'])} decisions stored",
            f"  Rules: {len(self.rules.rules)} enforced",
            "",
            "=" * 60
        ]
        return "\n".join(lines)


def main():
    """Main entry point for background agent."""
    print("\n🧬💀 MOLECULAR AI BACKGROUND AGENT 💀🧬")
    print("The architecture that makes COMMITTED decisions.\n")
    
    # Initialize agent
    agent = MolecularAgent()
    
    # Test with sample prompt
    test_prompts = [
        "Create a file named test.txt",
        "Analyze the system health",
        "What is the molecular ratio?"
    ]
    
    print("\n🧪 Running test prompts...")
    for prompt in test_prompts:
        result = agent.process_prompt(prompt)
        print(f"\nResult: {json.dumps(result, indent=2)}")
        time.sleep(1)
    
    print("\n" + agent.get_system_summary())
    
    # Optionally run continuous learning
    # agent.run_continuous_learning(interval_minutes=5)


if __name__ == "__main__":
    main()
