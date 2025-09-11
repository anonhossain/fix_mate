import requests
import base64
import json
import os
from typing import Tuple, Dict, Any, Optional


class IdentifySuggestion:
    def __init__(self, api_url: str = "http://localhost:11434/api/generate"):
        self.api_url = api_url

        # Get project root (one level up from src/)
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # resources/category.json (located in app/resources)
        category_path = os.path.join(self.project_root, "resources", "category.json")
        with open(category_path, "r", encoding="utf-8") as f:
            self.categories = [c["category_name"] for c in json.load(f)]

        # Ensure output dir (app/output)
        self.output_dir = os.path.join(self.project_root, "output")
        os.makedirs(self.output_dir, exist_ok=True)

        # Ensure file dir (app/file)
        self.file_dir = os.path.join(self.project_root, "file")
        os.makedirs(self.file_dir, exist_ok=True)

    def _encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        return base64.b64encode(image_bytes).decode("utf-8")

    def _call_ollama(self, model: str, prompt: str, image_path: Optional[str] = None) -> str:
        payload: Dict[str, Any] = {"model": model, "prompt": prompt}
        if image_path:
            payload["images"] = [self._encode_image(image_path)]

        resp = requests.post(self.api_url, json=payload, stream=True, timeout=120)
        resp.raise_for_status()

        result_text = ""
        for line in resp.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    result_text += data.get("response", "")
                except Exception:
                    pass
        return result_text.strip()

    def detect_with_gemma(self, image_path: str) -> Tuple[str, str]:
        """Step 1: Use gemma3:12b to describe objects."""
        prompt = (
            "Describe what is visible in this image with as much detail as possible. "
            "Specifically describe the objects and their situation."
        )
        result_text = self._call_ollama("gemma3:12b", prompt, image_path)
        detection_file = os.path.join(self.output_dir, "detection.txt")
        with open(detection_file, "w", encoding="utf-8") as f:
            f.write(result_text)
        return result_text, detection_file

    def analyze_with_gptoss(self, detection_text: str) -> Tuple[Dict[str, Any], str]:
        """Step 2: Classify + safety suggestions."""
        prompt = (
            f"The detected object is: {detection_text}\n\n"
            f"Categories: {self.categories}\n\n"
            "Task: Identify which category this belongs to and provide 2-3 actionable safety suggestions. "
            "Give suggestions in short with all necessary details in JSON format like this:\n"
            "{\n"
            '  \"category\": \"Home & Kitchen\",\n'
            '  \"suggestions\": [\"Suggestion 1\", \"Suggestion 2\"]\n'
            "}\n"
        )
        raw = self._call_ollama("gpt-oss:20b", prompt)

        try:
            result_json = json.loads(raw)
        except Exception:
            try:
                start = raw.index("{")
                end = raw.rindex("}") + 1
                result_json = json.loads(raw[start:end])
            except Exception:
                result_json = {"category": "Unknown", "suggestions": [raw]}

        result_file = os.path.join(self.output_dir, "result.json")
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump(result_json, f, indent=2)
        return result_json, result_file

    def run_pipeline(self, image_filename: str) -> Tuple[Dict[str, Any], str]:
        """Run the two-step pipeline on an image already saved in /file/."""
        image_path = os.path.join(self.file_dir, os.path.basename(image_filename))
        detection_text, _ = self.detect_with_gemma(image_path)
        final_output, result_file = self.analyze_with_gptoss(detection_text)
        return final_output, result_file
