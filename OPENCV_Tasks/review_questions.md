Review Questions
Sensors
1. What is an IMU?
A sensor that measures motion and orientation using an accelerometer (linear acceleration), a gyroscope (rotation rate) and sometimes a magnetometer (magnetic field).
2. 6 DOF vs 9 DOF IMU?
A 6 DOF IMU has an accelerometer and a gyroscope. A 9 DOF IMU adds a magnetometer, which gives an absolute heading reference.
3. 3 DOF of the magnetic component?
The magnetometer measures the Earth's magnetic field along the X, Y and Z axes. Together these give the direction of magnetic north.
4. What is yaw, and how does a 9 DOF IMU reduce it?
Yaw is rotation about the vertical axis, i.e. heading. A gyro-only yaw estimate drifts over time because errors accumulate. A 9 DOF IMU uses the magnetometer's north reference to correct that drift.
5. Encoder vs IMU for the arm?
Encoders are better for joint angles: they are precise, direct and drift-free. An IMU is useful only as a supplement, for example to sense end-effector or base orientation.
Cameras
6. Why is a stereo camera digital?
Depth comes from matching pixels between two images and computing their offset. That needs discrete pixel data and processing, which only digital output provides.
7. Analog vs digital camera use?
Analog cameras suit low-latency live viewing, such as FPV drones and legacy CCTV. Digital cameras suit anything that is processed, stored or analysed, such as computer vision, robotics and high resolution recording.
Git
8. git reset vs git revert?
Reset moves the branch back to an earlier commit and rewrites history, so use it only for local work. Revert adds a new commit that undoes an old one and keeps history, so it is safe on shared branches.
9. git pull vs git fetch?
Fetch downloads remote changes without touching your files. Pull is a fetch followed by a merge into your current branch.
10. How many levels in git config?
Three: system (all users), global (current user) and local (one repository). Local overrides global, and global overrides system.
Linux & Cloud
11. What do you mean by /etc/netplan?
It is the directory in Ubuntu-based Linux distros that holds the network configuration files, written in YAML.
12. What does /etc/netplan do in a Linux distro?
Netplan reads the YAML files there and applies the network settings, such as IP addresses, DHCP or static addressing, DNS and Wi-Fi. It works through a backend like systemd-networkd or NetworkManager. Changes are applied with sudo netplan apply.
13. Is a cloud service a virtual machine? Are all cloud services VMs? Differentiate between them.
No, not all cloud services are VMs. A VM is one kind of cloud service (IaaS, e.g. AWS EC2). Many others are not VMs from the user's side, such as PaaS (Heroku), SaaS (Gmail), serverless functions and cloud storage.
Difference: a VM is a virtualization technology, a full computer emulated in software with its own OS. Cloud is a delivery model: computing resources rented over the internet on demand. Every cloud VM is a cloud service, but not every cloud service is a VM.
14. Advantages of Docker?
It packages an app with its dependencies so it runs the same everywhere. Containers are lighter and faster than VMs, isolated from each other, portable, reproducible from a Dockerfile, and easy to scale.
How many distortion coefficients are there and what are they?
Camera lenses can introduce distortions that cause points in an image to appear away from their ideal positions. The two main forms are radial distortion and tangential distortion.
Radial distortion occurs when light bends unevenly through the lens, especially toward its edges, making straight lines look curved. Barrel distortion produces an outward bulge, while pincushion distortion bends lines inward. Tangential distortion occurs when the lens and image sensor are not perfectly parallel or aligned, which can make the image appear tilted or stretched.
In the standard OpenCV camera model, five distortion coefficients are commonly used: k1, k2 and k3 for radial distortion, and p1 and p2 for tangential distortion. During calibration, cv2.calibrateCamera() estimates these values along with the camera matrix and pose information for the calibration pattern. The coefficients can then be used by functions such as cv2.undistort() or cv2.initUndistortRectifyMap() to correct images. They can also be supplied to cv2.solvePnP() when estimating an object's position and orientation. OpenCV supports other models with additional coefficients, but these five are common in the standard model.
What is the difference between .npz and .yaml files, and how are they used to store camera calibration data?
Both .npz and.yaml files can save calibration values such as the camera matrix and lens-distortion coefficients, but they store the information differently.
A.npz file is a binary archive designed for NumPy arrays. It can be loaded with np.load() and is convenient when a Python program needs to save and retrieve numerical data directly. Its contents are not readily readable in an ordinary text editor.
A.yaml file stores structured data as readable text. It can be inspected or edited manually and can be read with a YAML parser or OpenCV's FileStorage interface. The choice depends on the project and how the calibration data will be accessed; storing the same values in either format does not change the calibration itself.
3. What does cv2.moments() do in OpenCV? Explain its different attributes and how they can be used to find the centre of an object.
The cv2.moments() function calculates numerical image moments for an image region or contour. These moments describe how the pixels or area are distributed and can be used to calculate an object's centroid, or geometric centre.
The zeroth-order moment, m00, represents the contour's area. The first-order moments, m10 and m01, are used to calculate the centroid coordinates. The centre is found using cx = m10/ m00 and cy = m01 / m00, provided that m00 is not zero.
Higher-order moments, including m20, m02 and m11, describe the distribution around the coordinate axes. Central moments such as mu20. mu02 and mu11 describe the distribution relative to the centroid, while normalized central moments such as nu20 and nu02 help compare shapes at different scales. In our detection program, the centroid coordinates can be used to mark and display the centre of the blue object.
4. What is the difference between Gaussian blur and
cv2.morphologyEx()? Explain how both work and their uses in object detection.
Gaussian blur and morphological processing serve different purposes in image processing. Gaussian blur reduces small variations and noise by combining nearby pixel values with weights determined by a Gaussian kernel. OpenCV applies it with cv2. GaussianBlur(). Using blur before colour thresholding can make detection less sensitive to minor noise, although too much blur may soften edges or erase small details.
The cv2.morphologyEx() function applies morphological operations to an image using a structuring element, usually a small kernel. Opening performs erosion followed by dilation and is useful for removing small noise from a binary mask. Closing performs dilation followed by erosion and can fill small holes or gaps. Other available operations include morphological gradient, top-hat and black-hat transformations.
In an object-detection workflow, Gaussian blur can be applied before converting the frame into a colour mask. Opening and closing can then clean the mask, helping the program find object contours more reliably.
