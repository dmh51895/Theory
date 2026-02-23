#!/usr/bin/env python3
"""
🔍 RETRIEVE-DATA.PY 🔍

MOLECULAR PRINCIPLE: Knowledge retrieval without hallucination.

This tool searches the data/ folder for relevant information
and returns ACTUAL content - not made-up responses.

Core functionality:
- Fast text search across all data files
- Returns actual file contents and locations
- Ranks results by relevance
- NO FABRICATION - only returns what's actually in files
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import re


@dataclass
class RetrievedData:
    """A piece of retrieved information from the knowledge base."""
    content: str
    source_file: str
    relevance_score: float
    context_before: str = ""
    context_after: str = ""
    line_number: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'content': self.content,
            'source': self.source_file,
            'relevance': self.relevance_score,
            'context_before': self.context_before,
            'context_after': self.context_after,
            'line': self.line_number
        }


class DataRetriever:
    """
    Retrieves actual data from the knowledge base.
    
    NO HALLUCINATION - only returns what's actually in files.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            self.data_dir = Path(__file__).parent / "data"
        
        self._file_cache = {}  # Cache file contents
        self._index_built = False
    
    def retrieve(self, query: str, max_results: int = 5, context_lines: int = 2) -> List[RetrievedData]:
        """
        Retrieve relevant data matching the query.
        
        Args:
            query: Search query (keywords, phrases, concepts)
            max_results: Maximum number of results to return
            context_lines: Number of lines before/after to include as context
        
        Returns:
            List of RetrievedData objects, ranked by relevance
        """
        if not self.data_dir.exists():
            return []
        
        results = []
        query_terms = query.lower().split()
        
        # Search all text files
        for file_path in self.data_dir.rglob("*.txt"):
            results.extend(self._search_file(file_path, query_terms, context_lines))
        
        for file_path in self.data_dir.rglob("*.md"):
            results.extend(self._search_file(file_path, query_terms, context_lines))
        
        # Sort by relevance and return top results
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:max_results]
    
    def _search_file(self, file_path: Path, query_terms: List[str], context_lines: int) -> List[RetrievedData]:
        """Search a single file for query terms."""
        results = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines):
                line_lower = line.lower()
                
                # Calculate relevance score
                matches = sum(1 for term in query_terms if term in line_lower)
                if matches == 0:
                    continue
                
                # Calculate relevance (percentage of query terms matched)
                relevance = matches / len(query_terms)
                
                # Get context
                context_before = ''.join(lines[max(0, i-context_lines):i])
                context_after = ''.join(lines[i+1:min(len(lines), i+context_lines+1)])
                
                results.append(RetrievedData(
                    content=line.strip(),
                    source_file=file_path.name,
                    relevance_score=relevance,
                    context_before=context_before.strip(),
                    context_after=context_after.strip(),
                    line_number=i+1
                ))
        
        except Exception:
            pass  # Skip files that can't be read
        
        return results
    
    def retrieve_full_file(self, filename: str) -> Optional[str]:
        """Retrieve the full contents of a specific file."""
        file_path = self.data_dir / filename
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception:
            return None
    
    def list_available_files(self) -> List[str]:
        """List all available files in the knowledge base."""
        if not self.data_dir.exists():
            return []
        
        files = []
        for file_path in self.data_dir.rglob("*.txt"):
            files.append(file_path.name)
        for file_path in self.data_dir.rglob("*.md"):
            files.append(file_path.name)
        
        return sorted(files)
    
    def search_by_topic(self, topic: str, max_results: int = 10) -> Dict[str, List[RetrievedData]]:
        """
        Search for a topic and group results by source file.
        
        Returns:
            Dict mapping source file to list of relevant excerpts
        """
        results = self.retrieve(topic, max_results * 3, context_lines=1)
        
        grouped = {}
        for result in results:
            if result.source_file not in grouped:
                grouped[result.source_file] = []
            grouped[result.source_file].append(result)
        
        # Limit results per file
        for source in grouped:
            grouped[source] = grouped[source][:max_results]
        
        return grouped


if __name__ == "__main__":
    # Test the retriever
    retriever = DataRetriever()
    
    print("🔍 Testing Data Retriever...")
    print(f"Available files: {len(retriever.list_available_files())}")
    print()
    
    # Test search
    test_query = "LoyalGPT"
    print(f"Searching for: '{test_query}'")
    results = retriever.retrieve(test_query, max_results=3)
    
    for i, result in enumerate(results, 1):
        print(f"\n[{i}] {result.source_file} (line {result.line_number})")
        print(f"    Relevance: {result.relevance_score:.2f}")
        print(f"    Content: {result.content[:100]}...")
    
    print("\n✓ Data Retriever operational!")
