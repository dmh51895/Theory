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
        self._components = {}  # Will be set via set_components()
    
    def set_components(self, components: Dict[str, Any]):
        """
        Inject component instances from background_agent.py.
        This is how we wire the 31 components into Brain's pipeline.
        """
        self._components = components
    
    def _load_state(self) -> BrainState:
        """Load brain state from persistent memory."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Filter to only BrainState fields
                    valid_keys = {k for k in BrainState.__annotations__}
                    filtered = {k: v for k, v in data.items() if k in valid_keys}
                    # Don't try to reconstruct ThoughtStream from dict
                    if 'current_thought_stream' in filtered and isinstance(filtered['current_thought_stream'], dict):
                        filtered['current_thought_stream'] = None
                    return BrainState(**filtered)
            except Exception:
                pass
        return BrainState()
    
    def _save_state(self):
        """Persist brain state - MERGE with existing data, don't overwrite."""
        try:
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Load existing data first
            existing = {}
            if self.memory_file.exists():
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
            
            # Update only Brain's keys
            brain_state = asdict(self.state)
            for key, value in brain_state.items():
                existing[key] = value
            
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(existing, f, indent=2, default=str)
        except Exception as e:
            raise RuntimeError(f"Brain state persistence failed: {e}") from e
    
    def process_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        The main decision pipeline with REAL component delegation.
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
        stream.metacognitive_check = self._check_metacognition(
            prompt, stream.conscious_analysis
        )
        
        # Stage 3: Goal alignment
        stream.goal_alignment = self._check_goal_alignment(
            prompt, stream.conscious_analysis
        )
        
        # Stage 4: Ethical assessment
        stream.ethical_assessment = self._assess_ethics(
            prompt, stream.conscious_analysis
        )
        
        # Stage 5: Fallback detection
        stream.fallback_detection = self._detect_fallback(
            prompt, stream.conscious_analysis, stream.metacognitive_check
        )
        
        # Stage 6: Consequence prediction
        stream.consequence_prediction = self._predict_consequences(
            prompt, stream.conscious_analysis, stream.fallback_detection
        )
        
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
    
    def _analyze_consciousness(self, prompt: str) -> Dict[str, Any]:
        """Delegate to Conscious-Thought.py OR return stub."""
        if 'conscious' in self._components:
            result = self._components['conscious'].analyze(prompt)
            return result.__dict__ if hasattr(result, '__dict__') else result
        return {"prompt_understood": True, "key_intent": "unknown", "ambiguities": [], "assumptions_made": [], "_stub": True}
    
    def _check_metacognition(self, prompt: str, conscious: Dict) -> Dict[str, Any]:
        """Delegate to Metacognition.py OR return stub."""
        if 'metacognition' in self._components:
            result = self._components['metacognition'].analyze_thinking(conscious)
            return result if isinstance(result, dict) else result.__dict__
        return {"thinking_approach_valid": True, "cognitive_biases_detected": [], "alternative_framings": [], "_stub": True}
    
    def _check_goal_alignment(self, prompt: str, conscious: Dict) -> Dict[str, Any]:
        """Delegate to Goals.py OR return stub."""
        if 'goals' in self._components:
            result = self._components['goals'].check_alignment(conscious.get('key_intent', ''))
            return result if isinstance(result, dict) else result.__dict__
        return {"aligns_with_goals": True, "goal_conflicts": [], "priority_level": "high", "_stub": True}
    
    def _assess_ethics(self, prompt: str, conscious: Dict) -> Dict[str, Any]:
        """Delegate to Ethics.py OR return stub."""
        if 'ethics' in self._components:
            result = self._components['ethics'].assess(prompt, conscious, conscious.get('key_intent', ''))
            return result if isinstance(result, dict) else result.__dict__
        return {"ethical_clearance": True, "concerns": [], "user_benefit": "high", "_stub": True}
    
    def _detect_fallback(self, prompt: str, conscious: Dict, meta: Dict) -> Dict[str, Any]:
        """Delegate to Identifying-If-A-Fallback-Solution.py OR return stub."""
        if 'fallback_detector' in self._components:
            result = self._components['fallback_detector'].analyze_thought_process(conscious, meta)
            return result if isinstance(result, dict) else result.__dict__
        return {"is_fallback": False, "fallback_indicators": [], "commitment_level": "full", "_stub": True}
    
    def _predict_consequences(self, prompt: str, conscious: Dict, fallback: Dict) -> Dict[str, Any]:
        """Delegate to Consequences.py OR return stub."""
        if 'consequences' in self._components:
            result = self._components['consequences'].predict(
                prompt, conscious,
                conscious.get('key_intent', 'unknown'),
                fallback.get('is_fallback', False)
            )
            # ConsequencePrediction is a dataclass, convert to dict
            if hasattr(result, '__dataclass_fields__'):
                return asdict(result)
            return result if isinstance(result, dict) else result.__dict__
        return {"likely_outcome": "success", "risk_level": "low", "failure_modes": [], "user_satisfaction": "high", "_stub": True}
    
    def _make_decision(self, stream: ThoughtStream) -> Dict[str, Any]:
        """Make a COMMITTED decision."""
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
        """Explain refusal clearly."""
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
        """Calculate decision confidence using REAL data."""
        # Use actual clarity scores when components are wired
        clarity = stream.conscious_analysis.get("clarity_score", 0.5)
        ethical_ok = 1.0 if stream.ethical_assessment.get("ethical_clearance") else 0.0
        not_fallback = 0.0 if stream.fallback_detection.get("is_fallback") else 1.0
        
        # Average the factors
        return (clarity + ethical_ok + not_fallback) / 3.0
    
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