import cv2
import subprocess
import numpy as np

# Capture frames from camera using ffmpeg
cmd = ['ffmpeg', '-f', 'v4l2', '-video_size', '640x480', '-input_format', 'mjpeg', '-i', '/dev/video0', '-vf', 'format=bgr24', '-f', 'rawvideo', '-']
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

while True:
    # Read frame from ffmpeg process
    raw_frame = process.stdout.read(640 * 480 * 3)
    if len(raw_frame) == 0:
        break
    
    # Convert raw frame to numpy array
    frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((480, 640, 3))
    
    # Process frame with OpenCV
    # (add your frame processing code here)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cv2.destroyAllWindows()
process.terminate()
