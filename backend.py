from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

app = FastAPI(title="Basketball Video Analysis API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create input_video directory if it doesn't exist
os.makedirs("input_video", exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Basketball Video Analysis API"}

@app.post("/upload-video")
async def upload_video(video: UploadFile = File(...)):
    """Upload a basketball video for analysis"""
    
    # Validate file type
    if not video.filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        raise HTTPException(status_code=400, detail="Only video files are allowed")
    
    try:
        # Save uploaded video to input_video directory
        input_path = f"input_video/{video.filename}"
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        
        return {
            "message": "Video uploaded successfully",
            "filename": video.filename,
            "status": "ready_for_processing"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading video: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
