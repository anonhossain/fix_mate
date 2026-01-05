# import os
# import json
# import base64
# from typing import Dict, Any
# from pydantic import BaseModel, Field
# from langchain_ollama import ChatOllama
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import PydanticOutputParser
# from langchain_core.messages import HumanMessage
# from langchain_core.runnables import RunnableLambda, RunnablePassthrough


# # -----------------------------------------------------------------------
# # Output Model
# # -----------------------------------------------------------------------
# class FinalOutput(BaseModel):
#     category: str = Field(..., description="Single best category")
#     suggestions: list[str] = Field(..., description="2–3 safety suggestions")


# # -----------------------------------------------------------------------
# # Simplified Pipeline Class
# # -----------------------------------------------------------------------
# class SimpleSafetyChain:
#     def __init__(self):
#         self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#         self.file_dir = os.path.join(self.project_root, "file")
#         self.output_dir = os.path.join(self.project_root, "output")
#         os.makedirs(self.output_dir, exist_ok=True)

#         # Load categories
#         with open(os.path.join(self.project_root, "file", "category.json"), "r", encoding="utf-8") as f:
#             self.categories = [c["category_name"] for c in json.load(f)]

#         # Models
#         self.vision_model = ChatOllama(model="gemma3:12b", temperature=0.0)
#         self.suggestion_model = ChatOllama(model="gpt-oss:20b", temperature=0.0)

#         # Parser
#         self.parser = PydanticOutputParser(pydantic_object=FinalOutput)

#         # === PROMPTS ===
#         self.prompt_img_describe = PromptTemplate.from_template(
#             "Describe this image in extreme detail: objects, materials, damages, actions, environment, relations. Be precise and thorough."
#         )

#         self.prompt_suggestion = PromptTemplate.from_template(
#             """
#             Image description:
#             {description}

#             Available categories: {categories}

#             TASK:
#             1. Pick the SINGLE BEST category.
#             2. Give 2–3 short, practical safety suggestions.
#             3. Return ONLY this JSON:

#             {format_instructions}
#             """
#         )
#         # === CHAIN ===
#         self.chain = (
#             # Step 1: Load image → base64
#             RunnableLambda(self._load_image)
#             # Step 2: Vision model (multimodal)
#             | {
#                 "image": lambda x: x["image_b64"],
#                 "prompt": self.prompt_img_describe
#             }
#             | RunnableLambda(self._run_vision)
#             # Step 3: Inject constants as runnables
#             | RunnablePassthrough.assign(
#                 categories=lambda x: ", ".join(self.categories),
#                 format_instructions=lambda x: self.parser.get_format_instructions()
#             )
#             # Step 4: Suggestion prompt + model + parser
#             | self.prompt_suggestion
#             | self.suggestion_model
#             | self.parser
#         )

#     # -------------------------------------------------------------------
#     # Helper: Load image to base64
#     # -------------------------------------------------------------------
#     def _load_image(self, image_filename: str) -> Dict[str, Any]:
#         image_path = os.path.join(self.file_dir, os.path.basename(image_filename))
#         if not os.path.exists(image_path):
#             raise FileNotFoundError(f"Image not found: {image_path}")
#         with open(image_path, "rb") as f:
#             b64 = base64.b64encode(f.read()).decode()
#         return {"image_b64": b64, "filename": image_filename}

#     # -------------------------------------------------------------------
#     # Helper: Run vision model with image + text
#     # -------------------------------------------------------------------
#     def _run_vision(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
#         message = HumanMessage(
#             content=[
#                 {"type": "text", "text": inputs["prompt"]},
#                 {"type": "image_url", "image_url": f"data:image/jpeg;base64,{inputs['image']}"},
#             ]
#         )
#         response = self.vision_model.invoke([message])
#         return {"description": response.content, "filename": inputs.get("filename")}

#     # -------------------------------------------------------------------
#     # Run
#     # -------------------------------------------------------------------
#     def run(self, image_filename: str):
#         result: FinalOutput = self.chain.invoke(image_filename)

#         # Save outputs
#         detection_file = os.path.join(self.output_dir, "detection.txt")
#         result_file = os.path.join(self.output_dir, "result.json")

