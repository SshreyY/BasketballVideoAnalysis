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
    
    # Determine the appropriate codec based on file extension
    file_ext = os.path.splitext(output_video_path)[1].lower()
    
    if file_ext == '.mp4':
        # For web compatibility, we need to create a proper MP4 file
        # Try multiple approaches to ensure compatibility
        
        # Approach 1: Try using H.264 codec directly
        try:
            # Try to use H.264 codec if available
            fourcc = cv2.VideoWriter_fourcc(*'H264')
            out = cv2.VideoWriter(output_video_path, fourcc, 24.0, (width, height))
            
            if out.isOpened():
                for frame in output_video_frames:
                    out.write(frame)
                out.release()
                print(f"Video saved successfully with H.264 codec to: {output_video_path}")
                return output_video_path
            else:
                out.release()
                print("H.264 codec not available, trying alternative approach")
        except Exception as e:
            print(f"H.264 codec failed: {e}")
        
        # Approach 2: Use MJPG codec which is more compatible
        try:
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            out = cv2.VideoWriter(output_video_path, fourcc, 24.0, (width, height))
            
            if out.isOpened():
                for frame in output_video_frames:
                    out.write(frame)
                out.release()
                print(f"Video saved successfully with MJPG codec to: {output_video_path}")
                return output_video_path
            else:
                out.release()
                print("MJPG codec not available, trying XVID")
        except Exception as e:
            print(f"MJPG codec failed: {e}")
        
        # Approach 3: Use XVID but save as AVI for better compatibility
        try:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            avi_path = output_video_path.replace('.mp4', '.avi')
            
            out = cv2.VideoWriter(avi_path, fourcc, 24.0, (width, height))
            
            if out.isOpened():
                for frame in output_video_frames:
                    out.write(frame)
                out.release()
                print(f"Video saved successfully as AVI with XVID codec to: {avi_path}")
                return avi_path
            else:
                out.release()
                print("XVID codec failed")
        except Exception as e:
            print(f"XVID codec failed: {e}")
        
        # Approach 4: Last resort - save as AVI with any available codec
        try:
            # Try to find any working codec
            codecs = ['XVID', 'MJPG', 'IYUV', 'YUY2']
            for codec in codecs:
                try:
                    fourcc = cv2.VideoWriter_fourcc(*codec)
                    avi_path = output_video_path.replace('.mp4', '.avi')
                    out = cv2.VideoWriter(avi_path, fourcc, 24.0, (width, height))
                    
                    if out.isOpened():
                        for frame in output_video_frames:
                            out.write(frame)
                        out.release()
                        print(f"Video saved successfully with {codec} codec to: {avi_path}")
                        return avi_path
                    else:
                        out.release()
                except Exception as e:
                    print(f"Codec {codec} failed: {e}")
                    continue
            
            print("All codecs failed, cannot save video")
            return None
            
        except Exception as e:
            print(f"Final fallback failed: {e}")
            return None
    
    else:
        # For other formats, use XVID as default
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_video_path, fourcc, 24.0, (width, height))
        
        for frame in output_video_frames:
            out.write(frame)
        
        out.release()
        print(f"Video saved successfully to: {output_video_path}")
        return output_video_path
