from copy import deepcopy
import os
import sys
import pathlib
import numpy as np
import cv2
from copy import deepcopy
from .homography import Homography

folder_path = pathlib.Path(__file__).parent.resolve()
sys.path.append(os.path.join(folder_path,"../"))
from utils import get_foot_position,measure_distance

class TacticalViewConverter:

    def __init__(self, court_image_path):
        self.court_image_path = court_image_path
        self.width = 300
        self.height = 161


        self.actual_width_in_meters = 28
        self.actual_height_in_meters = 15

        # Define keypoints in a more logical order for basketball court
        # The keypoints should map from left to right in the video frame
        self.key_points = [
        # Left baseline (0,0) - should map to leftmost detected keypoint
        (0,0),
        (0,int((0.91/self.actual_height_in_meters)*self.height)),
        (0,int((5.18/self.actual_height_in_meters)*self.height)),
        (0,int((10/self.actual_height_in_meters)*self.height)),
        (0,int((14.1/self.actual_height_in_meters)*self.height)),
        (0,int(self.height)),

        # Center line (should map to middle detected keypoints)
        (int(self.width/2),self.height),
        (int(self.width/2),0),
        
        # Left free throw line
        (int((5.79/self.actual_width_in_meters)*self.width),int((5.18/self.actual_height_in_meters)*self.height)),
        (int((5.79/self.actual_width_in_meters)*self.width),int((10/self.actual_height_in_meters)*self.height)),

        # Right free throw line
        (int(((self.actual_width_in_meters-5.79)/self.actual_width_in_meters)*self.width),int((5.18/self.actual_height_in_meters)*self.height)),
        (int(((self.actual_width_in_meters-5.79)/self.actual_width_in_meters)*self.width),int((10/self.actual_height_in_meters)*self.height)),

        # Right baseline (should map to rightmost detected keypoint)
        (self.width,int(self.height)),
        (self.width,int((14.1/self.actual_height_in_meters)*self.height)),
        (self.width,int((10/self.actual_height_in_meters)*self.height)),
        (self.width,int((5.18/self.actual_height_in_meters)*self.height)),
        (self.width,int((0.91/self.actual_height_in_meters)*self.height)),
        (self.width,0),
    ]

    def validate_keypoints(self, keypoints_list):
        keypoints_list = deepcopy(keypoints_list)

        for frame_idx, frame_keypoints in enumerate(keypoints_list):
            # Check if frame_keypoints has xy attribute and if it's not empty
            if not hasattr(frame_keypoints, 'xy') or frame_keypoints.xy is None:
                continue
                
            xy_list = frame_keypoints.xy.tolist()
            if not xy_list or len(xy_list) == 0:
                continue
                
            frame_keypoints = xy_list[0]
            
            # Get indices of detected keypoints (not (0, 0))
            detected_indices = [i for i, kp in enumerate(frame_keypoints) if kp[0] >0 and kp[1]>0]
            
            # Need at least 3 detected keypoints to validate proportions
            if len(detected_indices) < 3:
                continue
            
            invalid_keypoints = []
            # Validate each detected keypoint
            for i in detected_indices:
                # Skip if this is (0, 0)
                if frame_keypoints[i][0] == 0 and frame_keypoints[i][1] == 0:
                    continue

                # Choose two other random detected keypoints
                other_indices = [idx for idx in detected_indices if idx != i and idx not in invalid_keypoints]
                if len(other_indices) < 2:
                    continue

                # Take first two other indices for simplicity
                j, k = other_indices[0], other_indices[1]

                # Calculate distances between detected keypoints
                d_ij = measure_distance(frame_keypoints[i], frame_keypoints[j])
                d_ik = measure_distance(frame_keypoints[i], frame_keypoints[k])
                
                # Calculate distances between corresponding tactical keypoints
                t_ij = measure_distance(self.key_points[i], self.key_points[j])
                t_ik = measure_distance(self.key_points[i], self.key_points[k])

                # Calculate and compare proportions with 50% error margin
                if t_ij > 0 and t_ik > 0:
                    prop_detected = d_ij / d_ik if d_ik > 0 else float('inf')
                    prop_tactical = t_ij / t_ik if t_ik > 0 else float('inf')

                    error = (prop_detected - prop_tactical) / prop_tactical
                    error = abs(error)

                    if error >0.8:  # 80% error margin                        
                        keypoints_list[frame_idx].xy[0][i] *= 0
                        keypoints_list[frame_idx].xyn[0][i] *= 0
                        invalid_keypoints.append(i)
            
        return keypoints_list

    def transform_players_to_tactical_view(self, keypoints_list, player_tracks):
        tactical_player_positions = []
        
        for frame_idx, (frame_keypoints, frame_tracks) in enumerate(zip(keypoints_list, player_tracks)):
            # Initialize empty dictionary for this frame
            tactical_positions = {}

            # Check if frame_keypoints has xy attribute and if it's not empty
            if not hasattr(frame_keypoints, 'xy') or frame_keypoints.xy is None:
                tactical_player_positions.append(tactical_positions)
                continue
                
            xy_list = frame_keypoints.xy.tolist()
            if not xy_list or len(xy_list) == 0:
                tactical_player_positions.append(tactical_positions)
                continue
                
            frame_keypoints = xy_list[0]

            # Skip frames with insufficient keypoints
            if frame_keypoints is None or len(frame_keypoints) == 0:
                tactical_player_positions.append(tactical_positions)
                continue
            
            # Get detected keypoints for this frame
            detected_keypoints = frame_keypoints
            
            # Filter out undetected keypoints (those with coordinates (0,0))
            valid_indices = [i for i, kp in enumerate(detected_keypoints) if kp[0] > 0 and kp[1] > 0]
            
            # Need at least 2 points for coordinate transformation
            if len(valid_indices) < 2:
                tactical_player_positions.append(tactical_positions)
                continue
            
            # Use a more intelligent coordinate transformation that considers court orientation
            # Find the court boundaries from detected keypoints
            if len(valid_indices) >= 2:
                # Find leftmost and rightmost detected keypoints
                leftmost_idx = min(valid_indices, key=lambda i: detected_keypoints[i][0])
                rightmost_idx = max(valid_indices, key=lambda i: detected_keypoints[i][0])
                
                # Find topmost and bottommost detected keypoints
                topmost_idx = min(valid_indices, key=lambda i: detected_keypoints[i][1])
                bottommost_idx = max(valid_indices, key=lambda i: detected_keypoints[i][1])
                
                # Get the corresponding tactical view positions
                leftmost_tactical = self.key_points[leftmost_idx]
                rightmost_tactical = self.key_points[rightmost_idx]
                topmost_tactical = self.key_points[topmost_idx]
                bottommost_tactical = self.key_points[bottommost_idx]
                
                # Check if we need to flip the orientation
                # If the detected leftmost keypoint maps to a tactical position that's not on the left side,
                # we need to flip the mapping
                needs_flip = False
                if leftmost_tactical[0] > self.width / 2:  # Leftmost detected maps to right side of tactical
                    needs_flip = True
                elif rightmost_tactical[0] < self.width / 2:  # Rightmost detected maps to left side of tactical
                    needs_flip = True
                
                if needs_flip:
                    # Swap the tactical keypoints to correct the orientation
                    leftmost_tactical, rightmost_tactical = rightmost_tactical, leftmost_tactical
                
                # Ensure tactical keypoints are in the correct order (left < right, top < bottom)
                if leftmost_tactical[0] > rightmost_tactical[0]:
                    leftmost_tactical, rightmost_tactical = rightmost_tactical, leftmost_tactical
                if topmost_tactical[1] > bottommost_tactical[1]:
                    topmost_tactical, bottommost_tactical = bottommost_tactical, topmost_tactical
                
                # Calculate scaling factors
                court_width = detected_keypoints[rightmost_idx][0] - detected_keypoints[leftmost_idx][0]
                court_height = detected_keypoints[bottommost_idx][1] - detected_keypoints[topmost_idx][1]
                
                tactical_width = rightmost_tactical[0] - leftmost_tactical[0]
                tactical_height = bottommost_tactical[1] - topmost_tactical[1]
                
                if court_width > 0 and court_height > 0 and tactical_width > 0 and tactical_height > 0:
                    scale_x = tactical_width / court_width
                    scale_y = tactical_height / court_height
                    
                    # Transform each player's position using scaling
                    for player_id, player_data in frame_tracks.items():
                        bbox = player_data["bbox"]
                        player_position = get_foot_position(bbox)
                        
                        # Calculate relative position from top-left reference point
                        relative_x = player_position[0] - detected_keypoints[leftmost_idx][0]
                        relative_y = player_position[1] - detected_keypoints[topmost_idx][1]
                        
                        # Transform to tactical view
                        tactical_x = leftmost_tactical[0] + (relative_x * scale_x)
                        tactical_y = topmost_tactical[1] + (relative_y * scale_y)
                        
                        # Shift all players to the right side of the tactical court
                        # Add an offset to move players from left side to right side
                        tactical_x += 150  # Shift by half the tactical view width
                        
                        # Ensure coordinates are within bounds
                        tactical_x = max(0, min(self.width, tactical_x))
                        tactical_y = max(0, min(self.height, tactical_y))
                        
                        tactical_positions[player_id] = [tactical_x, tactical_y]
                else:
                    continue
            else:
                continue
            
            tactical_player_positions.append(tactical_positions)
        
        return tactical_player_positions

    def transform_player_positions(self, player_tracks, court_keypoints):
        """Alias for transform_players_to_tactical_view for backward compatibility"""
        return self.transform_players_to_tactical_view(court_keypoints, player_tracks)



