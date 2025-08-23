# Basketball Video Analysis System

A computer vision system that analyzes basketball videos to track players, detect the ball, identify court lines, and create tactical visualizations. Built as a full-stack web application with a React frontend and Python backend that integrates custom machine learning models.

## What This Project Does

This is a video analysis tool specifically designed for basketball footage. When you upload a basketball video, the system:

- Detects and tracks individual players throughout the video
- Identifies and follows the basketball's movement
- Recognizes key court lines and markings
- Generates a top-down tactical view showing player positions
- Calculates player movement speeds and distances
- Outputs an annotated video with all the tracking data overlaid

The goal was to create something that would help coaches, performance coaches, scouts, and analysts to break down the game footage more systematically so that they could manage their players' load in the game by evaluating the physicality of the game, on-court running, and overall player exertion levels. This data helps make informed decisions about player rotation, rest periods, and training intensity based on actual game demands.

## Features

### Video Processing
- **Player Detection & Tracking**: YOLO-based player detection with ByteTrack tracking
- **Ball Detection & Tracking**: Specialized ball detection model with trajectory analysis
- **Court Keypoint Detection**: Basketball court line and keypoint identification
- **Tactical View Generation**: Top-down tactical analysis view
- **Speed & Distance Analysis**: Player movement metrics and statistics

### Web Interface
- **Modern React Frontend**: Clean, responsive UI with basketball theme
- **Video Upload**: Drag-and-drop video file upload
- **Real-time Processing**: Live progress updates during analysis
- **Video Playback**: Integrated video player for processed results
- **Download Functionality**: Easy download of annotated videos

### Backend API
- **FastAPI Server**: High-performance Python backend
- **Video Processing Pipeline**: Complete ML pipeline integration
- **Format Compatibility**: Support for MP4, AVI, MOV, MKV formats
- **CORS Support**: Cross-origin resource sharing for frontend integration

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   ML Pipeline   │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (OpenCV/ML)   │
│                 │    │                 │    │                 │
│ • Video Upload  │    │ • File Handling │    │ • Player Track  │
│ • Video Player  │    │ • ML Pipeline   │    │ • Ball Detect   │
│ • Download      │    │ • Video Serving │    │ • Court Detect  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Technology Stack

### Frontend
- **React 19** with TypeScript
- **Modern CSS** with responsive design
- **Basketball-themed UI** with professional styling

### Backend
- **FastAPI** - High-performance Python web framework
- **Uvicorn** - ASGI server for production deployment
- **Python 3.11** - Core programming language

### Machine Learning
- **OpenCV** - Computer vision and video processing
- **PyTorch** - Deep learning framework
- **Ultralytics** - YOLO model implementation
- **Supervision** - Object detection and tracking utilities

### Video Processing
- **Multiple Codec Support** - H.264, MJPG, XVID with fallbacks
- **Format Conversion** - Automatic format optimization for web compatibility
- **Quality Preservation** - Maintains video quality during processing

## Project Structure

```
BasketballVideoAnalysis/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── App.tsx          # Main application component
│   │   ├── App.css          # Styling and basketball theme
│   │   └── index.tsx        # Application entry point
│   └── package.json         # Frontend dependencies
├── backend.py               # FastAPI backend server
├── main.py                  # Core video processing pipeline
├── models/                  # Pre-trained ML models
│   ├── player_detector.pt   # Player detection model
│   ├── ball_detector.pt     # Ball detection model
│   └── court_keypoint_detector.pt # Court detection model
├── trackers/                # Object tracking modules
│   ├── player_tracker.py    # Player tracking logic
│   └── ball_tracker.py      # Ball tracking logic
├── drawers/                 # Visualization modules
│   ├── player_tracks_drawer.py      # Player trajectory drawing
│   ├── ball_tracks_drawer.py        # Ball trajectory drawing
│   ├── court_key_points_drawer.py   # Court annotation drawing
│   ├── tactical_view_drawer.py      # Tactical view generation
│   └── speed_and_distance_drawer.py # Metrics visualization
├── utils/                   # Utility functions
│   ├── video_utils.py       # Video I/O operations
│   ├── bbox_utils.py        # Bounding box utilities
│   └── stubs_utils.py       # Data persistence utilities
├── stubs/                   # Pre-processed data cache
├── input_video/             # Uploaded video storage
├── output_video/            # Processed video output
└── requirements.txt         # Python dependencies
```

## Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 16+
- Git

### Backend Setup
```bash
# Clone the repository
git clone <repository-url>
cd BasketballVideoAnalysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python backend.py
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## Usage

### 1. Start the System
- Backend runs on `http://localhost:8000`
- Frontend runs on `http://localhost:3000`

### 2. Upload Video
- Navigate to the web interface
- Click "Choose File" to select a basketball video
- Supported formats: MP4, AVI, MOV, MKV

### 3. Process Video
- Click "Upload & Analyze" to start processing
- Wait for the ML pipeline to complete analysis
- Monitor progress in real-time

### 4. View Results
- Watch the annotated video with player tracking
- Analyze tactical view and court keypoints
- Download the processed video for further analysis

## Technical Implementation

### Video Processing Pipeline
1. **Video Input**: Read video frames using OpenCV
2. **Object Detection**: YOLO models detect players and ball
3. **Tracking**: ByteTrack algorithm tracks objects across frames
4. **Court Detection**: Identify basketball court lines and keypoints
5. **Analysis**: Calculate speed, distance, and tactical metrics
6. **Visualization**: Draw annotations and overlays
7. **Output**: Save processed video with optimal codec

### ML Model Architecture
- **Player Detection**: YOLO model trained on basketball player dataset
- **Ball Detection**: Specialized model for basketball detection
- **Court Detection**: Keypoint detection for court line identification
- **Tracking**: ByteTrack for robust multi-object tracking

### Codec Optimization
- **Primary**: H.264 for web compatibility
- **Fallback**: MJPG for broader compatibility
- **Final Fallback**: XVID with AVI format
- **Automatic Selection**: Based on system capabilities

## Performance Metrics

- **Processing Speed**: ~1.2 seconds per frame (24 FPS)
- **Accuracy**: High precision player and ball tracking
- **Format Support**: Multiple video formats with automatic conversion
- **Web Compatibility**: Optimized for browser playback

## Development Journey

### Phase 1: Core ML Pipeline
- Implemented player detection and tracking
- Added ball detection and trajectory analysis
- Created court keypoint detection system

### Phase 2: Backend Development
- Built FastAPI server with video upload handling
- Integrated ML pipeline with web interface
- Added video format compatibility and optimization

### Phase 3: Frontend Development
- Created React application with modern UI
- Implemented video upload and playback
- Added download functionality and progress tracking

### Phase 4: Integration & Optimization
- Fixed video format compatibility issues
- Optimized codec selection for web playback
- Cleaned up debug code and improved UI layout

## Troubleshooting

### Common Issues
1. **Video Not Playing**: Check if backend is running and video format is supported
2. **Upload Failures**: Ensure video file is valid and under size limits
3. **Processing Errors**: Check backend logs for ML pipeline errors

### Debug Tools
- Backend logs show processing progress and errors
- Frontend console displays video loading events
- Video file info available through API endpoints

## Future Enhancements

- **Real-time Processing**: Live video stream analysis
- **Advanced Analytics**: Player performance metrics
- **Team Strategy Analysis**: Tactical pattern recognition
- **Mobile App**: iOS/Android applications
- **Cloud Deployment**: Scalable cloud infrastructure

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- OpenCV community for computer vision tools
- Ultralytics for YOLO implementation
- FastAPI for high-performance web framework
- React team for frontend framework

---

**Built with love for basketball analytics and computer vision enthusiasts**