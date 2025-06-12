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
        # UPDATED FOR ENHANCED INTELLIGENT EMBEDDING SYSTEM (December 2024)
        # Based on actual namespaces created by enhanced processing
        self.semantic_to_actual = {
            # Electric Vehicle Policy - Multi-level granularity
            "electric-vehicles-policy": ["ev_policy_document", "ev_policy_section", "ev_policy_clause", "ev_policy_fact"],
            "electric-vehicles-guidelines": ["ev_policy_document", "ev_policy_section"],
            "ev-incentives": ["ev_policy_fact", "ev_policy_clause", "ev_policy_section"],
            "ev-targets": ["ev_policy_fact", "ev_policy_clause"],
            "ev-adoption": ["ev_policy_fact", "ev_policy_clause"],
            
            # Industrial Policy - Multi-level granularity  
            "industrial-policy-2015": ["industrial_policy_document", "industrial_policy_section", "industrial_policy_clause", "industrial_policy_fact"],
            "industrial-guidelines": ["industrial_policy_document", "industrial_policy_section"],
            "industrial-fees": ["industrial_policy_fact", "industrial_policy_clause"],
            "ease-of-business": ["industrial_policy_section", "industrial_policy_clause"],
            "building-plan-approval": ["industrial_policy_fact", "industrial_policy_clause"],
            "industrial-area": ["industrial_policy_fact", "industrial_policy_clause"],
            
            # Excise Policy - Multi-level granularity (HIGH PRIORITY for accuracy fixes)
            "excise-policy": ["excise_policy_document", "excise_policy_section", "excise_policy_clause", "excise_policy_fact"],
            "liquor-licenses": ["excise_policy_fact", "excise_policy_clause", "excise_policy_section"],
            "license-fees": ["excise_policy_fact", "excise_policy_clause"],
            "microbrewery": ["excise_policy_fact", "excise_policy_clause"],
            "participation-fee": ["excise_policy_fact", "excise_policy_clause"],
            "departmental-store": ["excise_policy_fact", "excise_policy_clause"],
            "bar-licenses": ["excise_policy_fact", "excise_policy_clause"],
            "l-10c": ["excise_policy_fact", "excise_policy_clause"],
            "l-10b": ["excise_policy_fact", "excise_policy_clause"],
            "excise-license": ["excise_policy_fact", "excise_policy_clause"],
            "bidding": ["excise_policy_fact", "excise_policy_clause"],
            
            # Parking Policy - Multi-level granularity
            "parking-policy": ["parking_policy_document", "parking_policy_section", "parking_policy_clause", "parking_policy_fact"],
            "parking-regulations": ["parking_policy_section", "parking_policy_clause"],
            "parking-fees": ["parking_policy_fact", "parking_policy_clause"],
            "population-statistics": ["parking_policy_fact", "parking_policy_clause"],
            "vehicle-statistics": ["parking_policy_fact", "parking_policy_clause"],
            "census": ["parking_policy_fact", "parking_policy_clause"],
            
            # Data Sharing Policy
            "data-sharing-policy": ["data_policy_document", "data_policy_section", "data_policy_clause", "data_policy_fact"],
            "data-access": ["data_policy_section", "data_policy_clause"],
            "data-accessibility": ["data_policy_section", "data_policy_clause"],
            
            # Construction & Demolition Waste Policy
            "cd-waste-policy": ["cd_waste_policy_document", "cd_waste_policy_section", "cd_waste_policy_clause", "cd_waste_policy_fact"],
            "waste-management": ["cd_waste_policy_section", "cd_waste_policy_clause"],
            "construction-demolition": ["cd_waste_policy_fact", "cd_waste_policy_clause"],
            
            # IT Policy
            "it-policy": ["it_policy_document", "it_policy_section", "it_policy_clause", "it_policy_fact"],
            "it-guidelines": ["it_policy_section", "it_policy_clause"],
            "ites-policy": ["it_policy_document", "it_policy_section", "it_policy_clause", "it_policy_fact"],
            "technology-park": ["it_policy_fact", "it_policy_clause"],
            "rgctp": ["it_policy_fact", "it_policy_clause"],
            "it-disposal": ["general_policy_fact", "general_policy_clause"],
            "obsolete-equipment": ["general_policy_fact", "general_policy_clause"],
            
            # General Policy Documents
            "general-policy": ["general_policy_document", "general_policy_section", "general_policy_clause", "general_policy_fact"],
            "sez-policy": ["general_policy_document", "general_policy_section", "general_policy_clause"],
            
            # Cross-cutting themes (ENHANCED for better accuracy)
            "fees-charges": ["excise_policy_fact", "industrial_policy_fact", "parking_policy_fact", "ev_policy_fact"],
            "license-requirements": ["excise_policy_fact", "industrial_policy_fact", "excise_policy_clause", "industrial_policy_clause"],
            "time-limits": ["industrial_policy_fact", "excise_policy_fact", "parking_policy_fact"],
            "area-requirements": ["industrial_policy_fact", "excise_policy_fact", "parking_policy_fact"],
            "application-process": ["industrial_policy_fact", "excise_policy_fact", "industrial_policy_clause", "excise_policy_clause"],
            "eligibility-criteria": ["ev_policy_fact", "industrial_policy_fact", "excise_policy_fact"],
        }
        
        # Create reverse mapping
        self.actual_to_semantic = {}
        for semantic, actual_list in self.semantic_to_actual.items():
            for actual in actual_list:
                if actual not in self.actual_to_semantic:
                    self.actual_to_semantic[actual] = []
                self.actual_to_semantic[actual].append(semantic)
        
        # Keywords for semantic namespace selection
        self.namespace_keywords = self._initialize_keywords()
    
    def _initialize_keywords(self):
        """Initialize keywords for each semantic namespace"""
        return {
            # Electric Vehicle namespaces (comprehensive)
            "electric-vehicles-policy": [
                "electric", "vehicle", "ev", "charging", "battery", "motor", "transport",
                "e-vehicle", "electric car", "electric transport", "green vehicle", "clean energy",
                "sustainable transport", "emission", "eco-friendly", "incentive", "subsidy",
                "registration", "infrastructure", "station", "point", "renewable"
            ],
            "electric-vehicles-guidelines": [
                "electric", "vehicle", "ev", "guidelines", "procedures", "implementation", 
                "infrastructure", "charging", "registration", "incentive"
            ],
            
            # Industrial Policy namespaces (comprehensive)  
            "industrial-policy-2015": [
                "industry", "industrial", "manufacturing", "msme", "factory", "production", 
                "business", "enterprise", "sector", "development", "investment", "infrastructure",
                "small scale", "medium scale", "micro enterprise", "startup", "policy",
                "growth", "promotion", "incentive", "subsidy", "support", "license", "permit",
                "registration", "clearance", "ease", "doing", "business", "facilitation"
            ],
            "industrial-development-policy": [
                "industry", "industrial", "development", "promotion", "investment", "manufacturing",
                "enterprise", "business", "policy", "growth", "infrastructure"
            ],
            
            # Excise Policy namespaces (comprehensive) - FIXED to match actual mapping
            "excise-policy": [
                "excise", "tax", "duty", "revenue", "alcohol", "license", "taxation",
                "fee", "charges", "rates", "collection", "assessment", "payment", "liquor",
                "wine", "beer", "spirit", "brewery", "distillery", "wholesale", "retail",
                "permit", "registration", "renewal", "compliance", "microbrewery", "micro",
                "l-10c", "l10c", "participation", "bidding", "departmental", "store"
            ],
            "liquor-licenses": [
                "liquor", "license", "permit", "alcohol", "excise", "registration", "renewal",
                "fee", "charges", "compliance", "application", "microbrewery", "l-10c"
            ],
            "license-fees": [
                "license", "fee", "fees", "charges", "cost", "amount", "payment", "deposit",
                "microbrewery", "l-10c", "participation", "bidding"
            ],
            "microbrewery": [
                "microbrewery", "micro", "brewery", "l-10c", "l10c", "beer", "brewing",
                "license", "fee", "10.00", "lac", "lakh"
            ],
            "participation-fee": [
                "participation", "fee", "bidding", "tender", "auction", "2,00,000",
                "2 lac", "2 lakh", "earnest", "money"
            ],
            
            # Parking Policy namespaces (comprehensive) - FIXED to match actual mapping
            "parking-policy": [
                "parking", "vehicle", "car", "transport", "space", "urban", "management",
                "slot", "zone", "fee", "regulation", "traffic", "mobility", "city planning",
                "meter", "charges", "violation", "penalty", "enforcement", "reserved",
                "commercial", "residential", "public", "private", "population", "census",
                "10.54", "lakh", "lac", "statistics"
            ],
            "parking-regulations": [
                "parking", "regulation", "rule", "violation", "penalty", "enforcement",
                "fee", "charges", "zone", "restriction"
            ],
            "population-statistics": [
                "population", "census", "statistics", "10.54", "lakh", "lac", "demographic",
                "people", "residents", "city", "urban"
            ],
            
            # Data Policy namespaces (comprehensive)
            "data-sharing-policy": [
                "data", "sharing", "accessibility", "information", "public", "government",
                "transparency", "citizen", "access", "privacy", "security", "digital",
                "platform", "portal", "database", "record", "document", "disclosure",
                "confidential", "classification", "protection"
            ],
            "data-accessibility-guidelines": [
                "data", "accessibility", "access", "public", "citizen", "information",
                "transparency", "sharing", "guidelines", "procedure"
            ],
            
            # Information Technology namespaces (comprehensive)
            "information-technology-policy": [
                "it", "information", "technology", "software", "digital", "computer",
                "tech", "automation", "system", "data", "cyber", "electronic",
                "digitization", "e-governance", "ites", "service", "export", "outsourcing",
                "bpo", "call center", "data processing", "software development",
                "tech services", "digital services", "disposal", "equipment", "hardware"
            ],
            "it-enabled-services-policy": [
                "ites", "it enabled", "services", "outsourcing", "bpo", "call center",
                "data processing", "software development", "tech services", "export"
            ],
            "data-disposal-guidelines": [
                "disposal", "it disposal", "equipment", "hardware", "electronic", "waste",
                "recycling", "destruction", "security", "data"
            ],
            
            # Special Economic Zone namespaces (comprehensive)
            "special-economic-zones-policy": [
                "sez", "zone", "economic", "special", "export", "business", "tax",
                "economic zone", "industrial zone", "free trade", "customs", "duty free",
                "investment", "manufacturing hub", "export promotion", "industry", "industries",
                "developer", "unit", "infrastructure", "facility", "exemption"
            ],
            "sez-regulations": [
                "sez", "special economic zone", "regulation", "rule", "compliance",
                "developer", "unit", "export", "duty free"
            ],
            
            # Waste Management namespaces (comprehensive)
            "construction-demolition-waste": [
                "construction", "demolition", "waste", "debris", "material", "recycling",
                "disposal", "management", "building", "concrete", "rubble", "brick",
                "steel", "wood", "processing", "facility", "segregation", "collection"
            ],
            "waste-management-policy": [
                "waste", "management", "disposal", "recycling", "collection", "treatment",
                "segregation", "processing", "facility"
            ],
            
            # General Policies (comprehensive)
            "general-policies": [
                "policy", "general", "administration", "governance", "public", "government",
                "regulation", "guideline", "procedure", "rule", "law", "citizen", "service",
                "implementation", "compliance", "authority", "department"
            ],
            "all-policies": [
                "policy", "policies", "all", "comprehensive", "complete", "overview",
                "summary", "general", "multiple", "various", "different", "cross"
            ]
        }
    
    def get_actual_namespace(self, semantic_name):
        """Convert semantic namespace name to actual Pinecone namespace names"""
        return self.semantic_to_actual.get(semantic_name, [semantic_name])
    
    def get_semantic_namespace(self, actual_name):
        """Convert actual Pinecone namespace name to semantic names"""
        return self.actual_to_semantic.get(actual_name, [actual_name])
    
    def get_all_semantic_namespaces(self):
        """Get list of all semantic namespace names"""
        return list(self.semantic_to_actual.keys())
    
    def get_all_actual_namespaces(self):
        """Get list of all actual namespace names"""
        all_actual = []
        for namespace_list in self.semantic_to_actual.values():
            all_actual.extend(namespace_list)
        return list(set(all_actual))
    
    def translate_namespaces(self, namespaces, to_actual=True):
        """
        Translate a list of namespaces
        
        Args:
            namespaces: List of namespace names
            to_actual: If True, convert semantic to actual. If False, convert actual to semantic
            
        Returns:
            List of translated namespace names (flattened)
        """
        if to_actual:
            result = []
            for ns in namespaces:
                actual_namespaces = self.get_actual_namespace(ns)
                result.extend(actual_namespaces)
            return list(set(result))  # Remove duplicates
        else:
            result = []
            for ns in namespaces:
                semantic_namespaces = self.get_semantic_namespace(ns)
                result.extend(semantic_namespaces)
            return list(set(result))  # Remove duplicates
    
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
            "Waste Management": ["construction-demolition-waste", "waste-management-policy"],
            "Urban Development": ["parking-management-policy"],
            "Taxation": ["excise-taxation-policy"],
            "Information Technology": ["information-technology-policy", "it-enabled-services-policy", "data-sharing-policy"],
            "Special Economic Zones": ["special-economic-zones-policy"],
            "General Policies": ["general-policies"]
        }
        
        for category, semantic_names in categories.items():
            info["categories"][category] = []
            for semantic_name in semantic_names:
                if semantic_name in self.semantic_to_actual:
                    actual_names = self.semantic_to_actual[semantic_name]
                    for actual in actual_names:
                        mapping = {
                            "semantic": semantic_name,
                            "actual": actual,
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