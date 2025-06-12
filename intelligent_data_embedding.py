#!/usr/bin/env python3
"""
INTELLIGENT DATA EMBEDDING FOR CHANDIGARH POLICY ASSISTANT
==========================================================

This script implements a comprehensive, intelligent embedding strategy that ensures:
1. Complete data coverage - no information left behind
2. Smart chunking with context preservation
3. Multi-level granularity (document, section, subsection levels)
4. Semantic coherence and proper overlapping
5. Metadata-rich embeddings for better retrieval

Features:
- Document-level embeddings for broad queries
- Section-level embeddings for specific topics
- Detailed clause-level embeddings for precise answers
- Intelligent chunking based on content structure
- Context preservation with overlapping windows
- Rich metadata for enhanced filtering and search
"""

import os
import json
import time
import hashlib
import requests
from typing import List, Dict, Any, Tuple
from pathlib import Path
import re
from dataclasses import dataclass
from pinecone import Pinecone
import config

@dataclass
class DocumentChunk:
    """Represents a processed document chunk with metadata"""
    content: str
    chunk_type: str  # 'document', 'section', 'subsection', 'clause'
    document_name: str
    section_title: str
    metadata: Dict[str, Any]
    embedding_vector: List[float] = None
    chunk_id: str = None

class IntelligentDataEmbedder:
    """
    Comprehensive data embedding system with intelligent processing
    """
    
    def __init__(self, pinecone_api_key: str, pinecone_index: str, jina_api_key: str):
        self.pinecone_api_key = pinecone_api_key
        self.pinecone_index = pinecone_index
        self.jina_api_key = jina_api_key
        self.pc = None
        self.index = None
        
        # Processing parameters
        self.overlap_size = 150  # Words overlap between chunks
        self.min_chunk_size = 100  # Minimum words per chunk
        self.max_chunk_size = 400  # Maximum words per chunk
        self.section_chunk_size = 800  # Words for section-level chunks
        
        # Document patterns for different policy types
        self.document_patterns = {
            'ev_policy': {
                'sections': [r'(\d+\.\s+[A-Z][^.]*)', r'(CHAPTER[^:]*:?)', r'(ANNEXURE[^:]*:?)'],
                'subsections': [r'(\d+\.\d+\s+[A-Z][^.]*)', r'(\w+\s+[A-Z][^:]*:)'],
                'important_keywords': ['incentive', 'scheme', 'policy', 'registration', 'fee', 'electric', 'vehicle', 'charging']
            },
            'industrial_policy': {
                'sections': [r'(CHAPTER[^:]*:?)', r'(\d+\.\s+[A-Z][^.]*)', r'(PREAMBLE)', r'(OBJECTIVES)'],
                'subsections': [r'(\d+\.\d+\s+[A-Z][^.]*)', r'([A-Z\s]+:)'],
                'important_keywords': ['industry', 'license', 'fee', 'enterprise', 'manufacturing', 'msme', 'policy']
            },
            'excise_policy': {
                'sections': [r'(\d+\.\s+[A-Z][^.]*)', r'(About [^:]*)', r'(Annexure[^:]*)', r'(EXCISE LEVIES)'],
                'subsections': [r'(\d+\.\s+\([a-z]\))', r'(\([a-z]+\))', r'([A-Z\s]+:)'],
                'important_keywords': ['license', 'fee', 'duty', 'excise', 'liquor', 'permit', 'wholesale', 'retail']
            },
            'parking_policy': {
                'sections': [r'(\d+\.\s+[A-Z][^.]*)', r'(CHAPTER[^:]*)', r'(SECTION[^:]*)', r'(POLICY[^:]*)', r'(FEE[^:]*)'],
                'subsections': [r'(\d+\.\d+\s+[A-Z][^.]*)', r'([A-Z\s]+:)'],
                'important_keywords': ['parking', 'fee', 'zone', 'vehicle', 'permit', 'space', 'rate']
            },
            'data_policy': {
                'sections': [r'(\d+\.\s+[A-Z][^.]*)', r'(CHAPTER[^:]*)', r'(FRAMEWORK)', r'(PRINCIPLES)'],
                'subsections': [r'(\d+\.\d+\s+[A-Z][^.]*)', r'([A-Z\s]+:)'],
                'important_keywords': ['data', 'sharing', 'access', 'governance', 'privacy', 'security', 'policy']
            },
            'general': {
                'sections': [r'(\d+\.\s+[A-Z][^.]*)', r'(CHAPTER[^:]*)', r'(SECTION[^:]*)', r'([A-Z\s]{10,}:?)'],
                'subsections': [r'(\d+\.\d+\s+[A-Z][^.]*)', r'(\w+\s+[A-Z][^:]*:)'],
                'important_keywords': ['policy', 'fee', 'license', 'scheme', 'procedure', 'application']
            }
        }
        
    def initialize_connections(self):
        """Initialize Pinecone connection"""
        print("🔗 Initializing Pinecone connection...")
        self.pc = Pinecone(api_key=self.pinecone_api_key)
        self.index = self.pc.Index(self.pinecone_index)
        print("✅ Pinecone connected successfully")
    
    def get_jina_embedding(self, text: str) -> List[float]:
        """Get embedding from Jina API"""
        url = "https://api.jina.ai/v1/embeddings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.jina_api_key}"
        }
        
        data = {
            "model": "jina-embeddings-v3",
            "task": "retrieval.passage",
            "dimensions": 1024,
            "input": [text]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result['data'][0]['embedding']
        except Exception as e:
            print(f"❌ Error getting embedding from Jina: {e}")
            return None
    
    def detect_document_type(self, filename: str, content: str) -> str:
        """Detect document type based on filename and content"""
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        if 'electric' in filename_lower or 'ev' in filename_lower:
            return 'ev_policy'
        elif 'industrial' in filename_lower:
            return 'industrial_policy'
        elif 'excise' in filename_lower:
            return 'excise_policy'
        elif 'parking' in filename_lower:
            return 'parking_policy'
        elif 'data' in filename_lower:
            return 'data_policy'
        else:
            return 'general'
    
    def extract_sections(self, content: str, doc_type: str) -> List[Tuple[str, str, int, int]]:
        """Extract sections from document with positions"""
        patterns = self.document_patterns[doc_type]['sections']
        sections = []
        
        for pattern in patterns:
            matches = list(re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE))
            for match in matches:
                sections.append((
                    match.group(1).strip(),
                    match.group(0).strip(),
                    match.start(),
                    match.end()
                ))
        
        # Sort by position
        sections.sort(key=lambda x: x[2])
        return sections
    
    def create_document_level_chunk(self, content: str, filename: str, doc_type: str) -> DocumentChunk:
        """Create document-level summary chunk"""
        # Extract key information from the document
        lines = content.split('\n')
        
        # Create comprehensive document summary
        summary_parts = []
        
        # Add document title and type
        clean_filename = filename.replace('.txt', '').replace('_', ' ').title()
        summary_parts.append(f"Document: {clean_filename}")
        
        # Extract key sections and their content
        sections = self.extract_sections(content, doc_type)
        important_keywords = self.document_patterns[doc_type]['important_keywords']
        
        # Create a comprehensive summary including all major topics
        summary_parts.append(f"Type: {doc_type.replace('_', ' ').title()}")
        
        if sections:
            section_summaries = []
            for section_title, _, start, end in sections[:10]:  # Top 10 sections
                section_summaries.append(section_title)
            summary_parts.append(f"Main sections: {'; '.join(section_summaries)}")
        
        # Extract sentences containing important keywords
        keyword_sentences = []
        for line in lines[:50]:  # First 50 lines for overview
            line_clean = line.strip()
            if any(keyword in line_clean.lower() for keyword in important_keywords):
                if len(line_clean) > 20 and len(line_clean) < 200:
                    keyword_sentences.append(line_clean)
        
        if keyword_sentences:
            summary_parts.append(f"Key information: {' '.join(keyword_sentences[:5])}")
        
        # Add first few paragraphs for context
        first_content = ' '.join(lines[:10])
        summary_parts.append(f"Overview: {first_content[:500]}...")
        
        summary_content = ' '.join(summary_parts)
        
        return DocumentChunk(
            content=summary_content,
            chunk_type='document',
            document_name=clean_filename,
            section_title='Document Overview',
            metadata={
                'document_type': doc_type,
                'filename': filename,
                'level': 'document',
                'word_count': len(summary_content.split()),
                'coverage': 'complete_document'
            }
        )
    
    def create_section_chunks(self, content: str, filename: str, doc_type: str) -> List[DocumentChunk]:
        """Create section-level chunks"""
        sections = self.extract_sections(content, doc_type)
        chunks = []
        
        if not sections:
            # No clear sections found, create content-based chunks
            return self.create_content_based_chunks(content, filename, doc_type, 'section')
        
        for i, (section_title, _, start, end) in enumerate(sections):
            # Determine section content
            next_start = sections[i + 1][2] if i + 1 < len(sections) else len(content)
            section_content = content[start:next_start].strip()
            
            # Clean up section content
            section_words = section_content.split()
            
            if len(section_words) < self.min_chunk_size:
                continue
            
            # If section is too long, split it
            if len(section_words) > self.section_chunk_size:
                sub_chunks = self.split_long_section(section_content, section_title, filename, doc_type)
                chunks.extend(sub_chunks)
            else:
                chunk = DocumentChunk(
                    content=section_content,
                    chunk_type='section',
                    document_name=filename.replace('.txt', ''),
                    section_title=section_title,
                    metadata={
                        'document_type': doc_type,
                        'filename': filename,
                        'level': 'section',
                        'section_index': i,
                        'word_count': len(section_words)
                    }
                )
                chunks.append(chunk)
        
        return chunks
    
    def split_long_section(self, content: str, section_title: str, filename: str, doc_type: str) -> List[DocumentChunk]:
        """Split long sections into manageable chunks with overlap"""
        words = content.split()
        chunks = []
        
        start_idx = 0
        chunk_idx = 0
        
        while start_idx < len(words):
            end_idx = min(start_idx + self.max_chunk_size, len(words))
            
            # Find a good breaking point (sentence end)
            if end_idx < len(words):
                for i in range(end_idx, max(start_idx + self.min_chunk_size, end_idx - 50), -1):
                    if i < len(words) and words[i].endswith(('.', '!', '?', ':')):
                        end_idx = i + 1
                        break
            
            chunk_words = words[start_idx:end_idx]
            chunk_content = ' '.join(chunk_words)
            
            chunk = DocumentChunk(
                content=chunk_content,
                chunk_type='subsection',
                document_name=filename.replace('.txt', ''),
                section_title=section_title,
                metadata={
                    'document_type': doc_type,
                    'filename': filename,
                    'level': 'subsection',
                    'chunk_index': chunk_idx,
                    'word_count': len(chunk_words),
                    'parent_section': section_title
                }
            )
            chunks.append(chunk)
            
            # Move to next chunk with overlap
            start_idx = max(start_idx + self.max_chunk_size - self.overlap_size, end_idx - self.overlap_size)
            chunk_idx += 1
        
        return chunks
    
    def create_content_based_chunks(self, content: str, filename: str, doc_type: str, level: str) -> List[DocumentChunk]:
        """Create chunks based on content structure when no clear sections exist"""
        lines = content.split('\n')
        chunks = []
        current_chunk = []
        current_words = 0
        chunk_idx = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            line_words = len(line.split())
            
            # Check if we should start a new chunk
            if (current_words + line_words > self.max_chunk_size and 
                current_words >= self.min_chunk_size):
                
                # Create chunk from current content
                chunk_content = ' '.join(current_chunk)
                chunk = DocumentChunk(
                    content=chunk_content,
                    chunk_type=level,
                    document_name=filename.replace('.txt', ''),
                    section_title=f"Section {chunk_idx + 1}",
                    metadata={
                        'document_type': doc_type,
                        'filename': filename,
                        'level': level,
                        'chunk_index': chunk_idx,
                        'word_count': current_words,
                        'auto_generated': True
                    }
                )
                chunks.append(chunk)
                
                # Start new chunk with overlap
                overlap_lines = current_chunk[-3:] if len(current_chunk) >= 3 else current_chunk
                current_chunk = overlap_lines + [line]
                current_words = sum(len(l.split()) for l in current_chunk)
                chunk_idx += 1
            else:
                current_chunk.append(line)
                current_words += line_words
        
        # Add final chunk
        if current_chunk and current_words >= self.min_chunk_size:
            chunk_content = ' '.join(current_chunk)
            chunk = DocumentChunk(
                content=chunk_content,
                chunk_type=level,
                document_name=filename.replace('.txt', ''),
                section_title=f"Section {chunk_idx + 1}",
                metadata={
                    'document_type': doc_type,
                    'filename': filename,
                    'level': level,
                    'chunk_index': chunk_idx,
                    'word_count': current_words,
                    'auto_generated': True,
                    'final_chunk': True
                }
            )
            chunks.append(chunk)
        
        return chunks
    
    def create_detailed_chunks(self, content: str, filename: str, doc_type: str) -> List[DocumentChunk]:
        """Create detailed, fine-grained chunks for specific queries"""
        chunks = []
        
        # Split by paragraphs and process each
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        current_chunk = []
        current_words = 0
        chunk_idx = 0
        
        for para in paragraphs:
            para_words = len(para.split())
            
            # If paragraph is very long, split it further
            if para_words > self.max_chunk_size:
                # Create chunk from accumulated content if any
                if current_chunk:
                    chunk_content = ' '.join(current_chunk)
                    chunk = DocumentChunk(
                        content=chunk_content,
                        chunk_type='clause',
                        document_name=filename.replace('.txt', ''),
                        section_title=f"Detailed Section {chunk_idx + 1}",
                        metadata={
                            'document_type': doc_type,
                            'filename': filename,
                            'level': 'clause',
                            'chunk_index': chunk_idx,
                            'word_count': current_words,
                            'granular': True
                        }
                    )
                    chunks.append(chunk)
                    current_chunk = []
                    current_words = 0
                    chunk_idx += 1
                
                # Split long paragraph
                sentences = re.split(r'[.!?]+', para)
                temp_chunk = []
                temp_words = 0
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    
                    sent_words = len(sentence.split())
                    
                    if temp_words + sent_words > self.max_chunk_size and temp_words >= self.min_chunk_size:
                        chunk_content = '. '.join(temp_chunk) + '.'
                        chunk = DocumentChunk(
                            content=chunk_content,
                            chunk_type='clause',
                            document_name=filename.replace('.txt', ''),
                            section_title=f"Detailed Section {chunk_idx + 1}",
                            metadata={
                                'document_type': doc_type,
                                'filename': filename,
                                'level': 'clause',
                                'chunk_index': chunk_idx,
                                'word_count': temp_words,
                                'granular': True,
                                'split_paragraph': True
                            }
                        )
                        chunks.append(chunk)
                        temp_chunk = [sentence]
                        temp_words = sent_words
                        chunk_idx += 1
                    else:
                        temp_chunk.append(sentence)
                        temp_words += sent_words
                
                # Add remaining content to current chunk
                if temp_chunk:
                    current_chunk.extend(temp_chunk)
                    current_words += temp_words
            
            elif current_words + para_words > self.max_chunk_size and current_words >= self.min_chunk_size:
                # Create chunk and start new one
                chunk_content = ' '.join(current_chunk)
                chunk = DocumentChunk(
                    content=chunk_content,
                    chunk_type='clause',
                    document_name=filename.replace('.txt', ''),
                    section_title=f"Detailed Section {chunk_idx + 1}",
                    metadata={
                        'document_type': doc_type,
                        'filename': filename,
                        'level': 'clause',
                        'chunk_index': chunk_idx,
                        'word_count': current_words,
                        'granular': True
                    }
                )
                chunks.append(chunk)
                current_chunk = [para]
                current_words = para_words
                chunk_idx += 1
            else:
                current_chunk.append(para)
                current_words += para_words
        
        # Add final chunk
        if current_chunk and current_words >= self.min_chunk_size:
            chunk_content = ' '.join(current_chunk)
            chunk = DocumentChunk(
                content=chunk_content,
                chunk_type='clause',
                document_name=filename.replace('.txt', ''),
                section_title=f"Detailed Section {chunk_idx + 1}",
                metadata={
                    'document_type': doc_type,
                    'filename': filename,
                    'level': 'clause',
                    'chunk_index': chunk_idx,
                    'word_count': current_words,
                    'granular': True,
                    'final_chunk': True
                }
            )
            chunks.append(chunk)
        
        return chunks
    
    def generate_chunk_id(self, chunk: DocumentChunk) -> str:
        """Generate unique ID for chunk"""
        content_hash = hashlib.md5(chunk.content.encode()).hexdigest()[:8]
        return f"{chunk.document_name}_{chunk.chunk_type}_{chunk.metadata.get('chunk_index', 0)}_{content_hash}"
    
    def process_document(self, filepath: str) -> List[DocumentChunk]:
        """Process a single document comprehensively"""
        print(f"📄 Processing: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        filename = os.path.basename(filepath)
        doc_type = self.detect_document_type(filename, content)
        
        all_chunks = []
        
        # 1. Document-level chunk for broad queries
        print(f"  📋 Creating document-level chunk...")
        doc_chunk = self.create_document_level_chunk(content, filename, doc_type)
        all_chunks.append(doc_chunk)
        
        # 2. Section-level chunks for topic-specific queries
        print(f"  📂 Creating section-level chunks...")
        section_chunks = self.create_section_chunks(content, filename, doc_type)
        all_chunks.extend(section_chunks)
        
        # 3. Detailed chunks for specific information
        print(f"  🔍 Creating detailed chunks...")
        detailed_chunks = self.create_detailed_chunks(content, filename, doc_type)
        all_chunks.extend(detailed_chunks)
        
        # Generate IDs and add embeddings
        for chunk in all_chunks:
            chunk.chunk_id = self.generate_chunk_id(chunk)
        
        print(f"  ✅ Created {len(all_chunks)} chunks ({len([c for c in all_chunks if c.chunk_type == 'document'])} document, "
              f"{len([c for c in all_chunks if c.chunk_type == 'section'])} section, "
              f"{len([c for c in all_chunks if c.chunk_type in ['subsection', 'clause']])} detailed)")
        
        return all_chunks
    
    def embed_chunks(self, chunks: List[DocumentChunk]) -> List[DocumentChunk]:
        """Add embeddings to all chunks"""
        print(f"🔮 Generating embeddings for {len(chunks)} chunks...")
        
        embedded_chunks = []
        for i, chunk in enumerate(chunks):
            print(f"  Embedding chunk {i+1}/{len(chunks)}...")
            
            embedding = self.get_jina_embedding(chunk.content)
            if embedding:
                chunk.embedding_vector = embedding
                embedded_chunks.append(chunk)
            else:
                print(f"  ⚠️ Failed to embed chunk {i+1}, skipping...")
        
        print(f"✅ Successfully embedded {len(embedded_chunks)} chunks")
        return embedded_chunks
    
    def create_namespace_name(self, doc_type: str, level: str) -> str:
        """Create namespace name based on document type and level"""
        return f"{doc_type}_{level}"
    
    def upload_to_pinecone(self, chunks: List[DocumentChunk]):
        """Upload chunks to Pinecone with appropriate namespaces"""
        print(f"📤 Uploading {len(chunks)} chunks to Pinecone...")
        
        # Group chunks by namespace
        namespaced_chunks = {}
        for chunk in chunks:
            namespace = self.create_namespace_name(chunk.metadata['document_type'], chunk.chunk_type)
            if namespace not in namespaced_chunks:
                namespaced_chunks[namespace] = []
            namespaced_chunks[namespace].append(chunk)
        
        # Upload each namespace
        for namespace, ns_chunks in namespaced_chunks.items():
            print(f"  📂 Uploading {len(ns_chunks)} chunks to namespace: {namespace}")
            
            vectors = []
            for chunk in ns_chunks:
                vector_data = {
                    'id': chunk.chunk_id,
                    'values': chunk.embedding_vector,
                    'metadata': {
                        'content': chunk.content,
                        'chunk_type': chunk.chunk_type,
                        'document_name': chunk.document_name,
                        'section_title': chunk.section_title,
                        'filename': chunk.metadata['filename'],
                        'document_type': chunk.metadata['document_type'],
                        'level': chunk.metadata['level'],
                        'word_count': chunk.metadata['word_count']
                    }
                }
                vectors.append(vector_data)
            
            # Upload in batches
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                try:
                    self.index.upsert(vectors=batch, namespace=namespace)
                    print(f"    ✅ Uploaded batch {i//batch_size + 1}")
                except Exception as e:
                    print(f"    ❌ Error uploading batch {i//batch_size + 1}: {e}")
        
        print(f"🎉 Successfully uploaded all chunks to Pinecone!")
    
    def process_all_documents(self, txt_files_dir: str = "txt_files"):
        """Process all documents in the txt_files directory"""
        print("🚀 Starting comprehensive document processing...")
        
        # Initialize connections
        self.initialize_connections()
        
        # Get all text files
        txt_dir = Path(txt_files_dir)
        if not txt_dir.exists():
            print(f"❌ Directory {txt_files_dir} not found!")
            return
        
        txt_files = list(txt_dir.glob("*.txt"))
        print(f"📁 Found {len(txt_files)} text files to process")
        
        if not txt_files:
            print("❌ No text files found!")
            return
        
        all_chunks = []
        
        # Process each document
        for txt_file in txt_files:
            try:
                doc_chunks = self.process_document(str(txt_file))
                all_chunks.extend(doc_chunks)
            except Exception as e:
                print(f"❌ Error processing {txt_file}: {e}")
                continue
        
        if not all_chunks:
            print("❌ No chunks created!")
            return
        
        print(f"\n📊 Processing Summary:")
        print(f"  • Total chunks created: {len(all_chunks)}")
        print(f"  • Document-level chunks: {len([c for c in all_chunks if c.chunk_type == 'document'])}")
        print(f"  • Section-level chunks: {len([c for c in all_chunks if c.chunk_type == 'section'])}")
        print(f"  • Detailed chunks: {len([c for c in all_chunks if c.chunk_type in ['subsection', 'clause']])}")
        
        # Generate embeddings
        embedded_chunks = self.embed_chunks(all_chunks)
        
        if not embedded_chunks:
            print("❌ No chunks were successfully embedded!")
            return
        
        # Upload to Pinecone
        self.upload_to_pinecone(embedded_chunks)
        
        print("\n🎊 COMPREHENSIVE DATA EMBEDDING COMPLETE!")
        print(f"📈 Successfully processed and embedded {len(embedded_chunks)} chunks")
        print("🔍 Your system now has complete coverage of all policy documents!")

def main():
    """Main execution function"""
    print("🌟 CHANDIGARH POLICY ASSISTANT - INTELLIGENT DATA EMBEDDING")
    print("=" * 70)
    
    # Load configuration
    pinecone_api_key = config.PINECONE_API_KEY
    pinecone_index = config.PINECONE_INDEX
    jina_api_key = getattr(config, 'JINA_API_KEY', None)
    
    if not all([pinecone_api_key, pinecone_index, jina_api_key]):
        print("❌ Missing required API keys or configuration!")
        print("Please ensure PINECONE_API_KEY, PINECONE_INDEX, and JINA_API_KEY are set")
        return
    
    # Create embedder and process all documents
    embedder = IntelligentDataEmbedder(
        pinecone_api_key=pinecone_api_key,
        pinecone_index=pinecone_index,
        jina_api_key=jina_api_key
    )
    
    embedder.process_all_documents()

if __name__ == "__main__":
    main()