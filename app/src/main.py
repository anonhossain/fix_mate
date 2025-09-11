from fastapi import FastAPI
from views import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Fix Mate", 
    description="This is a fix app powered by AI.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins to access the API, you can specify domains as well
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="10.10.13.7", port=8080, reload=True) #localhost