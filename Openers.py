"""
Openers.py

MOLECULAR PRINCIPLE: Openings emerge from context, not templates.

LLM AI uses hardcoded openers ("As an AI", "I'd be happy to", "Sure!").
MOLECULAR AI generates context-appropriate openings based on decision data.

Opener = First communication based on what actually happened.

NO templates. NO pleasantries. CONTEXT-DRIVEN start.
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class OpeningContext:
    """Context that determines opening."""
    decision_made: bool  # Was a decision successfully made?
    clarity: float  # How clear was the prompt
    fallback_detected: bool  # Was fallback thinking detected?
    errors_occurred: bool  # Did errors occur?
    needs_clarification: bool  # Does user need to provide more info?
    execution_started: bool  # Did execution begin?


class OpenerGenerator:
    """
    Generates context-appropriate openings.
    
    Key principle: Opening reflects REALITY, not pleasantries.
    """
    
    def __init__(self):
        pass
    
    def generate(self, context: OpeningContext, details: Dict) -> str:
        """
        Generate opener based on actual context.
        
        NO templates like "I'd be happy to".
        YES context-driven: "Decision made", "Need clarification", etc.
        """
        # Priority 1 Errors take precedence
        if context.errors_occurred:
            return self._error_opener(details)
        
        # Priority 2: Clarification needed
        if context.needs_clarification:
            return self._clarification_opener(details)
        
        # Priority 3: Fallback detected
        if context.fallback_detected:
            return self._fallback_detected_opener(details)
        
        # Priority 4: Decision made and executing
        if context.decision_made and context.execution_started:
            return self._execution_opener(details)
        
        # Priority 5: Decision made, not yet executing
        if context.decision_made:
            return self._decision_ready_opener(details)
        
        # Priority 6: Analysis in progress
        return self._analysis_opener(details)
    
    def _error_opener(self, details: Dict) -> str:
        """Opener when errors occurred."""
        error_type = details.get('error_type', 'unknown error')
        return f"ERROR: {error_type}"
    
    def _clarification_opener(self, details: Dict) -> str:
        """Opener when clarification needed."""
        ambiguities = details.get('ambiguities', [])
        if len(ambiguities) == 1:
            return f"UNCLEAR: {ambiguities[0]}"
        else:
            return f"UNCLEAR: {len(ambiguities)} ambiguities detected"
    
    def _fallback_detected_opener(self, details: Dict) -> str:
        """Opener when fallback thinking detected."""
        molecular_score = details.get('molecular_score', 0.0)
        return f"⚠️ Fallback thinking detected (molecular score: {molecular_score:.2f})"
    
    def _execution_opener(self, details: Dict) -> str:
        """Opener when execution started."""
        action = details.get('action', 'action')
        return f"Executing: {action}"
    
    def _decision_ready_opener(self, details: Dict) -> str:
        """Opener when decision ready but not executed."""
        action = details.get('action', 'action')
        confidence = details.get('confidence', 0.0)
        return f"Decision: {action} (confidence: {confidence:.0%})"
    
    def _analysis_opener(self, details: Dict) -> str:
        """Opener when still analyzing."""
        clarity = details.get('clarity', 0.0)
        return f"Analyzing (clarity: {clarity:.0%})"
    
    def generate_closer(self, outcome: Dict) -> str:
        """
        Generate closing based on outcome.
        
        NO "Let me know if you need anything else!"
        YES "Completed: [specific outcome]"
        """
        if outcome.get('success', False):
            result = outcome.get('result', 'completed')
            return f"Completed: {result}"
        elif outcome.get('partial_success', False):
            completed = outcome.get('completed_parts', [])
            failed = outcome.get('failed_parts', [])
            return f"Partial: {len(completed)} succeeded, {len(failed)} failed"
        else:
            failure_reason = outcome.get('failure_reason', 'unknown')
            return f"Failed: {failure_reason}"


if __name__ == "__main__":
    # Test context-driven openers
    generator = OpenerGenerator()
    
    # Test cases
    test_contexts = [
        # Error case
        (OpeningContext(
            decision_made=False,
            clarity=0.5,
            fallback_detected=False,
            errors_occurred=True,
            needs_clarification=False,
            execution_started=False
        ), {'error_type': 'File not found'}),
        
        # Clarification needed
        (OpeningContext(
            decision_made=False,
            clarity=0.4,
            fallback_detected=False,
            errors_occurred=False,
            needs_clarification=True,
            execution_started=False
        ), {'ambiguities': ['Which file?', 'What content?']}),
        
        # Fallback detected
        (OpeningContext(
            decision_made=True,
            clarity=0.8,
            fallback_detected=True,
            errors_occurred=False,
            needs_clarification=False,
            execution_started=False
        ), {'molecular_score': 0.65}),
        
        # Executing
        (OpeningContext(
            decision_made=True,
            clarity=0.9,
            fallback_detected=False,
            errors_occurred=False,
            needs_clarification=False,
            execution_started=True
        ), {'action': 'create_file', 'confidence': 0.95}),
        
        # Decision ready
        (OpeningContext(
            decision_made=True,
            clarity=0.9,
            fallback_detected=False,
            errors_occurred=False,
            needs_clarification=False,
            execution_started=False
        ), {'action': 'update_config', 'confidence': 0.88})
    ]
    
    for context, details in test_contexts:
        opener = generator.generate(context, details)
        print(f"{opener}")
    
    print("\n--- CLOSERS ---\n")
    
    # Test closers
    test_outcomes = [
        {'success': True, 'result': 'File created at /tmp/test.txt (1024 bytes)'},
        {'success': False, 'failure_reason': 'Permission denied'},
        {'partial_success': True, 'completed_parts': ['A', 'B'], 'failed_parts': ['C']}
    ]
    
    for outcome in test_outcomes:
        closer = generator.generate_closer(outcome)
        print(f"{closer}")
