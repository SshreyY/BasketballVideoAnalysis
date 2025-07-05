import cv2
import os

def read_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    return frames


def save_video(output_video_frames, output_video_path):
    if not output_video_frames:
        print("Error: No frames to save")
        return
    
    if not os.path.exists(os.path.dirname(output_video_path)):
        os.makedirs(os.path.dirname(output_video_path))

    # Get frame dimensions
    height, width = output_video_frames[0].shape[:2]
    
    # Try different codecs if one fails
    codecs = ["XVID", "MJPG", "mp4v"]
    
    for codec in codecs:
        try:
            fourcc = cv2.VideoWriter_fourcc(*codec)  # type: ignore
            out = cv2.VideoWriter(output_video_path, fourcc, 24.0, (width, height))
            
            if not out.isOpened():
                print(f"Failed to open video writer with codec {codec}")
                continue
                
            for frame in output_video_frames:
                out.write(frame)
            
            out.release()
            print(f"Video saved successfully to: {output_video_path} using codec {codec}")
            return
            
        except Exception as e:
            print(f"Error with codec {codec}: {e}")
            continue
    
    print("Failed to save video with any codec")
