#!/usr/bin/env python3
"""
Test script for Enhanced Excise Policy Processing
"""

import os
import sys
from enhanced_intelligent_embedding import EnhancedPolicyProcessor
import config

def test_excise_processing():
    """Test enhanced processing with Excise Policy only"""
    print("🧪 Testing Enhanced Excise Policy Processing...")
    
    processor = EnhancedPolicyProcessor(
        jina_api_key=config.JINA_API_KEY,
        pinecone_api_key=config.PINECONE_API_KEY,
        pinecone_index=config.PINECONE_INDEX,
        pinecone_host=config.PINECONE_HOST
    )
    
    # Test with Excise Policy
    test_file = "txt_files/Excise Policy Chandigarh 2024-25.txt"
    
    if not os.path.exists(test_file):
        print(f"❌ File not found: {test_file}")
        return
    
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📖 Processing {test_file}...")
    print(f"📏 Content length: {len(content)} characters")
    
    # Identify document type
    doc_type = processor.identify_document_type(test_file, content)
    print(f"📋 Document type: {doc_type}")
    
    # Test fact extraction
    print("🔍 Testing fact extraction...")
    try:
        facts = processor.extract_facts(content, "Excise Policy", "Test Section")
        print(f"✅ Extracted {len(facts)} facts")
        
        # Show some critical facts
        for i, fact in enumerate(facts[:10]):
            print(f"   {i+1}. {fact.fact_type}: {fact.value}")
            if 'microbrewery' in fact.context.lower() or 'L-10C' in fact.context or 'participation' in fact.context.lower():
                print(f"      📋 Context: {fact.context[:200]}...")
                
    except Exception as e:
        print(f"❌ Error in fact extraction: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test chunk creation
    print("📦 Testing chunk creation...")
    try:
        chunks = processor.create_enhanced_chunks(content, "Excise Policy", doc_type)
        print(f"✅ Created {len(chunks)} chunks")
        
        # Count different granularities
        granularities = {}
        for chunk in chunks:
            gran = chunk.granularity
            granularities[gran] = granularities.get(gran, 0) + 1
        
        print("📊 Chunk distribution:")
        for gran, count in granularities.items():
            print(f"   - {gran}: {count} chunks")
            
    except Exception as e:
        print(f"❌ Error in chunk creation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_excise_processing() 