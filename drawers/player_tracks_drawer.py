from .utils import draw_ellipse

class PlayerTracksDrawer:
    def __init__(self, team_1_color = (255, 234, 238), team_2_color = (128, 0, 0)):
        self.default_player_team_id = 1
        self.team_1_color = team_1_color
        self.team_2_color = team_2_color
    
    def draw_tracks(self, video_frames, tracks, player_assignment, ball_acquisition=None):

        output_video_frames = []
        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()

            player_dict = tracks[frame_num]

            player_assignment_for_frame = player_assignment[frame_num]
            
            #draw players tracks
            for track_id, player in player_dict.items():
                team_id = player_assignment_for_frame.get(track_id, self.default_player_team_id)

                if team_id == 1:
                    color = self.team_1_color
                else:
                    color = self.team_2_color

                frame = draw_ellipse(frame, player["bbox"], color, track_id)
                
                # Draw possession indicator if this player has the ball
                if ball_acquisition and frame_num < len(ball_acquisition):
                    if ball_acquisition[frame_num] == track_id:
                        # Draw a red possession indicator
                        frame = self.draw_possession_indicator(frame, player["bbox"])
            
            output_video_frames.append(frame)

        return output_video_frames

    def draw_possession_indicator(self, frame, bbox):
        """Draw a red possession indicator above the player's head."""
        import cv2
        
        # Get center and top of player bbox
        x_center = int((bbox[0] + bbox[2]) / 2)
        y_top = int(bbox[1])
        
        # Draw a red circle above the player's head
        cv2.circle(frame, (x_center, y_top - 30), 15, (0, 0, 255), -1)  # Red filled circle
        cv2.circle(frame, (x_center, y_top - 30), 15, (255, 255, 255), 2)  # White outline
        
        return frame