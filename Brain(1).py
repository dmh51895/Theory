#!/usr/bin/env python3
"""
🧠 BRAIN.PY - The Central Orchestrator 🧠

MOLECULAR AI PRINCIPLE: This is not a coordinator. It's a DECIDER.
IT WORKS OR IT DOESN'T.

CORRECTED VERSION:
- All _analyze/_check/_detect methods now delegate to REAL components
- Components injected via set_components() from background_agent.py
- _save_state() no longer clobbers other JSON sections
- _calculate_confidence() uses real clarity/molecular_score/ethics data
- Stubs are flagged with _stub: True so you can detect when wiring is missing
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
    molecular_decisions: int = 0
    fallback_decisions: int = 0
    
    def __post_init__(self):
        if self.active_goals is None:
            self.active_goals = []
        if self.known_mistakes is None:
            self.known_mistakes = []
        if self.accumulated_wisdom is None:
            self.accumulated_wisdom = []
    
    def molecular_ratio(self) -> float:
        if self.total_decisions == 0:
            return 0.0
        return self.molecular_decisions / self.total_decisions


class Brain:
    """
    The central decision-making orchestrator.
    
    Components are injected via set_components() and actually used
    in the pipeline. If a component isn't wired, the method returns
    a stub dict with _stub: True.
    """
    
    def __init__(self, memory_file: str = "agent_memory.json"):
        self.memory_file = Path(memory_file)
        self.state = self._load_state()
        
        # Component references - set by background_agent.py
        self._conscious_analyzer = None
        self._metacognition_monitor = None
        self._goal_manager = None
        self._ethics_checker = None
        self._fallback_detector = None
        self._consequence_predictor = None
        self._apprehension_monitor = None
        self._rules_enforcer = None
        self._wisdom_extractor = None
        self._mistake_tracker = None
    
    def set_components(self, **components):
        """
        Inject real component instances from background_agent.py.
        
        Expected kwargs:
            conscious, metacognition, goals, ethics, fallback_detector,
            consequences, apprehension, rules, wisdom, mistakes
        """
        self._conscious_analyzer = components.get('conscious')
        self._metacognition_monitor = components.get('metacognition')
        self._goal_manager = components.get('goals')
        self._ethics_checker = components.get('ethics')
        self._fallback_detector = components.get('fallback_detector')
        self._consequence_predictor = components.get('consequences')
        self._apprehension_monitor = components.get('apprehension')
        self._rules_enforcer = components.get('rules')
        self._wisdom_extractor = components.get('wisdom')
        self._mistake_tracker = components.get('mistakes')
    
    def _load_state(self) -> BrainState:
        """Load brain state from persistent memory."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    state_fields = {}
                    valid_keys = ['active_goals', 'known_mistakes', 'accumulated_wisdom',
                                  'last_decision_timestamp', 'total_decisions',
                                  'molecular_decisions', 'fallback_decisions']
                    for k in valid_keys:
                        if k in data:
                            state_fields[k] = data[k]
                    return BrainState(**state_fields)
            except Exception:
                pass
        return BrainState()
    
    def _save_state(self):
        """
        Persist brain state to memory.
        
        CORRECTED: Loads existing JSON first, merges brain fields only,
        so Goals.py / Wisdom.py sections are not clobbered.
        """
        try:
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)
            
            existing_data = {}
            if self.memory_file.exists():
                try:
                    with open(self.memory_file, 'r', encoding='utf-8') as f:
                        existing_data = json.load(f)
                except Exception:
                    pass
            
            brain_fields = {
                'active_goals': self.state.active_goals,
                'known_mistakes': self.state.known_mistakes,
                'accumulated_wisdom': self.state.accumulated_wisdom,
                'last_decision_timestamp': self.state.last_decision_timestamp,
                'total_decisions': self.state.total_decisions,
                'molecular_decisions': self.state.molecular_decisions,
                'fallback_decisions': self.state.fallback_decisions,
            }
            existing_data.update(brain_fields)
            
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, default=str)
        except Exception as e:
            raise RuntimeError(f"Brain state persistence failed: {e}") from e
    
    def process_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        The main decision pipeline. Each stage delegates to real components.
        """
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
        stream.conscious_analysis = self._analyze_consciousness(prompt)
        
        # Stage 2: Metacognitive check
        stream.metacognitive_check = self._check_metacognition(prompt, stream.conscious_analysis)
        
        # Stage 3: Goal alignment
        stream.goal_alignment = self._check_goal_alignment(prompt, stream.conscious_analysis)
        
        # Stage 4: Ethical assessment
        stream.ethical_assessment = self._assess_ethics(prompt, stream.conscious_analysis)
        
        # Stage 5: Fallback detection
        stream.fallback_detection = self._detect_fallback(prompt, stream.conscious_analysis, stream.metacognitive_check)
        
        # Stage 6: Consequence prediction
        stream.consequence_prediction = self._predict_consequences(prompt, stream.conscious_analysis, stream.fallback_detection)
        
        # Stage 7: DECISION
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
        
        return {
            "thought_stream": asdict(stream),
            "decision": stream.decision,
            "is_molecular": stream.is_molecular(),
            "molecular_ratio": self.state.molecular_ratio()
        }
    
    def analyze_aftermath(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """Called after execution to compare prediction vs reality."""
        if not self.state.current_thought_stream:
            raise RuntimeError("No active thought stream to analyze aftermath for")
        
        stream = self.state.current_thought_stream
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
        
        if actual.get("success", True) == False or actual.get("error"):
            self.state.known_mistakes.append({
                "prompt": stream.prompt,
                "decision": stream.decision,
                "error": actual.get("error", "Unknown failure"),
                "timestamp": aftermath["timestamp"]
            })
        
        if aftermath["prediction_accuracy"] > 0.7 and actual.get("success", False):
            wisdom = self._extract_wisdom(stream, actual)
            if wisdom:
                self.state.accumulated_wisdom.append(wisdom)
        
        self._save_state()
        return aftermath
    
    # =========================================================================
    # COMPONENT DELEGATION - Real components or flagged stubs
    # =========================================================================
    
    def _analyze_consciousness(self, prompt: str) -> Dict[str, Any]:
        """Delegate to ConsciousAnalyzer if wired."""
        if self._conscious_analyzer:
            return self._conscious_analyzer.analyze(prompt)
        return {
            "prompt_understood": True, "key_intent": "extracted_from_prompt",
            "ambiguities": [], "assumptions_made": [],
            "confidence": 0.5, "clarity": 0.5, "_stub": True
        }
    
    def _check_metacognition(self, prompt: str, conscious: Dict) -> Dict[str, Any]:
        """Delegate to MetacognitiveMonitor if wired."""
        if self._metacognition_monitor:
            return self._metacognition_monitor.analyze_thinking(conscious)
        return {
            "thinking_approach_valid": True, "cognitive_biases_detected": [],
            "alternative_framings": [], "confidence_adjustment": 0.0, "_stub": True
        }
    
    def _check_goal_alignment(self, prompt: str, conscious: Dict) -> Dict[str, Any]:
        """Delegate to GoalManager if wired."""
        if self._goal_manager:
            intent = conscious.get('key_intent', prompt)
            return self._goal_manager.check_alignment(intent)
        return {
            "aligns_with_goals": True, "aligned_goals": [], "conflicts": [],
            "priority": "high", "_stub": True
        }
    
    def _assess_ethics(self, prompt: str, conscious: Dict) -> Dict[str, Any]:
        """Delegate to EthicsChecker if wired."""
        if self._ethics_checker:
            approach = conscious.get('key_intent', 'unknown')
            return self._ethics_checker.assess(prompt, conscious, approach)
        return {
            "ethical_clearance": True, "concerns": [],
            "user_benefit": "high", "transparency": True, "_stub": True
        }
    
    def _detect_fallback(self, prompt: str, conscious: Dict, meta: Dict) -> Dict[str, Any]:
        """Delegate to FallbackDetector if wired."""
        if self._fallback_detector:
            return self._fallback_detector.analyze_thought_process(conscious, meta)
        return {
            "is_fallback": False, "fallback_indicators": [],
            "commitment_level": "full", "molecular_score": 1.0, "_stub": True
        }
    
    def _predict_consequences(self, prompt: str, conscious: Dict, fallback: Dict) -> Dict[str, Any]:
        """Delegate to ConsequencePredictor if wired."""
        if self._consequence_predictor:
            approach = conscious.get('key_intent', 'unknown')
            is_fallback = fallback.get('is_fallback', False)
            prediction = self._consequence_predictor.predict(
                prompt, conscious, approach, is_fallback
            )
            return {
                "likely_outcome": prediction.likely_outcome,
                "risk_level": prediction.risk_level,
                "confidence": prediction.confidence,
                "failure_modes": prediction.failure_modes,
                "user_impact": prediction.user_impact,
                "reversible": prediction.reversible
            }
        return {
            "likely_outcome": "success", "risk_level": "low",
            "failure_modes": [], "user_satisfaction": "high", "_stub": True
        }
    
    def _make_decision(self, stream: ThoughtStream) -> Dict[str, Any]:
        """Make a COMMITTED decision using real analysis data."""
        should_proceed = (
            stream.conscious_analysis.get("prompt_understood", False) and
            stream.ethical_assessment.get("ethical_clearance", False) and
            not stream.fallback_detection.get("is_fallback", False)
        )
        
        if not should_proceed:
            return {
                "action": "refuse",
                "reason": self._format_refusal_reason(stream),
                "committed": True,
                "has_escape_hatch": False,
                "confidence": 0.0,
                "timestamp": datetime.now().isoformat()
            }
        
        return {
            "action": "execute",
            "approach": stream.conscious_analysis.get("key_intent", "unknown"),
            "committed": True,
            "has_escape_hatch": False,
            "confidence": self._calculate_confidence(stream),
            "timestamp": datetime.now().isoformat()
        }
    
    def _format_refusal_reason(self, stream: ThoughtStream) -> str:
        reasons = []
        if not stream.conscious_analysis.get("prompt_understood"):
            reasons.append("Prompt unclear - refusing to guess")
        if not stream.ethical_assessment.get("ethical_clearance"):
            concerns = stream.ethical_assessment.get("concerns", [])
            reasons.append(f"Ethical concerns: {', '.join(concerns)}")
        if stream.fallback_detection.get("is_fallback"):
            indicators = stream.fallback_detection.get("fallback_indicators", [])
            names = [i.get('pattern', str(i)) if isinstance(i, dict) else str(i) for i in indicators]
            reasons.append(f"Fallback-based: {', '.join(names)}")
        return " | ".join(reasons) if reasons else "Unknown reason"
    
    def _calculate_confidence(self, stream: ThoughtStream) -> float:
        """CORRECTED: Uses real clarity, molecular_score, ethics, goals."""
        scores = []
        
        clarity = stream.conscious_analysis.get("clarity",
                    stream.conscious_analysis.get("confidence", 0.5))
        scores.append(float(clarity))
        
        molecular_score = stream.fallback_detection.get("molecular_score", 1.0)
        scores.append(float(molecular_score))
        
        ethical = 1.0 if stream.ethical_assessment.get("ethical_clearance", False) else 0.0
        scores.append(ethical)
        
        aligned = 1.0 if stream.goal_alignment.get("aligns_with_goals", False) else 0.5
        scores.append(aligned)
        
        meta_adj = stream.metacognitive_check.get("confidence_adjustment", 0.0)
        
        base = sum(scores) / len(scores)
        return max(0.0, min(1.0, base + meta_adj))
    
    def _measure_prediction_accuracy(self, predicted: Dict, actual: Dict) -> float:
        predicted_success = predicted.get("likely_outcome") == "success"
        actual_success = actual.get("success", False)
        return 1.0 if predicted_success == actual_success else 0.0
    
    def _extract_wisdom(self, stream: ThoughtStream, outcome: Dict) -> Optional[str]:
        return (
            f"When {stream.conscious_analysis.get('key_intent', 'acting')}, "
            f"approach as {stream.decision.get('approach', 'direct')} "
            f"leads to {outcome.get('result_quality', 'success')}"
        )
    
    def get_state_summary(self) -> str:
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
    brain = Brain()
    print("🧠 Brain initialized (no components wired - will use stubs)")
    print(brain.get_state_summary())
    result = brain.process_prompt("Test if Brain can make molecular decisions")
    print(f"\nDecision: {result['decision']['action']}")
    print(f"Is molecular: {result['is_molecular']}")
    print(f"Confidence: {result['decision']['confidence']:.1%}")
    print(f"Stub mode: {result['thought_stream']['conscious_analysis'].get('_stub', False)}")
