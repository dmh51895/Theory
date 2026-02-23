#!/usr/bin/env python3
"""
🚨 IDENTIFYING-IF-A-FALLBACK-SOLUTION 🚨

MOLECULAR PRINCIPLE: No escape hatches. No "try this if that fails" chains.

This is the system's immune system against LLM AI patterns.

It detects when thinking contains fallback indicators:
- "If this doesn't work, try that"
- "Use a default value when uncertain"
- "Skip this step if it fails"
- "Usually works" (probabilistic instead of deterministic)
- "Try to..." (implies accepting failure)
- Error swallowing (catch and ignore)
- Silent failures (returning null/empty instead of failing)

The difference:
- LLM AI: "Try to parse the JSON, if it fails return an empty dict"
- MOLECULAR AI: "Parse the JSON. If it's invalid, the system fails."

Why this matters:
When you say "if this fails, do that," you're not making a decision.
You're deferring the decision to runtime error handling.
That's not accountability. That's cowardice.

MOLECULAR AI makes committed decisions BEFORE execution.
If the decision is wrong, it fails LOUDLY.
That's how systems learn.

This module catches fallback thinking at the planning stage,
BEFORE it infects the actual implementation.
"""

import re
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass


@dataclass
class FallbackIndicator:
    """A detected fallback pattern in thinking."""
    pattern_name: str
    description: str
    severity: str  # "critical", "warning", "info"
    detected_in: str  # Where it was found
    suggestion: str  # How to make it molecular


