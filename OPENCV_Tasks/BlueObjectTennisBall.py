
import cv2
import numpy as np
import math

camera = cv2.VideoCapture(0)

blue_low = np.array([90, 70, 50])
blue_high = np.array([130, 255, 255])
ball_low = np.array([20, 70, 70])
ball_high = np.array([45, 255, 255])

selected_center = None
blue_objects = []


# Select a blue object by clicking its bounding box
def select_object(event, x, y, flags, param):
    global selected_center

    if event == cv2.EVENT_LBUTTONDOWN:
        for obj in blue_objects:
            bx, by, bw, bh = obj["box"]

            if bx <= x <= bx + bw and by <= y <= by + bh:
                selected_center = obj["center"]
                break


# Remove small noise from a mask
def clean_mask(mask):
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    return cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)


# Find blue objects of any shape
def detect_blue(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = clean_mask(cv2.inRange(hsv, blue_low, blue_high))

    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    objects = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 300:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        moments = cv2.moments(contour)

        if moments["m00"] == 0:
            continue

        center = (
            int(moments["m10"] / moments["m00"]),
            int(moments["m01"] / moments["m00"])
        )

        objects.append({
            "box": (x, y, w, h),
            "center": center,
            "area": area
        })

    return mask, objects


# Detect the tennis ball separately
def detect_ball(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = clean_mask(cv2.inRange(hsv, ball_low, ball_high))

    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    ball = None

    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)

        if area < 150 or perimeter == 0:
            continue

        circularity = 4 * math.pi * area / perimeter**2
        if circularity < 0.5:
            continue

        (cx, cy), radius = cv2.minEnclosingCircle(contour)

        if ball is None or area > ball["area"]:
            ball = {
                "center": (int(cx), int(cy)),
                "radius": int(radius),
                "area": area
            }

    return mask, ball


# Find the closest detection to the selected blue object
def track_blue(objects):
    global selected_center

    if selected_center is None or not objects:
        return None

    nearest = min(
        objects,
        key=lambda obj: math.dist(obj["center"], selected_center)
    )

    if math.dist(nearest["center"], selected_center) <= 120:
        selected_center = nearest["center"]
        return nearest

    return None


# Draw blue-object information
def draw_blue(frame, objects, selected):
    for obj in objects:
        x, y, w, h = obj["box"]
        cx, cy = obj["center"]
        area = obj["area"]

        chosen = obj is selected
        colour = (0, 255, 0) if chosen else (255, 0, 0)

        cv2.rectangle(frame, (x, y), (x+w, y+h), colour, 2)
        cv2.circle(frame, (cx, cy), 4, colour, -1)

        cv2.putText(
            frame, f"Area: {area:.0f} px^2",
            (x, max(y-8, 20)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour, 2
        )

    if selected:
        x, y, w, h = selected["box"]
        cx, cy = selected["center"]

        cv2.putText(
            frame, f"Blue center: ({cx},{cy})",
            (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
            (0, 255, 0), 2
        )
        cv2.putText(
            frame, f"Box: {x},{y},{w},{h}",
            (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
            (0, 255, 0), 2
        )


# Draw tennis-ball measurements
def draw_ball(frame, ball):
    if ball is None:
        cv2.putText(
            frame, "Tennis ball not detected",
            (10, 80), cv2.FONT_HERSHEY_SIMPLEX,
            0.55, (0, 0, 255), 2
        )
        return

    cx, cy = ball["center"]
    radius = ball["radius"]

    cv2.circle(frame, (cx, cy), radius, (0, 255, 255), 2)
    cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

    cv2.putText(
        frame, f"Ball center: ({cx},{cy})",
        (10, 80), cv2.FONT_HERSHEY_SIMPLEX,
        0.55, (0, 255, 255), 2
    )
    cv2.putText(
        frame, f"Radius: {radius} px",
        (10, 110), cv2.FONT_HERSHEY_SIMPLEX,
        0.55, (0, 255, 255), 2
    )
    cv2.putText(
        frame, f"Ball area: {ball['area']:.0f} px^2",
        (10, 140), cv2.FONT_HERSHEY_SIMPLEX,
        0.55, (0, 255, 255), 2
    )


# Show the position of the blue object relative to the ball
def draw_relative(frame, selected, ball):
    if selected is None or ball is None:
        return

    bx, by = selected["center"]
    tx, ty = ball["center"]

    dx = bx - tx
    dy = by - ty
    distance = math.hypot(dx, dy)

    cv2.line(frame, (bx, by), (tx, ty), (0, 0, 255), 2)

    cv2.putText(
        frame, f"Relative: dx={dx}, dy={dy}",
        (10, 170), cv2.FONT_HERSHEY_SIMPLEX,
        0.55, (0, 0, 255), 2
    )
    cv2.putText(
        frame, f"Center distance: {distance:.1f} px",
        (10, 200), cv2.FONT_HERSHEY_SIMPLEX,
        0.55, (0, 0, 255), 2
    )


# Main camera window
if not camera.isOpened():
    print("Could not open camera")
    exit()

cv2.namedWindow("Detection")
cv2.setMouseCallback("Detection", select_object)

while True:
    ret, frame = camera.read()

    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))

    # Run both detection systems independently
    blue_mask, blue_objects = detect_blue(frame)
    ball_mask, ball = detect_ball(frame)

    selected = track_blue(blue_objects)

    draw_blue(frame, blue_objects, selected)
    draw_ball(frame, ball)
    draw_relative(frame, selected, ball)

    cv2.putText(
        frame, "Click blue object | R: Reset | Q: Quit",
        (10, 460), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (255, 255, 255), 1
    )

    cv2.imshow("Detection", frame)
    cv2.imshow("Blue Mask", blue_mask)
    cv2.imshow("Ball Mask", ball_mask)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q") or key == 27:
        break
    elif key == ord("r"):
        selected_center = None

camera.release()
cv2.destroyAllWindows()
