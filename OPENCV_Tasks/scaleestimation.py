
import math
import cv2
import numpy as np

# Settings
CAMERA_NUMBER = 0
WINDOW_NAME = "Blue Object and Tennis Ball Detection"
INFO_WINDOW_NAME = "Blue Object Info"
INFO_WIDTH, INFO_HEIGHT = 560, 520

BLUE_LOWER = np.array([90, 70, 40])
BLUE_UPPER = np.array([135, 255, 255])
BALL_LOWER = np.array([25, 120, 100])
BALL_UPPER = np.array([45, 255, 255])

MIN_BLUE_AREA = 500
MIN_BALL_AREA = 400
MIN_BALL_CIRCULARITY = 0.70
MAX_TRACK_DISTANCE = 60
MAX_MISSING_FRAMES = 10
MAX_PATH_LENGTH = 25

ARUCO_MARKER_SIZE_CM = 5.0
ARUCO_DICTIONARY = cv2.aruco.DICT_4X4_50

BLUE_COLOR = (255, 100, 0)
BALL_COLOR = (0, 255, 0)
LINE_COLOR = (0, 255, 255)
INFO_COLOR = (0, 200, 200)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
FONT = cv2.FONT_HERSHEY_SIMPLEX
KERNEL = np.ones((5, 5), np.uint8)


def put_text(frame, text, position, color, scale=0.5):
    cv2.putText(frame, text, position, FONT, scale, color, 2)


def clean_mask(mask):
    mask = cv2.erode(mask, KERNEL, iterations=1)
    return cv2.dilate(mask, KERNEL, iterations=2)


def find_contours(mask):
    result = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    return result[0] if len(result) == 2 else result[1]


def relative_position(center, ball):
    return center[0] - ball["center"][0], center[1] - ball["center"][1]


def calculate_area(contour, homography):
    if homography is None:
        return None
    points = cv2.perspectiveTransform(
        contour.astype(np.float32), homography
    )
    return abs(cv2.contourArea(points))


# ArUco scale estimation
def detect_aruco_scale(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICTIONARY)

    if hasattr(cv2.aruco, "ArucoDetector"):
        detector = cv2.aruco.ArucoDetector(
            dictionary, cv2.aruco.DetectorParameters()
        )
        corners, ids, _ = detector.detectMarkers(gray)
    else:
        parameters = cv2.aruco.DetectorParameters_create()
        corners, ids, _ = cv2.aruco.detectMarkers(
            gray, dictionary, parameters=parameters
        )

    if ids is None:
        return None

    cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    image_corners = corners[0][0].astype(np.float32)
    size = ARUCO_MARKER_SIZE_CM

    real_corners = np.array([
        [0, 0], [size, 0], [size, size], [0, size]
    ], dtype=np.float32)

    homography = cv2.getPerspectiveTransform(image_corners, real_corners)
    put_text(frame, f"ArUco: {size} cm", (10, 25), WHITE)
    return homography


# Blue object detection
def detect_blue_objects(hsv, homography=None):
    mask = clean_mask(cv2.inRange(hsv, BLUE_LOWER, BLUE_UPPER))
    objects = []

    for contour in find_contours(mask):
        area = cv2.contourArea(contour)
        moments = cv2.moments(contour)

        if area < MIN_BLUE_AREA or moments["m00"] == 0:
            continue

        center = (
            int(moments["m10"] / moments["m00"]),
            int(moments["m01"] / moments["m00"])
        )

        objects.append({
            "area": area,
            "actual_area": calculate_area(contour, homography),
            "box": cv2.boundingRect(contour),
            "contour": contour,
            "center": center
        })

    return objects


# Track blue objects
def update_tracks(tracks, blue_objects, frame_number, next_id):
    free_ids = set(tracks)

    for obj in blue_objects:
        cx, cy = obj["center"]
        best_id = None
        best_distance = MAX_TRACK_DISTANCE

        for track_id in free_ids:
            ox, oy = tracks[track_id]["center"]
            distance = math.hypot(cx - ox, cy - oy)

            if distance < best_distance:
                best_id, best_distance = track_id, distance

        if best_id is None:
            best_id = next_id
            next_id += 1
            tracks[best_id] = {
                "center": (cx, cy), "path": [],
                "last_seen": frame_number, "distance": 0.0
            }
        else:
            ox, oy = tracks[best_id]["center"]
            tracks[best_id]["distance"] += math.hypot(cx - ox, cy - oy)

        free_ids.discard(best_id)
        track = tracks[best_id]
        track["center"] = (cx, cy)
        track["last_seen"] = frame_number
        track["path"] = (track["path"] + [(cx, cy)])[-MAX_PATH_LENGTH:]
        obj["track_id"] = best_id

    for track_id in list(tracks):
        if frame_number - tracks[track_id]["last_seen"] > MAX_MISSING_FRAMES:
            del tracks[track_id]

    return next_id


# Tennis ball detection
def detect_tennis_ball(hsv, homography=None):
    mask = clean_mask(cv2.inRange(hsv, BALL_LOWER, BALL_UPPER))
    ball, best_area = None, 0

    for contour in find_contours(mask):
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)

        if area < MIN_BALL_AREA or perimeter == 0:
            continue

        circularity = 4 * math.pi * area / perimeter ** 2
        if circularity < MIN_BALL_CIRCULARITY or area <= best_area:
            continue

        (x, y), radius = cv2.minEnclosingCircle(contour)
        ball = {
            "area": area,
            "actual_area": calculate_area(contour, homography),
            "center": (int(x), int(y)),
            "radius": int(radius)
        }
        best_area = area

    return ball


