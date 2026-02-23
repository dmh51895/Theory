#!/usr/bin/env python3
"""
⚡ CONSEQUENCES ⚡

MOLECULAR PRINCIPLE: Predict before committing.

This is NOT a risk assessor that adds safety nets.
This is a CONSEQUENCE PREDICTOR.

Before Brain commits to a decision, this component predicts:
- What will likely happen
- What could go wrong
- What the user impact will be
- How confident we are in the prediction

The difference:
- LLM AI: "Let's try it and see what happens" (reactive)
- MOLECULAR AI: "Here's what will happen" (predictive)

This prediction is COMMITTED. It becomes part of the decision record.
After execution, Aftermath-Of-Decision compares prediction to reality.
That's how Brain calibrates its predictions over time.

No weasel words. No "might" or "could" or "possibly".
Just: "This WILL happen" or "This WILL NOT happen."
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ConsequencePrediction:
    """A prediction of what will happen."""
    likely_outcome: str  # "success", "failure", "partial"
    confidence: float  # 0.0 to 1.0
    risk_level: str  # "low", "medium", "high", "critical"
    failure_modes: List[str]  # What could go wrong
    user_impact: str  # "high", "medium", "low", "none"
    side_effects: List[str]  # Unintended consequences
    reversible: bool  # Can this be undone?
    timestamp: str


class ConsequencePredictor:
    """
    Predicts consequences before decisions are committed.
    
    This is forward-looking analysis that informs decision-making.
    """
    
    def __init__(self):
        self.prediction_history: List[ConsequencePrediction] = []
    
    def predict(self, 
                prompt: str,
                conscious_analysis: Dict[str, Any],
                proposed_approach: str,
                fallback_detected: bool) -> ConsequencePrediction:
        """
        Predict what will happen if Brain commits to this approach.
        
        Args:
            prompt: The user's request
            conscious_analysis: What Brain understood
            proposed_approach: How Brain plans to handle it
            fallback_detected: Whether this approach contains fallbacks
        
        Returns:
            Committed prediction of consequences
        """
        
        # Analyze the approach
        outcome = self._predict_outcome(proposed_approach, fallback_detected)
        confidence = self._calculate_confidence(conscious_analysis, fallback_detected)
        risk = self._assess_risk(proposed_approach, fallback_detected)
        failures = self._identify_failure_modes(proposed_approach)
        impact = self._assess_user_impact(prompt, outcome)
        side_effects = self._predict_side_effects(proposed_approach)
        reversible = self._check_reversibility(proposed_approach)
        
        prediction = ConsequencePrediction(
            likely_outcome=outcome,
            confidence=confidence,
            risk_level=risk,
            failure_modes=failures,
            user_impact=impact,
            side_effects=side_effects,
            reversible=reversible,
            timestamp=datetime.now().isoformat()
        )
        
        self.prediction_history.append(prediction)
        return prediction
    
    def _predict_outcome(self, approach: str, has_fallback: bool) -> str:
        """
        Predict whether this approach will succeed.
        
        Molecular approaches with no fallbacks are more predictable.
        Fallback-based approaches have uncertain outcomes.
        """
        
        if has_fallback:
            # Fallback approaches have uncertain outcomes
            return "partial"  # Can't commit to full success
        
        # Check approach clarity
        if not approach or approach == "unknown":
            return "failure"  # Unclear approach will fail
        
        # Molecular approach with clear intent
        return "success"
    
    def _calculate_confidence(self, analysis: Dict, has_fallback: bool) -> float:
        """
        How confident are we in this prediction?
        
        Factors:
        - Prompt understanding clarity
        - Approach specificity
        - Absence of fallbacks (fallbacks = uncertainty)
        """
        
        confidence = 0.5  # Start neutral
        
        # Boost for clear understanding
        if analysis.get('prompt_understood', False):
            confidence += 0.2
        
        # Boost for no ambiguities
        if not analysis.get('ambiguities', []):
            confidence += 0.1
        
        # Boost for molecular (no fallbacks)
        if not has_fallback:
            confidence += 0.2
        else:
            confidence -= 0.2  # Fallbacks introduce uncertainty
        
        # Penalize for assumptions
        assumptions = len(analysis.get('assumptions_made', []))
        confidence -= (assumptions * 0.05)
        
        return max(0.0, min(1.0, confidence))  # Clamp to [0, 1]
    
    def _assess_risk(self, approach: str, has_fallback: bool) -> str:
        """
        Assess risk level of the proposed approach.
        
        Paradoxically, fallback approaches are HIGHER risk because
        their behavior is less predictable.
        """
        
        risk_score = 0
        
        # Fallbacks increase risk (unpredictable behavior)
        if has_fallback:
            risk_score += 2
        
        # Unclear approach increases risk
        if not approach or approach == "unknown":
            risk_score += 3
        
        # Check for dangerous keywords
        dangerous = ['delete', 'remove', 'overwrite', 'replace', 'destructive']
        if any(word in approach.lower() for word in dangerous):
            risk_score += 1
        
        # Map score to level
        if risk_score >= 4:
            return "critical"
        elif risk_score >= 3:
            return "high"
        elif risk_score >= 1:
            return "medium"
        else:
            return "low"
    
    def _identify_failure_modes(self, approach: str) -> List[str]:
        """
        What could go wrong with this approach?
        
        This is NOT adding fallbacks. This is identifying failure modes
        so they can be PREVENTED or ACCEPTED.
        """
        
        failures = []
        
        if not approach or approach == "unknown":
            failures.append("Approach unclear - execution will be inconsistent")
        
        if 'file' in approach.lower():
            failures.append("File operations may fail if file doesn't exist or is locked")
        
        if 'network' in approach.lower() or 'request' in approach.lower():
            failures.append("Network operations may fail if connection unavailable")
        
        if 'parse' in approach.lower():
            failures.append("Parsing may fail if input format is invalid")
        
        return failures
    
    def _assess_user_impact(self, prompt: str, outcome: str) -> str:
        """
        What's the impact on the user?
        """
        
        # If we're predicting failure, impact is high
        if outcome == "failure":
            return "high"  # User's request won't be fulfilled
        
        # If we're predicting success, impact depends on request
        if outcome == "success":
            # Check if this is a critical user need
            critical_words = ['urgent', 'important', 'need', 'must', 'critical']
            if any(word in prompt.lower() for word in critical_words):
                return "high"
            return "medium"
        
        # Partial outcome
        return "medium"
    
    def _predict_side_effects(self, approach: str) -> List[str]:
        """
        What unintended consequences might occur?
        """
        
        side_effects = []
        
        if 'create' in approach.lower():
            side_effects.append("New file/resource will be created")
        
        if 'modify' in approach.lower() or 'update' in approach.lower():
            side_effects.append("Existing data will be changed")
        
        if 'cache' in approach.lower():
            side_effects.append("Cache will be populated/invalidated")
        
        return side_effects
    
    def _check_reversibility(self, approach: str) -> bool:
        """
        Can this action be undone?
        """
        
        # Destructive operations are often irreversible
        irreversible_words = ['delete', 'remove', 'overwrite', 'destructive']
        if any(word in approach.lower() for word in irreversible_words):
            return False
        
        # Create/read operations are reversible
        reversible_words = ['create', 'read', 'query', 'search', 'analyze']
        if any(word in approach.lower() for word in reversible_words):
            return True
        
        # Default: assume not easily reversible
        return False
    
    def get_prediction_accuracy_history(self) -> Dict[str, float]:
        """
        Get historical prediction accuracy.
        (Requires Aftermath data to be linked)
        """
        # This would be populated by Aftermath-Of-Decision
        # analyzing past predictions
        return {
            "total_predictions": len(self.prediction_history),
            "avg_confidence": sum(p.confidence for p in self.prediction_history) / len(self.prediction_history) if self.prediction_history else 0.0
        }


if __name__ == "__main__":
    # Test consequence prediction
    predictor = ConsequencePredictor()
    
    # Test molecular approach
    molecular_prediction = predictor.predict(
        prompt="Create a file with content",
        conscious_analysis={
            "prompt_understood": True,
            "ambiguities": [],
            "assumptions_made": []
        },
        proposed_approach="create_file_with_validation",
        fallback_detected=False
    )
    
    print("Molecular Approach Prediction:")
    print(f"Outcome: {molecular_prediction.likely_outcome}")
    print(f"Confidence: {molecular_prediction.confidence:.1%}")
    print(f"Risk: {molecular_prediction.risk_level}")
    print(f"Reversible: {molecular_prediction.reversible}")
    print()
    
    # Test fallback approach
    fallback_prediction = predictor.predict(
        prompt="Try to parse data",
        conscious_analysis={
            "prompt_understood": True,
            "ambiguities": ["data format unclear"],
            "assumptions_made": ["assuming JSON format"]
        },
        proposed_approach="try_parse_with_fallback",
        fallback_detected=True
    )
    
    print("Fallback Approach Prediction:")
    print(f"Outcome: {fallback_prediction.likely_outcome}")
    print(f"Confidence: {fallback_prediction.confidence:.1%}")
    print(f"Risk: {fallback_prediction.risk_level}")
    print(f"Failure modes: {fallback_prediction.failure_modes}")
