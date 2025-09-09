def detection_prompt():
    return "Describe what is visible in this image with as much detail as possible. Specially describe the objects and its situation."


def suggestion_prompt(detection_text, categories):
    return (
        f"The detected object is: {detection_text}\n\n"
        f"Categories: {categories}\n\n"
        "Task: Identify which category this belongs to and provide 2-3 actionable safety suggestions "
        "in JSON format like this:\n"
        "{\n"
        '  \"category\": \"Home & Kitchen\",\n'
        '  \"suggestions\": [\"Suggestion 1\", \"Suggestion 2\"]\n'
        "}\n"
    )