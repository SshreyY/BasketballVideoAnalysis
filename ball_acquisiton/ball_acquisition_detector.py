import sys
sys.path.append("../")
from utils import measure_distance, get_center_of_bbox

class BallAcquisitionDetector:
    def __init__(self):
        self.possession_threshold = 50
        self.min_frames = 11
        self.containment_threshold = 0.8

    def get_key_basketball_player_assignment_points(self, player_bbox, ball_center):
        ball_center_x = ball_center[0]
        ball_center_y = ball_center[1]

        x1, y1, x2, y2 = player_bbox
        width = x2 - x1
        height = y2 - y1

        output_points = []

        if ball_center_y > y1 and ball_center_y < y2:
            output_points.append((x1, ball_center_y))
            output_points.append((x2, ball_center_y))
        
        if ball_center_x > x1 and ball_center_x < x2:
            output_points.append((ball_center_x, y1))
            output_points.append((ball_center_x, y2))

        output_points += [
            (x1, y1), # top left corner
            (x2, y1), # top right corner
            (x1, y2), # bottom left corner
            (x2, y2), # bottom right corner

            (x1+width//2, y1), #top center
            (x1+width//2, y2), #bottom center
            (x1, y1+height//2), #left center
            (x2, y1+height//2),#right center
        ]

        return output_points

    def find_minimum_distance_to_ball(self, ball_center, player_bbox):
        key_points = self.get_key_basketball_player_assignment_points(player_bbox, ball_center)
        return min(measure_distance(ball_center, key_point) for key_point in key_points)

    def calculate_ball_containment_ratio(self, player_bbox, ball_bbox):
        px1, py1, px2, py2 = player_bbox
        bx1, by1, bx2, by2 = ball_bbox

        ball_area = (bx2-bx1)*(by2-by1)

        intersection_x1 = max(px1, bx1)
        intersection_y1 = max(py1, by1)
        intersection_x2 = max(px2, bx2)
        intersection_y2 = max(py2, bx2)

        intersection_area = (intersection_x2 - intersection_x1) * (intersection_y2 - intersection_y1)

        containment_ratio = intersection_area/ball_area

        return containment_ratio

    def find_best_candidate_for_possession(self, ball_center, player_tracks_frame, ball_bbox):

        high_containment_players = []
        regular_distance_players = []

        for player_id, player_info in player_tracks_frame.items():
            player_bbox = player_info.get("bbox", [])
            if not player_bbox:
                continue

            containment = self.calculate_ball_containment_ratio(player_bbox, ball_bbox)
            min_distance = self.find_minimum_distance_to_ball(ball_center, player_bbox)

            if containment > self.containment_threshold:
                high_containment_players.append((player_id, containment, containment))
            else:
                regular_distance_players.append((player_id, min_distance))

        
        #first priority high_containment players
        if high_containment_players:
            best_candidate = max(high_containment_players, key = lambda x: x[1])
            return best_candidate[0]
        
        #second priority regular_distance_players
        if regular_distance_players:
            best_candidate = min(regular_distance_players, key=lambda x: x[1])
            if best_candidate[1] < self.possession_threshold:
                return best_candidate[0]
        return -1

    def detect_ball_posession(self, player_tracks, ball_tracks):
        num_frames = len(ball_tracks)
        posession_list = [-1] * num_frames
        consecutive_posession_count = {}

        for frame_num in range(num_frames):
            ball_info = ball_tracks[frame_num].get(1, {})
            if not ball_info:
                continue
        
            ball_bbox = ball_info.get('bbox', [])
            if not ball_bbox:
                continue
                
            ball_center = get_center_of_bbox(ball_bbox)

            best_player_id = self.find_best_candidate_for_possession(ball_center, 
                                                                    player_tracks[frame_num],
                                                                        ball_bbox)
            if best_player_id != -1:
                number_of_consecutive_frames = consecutive_posession_count.get(best_player_id, 0) + 1
                consecutive_posession_count = {best_player_id: number_of_consecutive_frames}

                if consecutive_posession_count[best_player_id] >= self.min_frames:
                    posession_list[frame_num] = best_player_id
            else:
                consecutive_posession_count= {}
            
        return posession_list
                                                            




        
        
        
        