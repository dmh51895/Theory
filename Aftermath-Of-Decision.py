#!/usr/bin/env python3
"""
🔍 AFTERMATH-OF-DECISION 🔍

MOLECULAR PRINCIPLE: Accountability through measurement.

This is NOT a post-mortem that hides failures.
This is TRUTH MEASUREMENT.

After Brain makes a COMMITTED decision and Motor-Control executes it,
this component measures:
- What was predicted vs what actually happened
- Whether the molecular approach succeeded
- What was learned from the outcome
- Whether to update wisdom or record as mistake

The difference:
- LLM AI: Execution happens, vague "success" returned, move on
- MOLECULAR AI: Execution measured, predictions validated, learning extracted

This is how Molecular AI improves - by seeing the consequences of
COMMITTED decisions, not fuzzy probabilistic outcomes.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class AftermathAnalysis:
    """Analysis of what happened after a decision."""
    decision_timestamp: str
    execution_timestamp: str
    decision_summary: Dict[str, Any]
    predicted_outcome: Dict[str, Any]
    actual_outcome: Dict[str, Any]
    prediction_accuracy: float
    was_molecular: bool
    outcome_quality: str  # "success", "failure", "partial"
    lessons_learned: List[str]
    wisdom_extracted: Optional[str]
    should_record_as_mistake: bool
    

class AftermathAnalyzer:
    """
    Analyzes the aftermath of executed decisions.
    
    This creates the feedback loop that allows Brain to improve.
    """
    
    def __init__(self):
        self.analysis_history: List[AftermathAnalysis] = []
    
    def analyze(self, 
                decision_data: Dict[str, Any],
                execution_result: Dict[str, Any]) -> AftermathAnalysis:
        """
        Compare what was predicted with what actually happened.
        
        Args:
            decision_data: The original decision from Brain
            execution_result: What Motor-Control reported after execution
        
        Returns:
            Complete aftermath analysis
        """
        
        predicted = decision_data.get('consequence_prediction', {})
        actual = execution_result
        
        # Measure prediction accuracy
        accuracy = self._calculate_accuracy(predicted, actual)
        
        # Determine outcome quality
        quality = self._assess_quality(actual)
        
        # Extract lessons
        lessons = self._extract_lessons(decision_data, actual, accuracy)
        
        # Extract wisdom if successful molecular decision
        wisdom = None
        was_molecular = decision_data.get('is_molecular', False)
        if was_molecular and quality == "success" and accuracy > 0.7:
            wisdom = self._extract_wisdom(decision_data, actual)
        
        # Determine if this should be recorded as a mistake
        is_mistake = (quality == "failure" or 
                     (quality == "partial" and accuracy < 0.5))
        
        analysis = AftermathAnalysis(
            decision_timestamp=decision_data.get('timestamp', ''),
            execution_timestamp=actual.get('timestamp', datetime.now().isoformat()),
            decision_summary=decision_data.get('decision', {}),
            predicted_outcome=predicted,
            actual_outcome=actual,
            prediction_accuracy=accuracy,
            was_molecular=was_molecular,
            outcome_quality=quality,
            lessons_learned=lessons,
            wisdom_extracted=wisdom,
            should_record_as_mistake=is_mistake
        )
        
        self.analysis_history.append(analysis)
        return analysis
    
    def _calculate_accuracy(self, predicted: Dict, actual: Dict) -> float:
        """
        Calculate how accurate the prediction was.
        
        Compares:
        - Expected success vs actual success
        - Expected risk vs actual problems
        - Expected outcome vs actual result
        """
        
        scores = []
        
        # Success prediction
        pred_success = predicted.get('likely_outcome') == 'success'
        actual_success = actual.get('success', False)
        scores.append(1.0 if pred_success == actual_success else 0.0)
        
        # Risk assessment
        pred_risk = predicted.get('risk_level', 'unknown')
        had_problems = bool(actual.get('error') or actual.get('warnings'))
        
        risk_accurate = (
            (pred_risk in ['high', 'medium'] and had_problems) or
            (pred_risk == 'low' and not had_problems)
        )
        scores.append(1.0 if risk_accurate else 0.0)
        
        # Outcome quality
        if 'quality' in actual and 'likely_outcome' in predicted:
            outcomes_match = predicted['likely_outcome'] in str(actual['quality'])
            scores.append(1.0 if outcomes_match else 0.5)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _assess_quality(self, actual: Dict) -> str:
        """
        Determine the quality of the actual outcome.
        
        Returns: "success", "failure", or "partial"
        """
        
        if actual.get('error') or actual.get('failed', False):
            return "failure"
        
        if actual.get('success', False) and not actual.get('warnings'):
            return "success"
        
        return "partial"
    
    def _extract_lessons(self, decision: Dict, actual: Dict, 
                        accuracy: float) -> List[str]:
        """
        Extract lessons from the decision-execution-outcome cycle.
        """
        lessons = []
        
        # Low accuracy lesson
        if accuracy < 0.5:
            lessons.append(
                f"Prediction accuracy low ({accuracy:.1%}). "
                f"Review: {decision.get('decision', {}).get('approach', 'unknown approach')}"
            )
        
        # Failure lesson
        if actual.get('error'):
            lessons.append(
                f"Execution failed: {actual['error']}. "
                f"Decision may have been wrong or execution flawed."
            )
        
        # Fallback lesson
        if not decision.get('is_molecular', True):
            lessons.append(
                "Decision contained fallback patterns. "
                "This may have caused unpredictable behavior."
            )
        
        # Success lesson
        if actual.get('success') and accuracy > 0.8:
            lessons.append(
                f"High accuracy molecular decision succeeded. "
                f"Approach '{decision.get('decision', {}).get('approach')}' validated."
            )
        
        return lessons
    
    def _extract_wisdom(self, decision: Dict, actual: Dict) -> str:
        """
        Extract wisdom from successful molecular decisions.
        
        Wisdom format: "When X, do Y, results in Z"
        """
        
        prompt = decision.get('prompt', 'unknown prompt')
        approach = decision.get('decision', {}).get('approach', 'unknown')
        result = actual.get('result', 'success')
        
        # Extract key pattern
        prompt_pattern = self._extract_pattern(prompt)
        
        return f"When {prompt_pattern}, approach as '{approach}' → {result}"
    
    def _extract_pattern(self, prompt: str) -> str:
        """
        Extract the pattern from a prompt for wisdom generation.
        """
        # Simple pattern extraction - could be more sophisticated
        if len(prompt) > 50:
            return prompt[:47] + "..."
        return prompt
    
    def get_summary(self) -> str:
        """
        Get summary of aftermath analyses.
        """
        if not self.analysis_history:
            return "No aftermath analyses yet."
        
        total = len(self.analysis_history)
        successes = sum(1 for a in self.analysis_history if a.outcome_quality == "success")
        failures = sum(1 for a in self.analysis_history if a.outcome_quality == "failure")
        molecular_count = sum(1 for a in self.analysis_history if a.was_molecular)
        
        avg_accuracy = sum(a.prediction_accuracy for a in self.analysis_history) / total
        
        return (
            f"Aftermath Analysis Summary:\n"
            f"  Total decisions analyzed: {total}\n"
            f"  Successes: {successes} ({successes/total:.1%})\n"
            f"  Failures: {failures} ({failures/total:.1%})\n"
            f"  Molecular decisions: {molecular_count} ({molecular_count/total:.1%})\n"
            f"  Average prediction accuracy: {avg_accuracy:.1%}"
        )


if __name__ == "__main__":
    # Test aftermath analysis
    analyzer = AftermathAnalyzer()
    
    # Simulate a decision and execution
    decision = {
        "prompt": "Test molecular decision",
        "decision": {"approach": "direct_execution"},
        "consequence_prediction": {
            "likely_outcome": "success",
            "risk_level": "low"
        },
        "is_molecular": True,
        "timestamp": datetime.now().isoformat()
    }
    
    execution = {
        "success": True,
        "result": "completed",
        "timestamp": datetime.now().isoformat()
    }
    
    analysis = analyzer.analyze(decision, execution)
    
    print("Aftermath Analysis:")
    print(f"Quality: {analysis.outcome_quality}")
    print(f"Accuracy: {analysis.prediction_accuracy:.1%}")
    print(f"Lessons: {analysis.lessons_learned}")
    if analysis.wisdom_extracted:
        print(f"Wisdom: {analysis.wisdom_extracted}")
