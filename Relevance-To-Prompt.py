"""
Relevance-To-Prompt.py

MOLECULAR PRINCIPLE: Filter information by ACTUAL relevance, not vibes.

LLM AI uses semantic similarity (probabilistic matching) to determine relevance.
MOLECULAR AI uses explicit criteria: Does this information enable decision execution?

Relevance is BINARY and MEASURABLE:
- Does data answer a question posed in the prompt? YES/NO
- Does data enable constraint satisfaction? YES/NO  
- Does data provide required context? YES/NO

NO middle ground. Either relevant or not.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
import re


@dataclass
class RelevanceCriteria:
    """Explicit criteria for what makes information relevant."""
    required_keywords: Set[str]  # Must appear
    target_entities: Set[str]  # Specific things mentioned
    questions_to_answer: List[str]  # What needs to be known
    constraints_to_satisfy: List[str]  # What must be checked
    success_criteria: List[str]  # What determines completion


@dataclass
class RelevanceScore:
    """Binary relevance assessment with justification."""
    is_relevant: bool
    relevance_type: str  # "answers_question", "satisfies_constraint", "provides_context", "irrelevant"
    justification: str
    matched_criteria: List[str]
    information: str


class RelevanceFilter:
    """
    Filters information based on ACTUAL relevance to prompt requirements.
    
    Key principle: Relevance is not "kinda related" - it's "directly enables execution".
    """
    
    def __init__(self):
        pass
    
    def extract_criteria(self, prompt_structure) -> RelevanceCriteria:
        """
        Extract relevance criteria from structured prompt.
        
        Takes output from Prompt-Breakdown.py and determines what information
        would be relevant to executing this prompt.
        """
        required_keywords = set()
        target_entities = set()
        questions = []
        constraints = []
        success_checks = []
        
        # Extract from actions
        for action in prompt_structure.actions:
            required_keywords.add(action.content.lower())
            
            # Generate question based on action
            if action.content in ['create', 'write', 'add']:
                questions.append(f"What content should be created?")
            elif action.content in ['delete', 'remove']:
                questions.append(f"What exists that can be deleted?")
            elif action.content in ['modify', 'update']:
                questions.append(f"What is the current state?")
                questions.append(f"What is the desired state?")
            elif action.content in ['read', 'find', 'search']:
                questions.append(f"Where is the data located?")
        
        # Extract from targets
        for target in prompt_structure.targets:
            if not target.requires_clarification:  # Only clear targets
                target_entities.add(target.content.lower())
        
        # Extract from constraints
        for constraint in prompt_structure.constraints:
            constraints.append(constraint.content)
            required_keywords.update(self._extract_keywords(constraint.content))
        
        # Extract from success criteria
        for criterion in prompt_structure.success_criteria:
            success_checks.append(criterion.content)
        
        return RelevanceCriteria(
            required_keywords=required_keywords,
            target_entities=target_entities,
            questions_to_answer=questions,
            constraints_to_satisfy=constraints,
            success_criteria=success_checks
        )
    
    def assess_relevance(self, information: str, criteria: RelevanceCriteria) -> RelevanceScore:
        """
        Assess if information is relevant to prompt execution.
        
        Relevance is BINARY: either this information enables execution or it doesn't.
        """
        info_lower = information.lower()
        matched = []
        
        # Check 1: Does it mention required keywords?
        keyword_matches = [kw for kw in criteria.required_keywords if kw in info_lower]
        if keyword_matches:
            matched.append(f"Keywords: {', '.join(keyword_matches)}")
        
        # Check 2: Does it mention target entities?
        entity_matches = [ent for ent in criteria.target_entities if ent in info_lower]
        if entity_matches:
            matched.append(f"Entities: {', '.join(entity_matches)}")
        
        # Check 3: Does it answer a question?
        answered_questions = []
        for question in criteria.questions_to_answer:
            if self._answers_question(information, question):
                answered_questions.append(question)
        if answered_questions:
            matched.append(f"Answers: {answered_questions[0][:50]}...")
        
        # Check 4: Does it help satisfy constraints?
        relevant_constraints = []
        for constraint in criteria.constraints_to_satisfy:
            constraint_keywords = self._extract_keywords(constraint)
            if any(kw in info_lower for kw in constraint_keywords):
                relevant_constraints.append(constraint[:50])
        if relevant_constraints:
            matched.append(f"Constraint: {relevant_constraints[0]}...")
        
        # Determine relevance type and binary decision
        if answered_questions:
            return RelevanceScore(
                is_relevant=True,
                relevance_type="answers_question",
                justification=f"Answers: {answered_questions[0]}",
                matched_criteria=matched,
                information=information
            )
        elif relevant_constraints:
            return RelevanceScore(
                is_relevant=True,
                relevance_type="satisfies_constraint",
                justification=f"Helps check: {relevant_constraints[0]}",
                matched_criteria=matched,
                information=information
            )
        elif keyword_matches or entity_matches:
            return RelevanceScore(
                is_relevant=True,
                relevance_type="provides_context",
                justification=f"Contains required terms: {', '.join(keyword_matches + entity_matches)}",
                matched_criteria=matched,
                information=information
            )
        else:
            return RelevanceScore(
                is_relevant=False,
                relevance_type="irrelevant",
                justification="Does not enable prompt execution",
                matched_criteria=[],
                information=information
            )
    
    def filter_information(self, information_list: List[str], 
                          criteria: RelevanceCriteria) -> Dict[str, List[RelevanceScore]]:
        """
        Filter a list of information items by relevance.
        
        Returns categorized results: relevant vs irrelevant.
        """
        results = {
            "relevant": [],
            "irrelevant": []
        }
        
        for info in information_list:
            score = self.assess_relevance(info, criteria)
            if score.is_relevant:
                results["relevant"].append(score)
            else:
                results["irrelevant"].append(score)
        
        return results
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract significant keywords from text."""
        # Remove common words
        stopwords = {
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
            'can', 'could', 'may', 'might', 'must', 'shall', 'to', 'of', 'in',
            'on', 'at', 'by', 'for', 'with', 'about', 'as', 'from', 'that'
        }
        
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = {w for w in words if w not in stopwords and len(w) > 2}
        return keywords
    
    def _answers_question(self, information: str, question: str) -> bool:
        """
        Check if information answers a specific question.
        
        This is a simplified check - looks for keywords from question in information.
        """
        question_keywords = self._extract_keywords(question)
        info_keywords = self._extract_keywords(information)
        
        # If at least 50% of question keywords appear in info
        if question_keywords:
            overlap = len(question_keywords & info_keywords)
            return overlap / len(question_keywords) >= 0.5
        return False
    
    def rank_by_relevance(self, relevant_items: List[RelevanceScore]) -> List[RelevanceScore]:
        """
        Rank relevant items by importance.
        
        Priority:
        1. Answers questions (directly enables execution)
        2. Satisfies constraints (prevents failure)
        3. Provides context (supplementary)
        """
        priority_order = {
            "answers_question": 0,
            "satisfies_constraint": 1,
            "provides_context": 2
        }
        
        return sorted(relevant_items, 
                     key=lambda x: (priority_order[x.relevance_type], -len(x.matched_criteria)))
    
    def format_relevance_report(self, filtered_results: Dict[str, List[RelevanceScore]]) -> str:
        """Format relevance filtering results for review."""
        lines = []
        
        relevant = filtered_results["relevant"]
        irrelevant = filtered_results["irrelevant"]
        
        lines.append(f"RELEVANCE FILTERING RESULTS")
        lines.append(f"Relevant: {len(relevant)} | Irrelevant: {len(irrelevant)}")
        lines.append("")
        
        if relevant:
            lines.append("RELEVANT INFORMATION:")
            ranked = self.rank_by_relevance(relevant)
            for score in ranked:
                lines.append(f"  ✓ [{score.relevance_type}]")
                lines.append(f"    {score.information[:80]}...")
                lines.append(f"    → {score.justification}")
                if score.matched_criteria:
                    lines.append(f"    Matched: {', '.join(score.matched_criteria)}")
                lines.append("")
        
        if irrelevant:
            lines.append("IRRELEVANT INFORMATION:")
            for score in irrelevant[:3]:  # Show first 3
                lines.append(f"  ✗ {score.information[:80]}...")
                lines.append(f"    → {score.justification}")
                lines.append("")
            
            if len(irrelevant) > 3:
                lines.append(f"  ... and {len(irrelevant) - 3} more irrelevant items")
                lines.append("")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test molecular relevance filtering
    from dataclasses import dataclass
    
    # Mock prompt structure
    @dataclass
    class MockComponent:
        content: str
        requires_clarification: bool = False
    
    @dataclass
    class MockPromptStructure:
        actions: List[MockComponent]
        targets: List[MockComponent]
        constraints: List[MockComponent]
        success_criteria: List[MockComponent]
    
    # Example: "Create a Python file that calculates factorial, must handle negative numbers"
    mock_structure = MockPromptStructure(
        actions=[MockComponent("create")],
        targets=[MockComponent("Python file"), MockComponent("factorial")],
        constraints=[MockComponent("must handle negative numbers")],
        success_criteria=[MockComponent("calculates factorial correctly")]
    )
    
    filter_system = RelevanceFilter()
    criteria = filter_system.extract_criteria(mock_structure)
    
    # Test information items
    test_info = [
        "Factorial is calculated as n! = n * (n-1)!",
        "Python uses .py file extension",
        "Negative numbers have no factorial in standard mathematics",
        "The weather today is sunny",
        "File creation requires write permissions",
        "Baseball is a popular sport"
    ]
    
    results = filter_system.filter_information(test_info, criteria)
    print(filter_system.format_relevance_report(results))
