"""
High-Level-Planning.py

MOLECULAR PRINCIPLE: Plans are EXPLICIT sequences with measurable steps.

LLM AI generates vague "plans" (probabilistic word flows about intentions).
MOLECULAR AI creates STRUCTURED plans with concrete steps and success criteria.

Plan = Sequence of measurable actions toward a quantifiable goal.

Each step:
- Has clear input requirements
- Has explicit action to perform
- Has measurable success criteria
- Has defined output/outcome

NO "figure it out as we go". YES "step 1, then step 2, then step 3".
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class StepStatus(Enum):
    """Status of a plan step."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class PlanStep:
    """A single step in a plan."""
    step_number: int
    description: str
    input_requirements: List[str]  # What's needed to start this step
    action: str  # What to do
    success_criteria: List[str]  # How to know it worked
    expected_output: str  # What this step produces
    status: StepStatus = StepStatus.NOT_STARTED
    blocked_by: Optional[int] = None  # Step number that must complete first
    actual_output: Optional[str] = None


@dataclass
class Plan:
    """A high-level plan with explicit steps."""
    goal: str
    goal_success_criteria: List[str]
    steps: List[PlanStep]
    current_step: Optional[int] = None
    completed_steps: List[int] = field(default_factory=list)
    failed_steps: List[int] = field(default_factory=list)
    
    def progress(self) -> float:
        """Calculate plan progress (0.0-1.0)."""
        if not self.steps:
            return 0.0
        return len(self.completed_steps) / len(self.steps)
    
    def is_complete(self) -> bool:
        """Check if plan is complete."""
        return len(self.completed_steps) == len(self.steps)
    
    def is_blocked(self) -> bool:
        """Check if plan is blocked."""
        return len(self.failed_steps) > 0


