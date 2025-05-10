from .utils import draw_ellipse
class PlayerTracksDrawer:
    def __init__(self):
        pass

    def draw(self, video_frames, tracks):
        output_video_frames = []
        for frame_number, frame in enumerate(video_frames):
            frame = frame.copy()
            player_dict = tracks[frame_number]

            # draw players tracks
            for track_id, player in player_dict.items():
                print(player)
                frame = draw_ellipse(frame, player["bbox"], (0,0,225), track_id)
            output_video_frames.append(frame) # if this line is inside for loop above, it will be laggy
        return output_video_frames