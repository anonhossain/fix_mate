from fastapi import APIRouter, UploadFile, File, HTTPException
from img_to_text import IdentifySuggestion
import os
import shutil

router = APIRouter()

# Initialize pipeline once
pipeline = IdentifySuggestion()


# @router.post("/analyze-image")
# async def analyze_image(file: UploadFile = File(...)):
#     """
#     Upload an image → Run AI pipeline → Return JSON result + file path.
#     """
#     try:
#         # Save uploaded file into pipeline's file directory
#         save_path = os.path.join(pipeline.file_dir, file.filename)
#         with open(save_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         # Run pipeline
#         result_json, result_file = pipeline.run_pipeline(file.filename)

#         return {"result": result_json, "file_saved": result_file}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/categories")
async def list_categories():
    """
    Get all available categories from resources/category.json.
    """
    try:
        return {"categories": pipeline.categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
import shutil
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any
from img_to_text import IdentifySuggestion  # Assuming IdentifySuggestion is in the 'identify.py' file

# Initialize pipeline once
pipeline = IdentifySuggestion()

# Create a thread pool executor for background tasks
executor = ThreadPoolExecutor(max_workers=1)

router = APIRouter()

@router.post("/analyze-image")
async def analyze_image(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Upload an image → Run AI pipeline in background → Return immediate dummy result.
    """
    try:
        # Save uploaded file into pipeline's file directory
        save_path = os.path.join(pipeline.file_dir, file.filename)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Dummy data to return immediately
        dummy_result = {
            "category": "Furniture",
            "suggestions": [
                "Remove all broken wood splinters and debris from the floor to prevent tripping or cuts.",
                "Wear protective gloves and eye protection when handling or disposing of damaged table pieces.",
                "Secure the area by marking it with caution tape or placing a warning sign until the damaged table is fully removed or repaired."
            ]
        }

        # Run background task in a separate thread
        background_tasks.add_task(run_pipeline_in_background, file.filename)

        # Return dummy data immediately
        return {"result": dummy_result, "status": "Processing started, please check back later."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Background task to handle the AI pipeline asynchronously
def run_pipeline_in_background(image_filename: str):
    try:
        # Run pipeline in the background using the ThreadPoolExecutor
        result_json, result_file = pipeline.run_pipeline(image_filename)
        
        # Log or save the result
        print(f"Pipeline complete for {image_filename}. Result saved at {result_file}")
    except Exception as e:
        print(f"Error in pipeline processing: {e}")