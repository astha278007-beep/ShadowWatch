import cv2
import os

input_video = "videos/primary_cctv.mp4"
output_video = "videos/tampered_cctv.mp4"

cap = cv2.VideoCapture(input_video)

if not cap.isOpened():
    print("Error: Could not open primary CCTV video.")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Video writer
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(
    output_video,
    fourcc,
    fps,
    (width, height)
)

# Last 5 seconds will become black
blackout_frames = int(fps * 5)
blackout_start = total_frames - blackout_frames

frame_number = 0

while True:
    success, frame = cap.read()

    if not success:
        break

    # Create blackout at the end of the video
    if frame_number >= blackout_start:
        frame[:] = 0

    out.write(frame)
    frame_number += 1

cap.release()
out.release()

print("Tampered video created successfully!")
print("Saved as:", output_video)