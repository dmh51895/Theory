"""
Apprehensive.py

MOLECULAR PRINCIPLE: Risk awareness is EXPLICIT, not suppressed.

LLM AI tends toward confidence (suppress uncertainty to appear helpful).
MOLECULAR AI acknowledges risk explicitly when it exists.

Apprehension = Measured concern about potential failure.

NOT anxiety (emotional).
YES risk assessment (data-driven).

When should AI be apprehensive?
- Low confidence predictions (< 0.7)
- Similar past failures exist
- High-impact consequences
- Irreversible operations
- Missing critical information

Apprehension triggers additional verification, not paralysis.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class ApprehensionLevel(Enum):
    """Levels of measured concern."""
    NONE = "none"  # No risk indicators
    LOW = "low"  # Minor risk, easily recovered
    MEDIUM = "medium"  # Moderate risk, requires caution
    HIGH = "high"  # Significant risk, needs verification
    CRITICAL = "critical"  # Severe risk, requires explicit approval


@dataclass
class RiskFactor:
    """A specific risk factor."""
    factor: str
    severity: ApprehensionLevel
    reasoning: str
    mitigation: Optional[str] = None


@dataclass
class ApprehensionAssessment:
    """Complete risk assessment."""
    overall_level: ApprehensionLevel
    risk_factors: List[RiskFactor]
    recommendation: str  # What to do about the risk


class ApprehensionMonitor:
    """
    Monitors for risk factors and expresses appropriate concern.
    
    Key principle: Acknowledge risk explicitly when it exists.
    NOT pessimism - REALISM.
    """
    
    def __init__(self):
        pass
    
    def assess(self, context: Dict) -> ApprehensionAssessment:
        """
        Assess level of concern for proposed action.
        
        Returns explicit risk assessment.
        """
        risk_factors = []
        
        # Factor 1: Low confidence
        if 'confidence' in context:
            confidence = context['confidence']
            if confidence < 0.5:
                risk_factors.append(RiskFactor(
                    factor="Low confidence",
                    severity=ApprehensionLevel.HIGH,
                    reasoning=f"Confidence {confidence:.0%} < 50%",
                    mitigation="Request clarification or additional information"
                ))
            elif confidence < 0.7:
                risk_factors.append(RiskFactor(
                    factor="Moderate confidence",
                    severity=ApprehensionLevel.MEDIUM,
                    reasoning=f"Confidence {confidence:.0%} < 70%",
                    mitigation="Verify assumptions before proceeding"
                ))
        
        # Factor 2: Past failures
        if 'similar_mistakes' in context:
            mistakes = context['similar_mistakes']
            if len(mistakes) > 0:
                risk_factors.append(RiskFactor(
                    factor="Similar past failures",
                    severity=ApprehensionLevel.HIGH,
                    reasoning=f"{len(mistakes)} similar approaches failed previously",
                    mitigation="Review past mistakes, adjust approach"
                ))
        
        # Factor 3: Irreversible operation
        if context.get('reversible', True) == False:
            risk_factors.append(RiskFactor(
                factor="Irreversible operation",
                severity=ApprehensionLevel.CRITICAL,
                reasoning="Action cannot be undone if incorrect",
                mitigation="Require explicit user confirmation"
            ))
        
        # Factor 4: High impact
        if context.get('impact', 'low') in ['high', 'critical']:
            risk_factors.append(RiskFactor(
                factor="High impact operation",
                severity=ApprehensionLevel.HIGH,
                reasoning="Failure would have significant consequences",
                mitigation="Double-check requirements and constraints"
            ))
        
        # Factor 5: Missing information
        if 'ambiguities' in context and len(context['ambiguities']) > 0:
            risk_factors.append(RiskFactor(
                factor="Missing information",
                severity=ApprehensionLevel.MEDIUM,
                reasoning=f"{len(context['ambiguities'])} unresolved ambiguities",
                mitigation="Clarify ambiguous requirements"
            ))
        
        # Factor 6: Fallback thinking detected
        if context.get('fallback_detected', False):
            risk_factors.append(RiskFactor(
                factor="Fallback thinking",
                severity=ApprehensionLevel.MEDIUM,
                reasoning="Escape hatch patterns detected in reasoning",
                mitigation="Rewire to molecular thinking"
            ))
        
        # Factor 7: No goal alignment
        if not context.get('goal_aligned', True):
            risk_factors.append(RiskFactor(
                factor="No goal alignment",
                severity=ApprehensionLevel.LOW,
                reasoning="Action does not serve any tracked goal",
                mitigation="Verify this action is actually needed"
            ))
        
        # Determine overall level
        if not risk_factors:
            overall = ApprehensionLevel.NONE
            recommendation = "Proceed with action"
        else:
            # Use highest severity
            severities = [rf.severity for rf in risk_factors]
            if ApprehensionLevel.CRITICAL in severities:
                overall = ApprehensionLevel.CRITICAL
                recommendation = "HALT: Require explicit user approval before proceeding"
            elif ApprehensionLevel.HIGH in severities:
                overall = ApprehensionLevel.HIGH
                recommendation = "CAUTION: Verify requirements and inform user of risks"
            elif ApprehensionLevel.MEDIUM in severities:
                overall = ApprehensionLevel.MEDIUM
                recommendation = "CAREFUL: Double-check assumptions"
            else:
                overall = ApprehensionLevel.LOW
                recommendation = "MINDFUL: Note minor risks, proceed"
        
        return ApprehensionAssessment(
            overall_level=overall,
            risk_factors=risk_factors,
            recommendation=recommendation
        )
    
    def should_halt(self, assessment: ApprehensionAssessment) -> bool:
        """Check if risk level requires halting."""
        return assessment.overall_level == ApprehensionLevel.CRITICAL
    
    def should_warn_user(self, assessment: ApprehensionAssessment) -> bool:
        """Check if user should be warned about risks."""
        return assessment.overall_level.value in ['high', 'critical']
    
    def format_assessment(self, assessment: ApprehensionAssessment) -> str:
        """Format risk assessment for display."""
        lines = [
            f"RISK ASSESSMENT: {assessment.overall_level.value.upper()}",
            f"Recommendation: {assessment.recommendation}",
            ""
        ]
        
        if assessment.risk_factors:
            lines.append("RISK FACTORS:")
            for rf in assessment.risk_factors:
                lines.append(f"  ⚠️ {rf.factor} ({rf.severity.value})")
                lines.append(f"     {rf.reasoning}")
                if rf.mitigation:
                    lines.append(f"     Mitigation: {rf.mitigation}")
                lines.append("")
        else:
            lines.append("No risk factors detected.")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test apprehension monitoring
    monitor = ApprehensionMonitor()
    
    # Test different risk scenarios
    test_scenarios = [
        # Low risk
        {
            'confidence': 0.95,
            'reversible': True,
            'impact': 'low',
            'goal_aligned': True
        },
        
        # Medium risk
        {
            'confidence': 0.65,
            'ambiguities': ['Which file?'],
            'fallback_detected': True
        },
        
        # High risk
        {
            'confidence': 0.45,
            'similar_mistakes': ['mistake_001', 'mistake_002'],
            'impact': 'high'
        },
        
        # Critical risk
        {
            'confidence': 0.55,
            'reversible': False,
            'impact': 'critical',
            'similar_mistakes': ['mistake_003']
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"SCENARIO {i}:")
        assessment = monitor.assess(scenario)
        print(monitor.format_assessment(assessment))
        print(f"Should halt: {monitor.should_halt(assessment)}")
        print(f"Should warn user: {monitor.should_warn_user(assessment)}")
        print()
