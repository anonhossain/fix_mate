#!/usr/bin/env python3
"""
Demo script to show the improved prompts and functionality
without requiring Ollama to be running
"""
import json
from img_to_text import IdentifySuggestion
from prompt import detection_prompt, suggestion_prompt

def demo_improved_system():
    """Demo the improved Fix Mate system"""
    print("🔧 Fix Mate - Improved System Demo")
    print("=" * 50)
    
    # Initialize the system
    obj = IdentifySuggestion()
    print(f"📋 Loaded {len(obj.categories)} categories")
    
    # Show new repair-specific categories
    repair_cats = [cat for cat in obj.categories if any(word in cat.lower() for word in 
                   ['plumbing', 'electrical', 'hvac', 'structural', 'tools', 'safety'])]
    print(f"🔧 Repair-specific categories: {', '.join(repair_cats)}")
    
    # Show improved detection prompt
    print("\n📷 Improved Detection Prompt:")
    print("-" * 30)
    detection = detection_prompt()
    print(detection)
    
    # Show improved suggestion prompt with sample data
    print("\n💡 Improved Suggestion Prompt:")
    print("-" * 30)
    sample_detection = "Broken wooden table with snapped leg"
    suggestion = suggestion_prompt(sample_detection, obj.categories[:5])
    print(suggestion)
    
    # Show expected output format
    print("\n📊 Expected Enhanced Output Format:")
    print("-" * 35)
    expected_output = {
        "category": "Furniture",
        "damage_severity": "Medium",
        "immediate_actions": [
            "Clear area around broken table",
            "Remove any sharp wood fragments"
        ],
        "repair_suggestions": [
            "Assess if leg can be reattached with wood glue and clamps",
            "Consider professional furniture repair for structural integrity",
            "If DIY repair: sand broken surfaces, apply wood glue, clamp for 24 hours"
        ],
        "professional_help_needed": False,
        "estimated_difficulty": "Medium"
    }
    print(json.dumps(expected_output, indent=2))
    
    print("\n✅ Improvements Summary:")
    print("• Fixed file path case issue (R.jpg vs r.jpg)")
    print("• Enhanced prompts for better damage detection")
    print("• Added repair-specific categories")
    print("• Improved JSON output structure with more actionable fields")
    print("• Added model parameters for better consistency")
    print("• Better error handling and fallbacks")
    print("• Consolidated prompt management")

if __name__ == "__main__":
    demo_improved_system()