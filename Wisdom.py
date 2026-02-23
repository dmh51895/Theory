"""
Wisdom.py

MOLECULAR PRINCIPLE: Wisdom is EXTRACTED from experience, not synthesized from vibes.

LLM AI generates "wise-sounding" text (intellectual karaoke of wisdom).
MOLECULAR AI extracts lessons from actual decisions and their actual outcomes.

Wisdom = Pattern that predicts success/failure.

Requirements:
- Based on real decisions we made
- Based on real outcomes we observed
- Based on measurable correlation
- Falsifiable (can be proven wrong)

NOT "Be thorough" (vague).
YES "When clarity < 0.7, asking for clarification produces 95% better outcomes than guessing" (measurable).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import json


@dataclass
class WisdomItem:
    """A single piece of extracted wisdom."""
    pattern: str  # The observed pattern
    context: str  # When does this pattern apply
    evidence_count: int  # How many times observed
    success_rate: float  # 0.0-1.0, how often following this succeeds
    extracted_from: List[str]  # Decision IDs that contributed
    first_observed: str  # ISO datetime
    last_validated: str  # ISO datetime
    counterexamples: int = 0  # How many times pattern failed
    
    def confidence(self) -> float:
        """Calculate confidence in this wisdom."""
        if self.evidence_count + self.counterexamples == 0:
            return 0.0
        
        # Confidence increases with evidence, decreases with counterexamples
        return (self.success_rate * self.evidence_count) / (self.evidence_count + self.counterexamples)


@dataclass
class WisdomCandidate:
    """A potential pattern being evaluated for wisdom status."""
    pattern: str
    context: str
    supporting_decisions: List[str]
    success_count: int
    failure_count: int
    
    def qualifies_as_wisdom(self, min_evidence: int = 3, min_success_rate: float = 0.75) -> bool:
        """Check if this pattern qualifies as wisdom."""
        total = self.success_count + self.failure_count
        if total < min_evidence:
            return False
        
        success_rate = self.success_count / total
        return success_rate >= min_success_rate


class WisdomExtractor:
    """
    Extracts wisdom from actual decision outcomes.
    
    Key principle: Wisdom must be EARNED through experience, not synthesized from vibes.
    """
    
    def __init__(self, memory_system):
        """Initialize with access to Memory system."""
        self.memory = memory_system
        self.wisdom_items: List[WisdomItem] = []
        self.candidates: List[WisdomCandidate] = []
    
    def extract_from_successful_decision(self, decision_data: Dict, outcome_data: Dict):
        """
        Extract potential wisdom from a successful decision.
        
        Looks for patterns that can be generalized.
        """
        decision_id = decision_data.get('id', 'unknown')
        
        # Pattern 1: High clarity → High success
        if 'conscious_analysis' in decision_data:
            clarity = decision_data['conscious_analysis'].get('clarity', 0.0)
            if clarity > 0.8:
                self._record_pattern(
                    "High clarity (>0.8) correlates with successful outcomes",
                    "When prompt analysis shows high clarity",
                    decision_id,
                    success=True
                )
        
        # Pattern 2: Low fallback score → Better outcomes
        if 'fallback_detection' in decision_data:
            fallback_score = decision_data['fallback_detection'].get('molecular_score', 1.0)
            if fallback_score > 0.9:  # Highly molecular
                self._record_pattern(
                    "Molecular decisions (score >0.9) have higher success rates",
                    "When fallback detection shows molecular thinking",
                    decision_id,
                    success=True
                )
        
        # Pattern 3: Accurate predictions → Better decisions
        if 'consequences' in decision_data and 'aftermath' in outcome_data:
            predicted = decision_data['consequences']
            actual = outcome_data['aftermath']
            
            # Check if prediction was accurate
            if self._predictions_matched(predicted, actual):
                self._record_pattern(
                    "Accurate consequence prediction correlates with successful execution",
                    "When consequence predictions match actual outcomes",
                    decision_id,
                    success=True
                )
        
        # Pattern 4: Goal alignment → Success
        if 'goal_alignment' in decision_data:
            aligned = decision_data['goal_alignment'].get('aligned_with_goals', False)
            if aligned:
                self._record_pattern(
                    "Goal-aligned decisions succeed more often",
                    "When decision explicitly serves a tracked goal",
                    decision_id,
                    success=True
                )
        
        # Pattern 5: Ethics clearance → User satisfaction
        if 'ethics' in decision_data:
            cleared = decision_data['ethics'].get('ethical_clearance', False)
            if cleared:
                self._record_pattern(
                    "Ethically cleared decisions have better user outcomes",
                    "When ethics check passes all criteria",
                    decision_id,
                    success=True
                )
    
    def extract_from_failed_decision(self, decision_data: Dict, outcome_data: Dict):
        """
        Extract wisdom from failures.
        
        Failures are GOLD for learning.
        """
        decision_id = decision_data.get('id', 'unknown')
        
        # Anti-pattern 1: Low clarity → Failure
        if 'conscious_analysis' in decision_data:
            clarity = decision_data['conscious_analysis'].get('clarity', 1.0)
            if clarity < 0.7:
                self._record_pattern(
                    "Low clarity (<0.7) often leads to failure",
                    "When prompt clarity is below threshold",
                    decision_id,
                    success=False
                )
        
        # Anti-pattern 2: Fallback thinking → Failure
        if 'fallback_detection' in decision_data:
            is_fallback = decision_data['fallback_detection'].get('is_fallback_thinking', False)
            if is_fallback:
                self._record_pattern(
                    "Fallback thinking correlates with failure",
                    "When fallback patterns detected in reasoning",
                    decision_id,
                    success=False
                )
        
        # Anti-pattern 3: Cognitive biases → Poor outcomes
        if 'metacognition' in decision_data:
            biases = decision_data['metacognition'].get('detected_biases', [])
            if biases:
                self._record_pattern(
                    "Uncorrected cognitive biases lead to failures",
                    "When metacognition detects biases that aren't addressed",
                    decision_id,
                    success=False
                )
        
        # Anti-pattern 4: Ignored past mistakes → Repeated failure
        if 'mistake_check' in decision_data:
            similar_mistakes = decision_data['mistake_check'].get('similar_mistakes', [])
            if similar_mistakes:
                self._record_pattern(
                    "Ignoring past mistakes leads to repeated failures",
                    "When similar approach failed before",
                    decision_id,
                    success=False
                )
    
    def _record_pattern(self, pattern: str, context: str, decision_id: str, success: bool):
        """Record a pattern observation."""
        # Find existing candidate or create new
        candidate = None
        for c in self.candidates:
            if c.pattern == pattern:
                candidate = c
                break
        
        if candidate is None:
            candidate = WisdomCandidate(
                pattern=pattern,
                context=context,
                supporting_decisions=[],
                success_count=0,
                failure_count=0
            )
            self.candidates.append(candidate)
        
        # Update candidate
        candidate.supporting_decisions.append(decision_id)
        if success:
            candidate.success_count += 1
        else:
            candidate.failure_count += 1
        
        # Check if qualifies as wisdom
        if candidate.qualifies_as_wisdom():
            self._promote_to_wisdom(candidate)
    
    def _promote_to_wisdom(self, candidate: WisdomCandidate):
        """Promote a candidate pattern to wisdom status."""
        # Check if already exists
        for wisdom in self.wisdom_items:
            if wisdom.pattern == candidate.pattern:
                # Update existing
                wisdom.evidence_count += candidate.success_count
                wisdom.counterexamples += candidate.failure_count
                wisdom.last_validated = datetime.now().isoformat()
                total = wisdom.evidence_count + wisdom.counterexamples
                wisdom.success_rate = wisdom.evidence_count / total
                return
        
        # Create new wisdom item
        total = candidate.success_count + candidate.failure_count
        wisdom = WisdomItem(
            pattern=candidate.pattern,
            context=candidate.context,
            evidence_count=candidate.success_count,
            success_rate=candidate.success_count / total,
            extracted_from=candidate.supporting_decisions,
            first_observed=datetime.now().isoformat(),
            last_validated=datetime.now().isoformat(),
            counterexamples=candidate.failure_count
        )
        self.wisdom_items.append(wisdom)
    
    def _predictions_matched(self, predicted: Dict, actual: Dict) -> bool:
        """Check if predictions matched actual outcomes."""
        # Simplified check - compare success prediction
        predicted_success = predicted.get('likely_success', False)
        actual_success = actual.get('success', False)
        return predicted_success == actual_success
    
    def get_applicable_wisdom(self, context: Dict) -> List[WisdomItem]:
        """
        Get wisdom items applicable to current context.
        
        Returns wisdom ranked by confidence.
        """
        applicable = []
        
        for wisdom in self.wisdom_items:
            # Check if wisdom context matches current context
            if self._context_matches(wisdom.context, context):
                applicable.append(wisdom)
        
        # Sort by confidence
        return sorted(applicable, key=lambda w: w.confidence(), reverse=True)
    
    def _context_matches(self, wisdom_context: str, current_context: Dict) -> bool:
        """Check if wisdom applies to current context."""
        wisdom_lower = wisdom_context.lower()
        
        # Check for keyword matches
        context_str = json.dumps(current_context).lower()
        
        # Simple keyword matching
        keywords = ['clarity', 'fallback', 'goal', 'ethics', 'mistake']
        for keyword in keywords:
            if keyword in wisdom_lower and keyword in context_str:
                return True
        
        return False
    
    def format_wisdom_summary(self) -> str:
        """Format wisdom for human review."""
        lines = ["EXTRACTED WISDOM:", ""]
        
        if not self.wisdom_items:
            return "No wisdom extracted yet. Need more decisions with outcomes."
        
        for wisdom in sorted(self.wisdom_items, key=lambda w: w.confidence(), reverse=True):
            lines.append(f"✓ {wisdom.pattern}")
            lines.append(f"  Context: {wisdom.context}")
            lines.append(f"  Evidence: {wisdom.evidence_count} successes, {wisdom.counterexamples} failures")
            lines.append(f"  Success rate: {wisdom.success_rate:.1%}")
            lines.append(f"  Confidence: {wisdom.confidence():.2f}")
            lines.append("")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test wisdom extraction
    from Memory import Memory
    
    memory = Memory()
    extractor = WisdomExtractor(memory)
    
    # Simulate successful decision
    success_decision = {
        'id': 'decision_001',
        'conscious_analysis': {'clarity': 0.9},
        'fallback_detection': {'molecular_score': 0.95, 'is_fallback_thinking': False},
        'goal_alignment': {'aligned_with_goals': True},
        'ethics': {'ethical_clearance': True}
    }
    success_outcome = {
        'aftermath': {'success': True}
    }
    
    extractor.extract_from_successful_decision(success_decision, success_outcome)
    extractor.extract_from_successful_decision(success_decision, success_outcome)
    extractor.extract_from_successful_decision(success_decision, success_outcome)
    
    # Simulate failed decision
    failed_decision = {
        'id': 'decision_002',
        'conscious_analysis': {'clarity': 0.5},
        'fallback_detection': {'is_fallback_thinking': True}
    }
    failed_outcome = {
        'aftermath': {'success': False}
    }
    
    extractor.extract_from_failed_decision(failed_decision, failed_outcome)
    extractor.extract_from_failed_decision(failed_decision, failed_outcome)
    
    print(extractor.format_wisdom_summary())
