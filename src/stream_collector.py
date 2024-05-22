import yaml
import cv2 as cv
import threading
from os import path
import queue
import time
import argparse


def load_config(file_path):
    """
    Loads camera stream configuration from a yaml file.
    """

    with open(file_path, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None


def stream_camera_worker(url, id, width, height, fps, display_queue, display=False):
    """
    Worker function that streams a camera or video file.

    Args:
    - `url`: camera id or video file path
    - `id`: camera id
    - `width`: desired frame width
    - `height`: desired frame height
    - `fps`: desired frame rate
    - `display_queue`: queue to send frames to the main thread
    - `display`: whether to display the frames
    """

    # Open the camera or video file capture
    cap = cv.VideoCapture(url)
    if not cap.isOpened():
        print(f"Error: Could not open camera {id}")
        return

    prev_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            # if is video file, reset to the beginning
            if path.isfile(url):
                cap.set(cv.CAP_PROP_POS_FRAMES, 0)
                continue

            break

        # if file, we limit the frame rate with sleep
        if path.isfile(url):
            time.sleep(1 / fps)
        # if camera, we limit the frame rate by dropping frames
        else:
            curr_time = time.time()
            elapsed_time = curr_time - prev_time
            if elapsed_time < 1 / fps:
                continue
            prev_time = curr_time

        # --------- Start of frame processing
        frame = cv.resize(frame, (width, height), interpolation=cv.INTER_CUBIC)
        # TODO: Encode frame to base64 and send kafka message
        # --------- End of frame processing

        # Send the frame to the main thread
        if display:
            display_queue.put((id, frame))

    cap.release()


def start_camera_stream(urls, ids, width, height, fps, display=False):
    """
    Function that starts the camera stream.

    This is meant to be run in the main thread.

    Args:
    - `urls`: list of camera ids or video file paths
    - `ids`: list of camera ids
    - `width`: desired frame width
    - `height`: desired frame height
    - `fps`: desired frame rate
    - `display`: whether to display the frames
    """

    display_queue = queue.Queue()

    if display:
        for id in ids:
            cv.namedWindow(id, cv.WINDOW_NORMAL)

    threads = []
    for url, id in zip(urls, ids):
        t = threading.Thread(
            target=stream_camera_worker,
            args=(url, id, width, height, fps, display_queue, display),
            daemon=True
        )
        t.start()
        threads.append(t)

    c = 0
    while True:
        try:
            id, frame = display_queue.get_nowait()
            if display:
                c += 1
                cv.imshow(id, frame)

                # if we have displayed all frames, wait for a key press
                if c % len(ids) == 0:
                    cv.waitKey(1)

        except queue.Empty:
            pass
        except KeyboardInterrupt:
            break

    cv.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default=None,
                        help='Path to the configuration file')
    args = parser.parse_args()

    LOCAL_CONFIG_PATH = args.config if args.config else 'config/collector/8_file_local.yaml'

    config = load_config(LOCAL_CONFIG_PATH)

    URLS = config['camera']['urls']
    IDS = config['camera']['ids']
    DISPLAY = config['camera']['display']
    WIDTH = config['camera']['width']
    HEIGHT = config['camera']['height']
    FPS = config['camera']['fps']

    start_camera_stream(URLS, IDS, WIDTH, HEIGHT, FPS, DISPLAY)
