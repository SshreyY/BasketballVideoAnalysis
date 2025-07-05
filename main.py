from utils import read_video, save_video
from trackers import PlayerTracker
from drawers import PlayerTracksDrawer


def main():

    # Read the video
    video_path = "input_video/StephLayupVid.mp4"
    video_frames = read_video(video_path)

    #initialize the player tracker
    player_tracker = PlayerTracker("models/player_detector.pt")

    # Run trackers
    player_tracks = player_tracker.get_object_tracks(video_frames, read_from_stub=True, 
                                                    stub_path="stubs/player_tracks_stubs.pkl"
                                                    )
    
    # draw output
    #initialize the player drawer

    player_tracks_drawers = PlayerTracksDrawer()

    # draw object tracks
    output_video_frames = player_tracks_drawers.draw_tracks(video_frames, player_tracks)

    #Save the video
    save_video(output_video_frames, "output_video/StephLayupVid_output.avi")





if __name__ == "__main__":
    main()

