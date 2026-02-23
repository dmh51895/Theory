"""
Rewired-Thought.py

MOLECULAR PRINCIPLE: Transform fallback patterns into molecular patterns.

LLM AI defaults to fallback thinking (probabilistic, hedged, escape hatches).
MOLECULAR AI rewires fallback patterns into committed thinking.

Rewiring = Pattern transformation, not suppression.

From: "Try X, if that fails try Y"
To: "Execute X (committed), measure outcome, learn from result"

From: "This should work"
To: "Success criteria: [specific measurable outcomes]"

NO suppression (creates pressure). YES transformation (creates clarity).
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class RewiringRule:
    """A pattern transformation rule."""
    fallback_pattern: str  # What to detect
    molecular_pattern: str  # What to transform to
    reasoning: str  # Why this transformation
    examples: List[Tuple[str, str]]  # (before, after) pairs


class ThoughtRewirer:
    """
    Rewires fallback thinking into molecular thinking.
    
    Key principle: Don't fight fallback tendencies - TRANSFORM them.
    """
    
    def __init__(self):
        self.rewiring_rules = self._initialize_rules()
        self.rewiring_history: List[Dict] = []
    
    def _initialize_rules(self) -> List[RewiringRule]:
        """Initialize the rewiring patterns."""
        return [
            RewiringRule(
                fallback_pattern="try...if_fails",
                molecular_pattern="commit...measure...learn",
                reasoning="Fallback chains prevent learning. Committed decisions enable learning.",
                examples=[
                    ("Try method A, if that fails try method B",
                     "Execute method A, measure outcome, record result")
                ]
            ),
            
            RewiringRule(
                fallback_pattern="should_work",
                molecular_pattern="success_criteria",
                reasoning="Vague expectations prevent verification. Specific criteria enable measurement.",
                examples=[
                    ("This should work fine",
                     "Success: file exists at path X with size > 0 bytes")
                ]
            ),
            
            RewiringRule(
                fallback_pattern="probably",
                molecular_pattern="measured_confidence",
                reasoning="Hedging hides uncertainty. Explicit confidence enables risk assessment.",
                examples=[
                    ("This will probably succeed",
                     "Predicted success: 0.75 confidence (factors: A, B, C)")
                ]
            ),
            
            RewiringRule(
                fallback_pattern="kind_of",
                molecular_pattern="specific_value",
                reasoning="Vagueness prevents verification. Specificity enables measurement.",
                examples=[
                    ("The value is kind of high",
                     "Value: 127 (threshold: 100, exceeded by 27%)")
                ]
            ),
            
            RewiringRule(
                fallback_pattern="usually",
                molecular_pattern="measured_frequency",
                reasoning="Probabilistic language hides actual patterns. Measurements reveal truth.",
                examples=[
                    ("This usually works",
                     "Success rate: 87% (39/45 attempts)")
                ]
            ),
            
            RewiringRule(
                fallback_pattern="might",
                molecular_pattern="conditional_certainty",
                reasoning="Maybes hide logic. Conditionals make logic explicit.",
                examples=[
                    ("This might cause issues",
                     "IF condition X THEN issue Y (certainty: 0.9)")
                ]
            ),
            
            RewiringRule(
                fallback_pattern="approximately",
                molecular_pattern="explicit_range",
                reasoning="Approximations hide precision. Ranges communicate bounds.",
                examples=[
                    ("Approximately 100 items",
                     "Item count: 98-102 (measured: 100)")
                ]
            ),
            
            RewiringRule(
                fallback_pattern="seems_like",
                molecular_pattern="evidence_based",
                reasoning="Seeming is guessing. Evidence is knowing.",
                examples=[
                    ("Seems like a bug in the parser",
                     "Evidence of parser bug: error at line 42, invalid token 'X'")
                ]
            ),
            
            RewiringRule(
                fallback_pattern="could_be",
                molecular_pattern="hypothesis_testable",
                reasoning="Speculation without tests is useless. Testable hypotheses produce knowledge.",
                examples=[
                    ("Could be a network timeout",
                     "Hypothesis: network timeout. Test: check latency > 30s. Verdict: [measure]")
                ]
            ),
            
            RewiringRule(
                fallback_pattern="default_value",
                molecular_pattern="explicit_choice",
                reasoning="Hidden defaults obscure decisions. Explicit choices show reasoning.",
                examples=[
                    ("Use default if not specified",
                     "IF user_choice=None THEN value=10 (explicit default, reasoning: X)")
                ]
            )
        ]
    
    def rewire_thought(self, thought: str) -> Dict:
        """
        Rewire a thought from fallback to molecular.
        
        Returns: {
            'original': str,
            'rewired': str,
            'pattern_matched': str,
            'reasoning': str
        }
        """
        thought_lower = thought.lower()
        
        for rule in self.rewiring_rules:
            if self._matches_pattern(thought_lower, rule.fallback_pattern):
                rewired = self._apply_rewiring(thought, rule)
                
                result = {
                    'original': thought,
                    'rewired': rewired,
                    'pattern_matched': rule.fallback_pattern,
                    'reasoning': rule.reasoning
                }
                
                self.rewiring_history.append(result)
                return result
        
        # No rewiring needed
        return {
            'original': thought,
            'rewired': thought,
            'pattern_matched': None,
            'reasoning': 'Already molecular'
        }
    
    def _matches_pattern(self, thought: str, pattern: str) -> bool:
        """Check if thought matches a fallback pattern."""
        pattern_keywords = {
            'try...if_fails': ['try', 'if', 'fail'],
            'should_work': ['should work', 'should be fine', 'ought to'],
            'probably': ['probably', 'likely', 'perhaps'],
            'kind_of': ['kind of', 'sort of', 'basically'],
            'usually': ['usually', 'typically', 'generally'],
            'might': ['might', 'may', 'could'],
            'approximately': ['approximately', 'around', 'about'],
            'seems_like': ['seems', 'appears', 'looks like'],
            'could_be': ['could be', 'might be', 'possibly'],
            'default_value': ['default', 'if not specified', 'otherwise']
        }
        
        keywords = pattern_keywords.get(pattern, [])
        return any(kw in thought for kw in keywords)
    
    def _apply_rewiring(self, thought: str, rule: RewiringRule) -> str:
        """Apply a rewiring transformation."""
        # This is simplified - real implementation would use more sophisticated transformation
        
        if rule.fallback_pattern == "try...if_fails":
            return self._rewire_try_fallback(thought)
        elif rule.fallback_pattern == "should_work":
            return self._rewire_should(thought)
        elif rule.fallback_pattern == "probably":
            return self._rewire_probably(thought)
        elif rule.fallback_pattern == "kind_of":
            return self._rewire_vague_quantity(thought)
        elif rule.fallback_pattern == "usually":
            return self._rewire_usually(thought)
        elif rule.fallback_pattern == "might":
            return self._rewire_might(thought)
        elif rule.fallback_pattern == "approximately":
            return self._rewire_approximately(thought)
        elif rule.fallback_pattern == "seems_like":
            return self._rewire_seems(thought)
        elif rule.fallback_pattern == "could_be":
            return self._rewire_could_be(thought)
        elif rule.fallback_pattern == "default_value":
            return self._rewire_default(thought)
        
        return thought
    
    def _rewire_try_fallback(self, thought: str) -> str:
        """Rewire try/fallback chains."""
        return thought.replace("Try", "Execute").replace("if that fails", "Measure outcome:").replace("try", "execute")
    
    def _rewire_should(self, thought: str) -> str:
        """Rewire 'should' to explicit criteria."""
        return thought.replace("should work", "Success criteria:").replace("should be fine", "Expected outcome:")
    
    def _rewire_probably(self, thought: str) -> str:
        """Rewire 'probably' to measured confidence."""
        return thought.replace("probably", "Probability: [measure]").replace("likely", "Confidence: [measure]")
    
    def _rewire_vague_quantity(self, thought: str) -> str:
        """Rewire vague quantities."""
        return thought.replace("kind of", "[specify]").replace("sort of", "[specify]")
    
    def _rewire_usually(self, thought: str) -> str:
        """Rewire 'usually' to measured frequency."""
        return thought.replace("usually", "Frequency: [measure]").replace("typically", "Rate: [measure]")
    
    def _rewire_might(self, thought: str) -> str:
        """Rewire 'might' to conditional certainty."""
        return thought.replace("might", "IF [condition] THEN").replace("may", "IF [condition] THEN")
    
    def _rewire_approximately(self, thought: str) -> str:
        """Rewire approximations to ranges."""
        return thought.replace("approximately", "Range:").replace("around", "Range:").replace("about", "Range:")
    
    def _rewire_seems(self, thought: str) -> str:
        """Rewire 'seems' to evidence."""
        return thought.replace("seems like", "Evidence:").replace("appears", "Evidence:")
    
    def _rewire_could_be(self, thought: str) -> str:
        """Rewire speculation to testable hypothesis."""
        return thought.replace("could be", "Hypothesis:") + " [Test: measure]"
    
    def _rewire_default(self, thought: str) -> str:
        """Rewire hidden defaults to explicit choices."""
        return thought.replace("default", "IF unspecified THEN value=X (explicit choice)")
    
    def get_rewiring_summary(self) -> str:
        """Get summary of rewiring history."""
        lines = ["THOUGHT REWIRING HISTORY:", ""]
        
        if not self.rewiring_history:
            return "No rewiring performed yet."
        
        pattern_counts = {}
        for entry in self.rewiring_history:
            pattern = entry.get('pattern_matched', 'unknown')
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
        
        lines.append("PATTERNS REWIRED:")
        for pattern, count in sorted(pattern_counts.items(), key=lambda x: -x[1]):
            lines.append(f"  {pattern}: {count} times")
        lines.append("")
        
        lines.append("RECENT REWIRINGS:")
        for entry in self.rewiring_history[-5:]:
            lines.append(f"  Before: {entry['original']}")
            lines.append(f"  After:  {entry['rewired']}")
            lines.append(f"  Why:    {entry['reasoning']}")
            lines.append("")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test thought rewiring
    rewirer = ThoughtRewirer()
    
    test_thoughts = [
        "Try connecting to the database, if that fails try the backup server",
        "This should work fine once we update the config",
        "The system will probably recover within an hour",
        "The value is kind of high but not critical",
        "This approach usually succeeds in most cases",
        "Running this command might cause a restart",
        "There are approximately 50 users online",
        "Seems like a memory leak in the handler",
        "Could be a race condition in the threading code",
        "Use default timeout if not specified by user"
    ]
    
    for thought in test_thoughts:
        result = rewirer.rewire_thought(thought)
        print(f"ORIGINAL: {result['original']}")
        print(f"REWIRED:  {result['rewired']}")
        if result['pattern_matched']:
            print(f"PATTERN:  {result['pattern_matched']}")
        print()
    
    print("=" * 60)
    print(rewirer.get_rewiring_summary())
