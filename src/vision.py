import cv2 as cv
import numpy as np


def check_motion_v1(prev_frame, current_frame):
    """
    Check if there is motion between two frames.
    Returns if there is motion, the frame with the motion highlighted and the diff map.

    The method used in this funciton is exactly the same as the Java
    implementation of the original project. 

    See the original implementation at:
    https://github.com/baghelamit/video-stream-analytics/blob/master/video-stream-processor/src/main/java/com/iot/video/app/spark/processor/VideoMotionDetector.java

    Args:
    - `prev_frame`: opencv previous frame
    - `current_frame`: opencv current frame
    """
    # Copy current frame (for drawing)
    current_frame_copy = current_frame.copy()

    # Convert the frames to grayscale
    prev_gray = cv.cvtColor(prev_frame, cv.COLOR_BGR2GRAY)
    current_gray = cv.cvtColor(current_frame, cv.COLOR_BGR2GRAY)

    # Apply a gaussian blur to the frames
    prev_gray = cv.GaussianBlur(prev_gray, (3, 3), 0)
    current_gray = cv.GaussianBlur(current_gray, (3, 3), 0)

    # Compute the absolute difference between the two frames
    abs_diff = cv.absdiff(prev_gray, current_gray)

    # Apply a threshold to the difference
    _, frame_diff = cv.threshold(abs_diff, 20, 255, cv.THRESH_BINARY)

    # Get the contours of the difference
    contours, _ = cv.findContours(
        frame_diff, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Get the area (rect) of the relevant contours in a list
    MAX_AREA = 300
    contours_area = [cv.contourArea(contour) for contour in contours]
    contours_rects = [
        cv.boundingRect(contours[i]) for i, area in enumerate(contours_area) if area > MAX_AREA]

    if len(contours_rects) > 0:
        # Draw the contours on the current frame
        for contour_rect in contours_rects:
            x, y, w, h = contour_rect
            cv.rectangle(current_frame_copy, (x, y),
                         (x + w, y + h), (0, 255, 0), 2)

        return True, current_frame_copy, abs_diff

    return False, current_frame_copy, abs_diff


def check_motion_v2(prev_frame, current_frame):
    """
    Check if there is motion between two frames using optical flow.

    The optical flow is computed using the Farneback method.
    """
    mask = np.zeros_like(prev_frame)
    mask[..., 1] = 255

    # Copy current frame (for drawing)
    current_frame_copy = current_frame.copy()

    # Convert the frames to grayscale
    prev_gray = cv.cvtColor(prev_frame, cv.COLOR_BGR2GRAY)
    current_gray = cv.cvtColor(current_frame, cv.COLOR_BGR2GRAY)

    # Apply a gaussian blur to the frames
    prev_gray = cv.GaussianBlur(prev_gray, (3, 3), 0)
    current_gray = cv.GaussianBlur(current_gray, (3, 3), 0)

    # Compute the optical flow
    flow = cv.calcOpticalFlowFarneback(
        prev_gray, current_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    # Compute the magnitude and angle of the flow
    magnitude, angle = cv.cartToPolar(flow[..., 0], flow[..., 1])
    mask[..., 0] = angle * 180 / np.pi / 2
    mask[..., 2] = cv.normalize(magnitude, None, 0, 255, cv.NORM_MINMAX)
    optical_flow = cv.cvtColor(mask, cv.COLOR_HSV2BGR)

    # Remove low magnitude flow from optical_flow
    optical_flow_gray = cv.cvtColor(optical_flow, cv.COLOR_BGR2GRAY)
    _, optical_flow_mask = cv.threshold(
        optical_flow_gray, 50, 255, cv.THRESH_BINARY)
    optical_flow = cv.bitwise_and(
        optical_flow, optical_flow, mask=optical_flow_mask)

    # Get the contours of the optical flow
    contours, _ = cv.findContours(
        optical_flow_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Get the area (rect) of the relevant contours in a list
    MAX_AREA = 600
    contours_area = [cv.contourArea(contour) for contour in contours]
    contours_rects = [
        cv.boundingRect(contours[i]) for i, area in enumerate(contours_area) if area > MAX_AREA]

    if len(contours_rects) > 0:
        # Draw the contours on the current frame
        for contour_rect in contours_rects:
            x, y, w, h = contour_rect
            cv.rectangle(current_frame_copy, (x, y),
                         (x + w, y + h), (0, 255, 0), 2)

        return True, current_frame_copy, optical_flow

    return False, current_frame_copy, optical_flow
