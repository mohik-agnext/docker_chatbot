#!/usr/bin/env python3
"""
Semantic Namespace Mapper

This module provides a virtual mapping layer that translates semantic namespace names
to the actual cryptic names in Pinecone, giving you all the benefits of semantic names
without having to copy any data.
"""

class SemanticNamespaceMapper:
    def __init__(self):
        """Initialize the semantic namespace mapper"""
        
        # Mapping from semantic names to actual Pinecone namespace names
        # UPDATED TO MATCH CURRENT DATABASE AFTER VECTOR REBUILD
        self.semantic_to_actual = {
            # Electric Vehicle namespaces (fixed underscore)
            "electric-vehicles-guidelines": "electric_vehicles6",
            
            # Industrial Policy namespaces (fixed underscores)
            "industrial-policy-2015": "industry_2015_8",
            
            # Urban Development namespaces
            "parking-management-policy": "policy_parking_policy_11",
            
            # Revenue and Taxation namespaces
            "excise-taxation-policy": "excise2",
            
            # Information Technology namespaces
            "information-technology-policy": "policy_it_10",
            
            # Special Economic Zone namespaces
            "special-economic-zones-policy": "sez5",
            
            # General Policies (new namespace after rebuild)
            "general-policies": "general_policies"
        }
        
        # Reverse mapping for converting back
        self.actual_to_semantic = {v: k for k, v in self.semantic_to_actual.items()}
        
        # Keywords for semantic namespace selection
        self.namespace_keywords = self._initialize_keywords()
    
    def _initialize_keywords(self):
        """Initialize keywords for each semantic namespace"""
        return {
            # Electric Vehicle namespaces (updated)
            "electric-vehicles-guidelines": [
                "electric", "vehicle", "ev", "charging", "battery", "motor", "transport",
                "guidelines", "procedures", "implementation", "infrastructure", "e-vehicle",
                "electric car", "electric transport", "green vehicle", "clean energy",
                "sustainable transport", "emission", "eco-friendly"
            ],
            
            # Industrial Policy namespaces (updated)  
            "industrial-policy-2015": [
                "industry", "industrial", "manufacturing", "msme", "factory", "production", 
                "business", "enterprise", "sector", "development", "investment", "infrastructure",
                "small scale", "medium scale", "micro enterprise", "startup", "policy",
                "growth", "promotion", "incentive", "subsidy", "support"
            ],
            
            # Urban Development namespaces
            "parking-management-policy": [
                "parking", "vehicle", "car", "transport", "space", "urban", "management",
                "slot", "zone", "fee", "regulation", "traffic", "mobility", "city planning"
            ],
            
            # Revenue and Taxation namespaces
            "excise-taxation-policy": [
                "excise", "tax", "duty", "revenue", "alcohol", "license", "taxation",
                "fee", "charges", "rates", "collection", "assessment", "payment"
            ],
            
            # Information Technology namespaces
            "information-technology-policy": [
                "it", "information", "technology", "software", "digital", "computer",
                "tech", "automation", "system", "data", "cyber", "electronic",
                "digitization", "e-governance", "ites", "service", "export", "outsourcing",
                "bpo", "call center", "data processing", "software development",
                "tech services", "digital services"
            ],
            
            # Special Economic Zone namespaces
            "special-economic-zones-policy": [
                "sez", "zone", "economic", "special", "export", "business", "tax",
                "economic zone", "industrial zone", "free trade", "customs", "duty free",
                "investment", "manufacturing hub", "export promotion", "industry", "industries"
            ],
            
            # General Policies (new namespace)
            "general-policies": [
                "policy", "general", "administration", "governance", "public", "government",
                "regulation", "guideline", "procedure", "rule", "law", "citizen", "service"
            ]
        }
    
    def get_actual_namespace(self, semantic_name):
        """Convert semantic namespace name to actual Pinecone namespace name"""
        return self.semantic_to_actual.get(semantic_name, semantic_name)
    
    def get_semantic_namespace(self, actual_name):
        """Convert actual Pinecone namespace name to semantic name"""
        return self.actual_to_semantic.get(actual_name, actual_name)
    
    def get_all_semantic_namespaces(self):
        """Get list of all semantic namespace names"""
        return list(self.semantic_to_actual.keys())
    
    def get_all_actual_namespaces(self):
        """Get list of all actual namespace names"""
        return list(self.semantic_to_actual.values())
    
    def translate_namespaces(self, namespaces, to_actual=True):
        """
        Translate a list of namespaces
        
        Args:
            namespaces: List of namespace names
            to_actual: If True, convert semantic to actual. If False, convert actual to semantic
            
        Returns:
            List of translated namespace names
        """
        if to_actual:
            return [self.get_actual_namespace(ns) for ns in namespaces]
        else:
            return [self.get_semantic_namespace(ns) for ns in namespaces]
    
    def get_relevant_semantic_namespaces(self, query, min_namespaces=3, max_namespaces=6):
        """
        Get relevant semantic namespaces for a query
        
        Args:
            query: The search query
            min_namespaces: Minimum number of namespaces to return
            max_namespaces: Maximum number of namespaces to return
            
        Returns:
            List of relevant semantic namespace names
        """
        import re
        from collections import defaultdict
        
        query = query.lower()
        query_keywords = [word for word in re.findall(r'\b\w{2,}\b', query)]
        
        # Score each semantic namespace
        namespace_scores = defaultdict(int)
        
        for semantic_namespace, keywords in self.namespace_keywords.items():
            for query_word in query_keywords:
                for keyword in keywords:
                    if query_word == keyword.lower():
                        namespace_scores[semantic_namespace] += 3
                    elif query_word in keyword.lower() or keyword.lower() in query_word:
                        namespace_scores[semantic_namespace] += 1
        
        # Special boost for policy-related queries
        if any(word in query for word in ['policy', 'regulation', 'guideline', 'procedure']):
            for semantic_namespace in self.semantic_to_actual.keys():
                if 'policy' in semantic_namespace or 'guideline' in semantic_namespace:
                    namespace_scores[semantic_namespace] += 2
        
        # Sort by score
        sorted_namespaces = sorted(
            [(ns, score) for ns, score in namespace_scores.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        # Get relevant namespaces
        relevant_namespaces = [ns for ns, score in sorted_namespaces if score > 0]
        
        # Apply limits
        if len(relevant_namespaces) > max_namespaces:
            relevant_namespaces = relevant_namespaces[:max_namespaces]
        
        if len(relevant_namespaces) < min_namespaces:
            remaining = [ns for ns in self.semantic_to_actual.keys() if ns not in relevant_namespaces]
            relevant_namespaces.extend(remaining[:min_namespaces - len(relevant_namespaces)])
        
        return relevant_namespaces
    
    def get_namespace_info(self):
        """Get detailed information about namespace mappings"""
        info = {
            "total_namespaces": len(self.semantic_to_actual),
            "mappings": [],
            "categories": {}
        }
        
        # Group by categories
        categories = {
            "Electric Vehicles": ["electric-vehicles-policy", "electric-vehicles-guidelines"],
            "Industrial Policy": ["industrial-policy-2015", "industrial-development-policy"],
            "Waste Management": ["waste-disposal-guidelines", "construction-demolition-waste"],
            "Urban Development": ["parking-management-policy"],
            "Taxation": ["excise-taxation-policy"],
            "Information Technology": ["information-technology-policy", "it-enabled-services-policy", "data-sharing-guidelines"],
            "Special Economic Zones": ["special-economic-zones-policy"]
        }
        
        for category, semantic_names in categories.items():
            info["categories"][category] = []
            for semantic_name in semantic_names:
                if semantic_name in self.semantic_to_actual:
                    actual_name = self.semantic_to_actual[semantic_name]
                    mapping = {
                        "semantic": semantic_name,
                        "actual": actual_name,
                        "category": category
                    }
                    info["mappings"].append(mapping)
                    info["categories"][category].append(mapping)
        
        return info

# Create global instance
semantic_mapper = SemanticNamespaceMapper()

def demo_semantic_mapping():
    """Demonstrate the semantic namespace mapping"""
    print("🎯 Semantic Namespace Mapping Demo")
    print("="*60)
    
    mapper = SemanticNamespaceMapper()
    
    # Show all mappings
    info = mapper.get_namespace_info()
    print(f"\nTotal namespaces: {info['total_namespaces']}")
    
    for category, mappings in info["categories"].items():
        print(f"\n📂 {category}:")
        for mapping in mappings:
            print(f"   {mapping['semantic']:<35} → {mapping['actual']}")
    
    # Test queries
    test_queries = [
        "What types of industries are listed for SEZs in Chandigarh?",
        "How to apply for electric vehicle incentives?",
        "What are the waste management regulations?",
        "IT policy guidelines for software companies"
    ]
    
    print(f"\n🔍 Query Testing:")
    print("="*60)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        relevant_semantic = mapper.get_relevant_semantic_namespaces(query, max_namespaces=3)
        relevant_actual = mapper.translate_namespaces(relevant_semantic, to_actual=True)
        
        print("Semantic namespaces:")
        for i, ns in enumerate(relevant_semantic, 1):
            print(f"  {i}. {ns}")
        
        print("Actual namespaces (for Pinecone):")
        for i, ns in enumerate(relevant_actual, 1):
            print(f"  {i}. {ns}")

if __name__ == "__main__":
    demo_semantic_mapping() 