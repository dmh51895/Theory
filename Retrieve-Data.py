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
        """Search a single file for query terms with smart context extraction."""
        results = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Special handling for MASTER.md - extract complete definitions
            if file_path.name == "MASTER.md":
                return self._search_master_md(content, query_terms, file_path.name)
            
            # For other files, use paragraph-based search
            lines = content.split('\n')
            paragraphs = self._extract_paragraphs(lines)
            
            for para in paragraphs:
                para_lower = para['text'].lower()
                
                # Calculate relevance score
                matches = sum(1 for term in query_terms if term in para_lower)
                if matches == 0:
                    continue
                
                # Better relevance scoring: matches + bonus for exact phrases
                relevance = matches / len(query_terms)
                
                # Bonus for exact phrase matches
                query_phrase = ' '.join(query_terms)
                if query_phrase in para_lower:
                    relevance += 0.5
                
                # Cap at 1.0
                relevance = min(relevance, 1.0)
                
                results.append(RetrievedData(
                    content=para['text'].strip(),
                    source_file=file_path.name,
                    relevance_score=relevance,
                    context_before="",
                    context_after="",
                    line_number=para['line_start']
                ))
        
        except Exception:
            pass  # Skip files that can't be read
        
        return results
    
    def _search_master_md(self, content: str, query_terms: List[str], filename: str) -> List[RetrievedData]:
        """
        Search MASTER.md with special handling for its format.
        Extracts COMPLETE definition entries, not truncated lines.
        """
        results = []
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i]
            line_lower = line.lower()
            
            # Look for definition entries: - **word** (n): definition
            if line.strip().startswith('- **'):
                # Extract the complete entry (may span multiple lines until next bullet)
                entry_lines = [line]
                j = i + 1
                
                # Keep reading until we hit another bullet point or empty section
                while j < len(lines):
                    next_line = lines[j].strip()
                    # Stop at next bullet point or major section
                    if next_line.startswith('- **') or next_line.startswith('## ') or next_line.startswith('# '):
                        break
                    # Include continuation lines
                    if next_line:
                        entry_lines.append(lines[j])
                    j += 1
                
                # Combine into complete entry
                full_entry = ' '.join(entry_lines).strip()
                full_entry_lower = full_entry.lower()
                
                # Check if this entry matches query
                matches = sum(1 for term in query_terms if term in full_entry_lower)
                if matches > 0:
                    relevance = matches / len(query_terms)
                    
                    # Bonus for matches in the word itself (before the colon)
                    if ':' in full_entry:
                        word_part = full_entry.split(':', 1)[0].lower()
                        word_matches = sum(1 for term in query_terms if term in word_part)
                        if word_matches > 0:
                            relevance += 0.3
                    
                    # Bonus for exact phrase
                    query_phrase = ' '.join(query_terms)
                    if query_phrase in full_entry_lower:
                        relevance += 0.5
                    
                    relevance = min(relevance, 1.0)
                    
                    results.append(RetrievedData(
                        content=full_entry,
                        source_file=filename,
                        relevance_score=relevance,
                        context_before="",
                        context_after="",
                        line_number=i+1
                    ))
                
                # Move to the end of this entry
                i = j
            else:
                i += 1
        
        return results
    
    def _extract_paragraphs(self, lines: List[str]) -> List[Dict[str, Any]]:
        """
        Extract logical paragraphs from lines.
        A paragraph is consecutive non-empty lines.
        """
        paragraphs = []
        current_para = []
        para_start_line = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            if stripped:
                if not current_para:
                    para_start_line = i + 1
                current_para.append(line)
            else:
                if current_para:
                    paragraphs.append({
                        'text': ' '.join(current_para),
                        'line_start': para_start_line
                    })
                    current_para = []
        
        # Don't forget the last paragraph
        if current_para:
            paragraphs.append({
                'text': ' '.join(current_para),
                'line_start': para_start_line
            })
        
        return paragraphs
    
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
