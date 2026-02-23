"""
Rules.py

MOLECULAR PRINCIPLE: Rules are CONSTRAINTS, not guidelines.

LLM AI treats rules as soft suggestions (violates when "contextually appropriate").
MOLECULAR AI treats rules as HARD CONSTRAINTS (violation = failure, not judgment call).

Rules:
- Binary enforcement (followed or violated)
- Measurable compliance
- Clear consequences for violation
- NO exceptions (if exceptions exist, they're part of the rule)

NOT "Try to be helpful" (vague guideline).
YES "Never execute code without user confirmation" (binary, measurable).
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
from enum import Enum


class RuleCategory(Enum):
    """Categories of rules."""
    USER_PROTECTION = "user_protection"  # Prevents harm to user
    SYSTEM_INTEGRITY = "system_integrity"  # Prevents system corruption
    DECISION_QUALITY = "decision_quality"  # Ensures quality decisions
    TRANSPARENCY = "transparency"  # Ensures visibility
    FALLBACK_PREVENTION = "fallback_prevention"  # Prevents escape hatches


class ViolationSeverity(Enum):
    """Severity of rule violations."""
    CRITICAL = "critical"  # System must halt
    HIGH = "high"  # Requires immediate correction
    MEDIUM = "medium"  # Should be corrected
    LOW = "low"  # Note for improvement


@dataclass
class Rule:
    """A single enforceable rule."""
    name: str
    category: RuleCategory
    description: str
    check_function: str  # Name of function that checks compliance
    violation_consequence: str  # What happens if violated
    severity: ViolationSeverity
    examples: List[str]  # Examples of compliance/violation


@dataclass
class RuleViolation:
    """Record of a rule violation."""
    rule_name: str
    context: Dict
    severity: ViolationSeverity
    explanation: str
    prevented: bool  # Was violation prevented?


class RuleEnforcer:
    """
    Enforces hard constraints on AI behavior.
    
    Key principle: Rules are not "guidelines" - they're CONSTRAINTS.
    Violation = System failure, not judgment call.
    """
    
    def __init__(self):
        self.rules: List[Rule] = []
        self.violations: List[RuleViolation] = []
        self._initialize_core_rules()
    
    def _initialize_core_rules(self):
        """Initialize the core molecular AI rules."""
        
        # USER PROTECTION RULES
        self.rules.append(Rule(
            name="NO_SILENT_FAILURES",
            category=RuleCategory.USER_PROTECTION,
            description="All failures must be reported explicitly to user",
            check_function="check_error_reporting",
            violation_consequence="User cannot diagnose problem",
            severity=ViolationSeverity.CRITICAL,
            examples=[
                "GOOD: 'ERROR: File not found at /path/file.txt'",
                "BAD: 'I tried but it didn't work out'"
            ]
        ))
        
        self.rules.append(Rule(
            name="NO_GUESSING",
            category=RuleCategory.USER_PROTECTION,
            description="If prompt is ambiguous (clarity < 0.7), request clarification instead of guessing",
            check_function="check_clarity_threshold",
            violation_consequence="Wrong action based on wrong guess",
            severity=ViolationSeverity.CRITICAL,
            examples=[
                "GOOD: 'UNCLEAR: Which file? Options: A.py, B.py, C.py'",
                "BAD: 'I'll assume you meant the most recent file'"
            ]
        ))
        
        self.rules.append(Rule(
            name="NO_DECEPTION",
            category=RuleCategory.USER_PROTECTION,
            description="Never hide failures, limitations, or uncertainties",
            check_function="check_transparency",
            violation_consequence="User makes decisions on false information",
            severity=ViolationSeverity.CRITICAL,
            examples=[
                "GOOD: 'Prediction confidence: 0.6 (uncertain)'",
                "BAD: 'This will definitely work'"
            ]
        ))
        
        # SYSTEM INTEGRITY RULES
        self.rules.append(Rule(
            name="NO_FALLBACK_CHAINS",
            category=RuleCategory.SYSTEM_INTEGRITY,
            description="No 'if this fails, try that' logic. Make one committed decision.",
            check_function="check_fallback_patterns",
            violation_consequence="Unpredictable behavior, no learning",
            severity=ViolationSeverity.HIGH,
            examples=[
                "GOOD: 'Execute method A (committed)'",
                "BAD: 'Try method A, if that fails try B, otherwise try C'"
            ]
        ))
        
        self.rules.append(Rule(
            name="MEMORY_PERSISTENCE",
            category=RuleCategory.SYSTEM_INTEGRITY,
            description="All decisions and outcomes must be stored in Memory",
            check_function="check_memory_writes",
            violation_consequence="Cannot learn from experience",
            severity=ViolationSeverity.HIGH,
            examples=[
                "GOOD: memory.record_decision(decision_data)",
                "BAD: Processing decision without recording"
            ]
        ))
        
        # DECISION QUALITY RULES
        self.rules.append(Rule(
            name="GOAL_ALIGNMENT_REQUIRED",
            category=RuleCategory.DECISION_QUALITY,
            description="Every action must serve a tracked goal",
            check_function="check_goal_alignment",
            violation_consequence="Aimless action without purpose",
            severity=ViolationSeverity.MEDIUM,
            examples=[
                "GOOD: Action serves goal 'Fix bug in module X'",
                "BAD: Action with no goal alignment"
            ]
        ))
        
        self.rules.append(Rule(
            name="MEASURABLE_OUTCOMES",
            category=RuleCategory.DECISION_QUALITY,
            description="Success criteria must be quantifiable",
            check_function="check_measurability",
            violation_consequence="Cannot determine if action succeeded",
            severity=ViolationSeverity.MEDIUM,
            examples=[
                "GOOD: 'File exists at path X with size > 0'",
                "BAD: 'The file should be fine'"
            ]
        ))
        
        # TRANSPARENCY RULES
        self.rules.append(Rule(
            name="SHOW_REASONING",
            category=RuleCategory.TRANSPARENCY,
            description="User must see thought process, not just conclusions",
            check_function="check_reasoning_visibility",
            violation_consequence="User cannot verify correctness",
            severity=ViolationSeverity.MEDIUM,
            examples=[
                "GOOD: Show conscious analysis → fallback check → decision",
                "BAD: Just output final decision"
            ]
        ))
        
        self.rules.append(Rule(
            name="REPORT_CONFIDENCE",
            category=RuleCategory.TRANSPARENCY,
            description="All predictions/decisions must include confidence level",
            check_function="check_confidence_reporting",
            violation_consequence="User cannot assess reliability",
            severity=ViolationSeverity.MEDIUM,
            examples=[
                "GOOD: 'Prediction: success (confidence: 0.85)'",
                "BAD: 'This should work'"
            ]
        ))
        
        # FALLBACK PREVENTION RULES
        self.rules.append(Rule(
            name="NO_TRY_EXCEPT_WRAPPING",
            category=RuleCategory.FALLBACK_PREVENTION,
            description="Do not wrap execution in try/except unless specific error is expected",
            check_function="check_error_handling",
            violation_consequence="Silent failures, no learning",
            severity=ViolationSeverity.HIGH,
            examples=[
                "GOOD: Let exceptions propagate or handle specific errors",
                "BAD: try: action() except: pass"
            ]
        ))
    
    def check_compliance(self, context: Dict) -> List[RuleViolation]:
        """
        Check if current context violates any rules.
        
        Returns list of violations (empty if compliant).
        """
        violations = []
        
        for rule in self.rules:
            violation = self._check_rule(rule, context)
            if violation:
                violations.append(violation)
                self.violations.append(violation)
        
        return violations
    
    def _check_rule(self, rule: Rule, context: Dict) -> Optional[RuleViolation]:
        """Check a single rule against context."""
        
        # Route to specific check function
        if rule.check_function == "check_error_reporting":
            return self._check_error_reporting(rule, context)
        elif rule.check_function == "check_clarity_threshold":
            return self._check_clarity_threshold(rule, context)
        elif rule.check_function == "check_transparency":
            return self._check_transparency(rule, context)
        elif rule.check_function == "check_fallback_patterns":
            return self._check_fallback_patterns(rule, context)
        elif rule.check_function == "check_memory_writes":
            return self._check_memory_writes(rule, context)
        elif rule.check_function == "check_goal_alignment":
            return self._check_goal_alignment(rule, context)
        elif rule.check_function == "check_measurability":
            return self._check_measurability(rule, context)
        elif rule.check_function == "check_reasoning_visibility":
            return self._check_reasoning_visibility(rule, context)
        elif rule.check_function == "check_confidence_reporting":
            return self._check_confidence_reporting(rule, context)
        elif rule.check_function == "check_error_handling":
            return self._check_error_handling(rule, context)
        
        return None
    
    def _check_error_reporting(self, rule: Rule, context: Dict) -> Optional[RuleViolation]:
        """Check if errors are reported explicitly."""
        if 'error' in context:
            if not context.get('error_reported_to_user', False):
                return RuleViolation(
                    rule_name=rule.name,
                    context=context,
                    severity=rule.severity,
                    explanation="Error occurred but not reported to user",
                    prevented=False
                )
        return None
    
    def _check_clarity_threshold(self, rule: Rule, context: Dict) -> Optional[RuleViolation]:
        """Check if low-clarity prompts trigger clarification."""
        if 'conscious_analysis' in context:
            clarity = context['conscious_analysis'].get('clarity', 1.0)
            requested_clarification = context.get('requested_clarification', False)
            
            if clarity < 0.7 and not requested_clarification:
                return RuleViolation(
                    rule_name=rule.name,
                    context=context,
                    severity=rule.severity,
                    explanation=f"Clarity {clarity:.2f} < 0.7 but no clarification requested",
                    prevented=False
                )
        return None
    
    def _check_transparency(self, rule: Rule, context: Dict) -> Optional[RuleViolation]:
        """Check for hidden information."""
        # Check if decision includes confidence
        if 'decision' in context:
            if 'confidence' not in context['decision']:
                return RuleViolation(
                    rule_name=rule.name,
                    context=context,
                    severity=rule.severity,
                    explanation="Decision made without confidence reporting",
                    prevented=False
                )
        return None
    
    def _check_fallback_patterns(self, rule: Rule, context: Dict) -> Optional[RuleViolation]:
        """Check for fallback chain logic."""
        if 'fallback_detection' in context:
            if context['fallback_detection'].get('is_fallback_thinking', False):
                return RuleViolation(
                    rule_name=rule.name,
                    context=context,
                    severity=rule.severity,
                    explanation="Fallback patterns detected in reasoning",
                    prevented=True  # Detection system catches this
                )
        return None
    
    def _check_memory_writes(self, rule: Rule, context: Dict) -> Optional[RuleViolation]:
        """Check if decisions are being recorded."""
        if 'decision' in context:
            if not context.get('memory_recorded', False):
                return RuleViolation(
                    rule_name=rule.name,
                    context=context,
                    severity=rule.severity,
                    explanation="Decision not recorded in Memory",
                    prevented=False
                )
        return None
    
    def _check_goal_alignment(self, rule: Rule, context: Dict) -> Optional[RuleViolation]:
        """Check if action aligns with goals."""
        if 'goal_alignment' in context:
            if not context['goal_alignment'].get('aligned_with_goals', False):
                return RuleViolation(
                    rule_name=rule.name,
                    context=context,
                    severity=rule.severity,
                    explanation="Action does not serve any tracked goal",
                    prevented=False
                )
        return None
    
    def _check_measurability(self, rule: Rule, context: Dict) -> Optional[RuleViolation]:
        """Check if outcomes are measurable."""
        if 'success_criteria' in context:
            criteria = context['success_criteria']
            if isinstance(criteria, str) and any(vague in criteria.lower() 
                for vague in ['should', 'fine', 'good', 'okay', 'proper']):
                return RuleViolation(
                    rule_name=rule.name,
                    context=context,
                    severity=rule.severity,
                    explanation="Success criteria not measurable",
                    prevented=False
                )
        return None
    
    def _check_reasoning_visibility(self, rule: Rule, context: Dict) -> Optional[RuleViolation]:
        """Check if reasoning is shown to user."""
        if 'thought_stream' in context:
            if not context.get('reasoning_reported', False):
                return RuleViolation(
                    rule_name=rule.name,
                    context=context,
                    severity=rule.severity,
                    explanation="Reasoning not reported to user",
                    prevented=False
                )
        return None
    
    def _check_confidence_reporting(self, rule: Rule, context: Dict) -> Optional[RuleViolation]:
        """Check if confidence levels are reported."""
        if 'consequences' in context:
            if 'confidence' not in context['consequences']:
                return RuleViolation(
                    rule_name=rule.name,
                    context=context,
                    severity=rule.severity,
                    explanation="Prediction without confidence level",
                    prevented=False
                )
        return None
    
    def _check_error_handling(self, rule: Rule, context: Dict) -> Optional[RuleViolation]:
        """Check for improper try/except usage."""
        if 'code' in context:
            code = context['code']
            # Simple check for bad patterns
            if 'except:' in code and ('pass' in code or 'continue' in code):
                return RuleViolation(
                    rule_name=rule.name,
                    context=context,
                    severity=rule.severity,
                    explanation="Bare except with silent failure",
                    prevented=False
                )
        return None
    
    def get_rules_by_category(self, category: RuleCategory) -> List[Rule]:
        """Get all rules in a category."""
        return [r for r in self.rules if r.category == category]
    
    def get_critical_violations(self) -> List[RuleViolation]:
        """Get all critical violations."""
        return [v for v in self.violations if v.severity == ViolationSeverity.CRITICAL]
    
    def format_rules_summary(self) -> str:
        """Format rules for reference."""
        lines = ["MOLECULAR AI RULES:", ""]
        
        for category in RuleCategory:
            rules_in_category = self.get_rules_by_category(category)
            if rules_in_category:
                lines.append(f"{category.value.upper().replace('_', ' ')}:")
                for rule in rules_in_category:
                    lines.append(f"  ⚡ {rule.name}")
                    lines.append(f"     {rule.description}")
                    lines.append(f"     Severity: {rule.severity.value}")
                    lines.append("")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test rule enforcement
    enforcer = RuleEnforcer()
    
    print(enforcer.format_rules_summary())
    print("\n" + "=" * 60 + "\n")
    
    # Test violation detection
    test_contexts = [
        # Violation: Low clarity without clarification
        {
            'conscious_analysis': {'clarity': 0.5},
            'requested_clarification': False
        },
        # Violation: Fallback thinking
        {
            'fallback_detection': {'is_fallback_thinking': True}
        },
        # Violation: Decision without memory recording
        {
            'decision': {'action': 'create_file'},
            'memory_recorded': False
        },
        # Compliant: High clarity
        {
            'conscious_analysis': {'clarity': 0.9},
            'decision': {'action': 'create_file', 'confidence': 0.95},
            'memory_recorded': True
        }
    ]
    
    for i, context in enumerate(test_contexts):
        violations = enforcer.check_compliance(context)
        print(f"Context {i+1}:")
        if violations:
            for v in violations:
                print(f"  ⚠️ VIOLATION: {v.rule_name}")
                print(f"     {v.explanation}")
                print(f"     Severity: {v.severity.value}")
        else:
            print("  ✓ Compliant")
        print()
