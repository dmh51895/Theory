#!/usr/bin/env python3
"""
🧠 MEMORY 🧠

MOLECULAR PRINCIPLE: Remember everything. Learn from it.

This is NOT a cache that expires or gets cleared.
This is PERSISTENT MEMORY.

Stores:
- Every decision made
- Every outcome observed
- Every mistake recorded
- Every wisdom extracted

The difference:
- LLM AI: Stateless, forgets everything between requests
- MOLECULAR AI: Stateful, builds on all past experiences

Memory structure:
{
    "decisions": [...],
    "outcomes": [...],
    "mistakes": [...],
    "wisdom": [...],
    "goals": [...],
    "patterns": [...]
}

Memory never lies. It's the source of truth about what happened.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class Memory:
    """
    Persistent memory system for the molecular AI.
    
    This is the knowledge base that grows over time.
    """
    
    def __init__(self, memory_file: str = "agent_memory.json"):
        self.memory_file = Path(memory_file)
        self.data: Dict[str, Any] = {
            "decisions": [],
            "outcomes": [],
            "mistakes": [],
            "wisdom": [],
            "goals": [],
            "patterns": [],
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "version": "1.0"
            }
        }
        self._load()
    
    def _load(self):
        """Load memory from disk."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Merge with default structure
                    self.data.update(loaded)
            except Exception as e:
                print(f"Warning: Failed to load memory: {e}")
    
    def _save(self):
        """Save memory to disk."""
        try:
            self.data["metadata"]["last_updated"] = datetime.now().isoformat()
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, default=str)
        except Exception as e:
            # Memory save failure is CRITICAL
            raise RuntimeError(f"CRITICAL: Memory save failed: {e}") from e
    
    def store_decision(self, decision_data: Dict[str, Any]):
        """Store a decision in memory."""
        self.data["decisions"].append({
            **decision_data,
            "stored_at": datetime.now().isoformat()
        })
        self._save()
    
    def store_outcome(self, outcome_data: Dict[str, Any]):
        """Store an execution outcome."""
        self.data["outcomes"].append({
            **outcome_data,
            "stored_at": datetime.now().isoformat()
        })
        self._save()
    
    def store_mistake(self, mistake_data: Dict[str, Any]):
        """Store a mistake for learning."""
        self.data["mistakes"].append({
            **mistake_data,
            "stored_at": datetime.now().isoformat()
        })
        self._save()
    
    def store_wisdom(self, wisdom: str, context: Optional[Dict] = None):
        """Store extracted wisdom."""
        self.data["wisdom"].append({
            "wisdom": wisdom,
            "context": context or {},
            "stored_at": datetime.now().isoformat()
        })
        self._save()
    
    def recall_similar_decisions(self, current_decision: Dict[str, Any],
                                 limit: int = 5) -> List[Dict]:
        """
        Recall similar past decisions.
        
        This helps Brain learn from past experiences.
        """
        # Simple similarity: keyword matching
        current_approach = current_decision.get('approach', '').lower()
        current_words = set(current_approach.split())
        
        scored = []
        for past_decision in self.data["decisions"]:
            past_approach = past_decision.get('approach', '').lower()
            past_words = set(past_approach.split())
            
            # Calculate similarity (Jaccard index)
            if current_words and past_words:
                intersection = current_words & past_words
                union = current_words | past_words
                similarity = len(intersection) / len(union) if union else 0
            else:
                similarity = 0
            
            if similarity > 0:
                scored.append((similarity, past_decision))
        
        # Sort by similarity and return top matches
        scored.sort(reverse=True, key=lambda x: x[0])
        return [decision for _, decision in scored[:limit]]
    
    def get_applicable_wisdom(self, current_situation: str) -> List[str]:
        """Get wisdom applicable to current situation."""
        applicable = []
        situation_words = set(current_situation.lower().split())
        
        for wisdom_entry in self.data["wisdom"]:
            wisdom_text = wisdom_entry.get('wisdom', '').lower()
            wisdom_words = set(wisdom_text.split())
            
            # Check relevance
            overlap = situation_words & wisdom_words
            if len(overlap) >= 2:
                applicable.append(wisdom_entry['wisdom'])
        
        return applicable
    
    def get_relevant_mistakes(self, current_approach: str) -> List[Dict]:
        """Get mistakes relevant to current approach."""
        relevant = []
        approach_words = set(current_approach.lower().split())
        
        for mistake in self.data["mistakes"]:
            mistake_approach = mistake.get('approach', '').lower()
            mistake_words = set(mistake_approach.split())
            
            overlap = approach_words & mistake_words
            if len(overlap) >= 2:
                relevant.append(mistake)
        
        return relevant
    
    def get_stats(self) -> Dict[str, int]:
        """Get memory statistics."""
        return {
            "total_decisions": len(self.data["decisions"]),
            "total_outcomes": len(self.data["outcomes"]),
            "total_mistakes": len(self.data["mistakes"]),
            "total_wisdom": len(self.data["wisdom"]),
            "total_goals": len(self.data["goals"]),
            "total_patterns": len(self.data["patterns"])
        }
    
    def export_for_analysis(self) -> Dict[str, Any]:
        """Export complete memory for external analysis."""
        return self.data.copy()


if __name__ == "__main__":
    memory = Memory("test_memory.json")
    
    # Test storing
    memory.store_decision({
        "approach": "create_file_test",
        "committed": True
    })
    
    memory.store_wisdom("When creating files, validate path first")
    
    print("Memory stats:", memory.get_stats())
    
    # Test recall
    similar = memory.recall_similar_decisions({"approach": "create_file_new"})
    print(f"Similar decisions: {len(similar)}")
