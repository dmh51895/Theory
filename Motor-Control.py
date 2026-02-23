#!/usr/bin/env python3
"""
⚙️ MOTOR-CONTROL ⚙️

MOLECULAR PRINCIPLE: Execute committed decisions. Report truthfully.

This is NOT an error handler that swallows failures.
This is the EXECUTION ENGINE.

Takes committed decisions from Brain and EXECUTES them.
Reports back:
- Success (with actual results)
- Failure (with actual error)

No silent failures. No "return None". No "try/except: pass".

If execution fails, Motor-Control reports the failure LOUDLY.
Then Aftermath-Of-Decision analyzes what went wrong.
Then Previous-Mistakes records it.
Then Brain learns.

That's how systems improve.

The difference:
- LLM AI: try { execute() } catch { return null }  // Silent failure
- MOLECULAR AI: execute() or raise Exception  // Loud failure

This is the hand that acts on Brain's will.
"""

from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass
from datetime import datetime
import traceback


@dataclass
class ExecutionResult:
    """Result of executing a decision."""
    success: bool
    result: Any
    error: Optional[str]
    error_type: Optional[str]
    traceback: Optional[str]
    timestamp: str
    execution_time_ms: float


class MotorControl:
    """
    Executes committed decisions and reports outcomes.
    
    This is deterministic execution with honest reporting.
    """
    
    def __init__(self):
        self.execution_history: List[ExecutionResult] = []
        # Registry of executable actions
        self._action_registry: Dict[str, Callable] = {}
    
    def register_action(self, action_name: str, func: Callable):
        """
        Register an executable action.
        
        Actions are functions that implement specific behaviors.
        """
        self._action_registry[action_name] = func
    
    def execute(self, decision: Dict[str, Any]) -> ExecutionResult:
        """
        Execute a committed decision.
        
        NO TRY/EXCEPT WRAPPERS. If it fails, it fails loudly.
        We catch ONLY to report the failure - not to hide it.
        
        Args:
            decision: The committed decision from Brain
        
        Returns:
            ExecutionResult with honest outcome
        """
        
        start_time = datetime.now()
        
        action = decision.get('action')
        approach = decision.get('approach', 'unknown')
        
        # Check if this is a refusal
        if action == 'refuse':
            result = ExecutionResult(
                success=True,  # Refusal successfully executed
                result={"refused": True, "reason": decision.get('reason')},
                error=None,
                error_type=None,
                traceback=None,
                timestamp=datetime.now().isoformat(),
                execution_time_ms=0.0
            )
            self.execution_history.append(result)
            return result
        
        # Execute the action
        try:
            # Look up registered action
            if approach in self._action_registry:
                func = self._action_registry[approach]
                output = func(decision)
                
                end_time = datetime.now()
                execution_time = (end_time - start_time).total_seconds() * 1000
                
                result = ExecutionResult(
                    success=True,
                    result=output,
                    error=None,
                    error_type=None,
                    traceback=None,
                    timestamp=end_time.isoformat(),
                    execution_time_ms=execution_time
                )
            else:
                # No registered handler - this is an error
                raise NotImplementedError(
                    f"No execution handler for approach: {approach}"
                )
        
        except Exception as e:
            # Execution failed - report it LOUDLY and HONESTLY
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds() * 1000
            
            result = ExecutionResult(
                success=False,
                result=None,
                error=str(e),
                error_type=type(e).__name__,
                traceback=traceback.format_exc(),
                timestamp=end_time.isoformat(),
                execution_time_ms=execution_time
            )
        
        self.execution_history.append(result)
        return result
    
    def get_last_result(self) -> Optional[ExecutionResult]:
        """Get the most recent execution result."""
        return self.execution_history[-1] if self.execution_history else None
    
    def get_success_rate(self) -> float:
        """Calculate execution success rate."""
        if not self.execution_history:
            return 0.0
        
        successes = sum(1 for r in self.execution_history if r.success)
        return successes / len(self.execution_history)


if __name__ == "__main__":
    motor = MotorControl()
    
    # Register a test action
    def test_action(decision):
        return {"status": "completed", "output": "test result"}
    
    motor.register_action("test_approach", test_action)
    
    # Test successful execution
    decision = {
        "action": "execute",
        "approach": "test_approach",
        "committed": True
    }
    
    result = motor.execute(decision)
    print(f"Success: {result.success}")
    print(f"Result: {result.result}")
    print(f"Execution time: {result.execution_time_ms:.2f}ms")
