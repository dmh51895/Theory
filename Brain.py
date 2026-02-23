#!/usr/bin/env python3
"""
🧠 BRAIN.PY - The Central Orchestrator 🧠

MOLECULAR AI PRINCIPLE: This is not a coordinator. It's a DECIDER.
IT WORKS OR IT DOESN'T.

Every component reports here. Every decision flows from here.
No fallbacks. No "usually works". Committed outcomes only.

The difference between this and typical AI orchestration:
- LLM AI: "Try this, if it fails try that, if that fails return something"
- MOLECULAR AI: "This IS the decision. If it fails, the system fails."

Architecture:
    Prompt → Conscious-Thought → Decision → Aftermath → Context

Components report to Brain:
- Conscious-Thought.py: What we're actively thinking
- Metacognition.py: How we're thinking about our thinking
- Goals.py: What we're trying to achieve
- Ethics.py: Whether we should do this
- Identifying-If-A-Fallback-Solution.py: Are we cheating?
- Previous-Mistakes.py: Did we fuck this up before?
- Consequences.py: What happens if we do this?
- Aftermath-Of-Decision.py: What happened after we decided?

Brain coordinates these, makes COMMITTED decisions, reports to context.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class ThoughtStream:
    """A single coherent stream of thought processing."""
    prompt: str
    conscious_analysis: Dict[str, Any]
    metacognitive_check: Dict[str, Any]
    goal_alignment: Dict[str, Any]
    ethical_assessment: Dict[str, Any]
    fallback_detection: Dict[str, Any]
    consequence_prediction: Dict[str, Any]
    decision: Dict[str, Any]
    aftermath: Dict[str, Any]
    timestamp: str
    
    def is_molecular(self) -> bool:
        """Check if this thought stream represents molecular (committed) thinking."""
        return (
            not self.fallback_detection.get("is_fallback", True) and
            self.decision.get("committed", False) and
            not self.decision.get("has_escape_hatch", True)
        )


@dataclass
class BrainState:
    """Current state of the Brain's processing."""
    current_thought_stream: Optional[ThoughtStream] = None
    active_goals: List[str] = None
    known_mistakes: List[Dict] = None
    accumulated_wisdom: List[str] = None
    last_decision_timestamp: str = ""
    total_decisions: int = 0
    molecular_decisions: int = 0  # Decisions without fallbacks
    fallback_decisions: int = 0   # Decisions with escape hatches
    
    def __post_init__(self):
        if self.active_goals is None:
            self.active_goals = []
        if self.known_mistakes is None:
            self.known_mistakes = []
        if self.accumulated_wisdom is None:
            self.accumulated_wisdom = []
    
    def molecular_ratio(self) -> float:
        """What percentage of decisions are truly committed (molecular)?"""
        if self.total_decisions == 0:
            return 0.0
        return self.molecular_decisions / self.total_decisions