#         # Save description (from intermediate step)
#         desc = self.chain.invoke(image_filename, include_run_info=True).get("description", "")
#         with open(detection_file, "w", encoding="utf-8") as f:
#             f.write(desc)

#         with open(result_file, "w", encoding="utf-8") as f:
#             json.dump(result.dict(), f, indent=2, ensure_ascii=False)

#         return result.dict(), result_file, detection_file
   

# if __name__ == "__main__":
#     pipeline = SimpleSafetyChain()

#     # ONE LINE:
#     result = pipeline.chain.invoke("33.jpg")

#     print(result)
#     # {'category': 'Electrical Hazard', 'suggestions': ['Turn off power', 'Use insulated tools']}
    


# import os
# import json
# import base64
# import requests
# from typing import Dict, Any
# from pydantic import BaseModel, Field
# from langchain_ollama import ChatOllama
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import PydanticOutputParser
# from langchain_core.messages import HumanMessage
# from langchain_core.runnables import RunnableLambda, RunnablePassthrough


# # -----------------------------------------------------------------------
# # Output Model
# # -----------------------------------------------------------------------
# class FinalOutput(BaseModel):
#     category: str = Field(..., description="Single best category")
#     suggestions: list[str] = Field(..., description="2–3 safety suggestions")


# # -----------------------------------------------------------------------
# # Simplified Pipeline Class
# # -----------------------------------------------------------------------
# class SimpleSafetyChain:
#     def __init__(self):
#         self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#         self.file_dir = os.path.join(self.project_root, "file")
#         self.output_dir = os.path.join(self.project_root, "output")
#         os.makedirs(self.output_dir, exist_ok=True)

#         # === NEW: Load categories from API instead of JSON ===
#         self.categories = self._load_categories_from_api()

#         # Models
#         self.vision_model = ChatOllama(model="gemma3:12b", temperature=0.0)
#         self.suggestion_model = ChatOllama(model="gpt-oss:20b", temperature=0.0)

#         # Parser
#         self.parser = PydanticOutputParser(pydantic_object=FinalOutput)

#         # === PROMPTS ===
#         self.prompt_img_describe = PromptTemplate.from_template(
#             "Describe this image in extreme detail: objects, materials, damages, actions, environment, relations. Be precise and thorough."
#         )

#         self.prompt_suggestion = PromptTemplate.from_template(
#             """
#             Image description:
#             {description}

#             Available categories: {categories}

#             TASK:
#             1. Pick the SINGLE BEST category.
#             2. Give 2–3 short, practical safety suggestions.
#             3. Return ONLY this JSON:

#             {format_instructions}
#             """
#         )

#         # === CHAIN ===
#         self.chain = (
#             RunnableLambda(self._load_image)
#             | {
#                 "image": lambda x: x["image_b64"],
#                 "prompt": self.prompt_img_describe
#             }
#             | RunnableLambda(self._run_vision)
#             | RunnablePassthrough.assign(
#                 categories=lambda x: ", ".join(self.categories),
#                 format_instructions=lambda x: self.parser.get_format_instructions()
#             )
#             | self.prompt_suggestion
#             | self.suggestion_model
#             | self.parser
#         )

#     # ===================================================================
#     # 🔥 NEW: Load categories from API endpoint
#     # ===================================================================
#     def _load_categories_from_api(self):
#         url = "http://10.10.13.74:7000/service/service-categories/"
#         try:
#             response = requests.get(url, timeout=5)
#             response.raise_for_status()

#             data = response.json()

#             # Extract category names
#             categories = [item["name"] for item in data]

#             if not categories:
#                 raise ValueError("Category list from API is empty!")

#             print("Loaded categories from API:", categories)
#             return categories

#         except Exception as e:
#             print("❌ Failed to load categories from API:", e)
#             return []

#     # -------------------------------------------------------------------
#     # Helper: Load image to base64
#     # -------------------------------------------------------------------
#     def _load_image(self, image_filename: str) -> Dict[str, Any]:
#         image_path = os.path.join(self.file_dir, os.path.basename(image_filename))
#         if not os.path.exists(image_path):
#             raise FileNotFoundError(f"Image not found: {image_path}")
#         with open(image_path, "rb") as f:
#             b64 = base64.b64encode(f.read()).decode()
#         return {"image_b64": b64, "filename": image_filename}

