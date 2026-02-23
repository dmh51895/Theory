"""
Synchronized-Patterns.py

MOLECULAR PRINCIPLE: Patterns across components must ALIGN, not conflict.

LLM AI has no cross-component consistency (each module probabilistic).
MOLECULAR AI ensures all components recognize the same patterns.

Pattern synchronization = Shared truth about observed patterns.

When Brain detects fallback thinking, ALL components see it.
When Memory records a pattern, ALL components can access it.
When Wisdom extracts a lesson, ALL components learn from it.

NO conflicting interpretations. YES synchronized knowledge.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set, Any, Optional
from datetime import datetime


@dataclass
class SharedPattern:
    """A pattern recognized across components."""
    pattern_id: str
    pattern_type: str  # "fallback", "success", "failure", "behavior"
    pattern_data: Dict[str, Any]
    observed_by: Set[str]  # Which components observed this
    first_observed: str
    last_observed: str
    observation_count: int
    confidence: float  # Agreement across components


class PatternSynchronizer:
    """
    Ensures pattern consistency across all components.
    
    Key principle: All components share same understanding of patterns.
    """
    
    def __init__(self):
        self.shared_patterns: Dict[str, SharedPattern] = {}
        self.component_views: Dict[str, Set[str]] = {}  # component_name -> pattern_ids
    
    def register_pattern(self, pattern_id: str, pattern_type: str, 
                        pattern_data: Dict, observed_by: str):
        """
        Register a pattern observed by a component.
        
        If pattern already exists, increment observation count.
        If new, create shared pattern.
        """
        if pattern_id in self.shared_patterns:
            # Update existing pattern
            pattern = self.shared_patterns[pattern_id]
            pattern.observed_by.add(observed_by)
            pattern.last_observed = datetime.now().isoformat()
            pattern.observation_count += 1
            
            # Update confidence based on cross-component agreement
            pattern.confidence = len(pattern.observed_by) / 10.0  # Simplified
            pattern.confidence = min(1.0, pattern.confidence)
        else:
            # Create new shared pattern
            pattern = SharedPattern(
                pattern_id=pattern_id,
                pattern_type=pattern_type,
                pattern_data=pattern_data,
                observed_by={observed_by},
                first_observed=datetime.now().isoformat(),
                last_observed=datetime.now().isoformat(),
                observation_count=1,
                confidence=0.1  # Low confidence initially
            )
            self.shared_patterns[pattern_id] = pattern
        
        # Track component's view
        if observed_by not in self.component_views:
            self.component_views[observed_by] = set()
        self.component_views[observed_by].add(pattern_id)
    
    def get_pattern(self, pattern_id: str) -> Optional[SharedPattern]:
        """Get a shared pattern by ID."""
        return self.shared_patterns.get(pattern_id)
    
    def get_patterns_by_type(self, pattern_type: str) -> List[SharedPattern]:
        """Get all patterns of a specific type."""
        return [p for p in self.shared_patterns.values() if p.pattern_type == pattern_type]
    
    def get_patterns_for_component(self, component_name: str) -> List[SharedPattern]:
        """Get all patterns visible to a component."""
        if component_name not in self.component_views:
            return []
        
        pattern_ids = self.component_views[component_name]
        return [self.shared_patterns[pid] for pid in pattern_ids if pid in self.shared_patterns]
    
    def check_consistency(self) -> Dict[str, Any]:
        """
        Check if components have consistent pattern views.
        
        Returns consistency metrics.
        """
        if not self.component_views:
            return {"consistent": True, "divergence": 0.0}
        
        # Calculate overlap between component views
        components = list(self.component_views.keys())
        if len(components) < 2:
            return {"consistent": True, "divergence": 0.0, "reason": "Only one component"}
        
        # Compare each pair of components
        total_overlap = 0
        comparisons = 0
        
        for i in range(len(components)):
            for j in range(i + 1, len(components)):
                view_a = self.component_views[components[i]]
                view_b = self.component_views[components[j]]
                
                if not view_a or not view_b:
                    continue
                
                overlap = len(view_a & view_b)
                total = len(view_a | view_b)
                
                if total > 0:
                    total_overlap += overlap / total
                    comparisons += 1
        
        if comparisons == 0:
            return {"consistent": True, "divergence": 0.0, "reason": "No overlapping patterns"}
        
        avg_overlap = total_overlap / comparisons
        divergence = 1.0 - avg_overlap
        
        return {
            "consistent": divergence < 0.3,
            "divergence": divergence,
            "avg_overlap": avg_overlap,
            "components_compared": comparisons
        }
    
    def synchronize_with_component(self, component_name: str):
        """
        Ensure component sees all relevant patterns.
        
        Propagates high-confidence patterns to component.
        """
        high_confidence_patterns = [
            p for p in self.shared_patterns.values() 
            if p.confidence >= 0.7
        ]
        
        if component_name not in self.component_views:
            self.component_views[component_name] = set()
        
        for pattern in high_confidence_patterns:
            self.component_views[component_name].add(pattern.pattern_id)
            pattern.observed_by.add(component_name)
    
    def invalidate_pattern(self, pattern_id: str, reason: str):
        """
        Invalidate a pattern (e.g., proven wrong).
        
        Removes from all component views.
        """
        if pattern_id in self.shared_patterns:
            pattern = self.shared_patterns[pattern_id]
            pattern.pattern_data['invalidated'] = True
            pattern.pattern_data['invalidation_reason'] = reason
            pattern.confidence = 0.0
            
            # Remove from component views
            for component in self.component_views:
                if pattern_id in self.component_views[component]:
                    self.component_views[component].remove(pattern_id)
    
    def format_synchronization_status(self) -> str:
        """Format synchronization status for review."""
        lines = ["PATTERN SYNCHRONIZATION STATUS:", ""]
        
        lines.append(f"Total shared patterns: {len(self.shared_patterns)}")
        lines.append(f"Active components: {len(self.component_views)}")
        lines.append("")
        
        consistency = self.check_consistency()
        lines.append(f"Consistency: {'✓ YES' if consistency['consistent'] else '✗ NO'}")
        lines.append(f"Divergence: {consistency.get('divergence', 0.0):.0%}")
        lines.append("")
        
        # Show high-confidence patterns
        high_conf = [p for p in self.shared_patterns.values() if p.confidence >= 0.7]
        if high_conf:
            lines.append("HIGH-CONFIDENCE PATTERNS:")
            for pattern in sorted(high_conf, key=lambda p: -p.confidence):
                lines.append(f"  {pattern.pattern_id}")
                lines.append(f"    Type: {pattern.pattern_type}")
                lines.append(f"    Confidence: {pattern.confidence:.0%}")
                lines.append(f"    Observed by: {', '.join(pattern.observed_by)}")
                lines.append("")
        
        # Show component views
        lines.append("COMPONENT VIEWS:")
        for component, pattern_ids in self.component_views.items():
            lines.append(f"  {component}: {len(pattern_ids)} patterns")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test pattern synchronization
    synchronizer = PatternSynchronizer()
    
    # Simulate components observing patterns
    synchronizer.register_pattern(
        pattern_id="fallback_try_catch",
        pattern_type="fallback",
        pattern_data={"description": "Try/catch escape hatch"},
        observed_by="FallbackDetector"
    )
    
    synchronizer.register_pattern(
        pattern_id="fallback_try_catch",
        pattern_type="fallback",
        pattern_data={"description": "Try/catch escape hatch"},
        observed_by="Metacognition"
    )
    
    synchronizer.register_pattern(
        pattern_id="fallback_try_catch",
        pattern_type="fallback",
        pattern_data={"description": "Try/catch escape hatch"},
        observed_by="Rules"
    )
    
    synchronizer.register_pattern(
        pattern_id="high_clarity_success",
        pattern_type="success",
        pattern_data={"clarity_threshold": 0.9},
        observed_by="Brain"
    )
    
    synchronizer.register_pattern(
        pattern_id="high_clarity_success",
        pattern_type="success",
        pattern_data={"clarity_threshold": 0.9},
        observed_by="Wisdom"
    )
    
    print(synchronizer.format_synchronization_status())
    print()
    
    # Test synchronization
    synchronizer.synchronize_with_component("NewComponent")
    print("After synchronizing with NewComponent:")
    print(synchronizer.format_synchronization_status())
