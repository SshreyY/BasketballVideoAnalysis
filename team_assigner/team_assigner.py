from PIL import Image
import requests
import cv2
import sys
sys.path.append("../")
from utils import read_stub, save_stub

from transformers import CLIPProcessor, CLIPModel

class TeamAssigner:
    def __init__(self, team_1_class_name = "white shirt", team_2_class_name = "darkblue shirt"):
        self.team_1_class_name = team_1_class_name
        self.team_2_class_name = team_2_class_name

        self.player_team_dict = {}
        
    def load_model(self):
        try:
            self.model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
            self.processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def get_player_color(self, frame, bbox):
        # Ensure model is loaded
        if not hasattr(self, 'model') or not hasattr(self, 'processor'):
            self.load_model()
            
        image = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)

        classes = [self.team_1_class_name, self.team_2_class_name]

        # Ensure processor is callable
        if not callable(self.processor):
            raise ValueError("Processor is not callable. Please check if model was loaded correctly.")
            
        inputs = self.processor(text=classes, images=pil_image, return_tensors="pt", padding=True)

        outputs = self.model(**inputs)
        logits_per_image = outputs.logits_per_image # this is the image-text similarity score
        probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities

        class_name = classes[probs.argmax(dim=1)[0]]

        return class_name
    
    def get_player_team(self, frame, player_bbox, player_id):
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]
        
        player_color = self.get_player_color(frame, player_bbox)

        team_id = 2
        if player_color == self.team_1_class_name:
            team_id = 1
        
        self.player_team_dict[player_id] = team_id
        
        return team_id

    def get_player_teams_accross_frames(self, video_frame, player_tracks, read_from_stub = False, stub_path = None):

        player_assignment = read_stub(read_from_stub, stub_path)
        if player_assignment is not None:
            if len(player_assignment) == len(video_frame):
                return player_assignment

        self.load_model()

        # Initialize player_assignment with empty dictionaries for all frames
        player_assignment = [{} for _ in range(len(player_tracks))]

        for frame_num, player_track in enumerate(player_tracks):
            if frame_num %50 == 0:
                self.player_team_dict = {}

            for player_id, track in player_track.items():
                team = self.get_player_team(video_frame[frame_num], track["bbox"], player_id)
                player_assignment[frame_num][player_id] = team

        save_stub(stub_path, player_assignment)

        return player_assignment

