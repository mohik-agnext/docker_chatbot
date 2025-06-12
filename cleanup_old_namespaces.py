#!/usr/bin/env python3
"""
Cleanup old namespaces that might be interfering with enhanced system
"""

import config
from pinecone import Pinecone

def cleanup_old_namespaces():
    """Clean up old namespaces"""
    print("🧹 Cleaning up old namespaces...")
    
    pc = Pinecone(api_key=config.PINECONE_API_KEY)
    index = pc.Index(config.PINECONE_INDEX)
    
    # List of old namespaces to remove
    old_namespaces = [
        'excise_policy',
        'industrial_policy', 
        'ev_policy',
        'parking_policy',
        'data_policy',
        'general_policy'
    ]
    
    stats = index.describe_index_stats()
    existing_namespaces = list(stats['namespaces'].keys())
    
    print(f"📊 Found {len(existing_namespaces)} total namespaces")
    
    for old_ns in old_namespaces:
        if old_ns in existing_namespaces:
            try:
                print(f"🗑️ Deleting old namespace: {old_ns}")
                index.delete(namespace=old_ns, delete_all=True)
                print(f"✅ Deleted {old_ns}")
            except Exception as e:
                print(f"❌ Error deleting {old_ns}: {e}")
        else:
            print(f"ℹ️ Namespace {old_ns} not found (already clean)")
    
    # Check final state
    final_stats = index.describe_index_stats()
    final_namespaces = list(final_stats['namespaces'].keys())
    
    print(f"\n📊 Final state: {len(final_namespaces)} namespaces")
    print("Enhanced namespaces present:")
    for ns in sorted(final_namespaces):
        if any(suffix in ns for suffix in ['_fact', '_clause', '_section', '_document']):
            print(f"  ✅ {ns}: {final_stats['namespaces'][ns]['vector_count']} vectors")

if __name__ == "__main__":
    cleanup_old_namespaces() 