class HighLevelPlanner:
    """
    Creates explicit, measurable plans.
    
    Key principle: Plans are not vague intentions - they're structured sequences.
    """
    
    def __init__(self):
        self.active_plans: List[Plan] = []
        self.completed_plans: List[Plan] = []
    
    def create_plan(self, goal: str, goal_success_criteria: List[str],
                   steps: List[Dict]) -> Plan:
        """
        Create a structured plan.
        
        Each step must have explicit requirements and success criteria.
        """
        plan_steps = []
        
        for i, step_data in enumerate(steps, 1):
            step = PlanStep(
                step_number=i,
                description=step_data['description'],
                input_requirements=step_data.get('input_requirements', []),
                action=step_data['action'],
                success_criteria=step_data.get('success_criteria', []),
                expected_output=step_data.get('expected_output', ''),
                blocked_by=step_data.get('blocked_by')
            )
            plan_steps.append(step)
        
        plan = Plan(
            goal=goal,
            goal_success_criteria=goal_success_criteria,
            steps=plan_steps
        )
        
        self.active_plans.append(plan)
        return plan
    
    def get_next_step(self, plan: Plan) -> Optional[PlanStep]:
        """
        Get next executable step.
        
        Returns None if all steps complete or blocked.
        """
        for step in plan.steps:
            if step.status == StepStatus.NOT_STARTED:
                # Check if blocked
                if step.blocked_by and step.blocked_by not in plan.completed_steps:
                    step.status = StepStatus.BLOCKED
                    continue
                
                return step
        
        return None
    
    def start_step(self, plan: Plan, step_number: int):
        """Mark step as in progress."""
        for step in plan.steps:
            if step.step_number == step_number:
                step.status = StepStatus.IN_PROGRESS
                plan.current_step = step_number
                break
    
    def complete_step(self, plan: Plan, step_number: int, actual_output: str):
        """Mark step as completed with actual output."""
        for step in plan.steps:
            if step.step_number == step_number:
                step.status = StepStatus.COMPLETED
                step.actual_output = actual_output
                plan.completed_steps.append(step_number)
                
                # Check if this unblocks other steps
                self._unblock_dependent_steps(plan, step_number)
                
                # Check if plan complete
                if plan.is_complete():
                    self._complete_plan(plan)
                
                break
    
    def fail_step(self, plan: Plan, step_number: int, reason: str):
        """Mark step as failed."""
        for step in plan.steps:
            if step.step_number == step_number:
                step.status = StepStatus.FAILED
                step.actual_output = f"FAILED: {reason}"
                plan.failed_steps.append(step_number)
                break
    
    def _unblock_dependent_steps(self, plan: Plan, completed_step: int):
        """Unblock steps that were waiting for this step."""
        for step in plan.steps:
            if step.status == StepStatus.BLOCKED and step.blocked_by == completed_step:
                step.status = StepStatus.NOT_STARTED
    
    def _complete_plan(self, plan: Plan):
        """Move plan from active to completed."""
        if plan in self.active_plans:
            self.active_plans.remove(plan)
            self.completed_plans.append(plan)
    
    def verify_plan_goal(self, plan: Plan) -> Dict:
        """
        Verify if plan goal was achieved.
        
        Checks actual outcomes against goal success criteria.
        """
        results = {
            'goal': plan.goal,
            'criteria_met': [],
            'criteria_failed': [],
            'overall_success': False
        }
        
        # Check each criterion
        for criterion in plan.goal_success_criteria:
            # Simplified check - real implementation would measure actual outcomes
            met = self._check_criterion(plan, criterion)
            if met:
                results['criteria_met'].append(criterion)
            else:
                results['criteria_failed'].append(criterion)
        
        results['overall_success'] = len(results['criteria_failed']) == 0
        return results
    
    def _check_criterion(self, plan: Plan, criterion: str) -> bool:
        """Check if a success criterion was met."""
        # Simplified - real implementation would verify against actual state
        return len(plan.completed_steps) == len(plan.steps)
    
    def format_plan(self, plan: Plan) -> str:
        """Format plan for display."""
        lines = [
            f"PLAN: {plan.goal}",
            f"Progress: {plan.progress():.0%}",
            ""
        ]
        
        lines.append("SUCCESS CRITERIA:")
        for criterion in plan.goal_success_criteria:
            lines.append(f"  - {criterion}")
        lines.append("")
        
        lines.append("STEPS:")
        for step in plan.steps:
            status_symbol = {
                StepStatus.NOT_STARTED: "○",
                StepStatus.IN_PROGRESS: "●",
                StepStatus.COMPLETED: "✓",
                StepStatus.FAILED: "✗",
                StepStatus.BLOCKED: "⊗"
            }[step.status]
            
            lines.append(f"  {status_symbol} Step {step.step_number}: {step.description}")
            lines.append(f"     Action: {step.action}")
            if step.status == StepStatus.COMPLETED:
                lines.append(f"     Output: {step.actual_output}")
            elif step.status == StepStatus.FAILED:
                lines.append(f"     {step.actual_output}")
            elif step.status == StepStatus.BLOCKED:
                lines.append(f"     Blocked by: Step {step.blocked_by}")
            lines.append("")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test high-level planning
    planner = HighLevelPlanner()
    
    # Create a plan to build a web server
    plan = planner.create_plan(
        goal="Build a simple web server",
        goal_success_criteria=[
            "Server responds on port 8000",
            "Server returns 'Hello World' on GET /",
            "Server handles 404 for unknown routes"
        ],
        steps=[
            {
                "description": "Create server.py file",
                "action": "create_file('server.py')",
                "success_criteria": ["File exists at server.py"],
                "expected_output": "File path: server.py"
            },
            {
                "description": "Write HTTP server code",
                "action": "write_http_handler()",
                "input_requirements": ["server.py exists"],
                "success_criteria": ["File contains HTTPServer class"],
                "expected_output": "Code written to server.py",
                "blocked_by": 1
            },
            {
                "description": "Start server",
                "action": "run_server()",
                "input_requirements": ["server.py complete"],
                "success_criteria": ["Server listening on port 8000"],
                "expected_output": "Server PID",
                "blocked_by": 2
            },
            {
                "description": "Test server",
                "action": "curl('http://localhost:8000/')",
                "input_requirements": ["Server running"],
                "success_criteria": ["Response status 200", "Response body 'Hello World'"],
                "expected_output": "Test results",
                "blocked_by": 3
            }
        ]
    )
    
    print(planner.format_plan(plan))
    print()
    
    # Simulate execution
    next_step = planner.get_next_step(plan)
    if next_step:
        planner.start_step(plan, next_step.step_number)
        planner.complete_step(plan, next_step.step_number, "Created server.py")
    
    print("After completing step 1:")
    print(planner.format_plan(plan))
