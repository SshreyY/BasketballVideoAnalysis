from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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
    """Upload and analyze a basketball video"""
    
    # Validate file type
    if not video.filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        raise HTTPException(status_code=400, detail="Only video files are allowed")
    
    try:
        # Save uploaded video to input_video directory
        input_path = f"input_video/{video.filename}"
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        
        print(f"Video uploaded to: {input_path}")
        
        # Process the video using main.py functions
        try:
            from main import process_video
            
            # Generate output filename
            output_filename = f"annotated_{video.filename}"
            output_path = f"output_video/{output_filename}"
            
            print(f"Starting video processing...")
            result = process_video(input_path, output_path)
            print(f"Video processing complete: {result}")
            
            return {
                "message": "Video processed successfully",
                "input_filename": video.filename,
                "output_filename": output_filename,
                "status": "completed"
            }
            
        except ImportError as e:
            print(f"Import error: {e}")
            return {
                "message": "Video uploaded but processing failed - import error",
                "filename": video.filename,
                "status": "uploaded_only",
                "error": str(e)
            }
        except Exception as e:
            print(f"Processing error: {e}")
            return {
                "message": "Video uploaded but processing failed",
                "filename": video.filename,
                "status": "uploaded_only",
                "error": str(e)
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading video: {str(e)}")

@app.get("/output-video/{filename}")
async def get_output_video(filename: str):
    """Get the processed output video"""
    file_path = f"output_video/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Output video not found")
    
    return FileResponse(file_path, media_type="video/mp4")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
