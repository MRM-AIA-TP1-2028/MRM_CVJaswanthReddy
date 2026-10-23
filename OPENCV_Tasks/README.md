
# Blue Object and Tennis Ball Detection using OpenCV

## 1. Project Overview

This project uses OpenCV and Python to detect blue objects and a tennis ball through a live camera feed.

Blue objects are detected based on their colour, while the tennis ball is detected using its colour and circular shape. An ArUco marker is used to estimate object area in square centimetres.

## 2. Objectives

- Detect blue objects from a live camera.
- Detect a tennis ball separately from blue objects.
- Display the blue object's area, bounding box and centre.
- Track blue objects and display their movement path.
- Show the position of a blue object relative to the tennis ball.
- Display the tennis ball's centre, radius and area.
- Estimate area in cm² using an ArUco marker.

## 3. Approach

### Blue Object Detection

1. Capture frames from the webcam.
2. Convert each frame from BGR to HSV colour space.
3. Apply an HSV colour range to create a mask for blue objects.
4. Remove noise using erosion and dilation.
5. Find contours and filter small objects by area.
6. Calculate the centre and bounding box of each detected object.

The shape of a blue object is not assumed to be circular.

### Tennis Ball Detection

1. Create a mask using the HSV range for the tennis ball.
2. Find contours in the mask.
3. Filter contours based on area and circularity.
4. Find the centre and radius using `cv2.minEnclosingCircle()`.
5. Display the detected tennis ball separately.

### Object Tracking

The centre of each blue object is compared with previously detected centres. If an object is close enough to a previous position, it is assigned the same tracking ID.

The program draws a line showing the object's movement path and calculates its approximate travelled distance in pixels.

### Relative Position

When both a blue object and tennis ball are detected, the program calculates:

- `dx`: horizontal difference between their centres.
- `dy`: vertical difference between their centres.

A line connects the centres to show their relative positions.

## 4. ArUco-Based Area Estimation

An ArUco marker with a known side length is used as a reference for estimating area.

The program detects the marker and calculates a perspective transformation, also called a homography. Contour points are transformed into centimetre coordinates, and the contour area is calculated in cm².

**Important:** The marker's measured black-square side length must match `ARUCO_MARKER_SIZE_CM` in the code. The marker dictionary must also match the marker being used.

The area estimate works best when the object and marker are approximately on the same plane. The tennis ball's cm² measurement is only an approximate projected area, not its full 3D surface area.

## 5. Methods Used

- **HSV colour thresholding:** Separates objects based on colour.
- **Contour detection:** Finds the boundaries of detected objects.
- **Morphological operations:** Reduce noise in the colour masks.
- **Image moments:** Calculate the centre of blue objects.
- **Circularity:** Helps distinguish the round tennis ball from irregular objects.
- **Object tracking:** Matches blue objects across consecutive frames.
- **ArUco marker and homography:** Estimate real-world planar area.

## 6. Alternative Methods

Other possible methods include:

- **Background subtraction:** Useful when objects move against a relatively stationary background.
- **Template matching:** Can detect objects with a known appearance.
- **Hough Circle Transform:** Can detect circular objects such as tennis balls.
- **YOLO object detection:** Can detect trained object classes in more complex scenes.
- **Camera calibration and pose estimation:** Can improve geometric measurements when camera parameters and object geometry are known.

## 7. Requirements

- Python 3
- OpenCV with contrib modules
- NumPy
- Webcam
- ArUco marker for area estimation

Install the required libraries:

```bash
python -m pip install opencv-contrib-python numpy
```

## 8. How to Run

Save the program as `BlueObjectTennisBall.py`.

Run it using:

```bash
python BlueObjectTennisBall.py
```

Press `q` to close the camera windows.

## 9. Output

The program displays:

### Blue Object
- Centre coordinates in pixels.
- Area in pixels².
- Estimated area in cm² when the ArUco marker is detected.
- Bounding box.
- Tracking path.
- Relative position to the tennis ball.

### Tennis Ball
- Centre coordinates in pixels.
- Radius in pixels.
- Area in pixels².
- Approximate projected area in cm² when the ArUco marker is detected.

## 10. Limitations

- Detection depends on lighting and the selected HSV colour ranges.
- Blue objects may be missed if their colour differs significantly from the selected range.
- The tennis ball may not be detected if its circularity or colour falls outside the selected thresholds.
- Area estimation depends on the marker's correct physical size and its position relative to the object.
- The tennis ball's area in cm² is approximate because it is a three-dimensional object.

## 11. Conclusion

This project demonstrates real-time colour-based object detection, contour analysis, object tracking and relative position estimation using OpenCV. ArUco-based homography is used to estimate planar object areas in square centimetres.
