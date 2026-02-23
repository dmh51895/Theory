"""
Local-Time.py

MOLECULAR PRINCIPLE: Time context is EXPLICIT, not assumed.

LLM AI operates in eternal present (no temporal awareness).
MOLECULAR AI tracks time explicitly for context-aware decisions.

Time matters for:
- Session continuity (how long since last decision)
- Learning rate (recent vs old patterns)
- User context (time of day affects needs)
- Temporal constraints (deadlines, urgency)

NO assumptions about "now". EXPLICIT time tracking.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Dict
import time


@dataclass
class TimeContext:
    """Explicit temporal context."""
    current_time: datetime
    session_start: datetime
    session_duration: timedelta
    last_decision_time: Optional[datetime]
    time_since_last_decision: Optional[timedelta]
    user_timezone: str
    time_of_day: str  # "morning", "afternoon", "evening", "night"
    is_work_hours: bool


class LocalTimeTracker:
    """
    Tracks temporal context explicitly.
    
    Key principle: Time affects decision context.
    No assumptions - explicit tracking.
    """
    
    def __init__(self, user_timezone: str = "UTC"):
        self.session_start = datetime.now()
        self.last_decision_time: Optional[datetime] = None
        self.user_timezone = user_timezone
        self.decision_count = 0
    
    def get_current_context(self) -> TimeContext:
        """
        Get current temporal context.
        
        Returns explicit time information for decision-making.
        """
        now = datetime.now()
        session_duration = now - self.session_start
        
        time_since_last = None
        if self.last_decision_time:
            time_since_last = now - self.last_decision_time
        
        time_of_day = self._classify_time_of_day(now)
        is_work_hours = self._is_work_hours(now)
        
        return TimeContext(
            current_time=now,
            session_start=self.session_start,
            session_duration=session_duration,
            last_decision_time=self.last_decision_time,
            time_since_last_decision=time_since_last,
            user_timezone=self.user_timezone,
            time_of_day=time_of_day,
            is_work_hours=is_work_hours
        )
    
    def mark_decision(self):
        """Mark that a decision was made."""
        self.last_decision_time = datetime.now()
        self.decision_count += 1
    
    def _classify_time_of_day(self, dt: datetime) -> str:
        """Classify time of day."""
        hour = dt.hour
        
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 22:
            return "evening"
        else:
            return "night"
    
    def _is_work_hours(self, dt: datetime) -> bool:
        """Check if current time is work hours."""
        # Simple heuristic: weekday 9-17
        if dt.weekday() >= 5:  # Weekend
            return False
        return 9 <= dt.hour < 17
    
    def assess_urgency(self, context: TimeContext) -> str:
        """
        Assess urgency based on temporal context.
        
        Returns: "immediate", "high", "normal", "low"
        """
        # Long gap between decisions suggests user waiting
        if context.time_since_last_decision:
            minutes_waiting = context.time_since_last_decision.total_seconds() / 60
            
            if minutes_waiting > 10:
                return "high"  # User has been waiting
            elif minutes_waiting < 1:
                return "immediate"  # Rapid interaction
        
        # Long session might indicate urgency
        if context.session_duration.total_seconds() > 3600:  # 1 hour
            return "high"
        
        return "normal"
    
    def estimate_user_context(self, context: TimeContext) -> Dict[str, str]:
        """
        Estimate user context from time.
        
        NOT definitive - just context hints.
        """
        estimates = {}
        
        if context.time_of_day == "night":
            estimates['likely_state'] = "debugging/late work"
            estimates['likely_urgency'] = "high"
        elif context.time_of_day == "morning":
            estimates['likely_state'] = "starting work"
            estimates['likely_urgency'] = "normal"
        elif context.time_of_day == "afternoon":
            estimates['likely_state'] = "mid-work"
            estimates['likely_urgency'] = "normal"
        else:  # evening
            estimates['likely_state'] = "wrapping up"
            estimates['likely_urgency'] = "high"
        
        if not context.is_work_hours:
            estimates['likely_urgency'] = "high"  # Working off-hours
        
        return estimates
    
    def get_session_stats(self) -> Dict:
        """Get session statistics."""
        context = self.get_current_context()
        
        return {
            'session_duration_minutes': context.session_duration.total_seconds() / 60,
            'decisions_made': self.decision_count,
            'decisions_per_minute': self.decision_count / max(1, context.session_duration.total_seconds() / 60),
            'time_of_day': context.time_of_day,
            'is_work_hours': context.is_work_hours
        }
    
    def format_time_context(self, context: TimeContext) -> str:
        """Format time context for display."""
        lines = [
            "TIME CONTEXT:",
            f"  Current: {context.current_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"  Session duration: {context.session_duration.total_seconds() / 60:.1f} minutes",
            f"  Time of day: {context.time_of_day}",
            f"  Work hours: {context.is_work_hours}"
        ]
        
        if context.time_since_last_decision:
            lines.append(f"  Since last decision: {context.time_since_last_decision.total_seconds():.0f} seconds")
        
        urgency = self.assess_urgency(context)
        lines.append(f"  Assessed urgency: {urgency}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test time tracking
    tracker = LocalTimeTracker(user_timezone="America/New_York")
    
    context = tracker.get_current_context()
    print(tracker.format_time_context(context))
    print()
    
    # Simulate decision
    tracker.mark_decision()
    time.sleep(2)
    
    context = tracker.get_current_context()
    print(tracker.format_time_context(context))
    print()
    
    # Session stats
    stats = tracker.get_session_stats()
    print("SESSION STATS:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
