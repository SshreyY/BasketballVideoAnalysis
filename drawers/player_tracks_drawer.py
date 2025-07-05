from .utils import draw_ellipse

class PlayerTracksDrawer:
    def __init__(self):
        pass
    
    def draw_tracks(self, video_frames, tracks):

        output_video_frames = []
        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()

            player_dict = tracks[frame_num]
            
            #draw players tracks
            for track_id, player in player_dict.items():
                frame = draw_ellipse(frame, player["box"], (0,0,255), track_id)
            output_video_frames.append(frame)

        return output_video_frames

    