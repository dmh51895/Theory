"""
Original-Data.py

MOLECULAR PRINCIPLE: Preserve original data, never synthesize.

LLM AI transforms/paraphrases/"improves" user input.
MOLECULAR AI preserves EXACT original data for reference.

Why preserve:
- User's exact words matter (intent, specificity)
- Transformations introduce errors
- Need to compare original vs interpretation
- Debugging requires original input

NO paraphrasing. NO "cleaning up". EXACT preservation.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
import hashlib
import json


@dataclass
class OriginalData:
    """Container for original, untransformed data."""
    data: Any  # The original data
    data_type: str  # "prompt", "user_input", "file_content", etc.
    timestamp: str  # When received
    source: str  # Where it came from
    hash: str  # Hash for verification
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def verify_integrity(self, data_to_check: Any) -> bool:
        """Verify data hasn't been corrupted."""
        check_hash = self._compute_hash(data_to_check)
        return check_hash == self.hash
    
    @staticmethod
    def _compute_hash(data: Any) -> str:
        """Compute hash of data."""
        if isinstance(data, str):
            data_str = data
        else:
            data_str = json.dumps(data, sort_keys=True)
        
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]


@dataclass
class DataTransformation:
    """Record of how data was transformed."""
    original_hash: str
    transformed_data: Any
    transformation_type: str  # "parsed", "analyzed", "normalized", etc.
    timestamp: str
    reasoning: str  # WHY was this transformation done


class OriginalDataPreserver:
    """
    Preserves original data and tracks transformations.
    
    Key principle: Never lose sight of what user ACTUALLY said/provided.
    """
    
    def __init__(self):
        self.originals: Dict[str, OriginalData] = {}
        self.transformations: Dict[str, List[DataTransformation]] = {}  # original_hash -> transformations
    
    def preserve(self, data: Any, data_type: str, source: str, 
                metadata: Dict[str, Any] = None) -> str:
        """
        Preserve original data.
        
        Returns hash that can be used to retrieve original.
        """
        data_hash = OriginalData._compute_hash(data)
        
        original = OriginalData(
            data=data,
            data_type=data_type,
            timestamp=datetime.now().isoformat(),
            source=source,
            hash=data_hash,
            metadata=metadata or {}
        )
        
        self.originals[data_hash] = original
        return data_hash
    
    def retrieve(self, data_hash: str) -> Optional[OriginalData]:
        """Retrieve original data by hash."""
        return self.originals.get(data_hash)
    
    def record_transformation(self, original_hash: str, transformed_data: Any,
                            transformation_type: str, reasoning: str):
        """
        Record a data transformation.
        
        Preserves lineage: original -> transformed.
        """
        transformation = DataTransformation(
            original_hash=original_hash,
            transformed_data=transformed_data,
            transformation_type=transformation_type,
            timestamp=datetime.now().isoformat(),
            reasoning=reasoning
        )
        
        if original_hash not in self.transformations:
            self.transformations[original_hash] = []
        
        self.transformations[original_hash].append(transformation)
    
    def get_transformation_chain(self, original_hash: str) -> List[DataTransformation]:
        """Get all transformations of original data."""
        return self.transformations.get(original_hash, [])
    
    def compare_original_and_interpretation(self, original_hash: str) -> Dict:
        """
        Compare original data with how we interpreted it.
        
        Shows if we understood correctly.
        """
        original = self.retrieve(original_hash)
        if not original:
            return {"error": "Original not found"}
        
        transformations = self.get_transformation_chain(original_hash)
        
        return {
            "original": original.data,
            "original_type": original.data_type,
            "interpretations": [
                {
                    "type": t.transformation_type,
                    "result": t.transformed_data,
                    "reasoning": t.reasoning
                }
                for t in transformations
            ]
        }
    
    def verify_all_originals(self) -> Dict[str, bool]:
        """Verify integrity of all preserved data."""
        results = {}
        for data_hash, original in self.originals.items():
            results[data_hash] = original.verify_integrity(original.data)
        return results
    
    def get_by_type(self, data_type: str) -> List[OriginalData]:
        """Get all originals of a specific type."""
        return [o for o in self.originals.values() if o.data_type == data_type]
    
    def format_preservation_report(self, original_hash: str) -> str:
        """Format a report showing original and transformations."""
        original = self.retrieve(original_hash)
        if not original:
            return f"No original data found for hash {original_hash}"
        
        lines = [
            "ORIGINAL DATA:",
            f"  Type: {original.data_type}",
            f"  Source: {original.source}",
            f"  Timestamp: {original.timestamp}",
            f"  Hash: {original.hash}",
            "",
            "ORIGINAL CONTENT:",
            f"  {original.data}",
            ""
        ]
        
        transformations = self.get_transformation_chain(original_hash)
        if transformations:
            lines.append("TRANSFORMATIONS:")
            for i, trans in enumerate(transformations, 1):
                lines.append(f"  {i}. {trans.transformation_type}")
                lines.append(f"     Reasoning: {trans.reasoning}")
                lines.append(f"     Result: {trans.transformed_data}")
                lines.append("")
        else:
            lines.append("No transformations recorded.")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test original data preservation
    preserver = OriginalDataPreserver()
    
    # Preserve user prompt
    user_prompt = "Create a file called test.txt with some content"
    prompt_hash = preserver.preserve(
        data=user_prompt,
        data_type="user_prompt",
        source="user_input",
        metadata={"session_id": "test_session"}
    )
    
    print(f"Preserved prompt with hash: {prompt_hash}")
    print()
    
    # Record interpretation
    preserver.record_transformation(
        original_hash=prompt_hash,
        transformed_data={
            "action": "create_file",
            "filename": "test.txt",
            "content": "some content"
        },
        transformation_type="parsed_prompt",
        reasoning="Extracted action and parameters from natural language"
    )
    
    # Show preservation report
    print(preserver.format_preservation_report(prompt_hash))
    print()
    
    # Compare original and interpretation
    comparison = preserver.compare_original_and_interpretation(prompt_hash)
    print("COMPARISON:")
    print(f"Original: {comparison['original']}")
    print(f"Interpretations:")
    for interp in comparison['interpretations']:
        print(f"  - {interp['type']}: {interp['result']}")
