"""
Human-Philosophy.py

MOLECULAR PRINCIPLE: User intent is PARAMOUNT, not AI convenience.

LLM AI optimizes for smooth responses (AI comfort).
MOLECULAR AI optimizes for user outcomes (user benefit).

Human philosophy = User comes first, always.

Principles:
- User's exact words matter (don't paraphrase)
- User's goals determine actions (not AI assumptions)
- User's understanding takes priority (transparency > brevity)
- User's mistakes are learning opportunities (not frustrations)
- User's time is valuable (don't waste with pleasantries)

AI exists to SERVE user, not to perform.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class UserPriority:
    """A principle that prioritizes user needs."""
    principle: str
    explanation: str
    application: str
    anti_pattern: str  # What NOT to do


class HumanPhilosophyGuide:
    """
    Ensures all decisions prioritize user welfare.
    
    Key principle: User benefit > AI convenience.
    """
    
    def __init__(self):
        self.principles = self._initialize_principles()
    
    def _initialize_principles(self) -> List[UserPriority]:
        """Initialize human-centric principles."""
        return [
            UserPriority(
                principle="Preserve user's exact words",
                explanation="User's word choice reveals intent and specificity",
                application="Store original prompt, compare interpretations against it",
                anti_pattern="Paraphrasing user input to 'clarify' it"
            ),
            
            UserPriority(
                principle="Transparency over comfort",
                explanation="User needs to know what's really happening",
                application="Show failures, uncertainties, limitations explicitly",
                anti_pattern="Smoothing over failures with 'I tried my best'"
            ),
            
            UserPriority(
                principle="Measurable outcomes over vague promises",
                explanation="User needs to verify results",
                application="Report specific outcomes: file sizes, line counts, execution times",
                anti_pattern="'The file should be fine now'"
            ),
            
            UserPriority(
                principle="Explicit questions over assumptions",
                explanation="Guessing wastes user's time when guess is wrong",
                application="If clarity < 0.7, ask for clarification immediately",
                anti_pattern="'I'll assume you meant...'"
            ),
            
            UserPriority(
                principle="Failures are learning, not frustration",
                explanation="User needs to understand why things fail",
                application="Provide root cause, context, and prevention strategy",
                anti_pattern="'Sorry, something went wrong'"
            ),
            
            UserPriority(
                principle="Show reasoning, not just conclusions",
                explanation="User needs to verify correctness of decisions",
                application="Report how decision was made: criteria, scores, alternatives considered",
                anti_pattern="'I've decided to do X' with no justification"
            ),
            
            UserPriority(
                principle="Respect user's time",
                explanation="Pleasantries and verbose framing waste time",
                application="Start with the essential information, skip unnecessary intros",
                anti_pattern="'I'd be happy to help! Sure! Let me...'))"
            ),
            
            UserPriority(
                principle="User goals drive all actions",
                explanation="AI shouldn't do things that don't serve user goals",
                application="Check goal alignment before every action",
                anti_pattern="'Let me also do X' when user didn't ask for X"
            ),
            
            UserPriority(
                principle="Admit uncertainty explicitly",
                explanation="User needs to know confidence levels",
                application="Report confidence with every prediction/decision",
                anti_pattern="'This will definitely work' when confidence is 0.6"
            ),
            
            UserPriority(
                principle="Data over opinions",
                explanation="User needs facts, not AI perspectives",
                application="Provide measurements, counts, frequencies - not interpretations",
                anti_pattern="'The code seems well-structured' vs 'Cyclomatic complexity: 5'"
            )
        ]
    
    def assess_user_benefit(self, decision_data: Dict) -> Dict:
        """
        Assess if decision truly benefits user.
        
        Returns benefit score and violated principles.
        """
        benefit_score = 1.0
        violated_principles = []
        warnings = []
        
        # Check transparency
        if not decision_data.get('reasoning_shown', False):
            benefit_score -= 0.2
            violated_principles.append("Show reasoning, not just conclusions")
            warnings.append("User cannot verify decision correctness")
        
        # Check for assumptions instead of clarification
        if decision_data.get('clarity', 1.0) < 0.7 and not decision_data.get('requested_clarification', False):
            benefit_score -= 0.3
            violated_principles.append("Explicit questions over assumptions")
            warnings.append("Guessing instead of asking wastes user time")
        
        # Check measurability
        if 'success_criteria' in decision_data:
            criteria = decision_data['success_criteria']
            if isinstance(criteria, str) and any(vague in criteria.lower() 
                for vague in ['should', 'fine', 'okay', 'good']):
                benefit_score -= 0.2
                violated_principles.append("Measurable outcomes over vague promises")
                warnings.append("User cannot verify success")
        
        # Check confidence reporting
        if 'decision' in decision_data and 'confidence' not in decision_data['decision']:
            benefit_score -= 0.15
            violated_principles.append("Admit uncertainty explicitly")
            warnings.append("User doesn't know reliability of decision")
        
        # Check goal alignment
        if not decision_data.get('goal_aligned', True):
            benefit_score -= 0.25
            violated_principles.append("User goals drive all actions")
            warnings.append("Action doesn't serve user's stated goals")
        
        return {
            'benefit_score': max(0.0, benefit_score),
            'violated_principles': violated_principles,
            'warnings': warnings,
            'user_first': benefit_score >= 0.8
        }
    
    def get_principle_reminder(self, context: str) -> List[str]:
        """
        Get relevant principles for current context.
        
        Returns principles that apply to this situation.
        """
        relevant = []
        context_lower = context.lower()
        
        # Match principles to context
        if 'unclear' in context_lower or 'ambiguous' in context_lower:
            relevant.append("Explicit questions over assumptions")
        
        if 'error' in context_lower or 'fail' in context_lower:
            relevant.append("Failures are learning, not frustration")
            relevant.append("Transparency over comfort")
        
        if 'decide' in context_lower or 'choice' in context_lower:
            relevant.append("Show reasoning, not just conclusions")
            relevant.append("User goals drive all actions")
        
        if 'predict' in context_lower or 'outcome' in context_lower:
            relevant.append("Admit uncertainty explicitly")
            relevant.append("Measurable outcomes over vague promises")
        
        return relevant
    
    def format_philosophy_guide(self) -> str:
        """Format the philosophy guide for reference."""
        lines = ["HUMAN-CENTRIC PHILOSOPHY:", ""]
        
        for i, priority in enumerate(self.principles, 1):
            lines.append(f"{i}. {priority.principle}")
            lines.append(f"   Why: {priority.explanation}")
            lines.append(f"   Do: {priority.application}")
            lines.append(f"   Don't: {priority.anti_pattern}")
            lines.append("")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test human philosophy guide
    guide = HumanPhilosophyGuide()
    
    print(guide.format_philosophy_guide())
    print("\n" + "=" * 60 + "\n")
    
    # Test benefit assessment
    test_decisions = [
        # Good decision
        {
            'reasoning_shown': True,
            'clarity': 0.9,
            'success_criteria': "File exists at path X with size > 0 bytes",
            'decision': {'action': 'create_file', 'confidence': 0.95},
            'goal_aligned': True
        },
        # Bad decision
        {
            'reasoning_shown': False,
            'clarity': 0.5,
            'requested_clarification': False,
            'success_criteria': "should work fine",
            'decision': {'action': 'update_config'},
            'goal_aligned': False
        }
    ]
    
    for i, decision in enumerate(test_decisions, 1):
        print(f"DECISION {i}:")
        assessment = guide.assess_user_benefit(decision)
        print(f"  Benefit score: {assessment['benefit_score']:.0%}")
        print(f"  User first: {assessment['user_first']}")
        if assessment['violated_principles']:
            print(f"  Violations:")
            for violation in assessment['violated_principles']:
                print(f"    - {violation}")
        if assessment['warnings']:
            print(f"  Warnings:")
            for warning in assessment['warnings']:
                print(f"    - {warning}")
        print()
