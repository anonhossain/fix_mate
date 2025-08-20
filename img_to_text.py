import requests
import base64
import json
from prompt import detection_prompt, suggestion_prompt

class IdentifySuggestion:
    def __init__(self):
        self.api_url = "http://localhost:11434/api/generate"

        # Load categories from category.json
        with open("category.json", "r") as f:
            self.categories = [c["category_name"] for c in json.load(f)]

    def _encode_image(self, image_path):
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        return base64.b64encode(image_bytes).decode("utf-8")

    def _call_ollama(self, model, prompt, image_path=None, temperature=0.3):
        payload = {
            "model": model,
            "prompt": prompt,
            "options": {
                "temperature": temperature,
                "top_p": 0.9,
                "top_k": 40,
                "repeat_penalty": 1.1
            }
        }

        if image_path:
            image_base64 = self._encode_image(image_path)
            payload["images"] = [image_base64]

        try:
            response = requests.post(self.api_url, json=payload, stream=True, timeout=60)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error calling Ollama API: {e}")
            return f"Error: Could not connect to Ollama API. Please ensure Ollama is running on localhost:11434"

        result_text = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    result_text += data.get("response", "")
                except Exception:
                    pass
        return result_text.strip()

    def detect_with_gemma(self, image_path):
        """Step 1: Use gemma3:12b to detect objects in the image"""
        prompt = detection_prompt()
        # Use slightly higher temperature for more detailed descriptions
        result_text = self._call_ollama("gemma3:12b", prompt, image_path, temperature=0.4)

        # Save detection
        with open("detection.txt", "w", encoding="utf-8") as f:
            f.write(result_text)

        return result_text

    def analyze_with_gptoss(self, detection_text):
        """Step 2: Use gpt-oss:20b to classify + suggest"""
        prompt = suggestion_prompt(detection_text, self.categories)
        # Use lower temperature for more structured/consistent JSON output
        result_text = self._call_ollama("gpt-oss:20b", prompt, temperature=0.2)

        try:
            result_json = json.loads(result_text)
        except:
            # fallback if model adds text around JSON
            try:
                start = result_text.index("{")
                end = result_text.rindex("}") + 1
                result_json = json.loads(result_text[start:end])
            except:
                # Enhanced fallback with basic structure
                result_json = {
                    "category": "Unknown", 
                    "damage_severity": "Unknown",
                    "immediate_actions": ["Ensure area is safe", "Keep people away from damaged item"],
                    "repair_suggestions": [result_text],
                    "professional_help_needed": True,
                    "estimated_difficulty": "Unknown"
                }

        # Save final result
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(json.dumps(result_json, indent=2))

        return result_json

    def main(self, image_path):
        detection = self.detect_with_gemma(image_path)
        final_output = self.analyze_with_gptoss(detection)
        return final_output


if __name__ == "__main__":
    obj = IdentifySuggestion()
    image_path = "file/R.jpg"  # Fixed case to match actual filename
    result = obj.main(image_path)

    print("✅ Detection saved to detection.txt")
    print("✅ Final result saved to result.txt")
    print(json.dumps(result, indent=2))