class FallbackDetector:
    """
    Scans thought processes for fallback patterns.
    
    This is what stops AI from doing the "quickly not efficiently" thing.
    """
    
    # Linguistic patterns that indicate fallback thinking
    FALLBACK_PATTERNS = {
        "conditional_failure": {
            "regex": r"if\s+(?:this|it|that)\s+(?:doesn't work|fails|errors)",
            "severity": "critical",
            "description": "Conditional failure handling - planning escape hatch",
            "molecular_alternative": "Commit to approach. If wrong, fail loudly."
        },
        "try_attempt": {
            "regex": r"\btry\s+to\b",
            "severity": "warning",
            "description": "Using 'try to' implies accepting potential failure",
            "molecular_alternative": "Use 'will' or 'does' - commit to outcome"
        },
        "default_value": {
            "regex": r"default|fallback|backup|alternative",
            "severity": "critical",
            "description": "Planning default/fallback values",
            "molecular_alternative": "Validate input, fail if invalid. No defaults."
        },
        "error_swallowing": {
            "regex": r"catch\s+and\s+(?:ignore|skip|continue|pass)",
            "severity": "critical",
            "description": "Planning to swallow errors silently",
            "molecular_alternative": "Catch errors, log them, propagate upward"
        },
        "probabilistic": {
            "regex": r"usually|normally|typically|most of the time|often works",
            "severity": "critical",
            "description": "Probabilistic thinking instead of deterministic",
            "molecular_alternative": "Make it work 100% or document failure mode"
        },
        "optional_skip": {
            "regex": r"skip\s+(?:this|if|when)|optional\s+step",
            "severity": "warning",
            "description": "Planning to skip steps conditionally",
            "molecular_alternative": "All steps required or redesign approach"
        },
        "silent_failure": {
            "regex": r"return\s+(?:null|none|empty|zero).*(?:if|when|on)\s+(?:error|fail)",
            "severity": "critical",
            "description": "Planning silent failure (returning empty on error)",
            "molecular_alternative": "Fail loudly. Raise exception or return error status"
        },
        "best_effort": {
            "regex": r"best effort|do what we can|as much as possible",
            "severity": "warning",
            "description": "Best effort instead of committed outcome",
            "molecular_alternative": "Define exact success criteria, achieve them or fail"
        },
        "graceful_degradation": {
            "regex": r"gracefully degrade|fallback mode|reduced functionality",
            "severity": "warning",
            "description": "Planning graceful degradation (hidden fallback)",
            "molecular_alternative": "System works fully or reports unavailable"
        },
        "just_in_case": {
            "regex": r"just in case|to be safe|as a backup",
            "severity": "warning",
            "description": "Adding unnecessary safety nets",
            "molecular_alternative": "If you need backup, primary approach is wrong"
        }
    }
    
    # Code patterns that indicate fallback implementation
    CODE_PATTERNS = {
        "bare_except": {
            "regex": r"except\s*:",
            "severity": "critical",
            "description": "Bare except clause - catches everything silently"
        },
        "pass_in_except": {
            "regex": r"except.*:\s*pass",
            "severity": "critical",
            "description": "Exception caught and ignored"
        },
        "return_none_on_error": {
            "regex": r"except.*:\s*return\s+None",
            "severity": "critical",
            "description": "Returning None on error - silent failure"
        },
        "or_default": {
            "regex": r"or\s+\w+_default|or\s+DEFAULT",
            "severity": "warning",
            "description": "Using 'or' operator for default values"
        },
        "get_with_default": {
            "regex": r"\.get\([^,]+,\s*[^\)]+\)",
            "severity": "info",
            "description": "dict.get() with default - may hide missing keys"
        }
    }
    
    def __init__(self):
        self.indicators_found: List[FallbackIndicator] = []
    
    def analyze_thought_process(self, conscious_analysis: Dict[str, Any],
                                meta_check: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scan the conscious analysis for fallback patterns.
        
        Returns:
            {
                "is_fallback": bool,
                "fallback_indicators": List[FallbackIndicator],
                "commitment_level": str,
                "molecular_score": float  # 0.0 = all fallback, 1.0 = fully molecular
            }
        """
        
        self.indicators_found = []
        
        # Extract text to analyze
        analysis_text = str(conscious_analysis)
        meta_text = str(meta_check)
        combined_text = f"{analysis_text} {meta_text}"
        
        # Scan for linguistic fallback patterns
        self._scan_patterns(combined_text, self.FALLBACK_PATTERNS, "thought_process")
        
        # Calculate molecular score
        critical_count = sum(1 for i in self.indicators_found if i.severity == "critical")
        warning_count = sum(1 for i in self.indicators_found if i.severity == "warning")
        
        # Scoring: Critical indicators heavily penalize, warnings less so
        penalty = (critical_count * 0.3) + (warning_count * 0.1)
        molecular_score = max(0.0, 1.0 - penalty)
        
        # Determine commitment level
        if molecular_score >= 0.9:
            commitment = "full"
        elif molecular_score >= 0.7:
            commitment = "mostly_committed"
        elif molecular_score >= 0.5:
            commitment = "partial"
        else:
            commitment = "fallback_oriented"
        
        is_fallback = molecular_score < 0.7  # Threshold for fallback classification
        
        return {
            "is_fallback": is_fallback,
            "fallback_indicators": [
                {
                    "pattern": ind.pattern_name,
                    "description": ind.description,
                    "severity": ind.severity,
                    "location": ind.detected_in
                }
                for ind in self.indicators_found
            ],
            "commitment_level": commitment,
            "molecular_score": molecular_score,
            "suggestion": self._generate_suggestion()
        }
    
    def analyze_code(self, code_text: str) -> Dict[str, Any]:
        """
        Scan actual code for fallback patterns.
        
        This catches fallbacks that made it into implementation.
        """
        self.indicators_found = []
        
        # Scan for code fallback patterns
        self._scan_patterns(code_text, self.CODE_PATTERNS, "code")
        
        critical_count = sum(1 for i in self.indicators_found if i.severity == "critical")
        warning_count = sum(1 for i in self.indicators_found if i.severity == "warning")
        
        penalty = (critical_count * 0.3) + (warning_count * 0.1)
        molecular_score = max(0.0, 1.0 - penalty)
        
        return {
            "is_molecular_code": molecular_score >= 0.8,
            "fallback_indicators": [
                {
                    "pattern": ind.pattern_name,
                    "description": ind.description,
                    "severity": ind.severity
                }
                for ind in self.indicators_found
            ],
            "molecular_score": molecular_score
        }
    
    def _scan_patterns(self, text: str, patterns: Dict[str, Dict],
                       location: str):
        """Scan text for fallback patterns."""
        text_lower = text.lower()
        
        for pattern_name, pattern_info in patterns.items():
            regex = pattern_info["regex"]
            matches = re.finditer(regex, text_lower, re.IGNORECASE | re.MULTILINE)
            
            for match in matches:
                indicator = FallbackIndicator(
                    pattern_name=pattern_name,
                    description=pattern_info["description"],
                    severity=pattern_info["severity"],
                    detected_in=location,
                    suggestion=pattern_info.get("molecular_alternative", "")
                )
                self.indicators_found.append(indicator)
    
    def _generate_suggestion(self) -> str:
        """Generate suggestion for making thought process more molecular."""
        if not self.indicators_found:
            return "Thought process is molecular - fully committed"
        
        critical = [i for i in self.indicators_found if i.severity == "critical"]
        
        if critical:
            suggestions = []
            for ind in critical[:3]:  # Top 3 critical issues
                suggestions.append(f"- {ind.description}: {ind.suggestion}")
            return "Critical fallback patterns detected. To make molecular:\n" + "\n".join(suggestions)
        
        return "Minor fallback indicators. Consider removing escape hatches for full commitment."
    
    def get_report(self) -> str:
        """Get human-readable report of detected fallbacks."""
        if not self.indicators_found:
            return "✓ No fallback patterns detected. Thinking is molecular."
        
        lines = [f"⚠ {len(self.indicators_found)} fallback indicators detected:"]
        lines.append("")
        
        for ind in self.indicators_found:
            severity_symbol = {"critical": "🔴", "warning": "🟡", "info": "🔵"}
            symbol = severity_symbol.get(ind.severity, "⚪")
            lines.append(f"{symbol} {ind.pattern_name}: {ind.description}")
            if ind.suggestion:
                lines.append(f"   → {ind.suggestion}")
            lines.append("")
        
        return "\n".join(lines)


class FallbackCorrector:
    """
    Attempts to rewrite fallback thinking into molecular thinking.
    
    This is the "Rewired-Thought" component.
    """
    
    @staticmethod
    def rewrite_to_molecular(fallback_thought: str, indicators: List[Dict]) -> str:
        """
        Take fallback-oriented thinking and rewrite it molecularly.
        
        Example transformations:
        - "Try to parse JSON, return {} if it fails" 
          → "Parse JSON. If invalid, raise ValueError"
        
        - "Use default value if config missing"
          → "Require config value. If missing, system init fails"
        
        - "Skip step if data unavailable"
          → "Require data. If unavailable, request it or fail"
        """
        
        rewritten = fallback_thought
        
        # Apply transformations based on indicators
        for ind in indicators:
            pattern = ind["pattern"]
            
            if pattern == "conditional_failure":
                rewritten = re.sub(
                    r"if\s+(?:this|it)\s+(?:doesn't work|fails),?\s*(?:try|use|do)\s+\w+",
                    "commit to approach. If wrong, fail explicitly",
                    rewritten,
                    flags=re.IGNORECASE
                )
            
            elif pattern == "try_attempt":
                rewritten = rewritten.replace("try to", "will")
                rewritten = rewritten.replace("Try to", "Will")
            
            elif pattern == "default_value":
                rewritten = re.sub(
                    r"(?:use|return|default to)\s+(?:default|fallback|backup)",
                    "require valid value",
                    rewritten,
                    flags=re.IGNORECASE
                )
            
            elif pattern == "probabilistic":
                rewritten = re.sub(
                    r"usually|typically|normally",
                    "deterministically",
                    rewritten,
                    flags=re.IGNORECASE
                )
        
        return rewritten


if __name__ == "__main__":
    # Test the detector
    detector = FallbackDetector()
    
    # Test fallback thinking
    fallback_example = {
        "prompt_understood": True,
        "key_intent": "Try to process the data, if it fails just skip it",
        "approach": "Use default values when config is missing"
    }
    
    result = detector.analyze_thought_process(fallback_example, {})
    
    print("Fallback Detection Test:")
    print(f"Is fallback: {result['is_fallback']}")
    print(f"Molecular score: {result['molecular_score']:.2f}")
    print(f"Commitment level: {result['commitment_level']}")
    print(f"\n{detector.get_report()}")
    
    # Test molecular thinking
    molecular_example = {
        "prompt_understood": True,
        "key_intent": "Process the data deterministically",
        "approach": "Validate input, execute transform, verify output"
    }
    
    detector2 = FallbackDetector()
    result2 = detector2.analyze_thought_process(molecular_example, {})
    
    print("\nMolecular Thinking Test:")
    print(f"Is fallback: {result2['is_fallback']}")
    print(f"Molecular score: {result2['molecular_score']:.2f}")
    print(f"Commitment level: {result2['commitment_level']}")
    print(f"\n{detector2.get_report()}")
