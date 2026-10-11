
import cv2
import numpy as np
import math

# Size of the marker is 10 cm
size = 0.10

# Camera settings (approximate values)
K = np.array([[600, 0, 320],
              [0, 600, 240],
              [0, 0, 1]], dtype=np.float32)
D = np.zeros((5, 1), dtype=np.float32)

# These are the three marker types we want to detect
names = ["4x4", "5x5", "6x6"]
dicts = [
    cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50),
    cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50),
    cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
]

# Prepare a detector for each marker type
detectors = []
for name, d in zip(names, dicts):
    detector = cv2.aruco.ArucoDetector(
        d, cv2.aruco.DetectorParameters())
    detectors.append((name, detector))

# Give the four corners of the marker their real-world coordinates
h = size / 2
obj = np.array([[-h, h, 0], [h, h, 0],
                [h, -h, 0], [-h, -h, 0]], dtype=np.float32)

# Open the laptop camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the image to grayscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Check the video for each type of ArUco marker
    for name, detector in detectors:
        corners, ids, _ = detector.detectMarkers(gray)

        if ids is None:
            continue

        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        for i, points in enumerate(corners):
            # Find the marker's position and orientation
            ok, rvec, tvec = cv2.solvePnP(
                obj, points.reshape(4, 2), K, D)

            if not ok:
                continue

            # Get the X, Y and Z position
            x, y, z = tvec.flatten()

            # Calculate the distance from the camera
            distance = math.sqrt(x*x + y*y + z*z)

            # Convert the rotation vector into a rotation matrix
            R, _ = cv2.Rodrigues(rvec)

            # Find the roll, pitch and yaw angles
            sy = math.sqrt(R[0, 0]**2 + R[1, 0]**2)
            roll = math.degrees(math.atan2(R[2, 1], R[2, 2]))
            pitch = math.degrees(math.atan2(-R[2, 0], sy))
            yaw = math.degrees(math.atan2(R[1, 0], R[0, 0]))

            # Show the marker's coordinate axes
            cv2.drawFrameAxes(frame, K, D, rvec, tvec, 0.05)

            # Display the results near the marker
            px, py = map(int, points.reshape(4, 2)[0])
            lines = [
                f"{name} ID: {int(ids[i])}",
                f"X:{x:.2f} Y:{y:.2f} Z:{z:.2f} m",
                f"Distance: {distance:.2f} m",
                f"Roll:{roll:.1f} Pitch:{pitch:.1f} Yaw:{yaw:.1f}"
            ]

            for j, line in enumerate(lines):
                cv2.putText(frame, line, (px, py - 10 - j*20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                            (0, 255, 0), 1)

    # Display the live camera feed
    cv2.imshow("ArUco Pose Estimation", frame)

    # Press Q when you want to close the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the camera properly
cap.release()
cv2.destroyAllWindows()
