import cv2
import numpy as np


def detect_tampering(video_path):
    """
    Detects basic CCTV tampering:
    1. Camera feed unavailable
    2. Continuous black/dark screen
    """

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return {
            "tampering_detected": True,
            "reason": "Camera feed unavailable"
        }

    dark_frame_count = 0
    total_frames_checked = 0

    while True:
        success, frame = cap.read()

        if not success:
            break

        total_frames_checked += 1

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate average brightness
        brightness = np.mean(gray)

        # Detect continuous black/dark screen
        if brightness < 10:
            dark_frame_count += 1
        else:
            dark_frame_count = 0

        # Tampering only if darkness continues for many frames
        if dark_frame_count >= 100:
            cap.release()

            return {
                "tampering_detected": True,
                "reason": "Camera blackout or lens obstruction detected"
            }

    cap.release()

    return {
        "tampering_detected": False,
        "reason": f"No tampering detected. {total_frames_checked} frames analyzed."
    }