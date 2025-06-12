#!/usr/bin/env python3
"""
Process only Excise Policy and upload to Pinecone
"""

import os
import sys
from enhanced_intelligent_embedding import EnhancedPolicyProcessor
import config
import json

def process_excise_only():
    """Process only the Excise Policy file"""
    print("🚀 Processing Excise Policy Only...")
    
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
    
    # Read and process the file
    print(f"📖 Reading {test_file}...")
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(test_file)
    doc_type = processor.identify_document_type(filename, content)
    print(f"📋 Document type: {doc_type}")
    
    # Create enhanced chunks
    print(f"📦 Creating enhanced chunks...")
    chunks = processor.create_enhanced_chunks(content, filename, doc_type)
    print(f"✅ Created {len(chunks)} chunks")
    
    # Count different granularities
    granularities = {}
    for chunk in chunks:
        gran = chunk.granularity
        granularities[gran] = granularities.get(gran, 0) + 1
    
    print("📊 Chunk distribution:")
    for gran, count in granularities.items():
        print(f"   - {gran}: {count} chunks")
    
    # Upload to Pinecone
    print(f"🚀 Uploading {len(chunks)} chunks to Pinecone...")
    upload_results = processor.upload_chunks_to_pinecone(chunks)
    
    print("✅ Upload complete!")
    for namespace, count in upload_results.items():
        print(f"   - {namespace}: {count} chunks")
    
    print("🎉 Excise Policy processing complete!")

if __name__ == "__main__":
    process_excise_only() 