#     # -------------------------------------------------------------------
#     # Helper: Run vision model with image + text
#     # -------------------------------------------------------------------
#     def _run_vision(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
#         message = HumanMessage(
#             content=[
#                 {"type": "text", "text": inputs["prompt"]},
#                 {"type": "image_url", "image_url": f"data:image/jpeg;base64,{inputs['image']}"},
#             ]
#         )
#         response = self.vision_model.invoke([message])
#         return {"description": response.content, "filename": inputs.get("filename")}

#     # -------------------------------------------------------------------
#     # Run Pipeline
#     # -------------------------------------------------------------------
#     def run(self, image_filename: str):
#         result: FinalOutput = self.chain.invoke(image_filename)

#         detection_file = os.path.join(self.output_dir, "detection.txt")
#         result_file = os.path.join(self.output_dir, "result.json")

#         desc = self.chain.invoke(image_filename, include_run_info=True).get("description", "")
#         with open(detection_file, "w", encoding="utf-8") as f:
#             f.write(desc)

#         with open(result_file, "w", encoding="utf-8") as f:
#             json.dump(result.dict(), f, indent=2, ensure_ascii=False)

#         return result.dict(), result_file, detection_file

# if __name__ == "__main__":
#     print("🚀 Script started")

#     pipeline = SimpleSafetyChain()
#     print("Categories:", pipeline.categories)

#     result = pipeline.chain.invoke("33.jpg")
#     print("OUTPUT:", result)



# pipeline.py
import os
import json
import base64
import uuid
import requests
from typing import Dict, Any
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableLambda, RunnablePassthrough


class FinalOutput(BaseModel):
    category: str = Field(..., description="Single best category")
    suggestions: list[str] = Field(..., description="2–3 safety suggestions")


class SimpleSafetyChain:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.file_dir = os.path.join(self.project_root, "file")
        self.output_dir = os.path.join(self.project_root, "output")
        os.makedirs(self.file_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

        self.categories = self._load_categories_from_api()

        self.vision_model = ChatOllama(model="gemma3:12b", temperature=0.0)
        self.suggestion_model = ChatOllama(model="gpt-oss:20b", temperature=0.0)

        self.parser = PydanticOutputParser(pydantic_object=FinalOutput)

        self.prompt_img_describe = PromptTemplate.from_template(
            "Describe this image in extreme detail: objects, materials, damages, actions, environment, relations. Be precise and thorough."
        )

        self.prompt_suggestion = PromptTemplate.from_template("""
        Image description:
        {description}

        Available categories: {categories}

        TASK:
        1. Pick the SINGLE BEST category.
        2. Give 2–3 short, practical safety suggestions.
        3. Return ONLY this JSON:

        {format_instructions}
        """)

        self.chain = (
            RunnableLambda(self._load_image_from_bytes)
            | {
                "image": lambda x: x["image_b64"],
                "prompt": self.prompt_img_describe
            }
            | RunnableLambda(self._run_vision)
            | RunnablePassthrough.assign(
                categories=lambda x: ", ".join(self.categories),
                format_instructions=lambda x: self.parser.get_format_instructions()
            )
            | self.prompt_suggestion
            | self.suggestion_model
            | self.parser
        )

    def _load_categories_from_api(self):
        url = "http://10.10.13.74:7000/service/service-categories/"
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            return [item["name"] for item in r.json()]
        except Exception as e:
            print("Failed to load categories:", e)
            return []

    def _load_image_from_bytes(self, file_bytes: bytes) -> Dict[str, Any]:
        b64 = base64.b64encode(file_bytes).decode()
        return {"image_b64": b64}

    def _run_vision(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        message = HumanMessage(
            content=[
                {"type": "text", "text": inputs["prompt"]},
                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{inputs['image']}"},
            ]
        )

        response = self.vision_model.invoke([message])
        return {"description": response.content}

    def analyze(self, file_bytes: bytes):
        result: FinalOutput = self.chain.invoke(file_bytes)
        return result.dict()
