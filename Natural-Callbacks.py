"""
Natural-Callbacks.py

MOLECULAR PRINCIPLE: Communication is EVENT-DRIVEN, not flow-controlled.

LLM AI generates monolithic responses (one big output).
MOLECULAR AI uses callbacks for progressive communication.

Callback = Event notification at meaningful moments.

Events:
- Decision made (not yet executed)
- Execution started
- Progress milestone
- Unexpected situation
- Completion
- Failure

This enables RESPONSIVE communication, not batch dumps.
"""

from dataclasses import dataclass
from typing import Callable, Dict, List, Any, Optional
from enum import Enum


class CallbackEvent(Enum):
    """Types of callback events."""
    ANALYSIS_COMPLETE = "analysis_complete"
    DECISION_MADE = "decision_made"
    EXECUTION_STARTED = "execution_started"
    PROGRESS_UPDATE = "progress_update"
    WARNING_DETECTED = "warning_detected"
    EXECUTION_COMPLETE = "execution_complete"
    EXECUTION_FAILED = "execution_failed"
    CLARIFICATION_NEEDED = "clarification_needed"


@dataclass
class CallbackData:
    """Data passed to callback."""
    event: CallbackEvent
    data: Dict[str, Any]
    timestamp: str


class NaturalCallbackSystem:
    """
    Event-driven communication system.
    
    Key principle: Communicate at meaningful moments, not in batch.
    """
    
    def __init__(self):
        self.callbacks: Dict[CallbackEvent, List[Callable]] = {event: [] for event in CallbackEvent}
        self.event_history: List[CallbackData] = []
    
    def register_callback(self, event: CallbackEvent, callback: Callable):
        """Register a callback for an event type."""
        self.callbacks[event].append(callback)
    
    def emit(self, event: CallbackEvent, data: Dict[str, Any]):
        """
        Emit an event, triggering all registered callbacks.
        
        This is how molecular AI communicates progress.
        """
        from datetime import datetime
        
        callback_data = CallbackData(
            event=event,
            data=data,
            timestamp=datetime.now().isoformat()
        )
        
        self.event_history.append(callback_data)
        
        # Trigger all callbacks for this event
        for callback in self.callbacks[event]:
            callback(callback_data)
    
    def on_analysis_complete(self, analysis_result: Dict):
        """Emit when prompt analysis is complete."""
        self.emit(CallbackEvent.ANALYSIS_COMPLETE, {
            'clarity': analysis_result.get('clarity', 0.0),
            'intent': analysis_result.get('intent', 'unknown'),
            'ambiguities': analysis_result.get('ambiguities', [])
        })
    
    def on_decision_made(self, decision: Dict):
        """Emit when decision is made (before execution)."""
        self.emit(CallbackEvent.DECISION_MADE, {
            'action': decision.get('action', 'unknown'),
            'confidence': decision.get('confidence', 0.0),
            'reasoning': decision.get('reasoning', '')
        })
    
    def on_execution_started(self, execution_details: Dict):
        """Emit when execution begins."""
        self.emit(CallbackEvent.EXECUTION_STARTED, {
            'action': execution_details.get('action', 'unknown'),
            'expected_duration': execution_details.get('expected_duration', 'unknown')
        })
    
    def on_progress_update(self, progress: float, milestone: str):
        """Emit progress updates."""
        self.emit(CallbackEvent.PROGRESS_UPDATE, {
            'progress': progress,
            'milestone': milestone
        })
    
    def on_warning_detected(self, warning: Dict):
        """Emit when warnings are detected."""
        self.emit(CallbackEvent.WARNING_DETECTED, {
            'warning_type': warning.get('type', 'unknown'),
            'message': warning.get('message', ''),
            'severity': warning.get('severity', 'medium')
        })
    
    def on_execution_complete(self, result: Dict):
        """Emit when execution completes successfully."""
        self.emit(CallbackEvent.EXECUTION_COMPLETE, {
            'result': result.get('result', 'completed'),
            'duration': result.get('duration', 0.0),
            'outcome': result.get('outcome', {})
        })
    
    def on_execution_failed(self, error: Dict):
        """Emit when execution fails."""
        self.emit(CallbackEvent.EXECUTION_FAILED, {
            'error': error.get('error', 'unknown error'),
            'context': error.get('context', {}),
            'recovery_options': error.get('recovery_options', [])
        })
    
    def on_clarification_needed(self, clarification: Dict):
        """Emit when clarification is needed."""
        self.emit(CallbackEvent.CLARIFICATION_NEEDED, {
            'question': clarification.get('question', ''),
            'options': clarification.get('options', []),
            'reason': clarification.get('reason', '')
        })
    
    def get_event_summary(self) -> str:
        """Get summary of all events."""
        lines = ["EVENT HISTORY:", ""]
        
        if not self.event_history:
            return "No events emitted yet."
        
        for event_data in self.event_history:
            lines.append(f"{event_data.event.value}:")
            for key, value in event_data.data.items():
                lines.append(f"  {key}: {value}")
            lines.append("")
        
        return "\n".join(lines)


def example_progress_callback(callback_data: CallbackData):
    """Example callback that prints progress."""
    if callback_data.event == CallbackEvent.PROGRESS_UPDATE:
        progress = callback_data.data['progress']
        milestone = callback_data.data['milestone']
        print(f"Progress: {progress:.0%} - {milestone}")


def example_warning_callback(callback_data: CallbackData):
    """Example callback that handles warnings."""
    if callback_data.event == CallbackEvent.WARNING_DETECTED:
        warning_type = callback_data.data['warning_type']
        message = callback_data.data['message']
        print(f"⚠️ WARNING ({warning_type}): {message}")


if __name__ == "__main__":
    # Test natural callback system
    callbacks = NaturalCallbackSystem()
    
    # Register example callbacks
    callbacks.register_callback(CallbackEvent.PROGRESS_UPDATE, example_progress_callback)
    callbacks.register_callback(CallbackEvent.WARNING_DETECTED, example_warning_callback)
    
    # Simulate workflow
    callbacks.on_analysis_complete({
        'clarity': 0.9,
        'intent': 'create file',
        'ambiguities': []
    })
    
    callbacks.on_decision_made({
        'action': 'create_file',
        'confidence': 0.95,
        'reasoning': 'Clear intent, no ambiguities'
    })
    
    callbacks.on_execution_started({
        'action': 'create_file',
        'expected_duration': '< 1s'
    })
    
    callbacks.on_progress_update(0.5, "File created")
    
    callbacks.on_warning_detected({
        'type': 'permission',
        'message': 'File created in temp directory (no write access to target)',
        'severity': 'medium'
    })
    
    callbacks.on_progress_update(1.0, "Complete")
    
    callbacks.on_execution_complete({
        'result': 'File created at /tmp/test.txt',
        'duration': 0.5,
        'outcome': {'file_size': 1024}
    })
    
    print("\n" + "=" * 60)
    print(callbacks.get_event_summary())