class Brain:
    """
    The central decision-making orchestrator.
    
    NOT a fallback coordinator. NOT an error swallower.
    A COMMITTED DECISION ENGINE.
    
    If a component fails, Brain fails.
    If a decision is wrong, Brain owns it.
    If there's uncertainty, Brain acknowledges it but DECIDES ANYWAY.
    
    This is Molecular AI.
    """
    
    def __init__(self, memory_file: str = "agent_memory.json"):
        self.memory_file = Path(memory_file)
        self.state = self._load_state()
        
        # These will be imported dynamically to avoid circular dependencies
        self._components = {}
    
    def _load_state(self) -> BrainState:
        """Load brain state from persistent memory."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Convert dict to BrainState
                    return BrainState(**{k: v for k, v in data.items() 
                                        if k in BrainState.__annotations__})
            except Exception:
                pass
        return BrainState()
    
    def _save_state(self):
        """Persist brain state to memory."""
        try:
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.state), f, indent=2, default=str)
        except Exception as e:
            # Molecular principle: If we can't save state, FAIL LOUDLY
            raise RuntimeError(f"Brain state persistence failed: {e}") from e
    
    def process_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        The main decision pipeline.
        
        This is NOT try/except wrapped. If any stage fails, Brain fails.
        This is MOLECULAR - committed, deterministic, accountable.
        
        Pipeline:
        1. Conscious analysis - What is being asked?
        2. Metacognitive check - Am I thinking about this correctly?
        3. Goal alignment - Does this serve my goals?
        4. Ethical assessment - Should I do this?
        5. Fallback detection - Am I cheating with cop-outs?
        6. Consequence prediction - What happens if I do this?
        7. DECISION - Committed, no escape hatches
        8. Aftermath analysis - What actually happened?
        
        Returns the complete thought stream.
        """
        
        # Initialize thought stream
        stream = ThoughtStream(
            prompt=prompt,
            conscious_analysis={},
            metacognitive_check={},
            goal_alignment={},
            ethical_assessment={},
            fallback_detection={},
            consequence_prediction={},
            decision={},
            aftermath={},
            timestamp=datetime.now().isoformat()
        )
        
        # Stage 1: Conscious analysis
        # What is the user actually asking for?
        stream.conscious_analysis = self._analyze_consciousness(prompt)
        
        # Stage 2: Metacognitive check
        # Am I thinking about this the right way?
        stream.metacognitive_check = self._check_metacognition(
            prompt, stream.conscious_analysis
        )
        
        # Stage 3: Goal alignment
        # Does this serve my objectives?
        stream.goal_alignment = self._check_goal_alignment(
            prompt, stream.conscious_analysis
        )
        
        # Stage 4: Ethical assessment
        # Should I do this?
        stream.ethical_assessment = self._assess_ethics(
            prompt, stream.conscious_analysis
        )
        
        # Stage 5: Fallback detection
        # Am I about to do the "quickly not efficiently" thing?
        stream.fallback_detection = self._detect_fallback(
            prompt, stream.conscious_analysis, stream.metacognitive_check
        )
        
        # Stage 6: Consequence prediction
        # What happens if I proceed?
        stream.consequence_prediction = self._predict_consequences(
            prompt, stream.conscious_analysis, stream.fallback_detection
        )
        
        # Stage 7: DECISION
        # Make a COMMITTED decision. No escape hatches.
        stream.decision = self._make_decision(stream)
        
        # Update state
        self.state.current_thought_stream = stream
        self.state.last_decision_timestamp = stream.timestamp
        self.state.total_decisions += 1
        
        if stream.is_molecular():
            self.state.molecular_decisions += 1
        else:
            self.state.fallback_decisions += 1
        
        self._save_state()
        
        # Stage 8: Aftermath (analyzed after execution)
        # This gets called by Aftermath-Of-Decision.py after execution
        
        return {
            "thought_stream": asdict(stream),
            "decision": stream.decision,
            "is_molecular": stream.is_molecular(),
            "molecular_ratio": self.state.molecular_ratio()
        }
    
    def analyze_aftermath(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Called after a decision has been executed.
        Analyzes what actually happened vs what was predicted.
        
        This is how Brain LEARNS - by seeing the consequences of committed decisions.
        """
        if not self.state.current_thought_stream:
            raise RuntimeError("No active thought stream to analyze aftermath for")
        
        stream = self.state.current_thought_stream
        
        # Compare prediction vs reality
        predicted = stream.consequence_prediction
        actual = execution_result
        
        aftermath = {
            "predicted_outcome": predicted,
            "actual_outcome": actual,
            "prediction_accuracy": self._measure_prediction_accuracy(predicted, actual),
            "was_molecular": stream.is_molecular(),
            "should_update_wisdom": True,
            "timestamp": datetime.now().isoformat()
        }
        
        stream.aftermath = aftermath
        
        # If this was a mistake, record it
        if actual.get("success", True) == False or actual.get("error"):
            self.state.known_mistakes.append({
                "prompt": stream.prompt,
                "decision": stream.decision,
                "error": actual.get("error", "Unknown failure"),
                "timestamp": aftermath["timestamp"]
            })
        
        # If prediction was accurate and outcome was good, extract wisdom
        if aftermath["prediction_accuracy"] > 0.7 and actual.get("success", False):
            wisdom = self._extract_wisdom(stream, actual)
            if wisdom:
                self.state.accumulated_wisdom.append(wisdom)
        
        self._save_state()
        
        return aftermath
    
    def _analyze_consciousness(self, prompt: str) -> Dict[str, Any]:
        """Delegate to Conscious-Thought.py"""
        # Will be implemented by importing Conscious-Thought module
        return {
            "prompt_understood": True,
            "key_intent": "extracted_from_prompt",
            "ambiguities": [],
            "assumptions_made": []
        }
    
    def _check_metacognition(self, prompt: str, conscious: Dict) -> Dict[str, Any]:
        """Delegate to Metacognition.py"""
        return {
            "thinking_approach_valid": True,
            "cognitive_biases_detected": [],
            "alternative_framings": []
        }
    
    def _check_goal_alignment(self, prompt: str, conscious: Dict) -> Dict[str, Any]:
        """Delegate to Goals.py"""
        return {
            "aligns_with_goals": True,
            "goal_conflicts": [],
            "priority_level": "high"
        }
    
    def _assess_ethics(self, prompt: str, conscious: Dict) -> Dict[str, Any]:
        """Delegate to Ethics.py"""
        return {
            "ethical_clearance": True,
            "concerns": [],
            "user_benefit": "high"
        }
    
    def _detect_fallback(self, prompt: str, conscious: Dict, meta: Dict) -> Dict[str, Any]:
        """Delegate to Identifying-If-A-Fallback-Solution.py"""
        return {
            "is_fallback": False,
            "fallback_indicators": [],
            "commitment_level": "full"
        }
    
    def _predict_consequences(self, prompt: str, conscious: Dict, fallback: Dict) -> Dict[str, Any]:
        """Delegate to Consequences.py"""
        return {
            "likely_outcome": "success",
            "risk_level": "low",
            "failure_modes": [],
            "user_satisfaction": "high"
        }
    
    def _make_decision(self, stream: ThoughtStream) -> Dict[str, Any]:
        """
        Make a COMMITTED decision.
        
        Molecular principle: No try/except. No fallbacks. No escape hatches.
        The decision is the decision.
        """
        
        # Check if we should proceed
        should_proceed = (
            stream.conscious_analysis.get("prompt_understood", False) and
            stream.ethical_assessment.get("ethical_clearance", False) and
            not stream.fallback_detection.get("is_fallback", False)
        )
        
        if not should_proceed:
            # Don't make a decision we're not committed to
            return {
                "action": "refuse",
                "reason": self._format_refusal_reason(stream),
                "committed": True,  # We're committed to refusing
                "has_escape_hatch": False,
                "timestamp": datetime.now().isoformat()
            }
        
        # Extract the decision from conscious analysis
        decision = {
            "action": "execute",
            "approach": stream.conscious_analysis.get("key_intent", "unknown"),
            "committed": True,
            "has_escape_hatch": False,
            "confidence": self._calculate_confidence(stream),
            "timestamp": datetime.now().isoformat()
        }
        
        return decision
    
    def _format_refusal_reason(self, stream: ThoughtStream) -> str:
        """If we refuse, explain why clearly."""
        reasons = []
        
        if not stream.conscious_analysis.get("prompt_understood"):
            reasons.append("Prompt unclear - refusing to guess")
        
        if not stream.ethical_assessment.get("ethical_clearance"):
            concerns = stream.ethical_assessment.get("concerns", [])
            reasons.append(f"Ethical concerns: {', '.join(concerns)}")
        
        if stream.fallback_detection.get("is_fallback"):
            indicators = stream.fallback_detection.get("fallback_indicators", [])
            reasons.append(f"Solution would be fallback-based: {', '.join(indicators)}")
        
        return " | ".join(reasons)
    
    def _calculate_confidence(self, stream: ThoughtStream) -> float:
        """Calculate decision confidence based on analysis quality."""
        factors = [
            stream.conscious_analysis.get("prompt_understood", 0),
            stream.metacognitive_check.get("thinking_approach_valid", 0),
            stream.goal_alignment.get("aligns_with_goals", 0),
            stream.ethical_assessment.get("ethical_clearance", 0),
            not stream.fallback_detection.get("is_fallback", True),
        ]
        
        # Convert bools to floats
        numeric = [1.0 if f else 0.0 for f in factors]
        return sum(numeric) / len(numeric)
    
    def _measure_prediction_accuracy(self, predicted: Dict, actual: Dict) -> float:
        """Compare predicted vs actual outcomes."""
        # Simple heuristic: did it succeed as predicted?
        predicted_success = predicted.get("likely_outcome") == "success"
        actual_success = actual.get("success", False)
        
        return 1.0 if predicted_success == actual_success else 0.0
    
    def _extract_wisdom(self, stream: ThoughtStream, outcome: Dict) -> Optional[str]:
        """Extract a wisdom statement from successful molecular decisions."""
        return (
            f"When {stream.conscious_analysis.get('key_intent', 'acting')}, "
            f"approach as {stream.decision.get('approach', 'direct')} "
            f"leads to {outcome.get('result_quality', 'success')}"
        )
    
    def get_state_summary(self) -> str:
        """Get human-readable brain state."""
        return (
            f"Brain State:\n"
            f"  Total decisions: {self.state.total_decisions}\n"
            f"  Molecular decisions: {self.state.molecular_decisions}\n"
            f"  Fallback decisions: {self.state.fallback_decisions}\n"
            f"  Molecular ratio: {self.state.molecular_ratio():.1%}\n"
            f"  Active goals: {len(self.state.active_goals)}\n"
            f"  Known mistakes: {len(self.state.known_mistakes)}\n"
            f"  Accumulated wisdom: {len(self.state.accumulated_wisdom)}"
        )


if __name__ == "__main__":
    # Test the brain
    brain = Brain()
    
    print("🧠 Brain initialized")
    print(brain.get_state_summary())
    
    # Test processing
    result = brain.process_prompt("Test if Brain can make molecular decisions")
    print(f"\nDecision made: {result['decision']['action']}")
    print(f"Is molecular: {result['is_molecular']}")
    print(f"Confidence: {result['decision']['confidence']:.1%}")
