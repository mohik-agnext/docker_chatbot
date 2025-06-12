#!/usr/bin/env python3
"""
Test script for Enhanced Intelligent Data Embedding System
Tests with just one document to verify functionality.
"""

import os
import sys
from enhanced_intelligent_embedding import EnhancedPolicyProcessor
import config

def test_enhanced_processing():
    """Test enhanced processing with one document"""
    print("🧪 Testing Enhanced Embedding System with Single Document...")
    
    processor = EnhancedPolicyProcessor(
        jina_api_key=config.JINA_API_KEY,
        pinecone_api_key=config.PINECONE_API_KEY,
        pinecone_index=config.PINECONE_INDEX,
        pinecone_host=config.PINECONE_HOST
    )
    
    # Test with Excise Policy (the problematic one)
    test_file = "txt_files/Excise Policy Chandigarh 2024-25.txt"
    
    if not os.path.exists(test_file):
        print(f"❌ Test file not found: {test_file}")
        return
    
    print(f"📄 Processing test file: {test_file}")
    
    # Read the file
    with open(test_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    print(f"📊 File size: {len(content)} characters")
    
    # Identify document type
    doc_type = processor.identify_document_type(test_file, content)
    print(f"📋 Document type: {doc_type}")
    
    # Create enhanced chunks (limit to first 5000 chars for testing)
    test_content = content[:5000] if len(content) > 5000 else content
    chunks = processor.create_enhanced_chunks(test_content, test_file, doc_type)
    
    # Count different types of chunks
    fact_chunks = [c for c in chunks if c.granularity == 'fact']
    clause_chunks = [c for c in chunks if c.granularity == 'clause']
    section_chunks = [c for c in chunks if c.granularity == 'section']
    doc_chunks = [c for c in chunks if c.granularity == 'document']
    
    print(f"✅ Created {len(chunks)} total chunks:")
    print(f"   - Facts: {len(fact_chunks)}")
    print(f"   - Clauses: {len(clause_chunks)}")
    print(f"   - Sections: {len(section_chunks)}")
    print(f"   - Document: {len(doc_chunks)}")
    
    # Test fact extraction
    if fact_chunks:
        print(f"\n🔍 Sample facts extracted:")
        for i, fact_chunk in enumerate(fact_chunks[:3]):
            fact_type = fact_chunk.metadata.get('fact_type', 'unknown')
            fact_value = fact_chunk.metadata.get('fact_value', 'unknown')
            print(f"   {i+1}. {fact_type}: {fact_value}")
    
    # Test embedding generation for a few chunks
    print(f"\n🌐 Testing embedding generation...")
    test_chunks = chunks[:3]  # Test first 3 chunks
    
    for i, chunk in enumerate(test_chunks):
        print(f"   Testing chunk {i+1}...")
        embedding = processor.get_embedding(chunk.content[:200])  # Limit content length
        print(f"   ✅ Embedding dimensions: {len(embedding)}")
        if len(embedding) != 1024:
            print(f"   ❌ ERROR: Expected 1024 dimensions, got {len(embedding)}")
            return False
    
    print(f"\n🎉 Enhanced Embedding System Test PASSED!")
    return True

if __name__ == "__main__":
    success = test_enhanced_processing()
    sys.exit(0 if success else 1) 