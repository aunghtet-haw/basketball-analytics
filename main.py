from utils import read_video, save_video
from trackers import PlayerTracker, BallTracker
from drawers import (
    PlayerTracksDrawer,
    BallTracksDrawer)

def main():
    # read video
    video_frames = read_video("input_videos/video_1.mp4")

    # Initialize trackers
    player_tracker = PlayerTracker("models/player.pt")
    ball_tracker = BallTracker("models/ball.pt")
    # Run Trackers
    player_tracks = player_tracker.get_object_tracks(video_frames, read_from_stub= True, stub_path= "stubs/player_track_stubs.pkl")
    ball_tracks = ball_tracker.get_object_tracks(video_frames, read_from_stub=True,
                                                     stub_path="stubs/ball_track_stubs.pkl")
    # draw output
    #initialize drawers
    player_tracks_drawer = PlayerTracksDrawer()
    ball_tracks_drawer = BallTracksDrawer()
    # draw object tracks
    output_videos_frames = player_tracks_drawer.draw(video_frames, player_tracks)
    output_videos_frames = ball_tracks_drawer.draw(output_videos_frames, ball_tracks)

    # save video
    save_video(output_videos_frames, "output_videos/output_video.avi")
if __name__ == "__main__":
    main()