# Draw blue objects
def draw_blue_object(frame, obj, path, ball):
    x, y, w, h = obj["box"]
    cx, cy = obj["center"]

    cv2.drawContours(frame, [obj["contour"]], -1, BLUE_COLOR, 2)
    cv2.rectangle(frame, (x, y), (x + w, y + h), BLUE_COLOR, 1)
    cv2.circle(frame, (cx, cy), 4, BLUE_COLOR, -1)

    put_text(frame, f"Blue #{obj['track_id']}", (x, max(20, y - 55)), BLUE_COLOR)
    put_text(frame, f"Area: {obj['area']:.0f} px^2", (x, max(40, y - 32)), BLUE_COLOR)

    area = obj["actual_area"]
    text = f"Area: {area:.2f} cm^2" if area is not None else "Area: unavailable"
    put_text(frame, text, (x, max(60, y - 9)), INFO_COLOR)
    put_text(frame, f"Box: {w} x {h} px", (x, y + h + 18), BLUE_COLOR)

    for start, end in zip(path, path[1:]):
        cv2.line(frame, start, end, BLUE_COLOR, 2)

    if ball is not None:
        bx, by = ball["center"]
        dx, dy = relative_position(obj["center"], ball)
        cv2.line(frame, (cx, cy), (bx, by), LINE_COLOR, 2)
        put_text(frame, f"Relative to ball: dx={dx}, dy={dy}",
                 (x, min(frame.shape[0] - 10, y + h + 38)), INFO_COLOR)


# Draw tennis ball
def draw_tennis_ball(frame, ball):
    if ball is None:
        put_text(frame, "Tennis ball: not detected", (10, 30), RED, 0.65)
        return

    bx, by = ball["center"]
    radius = ball["radius"]
    cv2.circle(frame, (bx, by), radius, BALL_COLOR, 2)
    cv2.circle(frame, (bx, by), 4, RED, -1)

    put_text(frame, f"Center: ({bx}, {by}) px", (10, 30), BALL_COLOR)
    put_text(frame, f"Radius: {radius} px", (10, 55), BALL_COLOR)
    put_text(frame, f"Pixel area: {ball['area']:.0f} px^2", (10, 80), BALL_COLOR)

    area = ball["actual_area"]
    text = f"Projected area: {area:.2f} cm^2" if area is not None else "Area: scale unavailable"
    put_text(frame, text, (10, 105), INFO_COLOR)


def draw_info_window(blue_objects, tracks, ball):
    panel = np.zeros((INFO_HEIGHT, INFO_WIDTH, 3), np.uint8)
    put_text(panel, "BLUE OBJECTS", (10, 28), WHITE, 0.7)

    if ball is None:
        put_text(panel, "Ball: not detected", (10, 55), RED)
    else:
        put_text(panel, f"Ball center: {ball['center']}", (10, 55), BALL_COLOR)

    y = 90
    for obj in sorted(blue_objects, key=lambda item: item["track_id"]):
        if y + 90 > INFO_HEIGHT:
            break

        cx, cy = obj["center"]
        track = tracks[obj["track_id"]]
        area = obj["actual_area"]
        area_text = f"{area:.2f} cm^2" if area is not None else "unavailable"

        put_text(panel, f"Blue #{obj['track_id']} Center: ({cx}, {cy})", (10, y), BLUE_COLOR)
        put_text(panel, f"Area: {area_text}", (20, y + 22), INFO_COLOR)

        if ball is not None:
            dx, dy = relative_position(obj["center"], ball)
            put_text(panel, f"Ball dx={dx}, dy={dy}", (20, y + 44), WHITE)

        put_text(panel, f"Travelled: {track['distance']:.0f} px", (20, y + 66), WHITE)
        y += 90

    cv2.imshow(INFO_WINDOW_NAME, panel)


# Main program
def main():
    camera = cv2.VideoCapture(CAMERA_NUMBER)

    if not camera.isOpened():
        print("Error: Could not open camera.")
        return

    tracks, next_id, frame_number = {}, 1, 0

    try:
        while True:
            success, frame = camera.read()
            if not success:
                print("Error: Could not read camera frame.")
                break

            frame_number += 1
            frame = cv2.flip(frame, 1)
            homography = detect_aruco_scale(frame)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            blue_objects = detect_blue_objects(hsv, homography)
            next_id = update_tracks(tracks, blue_objects, frame_number, next_id)
            ball = detect_tennis_ball(hsv, homography)

            for obj in blue_objects:
                draw_blue_object(frame, obj, tracks[obj["track_id"]]["path"], ball)

            draw_tennis_ball(frame, ball)

            if homography is None:
                put_text(frame, "Show ArUco marker for cm^2 estimation",
                         (10, 135), WHITE)

            put_text(frame, "Press q to quit", (10, frame.shape[0] - 15), WHITE)
            cv2.imshow(WINDOW_NAME, frame)
            draw_info_window(blue_objects, tracks, ball)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
