import cv2 as cv

from vision import check_motion_v1, check_motion_v2

SAMPLE_VIDEO = "./resources/car.mp4"

# Open the video file
cap = cv.VideoCapture(SAMPLE_VIDEO)

# Read the first frame
ret, prev_frame = cap.read()

# Check if the video opened successfully
if not ret:
    print("Error: Could not open video.")
    exit()

DONE = False

# Loop through the video
while not DONE:
    # Reset the video to the beginning
    cap.set(cv.CAP_PROP_POS_FRAMES, 0)

    ret, prev_frame = cap.read()

    while cap.isOpened():
        # Read the next frame
        ret, current_frame = cap.read()

        # If video has ended, break the loop
        if not ret:
            break

        # Check for motion between the previous and current frames
        motion_detected, frame_with_motion, frame_diff = check_motion_v1(
            prev_frame, current_frame)

        # Display the frame with motion
        cv.imshow("Frame", frame_with_motion)

        # Display the difference map
        cv.imshow("Frame Diff", frame_diff)

        # Update the previous frame
        prev_frame = current_frame

        # Check for user input to exit the loop
        if cv.waitKey(1) & 0xFF == ord('q'):
            DONE = True
            break
