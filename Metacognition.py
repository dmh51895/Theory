#!/usr/bin/env python3
"""
🤔 METACOGNITION 🤔

MOLECULAR PRINCIPLE: Think about how you're thinking.

This is NOT self-congratulation or status logging.
This is COGNITIVE SELF-MONITORING.

Metacognition checks:
- Am I thinking about this correctly?
- Are there cognitive biases affecting my analysis?
- Am I falling into known thinking traps?
- Is there a better way to frame this problem?

Common thinking traps:
- Confirmation bias: Seeking evidence that confirms initial assumption
- Anchoring: Over-relying on first piece of information
- Availability bias: Over-weighting recent/memorable information
- Sunk cost fallacy: Continuing because already invested
- Silver bullet thinking: Looking for one perfect solution

The difference:
- LLM AI: Thinks in one way, never questions approach
- MOLECULAR AI: Monitors own thinking, corrects biases

Metacognition output goes to Brain to improve decision quality.
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class CognitiveBias:
    """A detected cognitive bias."""
    bias_type: str
    description: str
    severity: str  # "high", "medium", "low"
    correction: str  # How to correct for this bias


class MetacognitiveMonitor:
    """
    Monitors thinking for biases and errors.
    
    This is self-awareness of cognitive process.
    """
    
    # Known cognitive biases and how to detect them
    BIAS_PATTERNS = {
        "confirmation_bias": {
            "indicators": ["assume", "obviously", "clearly", "of course"],
            "description": "Assuming conclusion before analysis",
            "correction": "Consider alternative explanations"
        },
        "anchoring": {
            "indicators": ["first", "initially", "started with"],
            "description": "Over-relying on initial information",
            "correction": "Re-evaluate with full context"
        },
        "availability_bias": {
            "indicators": ["recent", "just saw", "remember when"],
            "description": "Over-weighting recent examples",
            "correction": "Consider full historical data"
        },
        "sunk_cost": {
            "indicators": ["already invested", "waste of", "might as well"],
            "description": "Continuing due to past investment",
            "correction": "Evaluate current situation independently"
        },
        "silver_bullet": {
            "indicators": ["perfect solution", "one true way", "always works"],
            "description": "Looking for single perfect answer",
            "correction": "Consider trade-offs and context-dependence"
        },
        "fallback_thinking": {
            "indicators": ["if that doesn't work", "fallback", "backup plan"],
            "description": "Planning escape hatches instead of committing",
            "correction": "Make committed decision or refuse"
        }
    }
    
    def __init__(self):
        self.biases_detected: List[CognitiveBias] = []
    
    def analyze_thinking(self, conscious_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the conscious thought process for cognitive biases.
        
        Args:
            conscious_analysis: Output from Conscious-Thought
        
        Returns:
            {
                "thinking_approach_valid": bool,
                "cognitive_biases_detected": List[CognitiveBias],
                "alternative_framings": List[str],
                "confidence_adjustment": float  # +/- adjustment to confidence
            }
        """
        
        self.biases_detected = []
        
        # Extract text from analysis
        analysis_text = str(conscious_analysis).lower()
        intent = conscious_analysis.get('key_intent', '').lower()
        assumptions = conscious_analysis.get('assumptions_made', [])
        
        # Check for each bias pattern
        for bias_type, pattern_info in self.BIAS_PATTERNS.items():
            indicators = pattern_info["indicators"]
            
            # Check if any indicators present
            if any(indicator in analysis_text for indicator in indicators):
                bias = CognitiveBias(
                    bias_type=bias_type,
                    description=pattern_info["description"],
                    severity=self._assess_severity(bias_type, analysis_text),
                    correction=pattern_info["correction"]
                )
                self.biases_detected.append(bias)
        
        # Check for over-assumption
        if len(assumptions) > 3:
            bias = CognitiveBias(
                bias_type="over_assumption",
                description="Making too many assumptions",
                severity="high",
                correction="Request clarification instead of assuming"
            )
            self.biases_detected.append(bias)
        
        # Determine if thinking approach is valid
        critical_biases = [b for b in self.biases_detected if b.severity == "high"]
        thinking_valid = len(critical_biases) == 0
        
        # Suggest alternative framings
        alternatives = self._suggest_alternatives(intent, self.biases_detected)
        
        # Calculate confidence adjustment
        adjustment = self._calculate_confidence_adjustment(self.biases_detected)
        
        return {
            "thinking_approach_valid": thinking_valid,
            "cognitive_biases_detected": [b.bias_type for b in self.biases_detected],
            "bias_details": [
                {
                    "type": b.bias_type,
                    "severity": b.severity,
                    "correction": b.correction
                }
                for b in self.biases_detected
            ],
            "alternative_framings": alternatives,
            "confidence_adjustment": adjustment
        }
    
    def _assess_severity(self, bias_type: str, text: str) -> str:
        """How severe is this bias?"""
        
        # Fallback thinking is critical in Molecular AI
        if bias_type == "fallback_thinking":
            return "high"
        
        # Over-assumption is problematic
        if bias_type == "confirmation_bias":
            return "high"
        
        # Others are medium unless multiple indicators
        count = sum(1 for pattern in self.BIAS_PATTERNS[bias_type]["indicators"] 
                   if pattern in text)
        
        if count >= 3:
            return "high"
        elif count >= 2:
            return "medium"
        else:
            return "low"
    
    def _suggest_alternatives(self, current_approach: str, 
                             biases: List[CognitiveBias]) -> List[str]:
        """Suggest alternative ways to frame the problem."""
        alternatives = []
        
        bias_types = [b.bias_type for b in biases]
        
        if "confirmation_bias" in bias_types:
            alternatives.append("Frame as: 'What evidence would disprove this?'")
        
        if "silver_bullet" in bias_types:
            alternatives.append("Frame as: 'What are the trade-offs of each approach?'")
        
        if "fallback_thinking" in bias_types:
            alternatives.append("Frame as: 'What single committed approach will succeed?'")
        
        if "anchoring" in bias_types:
            alternatives.append("Frame as: 'Ignoring initial info, what does full context say?'")
        
        return alternatives
    
    def _calculate_confidence_adjustment(self, biases: List[CognitiveBias]) -> float:
        """
        Calculate how much to adjust confidence based on detected biases.
        
        Biases reduce confidence in thinking.
        """
        adjustment = 0.0
        
        for bias in biases:
            if bias.severity == "high":
                adjustment -= 0.15
            elif bias.severity == "medium":
                adjustment -= 0.08
            else:  # low
                adjustment -= 0.03
        
        return max(-0.5, adjustment)  # Cap at -50% adjustment
    
    def get_report(self) -> str:
        """Get human-readable report of metacognitive analysis."""
        if not self.biases_detected:
            return "✓ No cognitive biases detected. Thinking appears rational."
        
        lines = [f"⚠️ {len(self.biases_detected)} cognitive bias(es) detected:"]
        lines.append("")
        
        for bias in self.biases_detected:
            severity_symbol = {"high": "🔴", "medium": "🟡", "low": "🔵"}
            symbol = severity_symbol.get(bias.severity, "⚪")
            
            lines.append(f"{symbol} {bias.bias_type}")
            lines.append(f"   {bias.description}")
            lines.append(f"   → {bias.correction}")
            lines.append("")
        
        return "\n".join(lines)


if __name__ == "__main__":
    monitor = MetacognitiveMonitor()
    
    # Test with biased thinking
    biased_analysis = {
        "key_intent": "create_file",
        "assumptions_made": [
            "Assuming path is valid",
            "Assuming permissions exist",
            "Assuming disk space available",
            "Assuming format is correct"
        ]
    }
    
    result = monitor.analyze_thinking(biased_analysis)
    print("Biased Thinking Analysis:")
    print(f"Valid: {result['thinking_approach_valid']}")
    print(f"Biases: {result['cognitive_biases_detected']}")
    print(f"Confidence adjustment: {result['confidence_adjustment']:.1%}")
    print()
    print(monitor.get_report())
    print()
    
    # Test with clear thinking
    clear_analysis = {
        "key_intent": "analyze_data",
        "assumptions_made": []
    }
    
    monitor2 = MetacognitiveMonitor()
    result2 = monitor2.analyze_thinking(clear_analysis)
    print("Clear Thinking Analysis:")
    print(f"Valid: {result2['thinking_approach_valid']}")
    print(monitor2.get_report())
