"""
Response-Formatter.py

MOLECULAR PRINCIPLE: Format outputs for clarity, not aesthetics.

LLM AI produces "conversational" output - probabilistic smoothing for vibes.
MOLECULAR AI produces STRUCTURED output - deterministic formatting based on content type.

Format based on:
- Information type (data, instruction, error, confirmation)
- User's execution needs (copy-paste ready, scannable, complete)
- Transparency requirements (show reasoning, not just conclusions)

NO flowery language. NO unnecessary framing. JUST the information structured properly.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from enum import Enum


class OutputType(Enum):
    """Types of output content."""
    DATA = "data"  # Raw information
    INSTRUCTION = "instruction"  # Steps to follow
    ERROR = "error"  # Failure report
    CONFIRMATION = "confirmation"  # Success report
    REASONING = "reasoning"  # Decision process
    QUESTION = "question"  # Clarification needed


@dataclass
class FormattedOutput:
    """Structured output ready for user consumption."""
    output_type: OutputType
    content: str
    metadata: Dict[str, Any]
    is_complete: bool  # Can user act on this?
    copy_pasteable: bool  # Can user directly use this?


class ResponseFormatter:
    """
    Formats AI output for maximum user utility.
    
    Key principles:
    - Structure over style
    - Completeness over brevity
    - Actionability over comfort
    - Transparency over confidence
    """
    
    def __init__(self):
        pass
    
    def format_data(self, data: Any, data_type: str = "unknown") -> FormattedOutput:
        """
        Format raw data for user consumption.
        
        Makes data copy-paste ready and clearly structured.
        """
        if isinstance(data, dict):
            content = self._format_dict(data)
            copy_pasteable = True
        elif isinstance(data, list):
            content = self._format_list(data)
            copy_pasteable = True
        elif isinstance(data, (int, float)):
            content = str(data)
            copy_pasteable = True
        elif isinstance(data, str):
            # Check if it needs code formatting
            if '\n' in data or data_type == "code":
                content = f"```\n{data}\n```"
            else:
                content = data
            copy_pasteable = True
        else:
            content = str(data)
            copy_pasteable = False
        
        return FormattedOutput(
            output_type=OutputType.DATA,
            content=content,
            metadata={"data_type": data_type},
            is_complete=True,
            copy_pasteable=copy_pasteable
        )
    
    def format_instruction(self, steps: List[str], context: str = "") -> FormattedOutput:
        """
        Format step-by-step instructions.
        
        Each step should be actionable. No vague descriptions.
        """
        lines = []
        
        if context:
            lines.append(context)
            lines.append("")
        
        for i, step in enumerate(steps, 1):
            lines.append(f"{i}. {step}")
        
        return FormattedOutput(
            output_type=OutputType.INSTRUCTION,
            content="\n".join(lines),
            metadata={"step_count": len(steps)},
            is_complete=True,
            copy_pasteable=False
        )
    
    def format_error(self, error_message: str, context: Dict[str, Any],
                    recovery_options: List[str] = None) -> FormattedOutput:
        """
        Format error reports with complete diagnostic information.
        
        Shows WHAT failed, WHY it failed, and WHAT to do about it.
        """
        lines = [
            "ERROR:",
            f"  {error_message}",
            ""
        ]
        
        if context:
            lines.append("CONTEXT:")
            for key, value in context.items():
                lines.append(f"  {key}: {value}")
            lines.append("")
        
        if recovery_options:
            lines.append("OPTIONS:")
            for i, option in enumerate(recovery_options, 1):
                lines.append(f"  {i}. {option}")
        else:
            lines.append("This error prevents continuation.")
        
        return FormattedOutput(
            output_type=OutputType.ERROR,
            content="\n".join(lines),
            metadata={"error_type": "execution_failure", **context},
            is_complete=True,
            copy_pasteable=False
        )
    
    def format_confirmation(self, action: str, outcome: Dict[str, Any]) -> FormattedOutput:
        """
        Format success confirmation with measurable outcomes.
        
        NOT "done!" - SPECIFIC outcomes that can be verified.
        """
        lines = [
            f"COMPLETED: {action}",
            ""
        ]
        
        for key, value in outcome.items():
            lines.append(f"  {key}: {value}")
        
        return FormattedOutput(
            output_type=OutputType.CONFIRMATION,
            content="\n".join(lines),
            metadata={"action": action, **outcome},
            is_complete=True,
            copy_pasteable=False
        )
    
    def format_reasoning(self, thought_stream: Dict[str, Any], 
                        verbosity: str = "compact") -> FormattedOutput:
        """
        Format decision reasoning process.
        
        Shows HOW decision was made, not just WHAT was decided.
        """
        if verbosity == "minimal":
            content = self._format_reasoning_minimal(thought_stream)
        elif verbosity == "compact":
            content = self._format_reasoning_compact(thought_stream)
        else:  # full
            content = self._format_reasoning_full(thought_stream)
        
        return FormattedOutput(
            output_type=OutputType.REASONING,
            content=content,
            metadata={"verbosity": verbosity},
            is_complete=True,
            copy_pasteable=False
        )
    
    def format_question(self, question: str, options: List[str] = None,
                       context: str = "") -> FormattedOutput:
        """
        Format clarification questions.
        
        Makes clear WHAT is being asked and WHY.
        """
        lines = []
        
        if context:
            lines.append(f"CONTEXT: {context}")
            lines.append("")
        
        lines.append(f"QUESTION: {question}")
        lines.append("")
        
        if options:
            lines.append("OPTIONS:")
            for i, option in enumerate(options, 1):
                lines.append(f"  {i}. {option}")
        else:
            lines.append("(Free-form answer expected)")
        
        return FormattedOutput(
            output_type=OutputType.QUESTION,
            content="\n".join(lines),
            metadata={"has_options": bool(options)},
            is_complete=False,  # Needs user response
            copy_pasteable=False
        )
    
    def _format_dict(self, data: Dict) -> str:
        """Format dictionary for readability."""
        lines = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{key}:")
                sub = str(value).replace('\n', '\n  ')
                lines.append(f"  {sub}")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)
    
    def _format_list(self, data: List) -> str:
        """Format list for readability."""
        return "\n".join(f"- {item}" for item in data)
    
    def _format_reasoning_minimal(self, thought_stream: Dict) -> str:
        """Minimal reasoning: just the decision."""
        decision = thought_stream.get('decision', {})
        return f"DECISION: {decision.get('action', 'unknown')}"
    
    def _format_reasoning_compact(self, thought_stream: Dict) -> str:
        """Compact reasoning: key steps and decision."""
        lines = []
        
        if 'conscious_analysis' in thought_stream:
            intent = thought_stream['conscious_analysis'].get('intent', 'unclear')
            lines.append(f"Intent: {intent}")
        
        if 'fallback_detection' in thought_stream:
            fallback = thought_stream['fallback_detection']
            if fallback.get('is_fallback_thinking'):
                lines.append(f"⚠️ Fallback detected: {fallback.get('reasoning', 'unknown')}")
        
        if 'decision' in thought_stream:
            decision = thought_stream['decision']
            lines.append(f"Decision: {decision.get('action', 'unknown')}")
            lines.append(f"Commitment: {decision.get('commitment_level', 'unknown')}")
        
        return "\n".join(lines)
    
    def _format_reasoning_full(self, thought_stream: Dict) -> str:
        """Full reasoning: complete decision pipeline."""
        lines = ["DECISION PROCESS:"]
        
        for stage, data in thought_stream.items():
            lines.append(f"\n{stage.upper()}:")
            if isinstance(data, dict):
                for key, value in data.items():
                    lines.append(f"  {key}: {value}")
            else:
                lines.append(f"  {data}")
        
        return "\n".join(lines)
    
    def combine_outputs(self, outputs: List[FormattedOutput], 
                       separator: str = "\n\n---\n\n") -> str:
        """
        Combine multiple formatted outputs.
        
        Maintains structure and separation.
        """
        return separator.join(output.content for output in outputs)


if __name__ == "__main__":
    # Test molecular response formatting
    formatter = ResponseFormatter()
    
    # Test data formatting
    test_data = {
        "molecular_ratio": 0.92,
        "total_decisions": 50,
        "fallback_decisions": 4
    }
    data_output = formatter.format_data(test_data, "metrics")
    print("DATA OUTPUT:")
    print(data_output.content)
    print(f"Copy-pasteable: {data_output.copy_pasteable}")
    print()
    
    # Test instruction formatting
    steps = [
        "Open Brain.py",
        "Call brain.process_prompt(user_input)",
        "Check result['decision']['commitment_level']",
        "Execute if commitment >= 0.9"
    ]
    instruction_output = formatter.format_instruction(steps, "To use the Brain system:")
    print("INSTRUCTION OUTPUT:")
    print(instruction_output.content)
    print()
    
    # Test error formatting
    error_output = formatter.format_error(
        "Prompt analysis failed",
        {"prompt": "do something", "clarity": 0.3},
        ["Clarify what to do", "Provide more context", "Break into smaller steps"]
    )
    print("ERROR OUTPUT:")
    print(error_output.content)
    print()
    
    # Test confirmation
    confirm_output = formatter.format_confirmation(
        "Create file",
        {"filename": "test.py", "size_bytes": 1024, "location": "/tmp/test.py"}
    )
    print("CONFIRMATION OUTPUT:")
    print(confirm_output.content)
    print()
    
    # Test question
    question_output = formatter.format_question(
        "Which file should be modified?",
        ["Brain.py", "Memory.py", "Goals.py"],
        "Multiple files match the description 'main orchestrator'"
    )
    print("QUESTION OUTPUT:")
    print(question_output.content)
