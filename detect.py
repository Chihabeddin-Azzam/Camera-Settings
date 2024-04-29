import subprocess
import cv2
import numpy as np
import keyboard

def check_brightness(image):
 avg_intensity = np.mean(image)
 if avg_intensity < 150:  # Adjust threshold as needed
  return 1
 elif avg_intensity > 200:  # Adjust threshold as needed
  return 2
 else:
  return 3

def check_contrast(image):
 std_dev = np.std(image)
 if std_dev < 20:  # Adjust threshold as needed
  return 1
 else:
  return 2

def check_saturation(image):
 hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
 avg_saturation = np.mean(hsv_image[:,:,1])
 if avg_saturation < 50:  # Adjust threshold as needed
  return 1
 else:
  return 2

def adjust_camera_settings(brightness, contrast, saturation):
 if brightness == 1:
  subprocess.run(['v4l2-ctl','-d','/dev/video1/', '-c', 'brightness=+10'])
 elif brightness == 2:
  subprocess.run(['v4l2-ctl','-d','/dev/video1', '-c', 'brightness=-10'])

 if contrast == 1:
  subprocess.run(['v4l2-ctl','-d','/dev/video1/', '-c', 'contrast=+5'])
 elif contrast == 2:
  pass  # Do nothing
    
 if saturation == 1:
  subprocess.run(['v4l2-ctl','-d','/dev/video1/', '-c', 'saturation=+5'])
 elif saturation == 2:
  pass

# Capture an image from camera
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FPS, 15)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,600)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
out = cv2.VideoWriter('output.mp4', fourcc, 15.0, (800, 600))

print("press \'q\' to quit")
while(True):
 ret, frame = cap.read()

 if not ret:
  print("no frame received")

 # Determine image settings
 brightness_level = check_brightness(frame)
 contrast_level = check_contrast(frame)
 saturation_level = check_saturation(frame)

 # Adjust camera settings based on image settings
 adjust_camera_settings(brightness_level, contrast_level, saturation_level)

 out.write(frame)
 cv2.waitKey(1)
 if cv2.waitKey(1) & 0xFF == ord('q'):
  break

cap.release()
out.release()
