import requests
import base64
import json

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

    def _call_ollama(self, model, prompt, image_path=None):
        payload = {
            "model": model,
            "prompt": prompt,
        }

        if image_path:
            image_base64 = self._encode_image(image_path)
            payload["images"] = [image_base64]

        response = requests.post(self.api_url, json=payload, stream=True)

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
        prompt = "Describe what is visible in this image with as much detail as possible. Specially describe the objects its situation."
        result_text = self._call_ollama("gemma3:12b", prompt, image_path)

        # Save detection
        with open("detection.txt", "w", encoding="utf-8") as f:
            f.write(result_text)

        return result_text

    def analyze_with_gptoss(self, detection_text):
        """Step 2: Use gpt-oss:20b to classify + suggest"""
        prompt = (
            f"The detected object is: {detection_text}\n\n"
            f"Categories: {self.categories}\n\n"
            "Task: Identify which category this belongs to and provide 2-3 actionable safety suggestions. Give suggestions in short with all necessary details "
            "in JSON format like this:\n"
            "{\n"
            '  \"category\": \"Home & Kitchen\",\n'
            '  \"suggestions\": [\"Suggestion 1\", \"Suggestion 2\"]\n'
            "}\n"
        )

        result_text = self._call_ollama("gpt-oss:20b", prompt)

        try:
            result_json = json.loads(result_text)
        except:
            # fallback if model adds text around JSON
            try:
                start = result_text.index("{")
                end = result_text.rindex("}") + 1
                result_json = json.loads(result_text[start:end])
            except:
                result_json = {"category": "Unknown", "suggestions": [result_text]}

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
    image_path = "file/r.jpg"
    result = obj.main(image_path)

    print("✅ Detection saved to detection.txt")
    print("✅ Final result saved to result.txt")
    print(json.dumps(result, indent=2))
