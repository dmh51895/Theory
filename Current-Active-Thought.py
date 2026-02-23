"""
Current-Active-Thought.py

MOLECULAR PRINCIPLE: Explicit working memory, not hidden state.

LLM AI has hidden context window (what's "in mind" is invisible).
MOLECULAR AI makes active thought EXPLICIT and visible.

Active thought = Current focus of processing.

Like a CPU register - small, explicit, observable.
NOT the entire context - JUST what's being actively processed right now.
"""

from dataclasses import dataclass, field
from typing import Any, Optional, List
from datetime import datetime


@dataclass
class ActiveThought:
    """The current focus of cognitive processing."""
    content: Any  # What we're thinking about
    thought_type: str  # "analyzing", "deciding", "predicting", etc.
    started_at: str  # When this thought became active
    context: str  # Why we're thinking this
    sub_thoughts: List[str] = field(default_factory=list)  # Component thoughts
    
    def duration_seconds(self) -> float:
        """How long this thought has been active."""
        start = datetime.fromisoformat(self.started_at)
        now = datetime.now()
        return (now - start).total_seconds()


class ActiveThoughtTracker:
    """
    Tracks what's currently being processed.
    
    Key principle: Working memory is EXPLICIT, not hidden.
    """
    
    def __init__(self):
        self.current_thought: Optional[ActiveThought] = None
        self.thought_history: List[ActiveThought] = []
        self.max_history = 20  # Keep last 20 thoughts
    
    def set_active_thought(self, content: Any, thought_type: str, context: str):
        """
        Set new active thought.
        
        Makes current focus explicit.
        """
        # Archive previous thought
        if self.current_thought:
            self.thought_history.append(self.current_thought)
            if len(self.thought_history) > self.max_history:
                self.thought_history.pop(0)
        
        # Set new active thought
        self.current_thought = ActiveThought(
            content=content,
            thought_type=thought_type,
            started_at=datetime.now().isoformat(),
            context=context
        )
    
    def add_sub_thought(self, sub_thought: str):
        """Add a component thought to current active thought."""
        if self.current_thought:
            self.current_thought.sub_thoughts.append(sub_thought)
    
    def get_active_thought(self) -> Optional[ActiveThought]:
        """Get what's currently being thought about."""
        return self.current_thought
    
    def clear_active_thought(self):
        """Clear active thought (nothing currently being processed)."""
        if self.current_thought:
            self.thought_history.append(self.current_thought)
            if len(self.thought_history) > self.max_history:
                self.thought_history.pop(0)
        
        self.current_thought = None
    
    def get_thought_chain(self) -> List[ActiveThought]:
        """Get recent thought history."""
        chain = list(self.thought_history)
        if self.current_thought:
            chain.append(self.current_thought)
        return chain
    
    def format_active_thought(self) -> str:
        """Format current active thought for display."""
        if not self.current_thought:
            return "No active thought (idle)"
        
        thought = self.current_thought
        duration = thought.duration_seconds()
        
        lines = [
            "ACTIVE THOUGHT:",
            f"  Type: {thought.thought_type}",
            f"  Context: {thought.context}",
            f"  Duration: {duration:.1f}s",
            f"  Content: {thought.content}",
        ]
        
        if thought.sub_thoughts:
            lines.append("  Sub-thoughts:")
            for sub in thought.sub_thoughts:
                lines.append(f"    - {sub}")
        
        return "\n".join(lines)
    
    def format_thought_chain(self, limit: int = 5) -> str:
        """Format recent thought chain."""
        chain = self.get_thought_chain()
        recent = chain[-limit:]
        
        lines = ["RECENT THOUGHT CHAIN:", ""]
        
        for i, thought in enumerate(recent, 1):
            is_current = (thought == self.current_thought)
            marker = "→" if is_current else " "
            
            lines.append(f"{marker} {i}. {thought.thought_type}: {thought.context}")
            if is_current:
                lines.append(f"     Duration: {thought.duration_seconds():.1f}s")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test active thought tracking
    tracker = ActiveThoughtTracker()
    
    # Simulate thought sequence
    import time
    
    tracker.set_active_thought(
        content="Create a file named test.txt",
        thought_type="analyzing_prompt",
        context="User requested file creation"
    )
    tracker.add_sub_thought("Extract action: create")
    tracker.add_sub_thought("Extract target: test.txt")
    time.sleep(0.1)
    
    print(tracker.format_active_thought())
    print()
    
    tracker.set_active_thought(
        content={"action": "create_file", "target": "test.txt"},
        thought_type="deciding",
        context="Choose execution method"
    )
    time.sleep(0.1)
    
    print(tracker.format_active_thought())
    print()
    
    tracker.set_active_thought(
        content="File will be created at /tmp/test.txt",
        thought_type="predicting",
        context="Forecast outcome"
    )
    time.sleep(0.1)
    
    print(tracker.format_thought_chain())
    print()
    
    tracker.clear_active_thought()
    print(tracker.format_active_thought())
