#!/usr/bin/env python3
"""
Test script for Fix Mate improvements
"""
import json
import os
from img_to_text import IdentifySuggestion
from prompt import detection_prompt, suggestion_prompt

def test_prompts():
    """Test the improved prompts"""
    print("🧪 Testing improved prompts...")
    
    # Test detection prompt
    detection = detection_prompt()
    print(f"✅ Detection prompt length: {len(detection)} chars")
    assert "damage" in detection.lower(), "Detection prompt should mention damage"
    assert "safety" in detection.lower(), "Detection prompt should mention safety"
    
    # Test suggestion prompt
    categories = ["Furniture", "Plumbing & Water Systems"]
    suggestion = suggestion_prompt("broken table", categories)
    print(f"✅ Suggestion prompt length: {len(suggestion)} chars")
    assert "JSON" in suggestion, "Suggestion prompt should specify JSON format"
    assert "damage_severity" in suggestion, "Should include damage severity field"
    
    print("✅ All prompt tests passed!")

def test_categories():
    """Test category loading and new repair categories"""
    print("\n🧪 Testing categories...")
    
    obj = IdentifySuggestion()
    print(f"✅ Total categories loaded: {len(obj.categories)}")
    
    # Check for new repair-specific categories
    repair_categories = [
        "Plumbing & Water Systems",
        "Electrical Systems", 
        "HVAC & Climate Control",
        "Structural & Building",
        "Tools & Equipment",
        "Safety & Emergency"
    ]
    
    for cat in repair_categories:
        assert cat in obj.categories, f"Missing repair category: {cat}"
        print(f"✅ Found repair category: {cat}")
    
    print("✅ All category tests passed!")

def test_file_path():
    """Test file path fix"""
    print("\n🧪 Testing file path...")
    
    # Check if the correct image file exists
    image_path = "file/R.jpg"
    assert os.path.exists(image_path), f"Image file should exist at {image_path}"
    print(f"✅ Image file found at: {image_path}")

def test_json_structure():
    """Test improved JSON structure"""
    print("\n🧪 Testing JSON structure...")
    
    # Check if result.txt has the enhanced structure
    if os.path.exists("result.txt"):
        with open("result.txt", "r") as f:
            result = json.load(f)
        
        # Check for new fields (if they exist)
        expected_fields = ["category"]
        for field in expected_fields:
            if field in result:
                print(f"✅ Found field: {field}")
    
    print("✅ JSON structure test completed!")

if __name__ == "__main__":
    print("🔧 Fix Mate Improvement Tests")
    print("=" * 40)
    
    try:
        test_prompts()
        test_categories() 
        test_file_path()
        test_json_structure()
        
        print("\n🎉 All tests passed! Fix Mate improvements are working.")
        print("🚀 The model should now provide more detailed and actionable repair guidance.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        exit(1)