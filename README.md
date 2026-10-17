# Blue Object Selection and Tennis Ball Detection using OpenCV

## 1. Approach

The program processes frames from a live webcam to detect blue objects and a tennis ball simultaneously. It uses separate colour masks in HSV colour space to identify the two types of objects.

- **Blue objects:** A blue HSV mask is created using predefined lower and upper colour limits. Contours are extracted from the mask, and regions above a minimum area are considered blue objects. For each detected object, the program calculates the contour area, bounding box and centre point. The detection method does not assume that the blue object is circular.
- **Tennis ball:** A separate yellow-green HSV mask is created to identify the tennis ball. The program finds contours, filters small regions and checks circularity to reduce false detections. The largest qualifying contour is selected, and its centre and radius are estimated using the minimum enclosing circle.
- **Object selection and tracking:** The user can select a blue object by clicking inside its bounding box. The program uses the selected object's centre to find the nearest detected blue object in subsequent frames. This provides basic tracking as the object moves.
- **Relative position:** When the selected blue object and tennis ball are both detected, a line is drawn between their centres. The horizontal and vertical offsets (`dx` and `dy`) and the distance between the centres are calculated in pixels.
- **Live visualisation:** The program displays the detected objects, bounding boxes, centres, measurements and separate colour masks in real time.

## 2. Method Used

1. Capture live video frames using `cv2.VideoCapture()`.
2. Resize each frame to a fixed resolution for consistent processing.
3. Convert the frame from BGR to HSV colour space using `cv2.cvtColor()`.
4. Apply `cv2.inRange()` separately to create the blue-object mask and tennis-ball mask.
5. Apply morphological opening and closing to reduce noise and clean the masks.
6. Extract external contours using `cv2.findContours()`.
7. For blue objects, calculate contour area using `cv2.contourArea()`, bounding boxes using `cv2.boundingRect()` and centres using image moments from `cv2.moments()`.
8. Allow the user to select a blue object with a mouse click and track it by comparing its centre with the detected centres in subsequent frames.
9. For the tennis ball, calculate contour area and perimeter, then use circularity to reject unsuitable candidates.
10. Use `cv2.minEnclosingCircle()` to estimate the tennis ball's centre and radius.
11. Draw the detection results, measurements and relative-position line when both objects are detected.
12. Display the live camera frame and colour masks until the user presses `q` or `Esc`.

## 3. Camera Output

The live camera window displays the detected objects and their measurements.

### Blue Object

  Contour area:** Area of the detected blue region in square pixels (`px²`).
  Bounding box:** Rectangle around the object, including its horizontal and vertical coordinates, width and height.
  Centre point:** Estimated centre of the blue object's contour.
  Object tracking:** The selected blue object is highlighted when it is successfully tracked.
  Relative-position line:** A line connects the selected blue object's centre to the tennis ball's centre when both are detected.
  `dx` and `dy`:** Horizontal and vertical pixel offsets between the two centres.
  Centre distance:** Euclidean distance between the blue object and tennis ball in pixels.

### Tennis Ball

- **Centre:** Estimated centre coordinates `(x, y)` in pixels.
- **Radius:** Estimated radius in pixels.
- **Contour area:** Area of the detected tennis-ball contour in square pixels (`px²`).
- **Circle outline:** A circle is drawn around the detected tennis-ball candidate.

### Additional Windows

- **Blue Mask:** Displays the binary mask used to identify blue objects.
- **Ball Mask:** Displays the binary mask used to identify the tennis ball.

These masks help check whether the selected colour thresholds are identifying the correct regions.

## 4. Other Possible Methods

1. **RGB/BGR colour thresholding:** Colour detection can be performed directly in RGB or BGR colour space. However, separating colour from brightness is generally less convenient than using HSV.
2. **Background subtraction:** Useful for detecting moving objects against a mostly stationary background. It may fail when the camera moves or the background changes.
3. **Hough Circle Transform:** Can detect circular shapes and estimate their centres and radii. It may be useful for tennis-ball detection, but it is not suitable for detecting arbitrary-shaped blue objects.
4. **Deep learning models:** Models such as YOLO can detect trained object categories using learned visual features. They may handle more varied backgrounds and lighting conditions, but require a suitable model and additional computation.
5. **CSRT object tracker:** Can track a selected object across video frames using visual features. It is an alternative to basic nearest-centre tracking.
6. **Optical flow or Kalman filtering:** These methods can help estimate object movement between frames and improve tracking when detections are temporarily lost. The current program uses a simpler centre-based approach.

## 5. Limitations and Tuning

- **Lighting conditions:** HSV thresholds depend on the camera, lighting and actual object colours. Adjust the blue and tennis-ball threshold values if detection is inaccurate.
- **False detections:** Blue objects in the background may be detected as blue targets, while other yellow-green objects may be mistaken for a tennis ball.
- **Circularity filtering:** Circularity helps reject irregular candidates, but it cannot guarantee that every accepted region is a tennis ball.
- **Tracking accuracy:** The basic tracking method may lose the selected object or switch to a nearby blue object if objects overlap, move quickly or change position significantly between frames.
- **Pixel measurements:** Area, radius and centre distance are measured in image pixels. They do not directly represent physical dimensions or distances.
- **Camera and image quality:** Poor lighting, motion blur, partial occlusion and low resolution can reduce detection accuracy.
- **Threshold adjustment:** The colour limits are predefined and may need to be tuned for different environments.

For reliable real-world measurements, camera calibration and an appropriate distance-estimation method would be required.

## 6. Colour Legend

- **Blue rectangle:** Bounding box around a detected blue object.
- **Green rectangle or centre marker:** Highlights the selected blue object when successfully tracked.
- **Yellow circle:** Estimated boundary of the detected tennis ball.
- **Red line:** Connects the selected blue object's centre to the tennis ball's centre.
- **Blue Mask window:** Shows pixels classified as blue.
- **Ball Mask window:** Shows pixels classified as tennis-ball colour.

*Note: The displayed colours represent the drawing colours used by the program and may differ if the code is modified.*

## 7. Conclusion

This project demonstrates real-time colour-based object detection and basic tracking using Python and OpenCV. It detects blue objects without assuming a circular shape and independently identifies a tennis-ball candidate using colour and circularity.

The program calculates contour areas, bounding boxes, centre coordinates and the tennis ball's estimated radius. When both objects are visible, it also calculates their relative position and centre-to-centre distance.

The project provides practical experience with HSV colour segmentation, image masks, morphological operations, contour analysis, image moments, geometric measurements and real-time camera processing. More advanced tracking and detection techniques could be added in the future to improve performance under challenging conditions.
