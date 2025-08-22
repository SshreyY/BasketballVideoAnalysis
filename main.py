from utils import read_video, save_video
from trackers import PlayerTracker, BallTracker
from drawers import PlayerTracksDrawer, BallTracksDrawer, CourtKeyPointsDrawer, TacticalViewDrawer
from team_assigner import TeamAssigner
from ball_acquisiton import BallAcquisitionDetector
from court_keypoint_detector import CourtKeypointDetector
from tactical_view_converter import TacticalViewConverter


def main():

    # Read the video
    video_path = "input_video/StephLayupVid.mp4"
    video_frames = read_video(video_path)

    #initialize the player tracker
    player_tracker = PlayerTracker("models/player_detector.pt")
    ball_tracker = BallTracker("models/ball_detector.pt")

    # Initialize the court keypoint detector
    court_keypoint_detector = CourtKeypointDetector("models/court_keypoint_detector.pt")

    # Run trackers
    player_tracks = player_tracker.get_object_tracks(video_frames, read_from_stub=True, 
                                                    stub_path="stubs/player_tracks_stubs.pkl"
                                                    )
    
    ball_tracks = ball_tracker.get_object_tracks(video_frames, read_from_stub=True, 
                                                    stub_path="stubs/ball_tracks_stubs.pkl"
                                                    )

    #get court keypoints
    court_keypoints = court_keypoint_detector.get_court_keypoints(video_frames, 
                                                    read_from_stub=True, 
                                                    stub_path="stubs/court_keypoints_stubs.pkl"
                                                    )

    # Remove wrong ball detections
    ball_tracks = ball_tracker.remove_wrong_detections(ball_tracks)

    # Interpolate ball positions
    ball_tracks = ball_tracker.interpolate_ball_positions(ball_tracks)

    # Assign player teams
    team_assigner = TeamAssigner()
    player_assignment = team_assigner.get_player_teams_accross_frames(video_frames, player_tracks, read_from_stub=True, stub_path="stubs/player_assignment_stubs.pkl")

    # Ball Acquisition 
    ball_acquisition_detector = BallAcquisitionDetector()
    ball_acquisition = ball_acquisition_detector.detect_ball_posession(player_tracks, ball_tracks)    
    # tactical view
    tactical_view_converter = TacticalViewConverter(court_image_path="./images/basketball_court.png")

    # draw output
    #initialize the drawers
    player_tracks_drawer = PlayerTracksDrawer()
    ball_tracks_drawer = BallTracksDrawer()
    court_key_points_drawer = CourtKeyPointsDrawer()
    tactical_view_drawer = TacticalViewDrawer()

    # draw object tracks
    output_video_frames = player_tracks_drawer.draw_tracks(video_frames, player_tracks, player_assignment, ball_acquisition)
    output_video_frames = ball_tracks_drawer.draw(output_video_frames, ball_tracks)

    # draw court keypoints
    output_video_frames = court_key_points_drawer.draw(output_video_frames, court_keypoints)


    #tactical view
    output_video_frames = tactical_view_drawer.draw(output_video_frames, tactical_view_converter.court_image_path, tactical_view_converter.width, tactical_view_converter.height)
    
    #Save the video
    save_video(output_video_frames, "output_video/StephLayupVid_output.avi")





if __name__ == "__main__":
    main()

