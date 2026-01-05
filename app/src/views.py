# views.py
from fastapi import APIRouter, UploadFile, File
from pipeline import SimpleSafetyChain  # or img_to_text

router = APIRouter()
pipeline = SimpleSafetyChain()

@router.post("/analyze")
async def analyze_image(image: UploadFile = File(...)):
    file_bytes = await image.read()
    output = pipeline.analyze(file_bytes)
    return {"status": "success", "data": output}
