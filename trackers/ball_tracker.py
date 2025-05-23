from ultralytics import YOLO
import supervision as sv
import sys
sys.path.append("../")
from utils import save_stub, read_stub

class BallTracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect_frames(self, frames):
        batch_size = 20
        detections = []
        for i in range(0, len(frames), batch_size):
            batch_frames = frames[i: i + batch_size]
            batch_detections = self.model.predict(batch_frames, conf=0.5)
            detections += batch_detections
        return detections

    def get_object_tracks(self, frames, read_from_stub = False, stub_path = None):
        tracks = read_stub(read_from_stub, stub_path)
        if tracks is not None:
            if len(tracks) == len (frames): # dont need to track already done
                return tracks

        detections = self.detect_frames(frames)
        tracks = []
        for frame_num, detection in enumerate(detections):
            cls_names = detection.names
            cls_names_inv = {v:k for k,v in cls_names.items()}

            # Covert to supervision Detection format
            detection_supervision = sv.Detections.from_ultralytics(detection)
            tracks.append({})
            max_confidence = 0
            chosen_bbox = None
            for frame_detection in detection_supervision:
                bbox = frame_detection[0].tolist() # it is originally a numpy array
                confidence = frame_detection[2]
                cls_id = frame_detection[3]
                # we do this only for the ball.
                if cls_id == cls_names_inv["Ball"]:
                    if confidence > max_confidence:
                        chosen_bbox = bbox
                        max_confidence = confidence
            # now we detect the ball in the chosen_bbox
            if chosen_bbox is not None:
                    tracks[frame_num][1] = {"bbox": chosen_bbox} # track_id is hardcoded as 1.

        save_stub(stub_path, tracks)  # check point
        return tracks
