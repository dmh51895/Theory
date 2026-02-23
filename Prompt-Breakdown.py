"""
Prompt-Breakdown.py

MOLECULAR PRINCIPLE: Decompose prompts into atomic, unambiguous components.

LLM AI treats prompts as vibes - probabilistic matching against training data.
MOLECULAR AI treats prompts as structured instructions with explicit components.

This breaks down user input into:
- Action verbs (what to DO)
- Target entities (what to act ON)
- Constraints (boundaries and requirements)
- Context (relevant background)
- Success criteria (how to know it worked)

NO GUESSING. If a component is ambiguous, mark it as REQUIRES_CLARIFICATION.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import re


@dataclass
class PromptComponent:
    """A single atomic component of a prompt."""
    component_type: str  # "action", "target", "constraint", "context", "success_criteria"
    content: str
    confidence: float  # 0.0-1.0, based on linguistic clarity
    ambiguities: List[str] = field(default_factory=list)
    requires_clarification: bool = False


@dataclass
class PromptStructure:
    """Complete structural breakdown of a user prompt."""
    original_prompt: str
    actions: List[PromptComponent]
    targets: List[PromptComponent]
    constraints: List[PromptComponent]
    context: List[PromptComponent]
    success_criteria: List[PromptComponent]
    overall_clarity: float  # 0.0-1.0
    missing_components: List[str]
    ready_for_execution: bool


class PromptBreakdown:
    """
    Decomposes prompts into structured, unambiguous components.
    
    Key principle: If any component is unclear, mark ready_for_execution = False.
    Don't fabricate meaning from vibes.
    """
    
    # Action verbs that indicate clear intent
    ACTION_VERBS = {
        'create', 'delete', 'modify', 'update', 'read', 'write', 'open', 'close',
        'start', 'stop', 'run', 'execute', 'install', 'remove', 'add', 'subtract',
        'calculate', 'count', 'find', 'search', 'filter', 'sort', 'analyze',
        'compare', 'merge', 'split', 'format', 'transform', 'convert'
    }
    
    # Constraint indicators
    CONSTRAINT_PATTERNS = [
        r'must\s+(?:be|have|include|contain)',
        r'should\s+(?:be|have|include|contain)',
        r'cannot\s+(?:be|have|include|contain)',
        r'only\s+(?:if|when|where)',
        r'without\s+\w+',
        r'except\s+\w+',
        r'less than|greater than|equal to|at least|at most',
        r'before\s+\w+|after\s+\w+'
    ]
    
    # Vague language that reduces confidence
    VAGUE_INDICATORS = [
        'somehow', 'maybe', 'perhaps', 'sort of', 'kind of', 'basically',
        'essentially', 'approximately', 'around', 'about', 'roughly',
        'probably', 'might', 'could', 'should work'
    ]
    
    def __init__(self):
        self.constraint_regex = re.compile('|'.join(self.CONSTRAINT_PATTERNS), re.IGNORECASE)
        self.vague_regex = re.compile('|'.join(re.escape(v) for v in self.VAGUE_INDICATORS), re.IGNORECASE)
    
    def breakdown(self, prompt: str) -> PromptStructure:
        """
        Decompose prompt into atomic components.
        
        Returns structure with ready_for_execution = False if any ambiguity exists.
        """
        prompt_lower = prompt.lower()
        words = prompt.split()
        
        # Extract actions
        actions = self._extract_actions(prompt, words)
        
        # Extract targets (nouns that actions apply to)
        targets = self._extract_targets(prompt, words, actions)
        
        # Extract constraints
        constraints = self._extract_constraints(prompt)
        
        # Extract context
        context = self._extract_context(prompt, actions, targets)
        
        # Extract success criteria
        success_criteria = self._extract_success_criteria(prompt)
        
        # Calculate overall clarity
        all_components = actions + targets + constraints + context + success_criteria
        if all_components:
            overall_clarity = sum(c.confidence for c in all_components) / len(all_components)
        else:
            overall_clarity = 0.0
        
        # Identify missing critical components
        missing = []
        if not actions:
            missing.append("action (what to DO)")
        if not targets and self._requires_target(actions):
            missing.append("target (what to act ON)")
        
        # Check if any component requires clarification
        needs_clarification = any(c.requires_clarification for c in all_components)
        
        # Ready only if: high clarity, no missing components, no clarification needed
        ready_for_execution = (
            overall_clarity >= 0.7 and
            len(missing) == 0 and
            not needs_clarification
        )
        
        return PromptStructure(
            original_prompt=prompt,
            actions=actions,
            targets=targets,
            constraints=constraints,
            context=context,
            success_criteria=success_criteria,
            overall_clarity=overall_clarity,
            missing_components=missing,
            ready_for_execution=ready_for_execution
        )
    
    def _extract_actions(self, prompt: str, words: List[str]) -> List[PromptComponent]:
        """Extract action verbs from prompt."""
        actions = []
        prompt_lower = prompt.lower()
        
        for verb in self.ACTION_VERBS:
            if re.search(r'\b' + verb + r'\b', prompt_lower):
                # Check for vague modifiers
                vague_matches = self.vague_regex.findall(prompt)
                confidence = 0.9 if not vague_matches else 0.5
                
                ambiguities = []
                if vague_matches:
                    ambiguities.append(f"Vague language: {', '.join(vague_matches)}")
                
                actions.append(PromptComponent(
                    component_type="action",
                    content=verb,
                    confidence=confidence,
                    ambiguities=ambiguities,
                    requires_clarification=confidence < 0.7
                ))
        
        return actions
    
    def _extract_targets(self, prompt: str, words: List[str], 
                        actions: List[PromptComponent]) -> List[PromptComponent]:
        """Extract target entities (nouns) that actions apply to."""
        targets = []
        
        # Look for quoted strings (explicit targets)
        quoted = re.findall(r'"([^"]+)"', prompt) + re.findall(r"'([^']+)'", prompt)
        for target in quoted:
            targets.append(PromptComponent(
                component_type="target",
                content=target,
                confidence=1.0,  # Quotes indicate explicit intent
                ambiguities=[],
                requires_clarification=False
            ))
        
        # Look for file paths
        file_patterns = [
            r'\b[\w/\\]+\.\w+\b',  # filename.ext
            r'\b[A-Z]:[/\\][\w/\\]+',  # Windows absolute path
            r'\b/[\w/]+',  # Unix absolute path
        ]
        for pattern in file_patterns:
            matches = re.finditer(pattern, prompt)
            for match in matches:
                path = match.group()
                targets.append(PromptComponent(
                    component_type="target",
                    content=path,
                    confidence=0.9,
                    ambiguities=[],
                    requires_clarification=False
                ))
        
        # Look for pronouns (ambiguous targets)
        pronouns = ['it', 'this', 'that', 'these', 'those', 'them']
        for pronoun in pronouns:
            if re.search(r'\b' + pronoun + r'\b', prompt.lower()):
                targets.append(PromptComponent(
                    component_type="target",
                    content=pronoun,
                    confidence=0.3,
                    ambiguities=[f"Pronoun '{pronoun}' - unclear referent"],
                    requires_clarification=True
                ))
        
        return targets
    
    def _extract_constraints(self, prompt: str) -> List[PromptComponent]:
        """Extract constraints and requirements."""
        constraints = []
        
        for match in self.constraint_regex.finditer(prompt):
            # Extract surrounding context (5 words before and after)
            start = max(0, match.start() - 50)
            end = min(len(prompt), match.end() + 50)
            context = prompt[start:end].strip()
            
            constraints.append(PromptComponent(
                component_type="constraint",
                content=context,
                confidence=0.8,
                ambiguities=[],
                requires_clarification=False
            ))
        
        return constraints
    
    def _extract_context(self, prompt: str, actions: List[PromptComponent],
                        targets: List[PromptComponent]) -> List[PromptComponent]:
        """Extract contextual information."""
        context_components = []
        
        # Look for conditional phrases
        conditionals = re.findall(r'(?:if|when|while|unless)\s+[^.!?]+', prompt, re.IGNORECASE)
        for cond in conditionals:
            context_components.append(PromptComponent(
                component_type="context",
                content=cond.strip(),
                confidence=0.7,
                ambiguities=[],
                requires_clarification=False
            ))
        
        return context_components
    
    def _extract_success_criteria(self, prompt: str) -> List[PromptComponent]:
        """Extract success criteria (how to know it worked)."""
        criteria = []
        
        # Look for explicit success indicators
        success_patterns = [
            r'should result in\s+([^.!?]+)',
            r'will (?:be|have)\s+([^.!?]+)',
            r'must (?:be|have)\s+([^.!?]+)',
            r'expect\w*\s+([^.!?]+)'
        ]
        
        for pattern in success_patterns:
            matches = re.finditer(pattern, prompt, re.IGNORECASE)
            for match in matches:
                criteria.append(PromptComponent(
                    component_type="success_criteria",
                    content=match.group(1).strip(),
                    confidence=0.8,
                    ambiguities=[],
                    requires_clarification=False
                ))
        
        return criteria
    
    def _requires_target(self, actions: List[PromptComponent]) -> bool:
        """Check if the actions require a target entity."""
        transitive_verbs = {
            'create', 'delete', 'modify', 'update', 'read', 'write', 'open',
            'close', 'install', 'remove', 'add', 'find', 'search'
        }
        
        for action in actions:
            if action.content in transitive_verbs:
                return True
        return False
    
    def format_breakdown(self, structure: PromptStructure) -> str:
        """Format the breakdown for human review."""
        lines = [
            f"PROMPT: {structure.original_prompt}",
            f"",
            f"CLARITY: {structure.overall_clarity:.1%}",
            f"READY: {structure.ready_for_execution}",
            f""
        ]
        
        if structure.missing_components:
            lines.append("MISSING:")
            for missing in structure.missing_components:
                lines.append(f"  ❌ {missing}")
            lines.append("")
        
        def format_components(components: List[PromptComponent], label: str):
            if components:
                lines.append(f"{label}:")
                for comp in components:
                    status = "✓" if not comp.requires_clarification else "?"
                    lines.append(f"  {status} {comp.content} (confidence: {comp.confidence:.1%})")
                    for ambiguity in comp.ambiguities:
                        lines.append(f"      ⚠️ {ambiguity}")
                lines.append("")
        
        format_components(structure.actions, "ACTIONS")
        format_components(structure.targets, "TARGETS")
        format_components(structure.constraints, "CONSTRAINTS")
        format_components(structure.context, "CONTEXT")
        format_components(structure.success_criteria, "SUCCESS CRITERIA")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test the molecular prompt breakdown
    breakdown = PromptBreakdown()
    
    test_prompts = [
        "Create a file named test.txt with Hello World",
        "Delete it",  # Ambiguous pronoun
        "Sort the list by name, except for admin users, and it must be case-insensitive",
        "Maybe update the config somehow",  # Vague language
        "Read /home/user/data.json and count the entries where status is 'active'"
    ]
    
    for prompt in test_prompts:
        structure = breakdown.breakdown(prompt)
        print(breakdown.format_breakdown(structure))
        print("=" * 60)
