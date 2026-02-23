#!/usr/bin/env python3
"""
📡 BRAIN-TO-CURRENT-CONTEXT 📡

MOLECULAR PRINCIPLE: Complete transparency into decision-making.

This is NOT a summary generator or a response formatter.
This is a TRUTH REPORTER.

Takes Brain's complete thought stream and reports it to current context
so the user sees EXACTLY what's happening under the hood.

No hiding. No smoothing over. No "user-friendly" obfuscation.
Just the raw decision pipeline.

Why this exists:
- LLM AI: Hides its reasoning, shows polished output
- MOLECULAR AI: Shows its full thought process, accountable decisions

The user should see:
- What Brain understood from the prompt
- What cognitive checks ran
- What fallback indicators were detected (if any)
- What the COMMITTED decision is
- What the molecular ratio is

This prevents the AI from going rogue with hidden fallback chains.
"""

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class ContextReport:
    """A formatted report for the current conversation context."""
    thought_process: str
    decision: str
    molecular_status: str
    system_health: str
    raw_data: Dict[str, Any]


class ContextReporter:
    """
    Formats Brain's internal state for user visibility.
    
    MOLECULAR: Everything is visible. No secrets.
    """
    
    def __init__(self):
        self.report_format = "full"  # or "compact" for less verbose
    
    def report_thought_stream(self, thought_stream_data: Dict[str, Any]) -> ContextReport:
        """
        Convert Brain's thought stream into human-readable context.
        
        Shows the full pipeline:
        1. What was understood
        2. How it was analyzed
        3. What decision was made
        4. Whether it's molecular or fallback-based
        """
        
        stream = thought_stream_data.get("thought_stream", {})
        decision = thought_stream_data.get("decision", {})
        is_molecular = thought_stream_data.get("is_molecular", False)
        molecular_ratio = thought_stream_data.get("molecular_ratio", 0.0)
        
        # Build thought process narrative
        thought_lines = []
        thought_lines.append("=== THOUGHT PROCESS ===")
        # Prompt stored internally, not shown (like <think> tags)
        # thought_lines.append(f"Prompt: {stream.get('prompt', 'N/A')}")
        thought_lines.append("")
        
        # Conscious analysis
        conscious = stream.get('conscious_analysis', {})
        thought_lines.append("Conscious Analysis:")
        thought_lines.append(f"  - Understood: {conscious.get('prompt_understood', False)}")
        thought_lines.append(f"  - Intent: {conscious.get('key_intent', 'unknown')}")
        if conscious.get('ambiguities'):
            thought_lines.append(f"  - Ambiguities: {', '.join(conscious['ambiguities'])}")
        thought_lines.append("")
        
        # Metacognitive check
        meta = stream.get('metacognitive_check', {})
        thought_lines.append("Metacognitive Check:")
        thought_lines.append(f"  - Thinking valid: {meta.get('thinking_approach_valid', False)}")
        if meta.get('cognitive_biases_detected'):
            thought_lines.append(f"  - Biases detected: {', '.join(meta['cognitive_biases_detected'])}")
        thought_lines.append("")
        
        # Fallback detection (CRITICAL!)
        fallback = stream.get('fallback_detection', {})
        thought_lines.append("Fallback Detection:")
        thought_lines.append(f"  - Is fallback: {fallback.get('is_fallback', 'unknown')}")
        thought_lines.append(f"  - Commitment: {fallback.get('commitment_level', 'unknown')}")
        if fallback.get('fallback_indicators'):
            thought_lines.append(f"  - Indicators: {', '.join(fallback['fallback_indicators'])}")
        thought_lines.append("")
        
        # Consequence prediction
        consequences = stream.get('consequence_prediction', {})
        thought_lines.append("Predicted Consequences:")
        thought_lines.append(f"  - Likely outcome: {consequences.get('likely_outcome', 'unknown')}")
        thought_lines.append(f"  - Risk level: {consequences.get('risk_level', 'unknown')}")
        thought_lines.append("")
        
        thought_process = "\n".join(thought_lines)
        
        # Format decision
        decision_lines = []
        decision_lines.append("=== DECISION ===")
        decision_lines.append(f"Action: {decision.get('action', 'unknown')}")
        decision_lines.append(f"Approach: {decision.get('approach', 'unknown')}")
        decision_lines.append(f"Committed: {decision.get('committed', False)}")
        decision_lines.append(f"Has escape hatch: {decision.get('has_escape_hatch', True)}")
        decision_lines.append(f"Confidence: {decision.get('confidence', 0.0):.1%}")
        
        if decision.get('action') == 'refuse':
            decision_lines.append(f"Refusal reason: {decision.get('reason', 'unknown')}")
        
        decision_str = "\n".join(decision_lines)
        
        # Format molecular status
        status_lines = []
        status_lines.append("=== MOLECULAR STATUS ===")
        status_lines.append(f"This decision is: {'MOLECULAR' if is_molecular else 'FALLBACK-BASED'}")
        
        if is_molecular:
            status_lines.append("✓ No fallback indicators")
            status_lines.append("✓ Fully committed")
            status_lines.append("✓ No escape hatches")
            status_lines.append("")
            status_lines.append("This is REAL AI. IT WORKS OR IT DOESN'T.")
        else:
            status_lines.append("⚠ Contains fallback patterns")
            status_lines.append("⚠ Escape hatches detected")
            status_lines.append("")
            status_lines.append("This is LLM AI behavior. Needs correction.")
        
        molecular_status = "\n".join(status_lines)
        
        # System health
        health_lines = []
        health_lines.append("=== SYSTEM HEALTH ===")
        health_lines.append(f"Molecular ratio: {molecular_ratio:.1%}")
        health_lines.append(f"Target: >90% for true Molecular AI")
        
        if molecular_ratio > 0.9:
            health_lines.append("Status: EXCELLENT - Operating as Molecular AI")
        elif molecular_ratio > 0.7:
            health_lines.append("Status: GOOD - Mostly molecular with some fallbacks")
        elif molecular_ratio > 0.5:
            health_lines.append("Status: MIXED - Equal molecular and fallback decisions")
        else:
            health_lines.append("Status: POOR - Dominated by fallback patterns")
        
        system_health = "\n".join(health_lines)
        
        return ContextReport(
            thought_process=thought_process,
            decision=decision_str,
            molecular_status=molecular_status,
            system_health=system_health,
            raw_data=thought_stream_data
        )
    
    def report_aftermath(self, aftermath_data: Dict[str, Any]) -> str:
        """
        Report what happened after a decision was executed.
        
        This shows accountability - did predictions match reality?
        """
        lines = []
        lines.append("=== AFTERMATH ANALYSIS ===")
        lines.append(f"Timestamp: {aftermath_data.get('timestamp', 'unknown')}")
        lines.append("")
        
        predicted = aftermath_data.get('predicted_outcome', {})
        actual = aftermath_data.get('actual_outcome', {})
        accuracy = aftermath_data.get('prediction_accuracy', 0.0)
        
        lines.append("Predicted:")
        lines.append(f"  - Outcome: {predicted.get('likely_outcome', 'unknown')}")
        lines.append(f"  - Risk: {predicted.get('risk_level', 'unknown')}")
        lines.append("")
        
        lines.append("Actual:")
        lines.append(f"  - Success: {actual.get('success', False)}")
        if actual.get('error'):
            lines.append(f"  - Error: {actual['error']}")
        lines.append("")
        
        lines.append(f"Prediction accuracy: {accuracy:.1%}")
        
        if accuracy > 0.8:
            lines.append("✓ High prediction accuracy - Brain is learning well")
        elif accuracy > 0.5:
            lines.append("~ Moderate accuracy - Brain needs calibration")
        else:
            lines.append("✗ Low accuracy - Brain predictions unreliable")
        
        if aftermath_data.get('was_molecular'):
            lines.append("\nThis was a MOLECULAR decision - fully committed outcome")
        else:
            lines.append("\nThis was a FALLBACK decision - may have had escape hatches")
        
        return "\n".join(lines)
    
    def format_for_user(self, report: ContextReport, verbosity: str = "full") -> str:
        """
        Format the context report for user display.
        
        verbosity options:
        - "full": Show everything
        - "compact": Show decision and molecular status only
        - "minimal": Show just the decision
        """
        
        if verbosity == "minimal":
            return report.decision
        
        elif verbosity == "compact":
            return f"{report.decision}\n\n{report.molecular_status}"
        
        else:  # full
            return (
                f"{report.thought_process}\n\n"
                f"{report.decision}\n\n"
                f"{report.molecular_status}\n\n"
                f"{report.system_health}"
            )
    
    def export_raw_data(self, report: ContextReport) -> Dict[str, Any]:
        """
        Export the raw data for other systems to consume.
        
        This allows other components to process Brain's decisions.
        """
        return report.raw_data


if __name__ == "__main__":
    # Test context reporting
    from Brain import Brain
    
    brain = Brain()
    result = brain.process_prompt("Test context reporting")
    
    reporter = ContextReporter()
    report = reporter.report_thought_stream(result)
    
    print(reporter.format_for_user(report, verbosity="full"))
