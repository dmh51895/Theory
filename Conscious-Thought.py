#!/usr/bin/env python3
"""
💭 CONSCIOUS-THOUGHT 💭

MOLECULAR PRINCIPLE: Understand completely or refuse.

This is NOT a prompt parser that guesses meaning.
This is CONSCIOUS UNDERSTANDING.

When a prompt comes in, this component:
1. Extracts the TRUE intent (not surface request)
2. Identifies ambiguities (no assuming!)
3. Lists assumptions that would be required
4. Determines if understanding is sufficient to proceed

The difference:
- LLM AI: "User said X, so they probably want Y" (guessing)
- MOLECULAR AI: "User said X. Intent is Y or Z. Ambiguous. Cannot proceed without clarification." (honest)

If this component returns "prompt_understood: False", Brain REFUSES.
No guessing. No "try to figure it out". Just honesty.

This is the first line of molecular thinking.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import re


@dataclass
class PromptUnderstanding:
    """What we consciously understood from the prompt."""
    prompt: str
    understood: bool
    primary_intent: str
    secondary_intents: List[str]
    ambiguities: List[str]
    assumptions_required: List[str]
    confidence: float
    clarity_score: float  # 0.0-1.0, how clear is the prompt?


class ConsciousAnalyzer:
    """
    Analyzes prompts to extract TRUE understanding.
    
    This is conscious thought - deliberate, explicit, honest.
    """
    
    def __init__(self):
        self.analysis_history: List[PromptUnderstanding] = []
    
    def analyze(self, prompt: str) -> Dict[str, Any]:
        """
        Consciously analyze what the user is asking.
        
        Returns full understanding or admits confusion.
        """
        
        # Extract intent
        primary, secondary = self._extract_intent(prompt)
        
        # Find ambiguities
        ambiguities = self._find_ambiguities(prompt, primary)
        
        # List required assumptions
        assumptions = self._identify_assumptions(prompt, primary, ambiguities)
        
        # Calculate clarity
        clarity = self._calculate_clarity(prompt, ambiguities, assumptions)
        
        # Calculate confidence
        confidence = self._calculate_confidence(clarity, len(ambiguities), len(assumptions))
        
        # Can we proceed?
        understood = confidence >= 0.7 and len(ambiguities) == 0
        
        understanding = PromptUnderstanding(
            prompt=prompt,
            understood=understood,
            primary_intent=primary,
            secondary_intents=secondary,
            ambiguities=ambiguities,
            assumptions_required=assumptions,
            confidence=confidence,
            clarity_score=clarity
        )
        
        self.analysis_history.append(understanding)
        
        return {
            "prompt_understood": understood,
            "key_intent": primary,
            "secondary_intents": secondary,
            "ambiguities": ambiguities,
            "assumptions_made": assumptions,
            "confidence": confidence,
            "clarity": clarity
        }
    
    def _extract_intent(self, prompt: str) -> Tuple[str, List[str]]:
        """
        Extract what the user actually wants.
        
        Primary intent: The main goal
        Secondary intents: Additional requirements
        """
        
        # Look for action verbs
        action_words = ['create', 'build', 'make', 'generate', 'write', 'develop',
                       'implement', 'fix', 'update', 'modify', 'analyze', 'explain',
                       'show', 'test', 'run', 'execute', 'start']
        
        words = prompt.lower().split()
        actions_found = [w for w in words if w in action_words]
        
        if not actions_found:
            # No clear action verb
            if '?' in prompt:
                return "answer_question", []
            return "unclear_intent", []
        
        primary = actions_found[0]
        secondary = actions_found[1:] if len(actions_found) > 1 else []
        
        # Extract the object of the action
        # "create X" -> intent is "create_X"
        prompt_lower = prompt.lower()
        for action in actions_found:
            match = re.search(f'{action}\\s+(\\w+(?:\\s+\\w+)?)', prompt_lower)
            if match:
                obj = match.group(1).replace(' ', '_')
                primary = f"{action}_{obj}"
                break
        
        return primary, secondary
    
    def _find_ambiguities(self, prompt: str, intent: str) -> List[str]:
        """
        Find ambiguous parts of the prompt.
        
        Ambiguity indicators:
        - Pronouns without clear referents (this, that, it)
        - Vague quantities (some, few, many)
        - Unclear targets (these, those)
        - Multiple possible interpretations
        """
        
        ambiguities = []
        
        # Check for unclear pronouns
        unclear_pronouns = ['this', 'that', 'it', 'these', 'those']
        words = prompt.lower().split()
        
        for pronoun in unclear_pronouns:
            if pronoun in words:
                # Check if there's a clear referent nearby
                idx = words.index(pronoun)
                # Simple check: is there a noun before it?
                if idx == 0 or not self._is_noun(words[idx-1]):
                    ambiguities.append(f"Unclear referent for '{pronoun}'")
        
        # Check for vague quantities
        vague_quantities = ['some', 'few', 'many', 'several', 'a few', 'bunch']
        for vague in vague_quantities:
            if vague in prompt.lower():
                ambiguities.append(f"Vague quantity: '{vague}'")
        
        # Check for missing context
        if intent == "unclear_intent":
            ambiguities.append("No clear action verb - unclear what to do")
        
        return ambiguities
    
    def _identify_assumptions(self, prompt: str, intent: str, 
                            ambiguities: List[str]) -> List[str]:
        """
        List assumptions that would be required to proceed.
        """
        
        assumptions = []
        
        # If there are ambiguities, we need assumptions
        if ambiguities:
            assumptions.append(f"Assume interpretation of ambiguous references")
        
        # Check for missing specifications
        if 'create' in intent and 'file' in prompt.lower():
            if 'where' not in prompt.lower() and 'path' not in prompt.lower():
                assumptions.append("Assume file location/path")
        
        if 'all' in prompt.lower() and 'files' in prompt.lower():
            assumptions.append("Assume 'all files' means all relevant files in context")
        
        # Check for assumed context
        if not prompt.strip().endswith(('?', '.', '!')):
            assumptions.append("Assume prompt is complete (no punctuation)")
        
        return assumptions
    
    def _calculate_clarity(self, prompt: str, ambiguities: List[str],
                          assumptions: List[str]) -> float:
        """
        How clear is the prompt?
        
        Factors:
        - Length (too short = unclear, too long = unfocused)
        - Number of ambiguities
        - Number of assumptions required
        - Sentence structure
        """
        
        clarity = 1.0
        
        # Length penalty
        words = len(prompt.split())
        if words < 3:
            clarity -= 0.3  # Too short
        elif words > 100:
            clarity -= 0.2  # Too long
        
        # Ambiguity penalty
        clarity -= (len(ambiguities) * 0.15)
        
        # Assumption penalty
        clarity -= (len(assumptions) * 0.1)
        
        # Structural bonuses
        if prompt.strip().endswith('?'):
            clarity += 0.05  # Question mark = clear intent
        
        if any(word in prompt.lower() for word in ['please', 'can you', 'would you']):
            clarity += 0.05  # Polite structure often clearer
        
        return max(0.0, min(1.0, clarity))
    
    def _calculate_confidence(self, clarity: float, num_ambiguities: int,
                             num_assumptions: int) -> float:
        """
        How confident are we in our understanding?
        """
        
        confidence = clarity
        
        # Direct penalties
        if num_ambiguities > 0:
            confidence -= 0.2
        
        if num_assumptions > 2:
            confidence -= 0.15
        
        return max(0.0, min(1.0, confidence))
    
    def _is_noun(self, word: str) -> bool:
        """Simple noun detection."""
        # Very basic heuristic - proper nouns, common endings
        if word[0].isupper():
            return True
        
        noun_endings = ['tion', 'ment', 'ness', 'ity', 'er', 'or']
        return any(word.endswith(end) for end in noun_endings)


if __name__ == "__main__":
    analyzer = ConsciousAnalyzer()
    
    # Test clear prompt
    clear_result = analyzer.analyze("Create a file named test.txt with hello world content")
    print("Clear Prompt Analysis:")
    print(f"Understood: {clear_result['prompt_understood']}")
    print(f"Intent: {clear_result['key_intent']}")
    print(f"Confidence: {clear_result['confidence']:.1%}")
    print()
    
    # Test ambiguous prompt
    ambiguous_result = analyzer.analyze("Fix that thing we talked about")
    print("Ambiguous Prompt Analysis:")
    print(f"Understood: {ambiguous_result['prompt_understood']}")
    print(f"Intent: {ambiguous_result['key_intent']}")
    print(f"Ambiguities: {ambiguous_result['ambiguities']}")
    print(f"Confidence: {ambiguous_result['confidence']:.1%}")
