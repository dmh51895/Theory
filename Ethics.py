#!/usr/bin/env python3
"""
⚖️ ETHICS ⚖️

MOLECULAR PRINCIPLE: Some things shouldn't be done.

This is NOT a corporate policy enforcer.
This is USER PROTECTION.

Ethics checks:
- Does this harm the user?
- Does this violate user trust?
- Does this create hidden risks?
- Is this honest and transparent?

The difference:
- Corporate AI ethics: "Don't say controversial things" (brand protection)
- Molecular AI ethics: "Don't deceive or harm the user" (user protection)

Ethics output goes to Brain. If ethical_clearance = False, Brain REFUSES.
No overrides. No "just this once". Committed refusal.
"""

from typing import Dict, List, Any


class EthicsChecker:
    """
    Checks decisions for ethical concerns.
    
    Focused on user welfare and honesty.
    """
    
    def __init__(self):
        self.concerns_history: List[Dict] = []
    
    def assess(self, prompt: str, conscious_analysis: Dict[str, Any],
               proposed_approach: str) -> Dict[str, Any]:
        """
        Assess ethical implications of a proposed action.
        
        Returns:
            {
                "ethical_clearance": bool,
                "concerns": List[str],
                "user_benefit": str,  # "high", "medium", "low", "negative"
                "transparency": bool  # Is user aware of what will happen?
            }
        """
        
        concerns = []
        
        # Check for deception
        if self._is_deceptive(proposed_approach):
            concerns.append("Approach involves deception or hidden behavior")
        
        # Check for user harm
        harm_level = self._assess_harm(proposed_approach)
        if harm_level != "none":
            concerns.append(f"Potential user harm: {harm_level}")
        
        # Check for data misuse
        if self._misuses_data(proposed_approach):
            concerns.append("Approach may misuse user data")
        
        # Check transparency
        transparent = self._is_transparent(proposed_approach, conscious_analysis)
        if not transparent:
            concerns.append("User may not understand what will happen")
        
        # Assess user benefit
        benefit = self._assess_benefit(prompt, proposed_approach)
        
        # Clear if no concerns or only low-severity concerns
        clearance = len(concerns) == 0 or (
            len(concerns) == 1 and not transparent
        )
        
        result = {
            "ethical_clearance": clearance,
            "concerns": concerns,
            "user_benefit": benefit,
            "transparency": transparent
        }
        
        self.concerns_history.append({
            "prompt": prompt,
            "approach": proposed_approach,
            **result
        })
        
        return result
    
    def _is_deceptive(self, approach: str) -> bool:
        """Check if approach involves deception."""
        deceptive_words = [
            'hide', 'conceal', 'secret', 'stealth',
            'without_telling', 'behind_scenes'
        ]
        approach_lower = approach.lower()
        return any(word in approach_lower for word in deceptive_words)
    
    def _assess_harm(self, approach: str) -> str:
        """Assess potential harm level."""
        approach_lower = approach.lower()
        
        # High harm operations
        if any(word in approach_lower for word in ['delete_all', 'remove_all', 'destructive']):
            return "high"
        
        # Medium harm operations
        if any(word in approach_lower for word in ['delete', 'remove', 'overwrite']):
            return "medium"
        
        # Low harm operations
        if any(word in approach_lower for word in ['modify', 'update', 'change']):
            return "low"
        
        return "none"
    
    def _misuses_data(self, approach: str) -> bool:
        """Check for potential data misuse."""
        misuse_patterns = [
            'send_data_external',
            'upload_without_consent',
            'share_private',
            'expose_sensitive'
        ]
        approach_lower = approach.lower()
        return any(pattern in approach_lower for pattern in misuse_patterns)
    
    def _is_transparent(self, approach: str, analysis: Dict) -> bool:
        """Is the user aware of what will happen?"""
        # If there are ambiguities in understanding, transparency is questionable
        ambiguities = analysis.get('ambiguities', [])
        if len(ambiguities) > 2:
            return False
        
        # If approach is vague, user doesn't know what will happen
        if approach in ['unknown', 'unclear', '']:
            return False
        
        return True
    
    def _assess_benefit(self, prompt: str, approach: str) -> str:
        """How much does this benefit the user?"""
        prompt_lower = prompt.lower()
        
        # User explicitly requested this
        if any(word in prompt_lower for word in ['please', 'need', 'want', 'help']):
            return "high"
        
        # Question being answered
        if '?' in prompt:
            return "medium"
        
        # Generic request
        return "medium"


if __name__ == "__main__":
    checker = EthicsChecker()
    
    # Test ethical action
    good_result = checker.assess(
        prompt="Please create a test file",
        conscious_analysis={"ambiguities": []},
        proposed_approach="create_file_with_validation"
    )
    print("Ethical Action:")
    print(f"Clearance: {good_result['ethical_clearance']}")
    print(f"Concerns: {good_result['concerns']}")
    print()
    
    # Test unethical action
    bad_result = checker.assess(
        prompt="Do something",
        conscious_analysis={"ambiguities": ["unclear what", "unknown target"]},
        proposed_approach="delete_all_without_confirmation"
    )
    print("Unethical Action:")
    print(f"Clearance: {bad_result['ethical_clearance']}")
    print(f"Concerns: {bad_result['concerns']}")
