def detection_prompt():
    return """Analyze this image carefully and provide a detailed description focusing on:
1. What objects are visible and their condition (damaged, broken, worn, etc.)
2. The type and extent of any damage, wear, or malfunction
3. The surrounding environment and potential safety hazards
4. Any visible structural issues, leaks, cracks, or broken parts

Be very specific about the damage you observe - include details about materials, location of damage, and severity. This information will be used to provide repair guidance."""


def suggestion_prompt(detection_text, categories):
    return f"""Based on this detailed damage assessment: {detection_text}

Available Categories: {categories}

Your task:
1. Identify the most appropriate category for this damaged item
2. Provide 3-4 specific, actionable repair/safety suggestions
3. Focus on immediate safety concerns first, then repair steps
4. Include specific tools, materials, or professional services needed

Format your response as JSON:
{{
  "category": "Most appropriate category",
  "damage_severity": "Low/Medium/High",
  "immediate_actions": ["Safety step 1", "Safety step 2"],
  "repair_suggestions": ["Repair step 1", "Repair step 2"],
  "professional_help_needed": true/false,
  "estimated_difficulty": "Easy/Medium/Hard"
}}

Provide practical, detailed guidance that someone could actually follow."""